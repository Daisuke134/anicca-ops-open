#!/usr/bin/env python3
"""ENG-3 / OE-P1c: channel=x_post drafts produced by the common engine contract.

Same principles and contract as the Manager product engine
(`models/manager/product/interventions.py` in Daisuke134/anicca):

  * validate_candidates: 2..8 candidates, exactly one `none`, probabilities are
    finite floats > 0 summing to 1, ids ascii-alnum and unique, text <= 500,
    `none` has empty text and every sending kind has text.
  * no fabricated premises: every sending candidate must cite `fact_ids` that
    exist in the fact sheet handed to the model; an unknown or missing citation
    rejects the whole generation (fail closed, nothing is written).
  * the model writes candidates, a weighted draw picks one, and the chosen
    variant is recorded with its assignment probability.

Differences from the product engine, on purpose:
  * channel is fixed to `x_post` and the kinds are X post shapes
    (insight/question/humor/resource/thread/none), not push intervention kinds.
  * this script never posts. It writes the chosen draft to
    `team/state/engine-x-drafts.jsonl` and appends a DRAFT block to
    `team/inbox/x-operator.md`; X Operator still runs post-gate / x_presim.

Model: OpenRouter `deepseek/deepseek-v4.1-flash` using the credential entry
`openrouter-anicca-bounty-build` in credentials.json. The key is read from the
file and never printed, logged, or written to the draft record.

Usage
  # offline check with a fixture (no network, no key needed)
  python3 team/scripts/engine_x_draft.py --fixture team/scripts/fixtures/engine_x_fixture.json

  # real generation
  python3 team/scripts/engine_x_draft.py --facts team/state/engine-x-facts-2026-11-23.json

  # tests
  python3 -m unittest team/scripts/test_engine_x_draft.py -v
"""
import argparse
import hashlib
import json
import math
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

CHANNEL = 'x_post'
KINDS = {'insight', 'question', 'humor', 'resource', 'thread', 'none'}
CANDIDATE_KEYS = {'id', 'kind', 'text', 'probability'}
CREDENTIAL_SERVICE = 'openrouter-anicca-bounty-build'
DEFAULT_MODEL = 'deepseek/deepseek-v4.1-flash'
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
MAX_TEXT = 500
ACCOUNT = '@diceai0'


# --------------------------------------------------------------------------
# contract
# --------------------------------------------------------------------------
def validate_candidates(candidates, fact_ids=None):
    """The engine contract. Raises ValueError; a rejected set is never used.

    With `fact_ids` (a set of allowed fact ids) every sending candidate must
    cite those ids only - that is the 'no fabricated premises' gate.
    """
    if not isinstance(candidates, list) or not 2 <= len(candidates) <= 8:
        raise ValueError('expected 2..8 candidates including no-post')
    seen = set()
    for c in candidates:
        if not isinstance(c, dict):
            raise ValueError('candidate must be an object')
        keys = set(c)
        extra = keys - CANDIDATE_KEYS - ({'fact_ids'} if fact_ids is not None else set())
        if not CANDIDATE_KEYS <= keys or extra:
            raise ValueError('invalid candidate shape: %s' % sorted(keys))
        if not isinstance(c['id'], str) or not c['id'].isascii() or not c['id'].isalnum() or len(c['id']) > 40:
            raise ValueError('invalid candidate id')
        if c['id'] in seen:
            raise ValueError('duplicate candidate id')
        seen.add(c['id'])
        p = c['probability']
        if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 < p <= 1:
            raise ValueError('invalid probability')
        if c['kind'] not in KINDS:
            raise ValueError('invalid kind: %r' % (c['kind'],))
        if not isinstance(c['text'], str):
            raise ValueError('text must be a string')
        if (c['kind'] == 'none') != (c['text'].strip() == ''):
            raise ValueError('no-post must have empty text; a post must have text')
        if c['kind'] != 'none' and len(c['text']) > MAX_TEXT:
            raise ValueError('text longer than %d characters' % MAX_TEXT)
        if c['text'] != c['text'].strip():
            raise ValueError('text must not have edge whitespace')
        if fact_ids is not None and c['kind'] != 'none':
            cited = c.get('fact_ids')
            if not isinstance(cited, list) or any(not isinstance(x, str) for x in cited):
                raise ValueError('sending candidate must carry a fact_ids list')
            unknown = set(cited) - set(fact_ids)
            if unknown:
                raise ValueError('fabricated premise: unknown fact ids %s' % sorted(unknown))
    if sum(c['kind'] == 'none' for c in candidates) != 1:
        raise ValueError('exactly one no-post candidate is required')
    if abs(math.fsum(c['probability'] for c in candidates) - 1) > 1e-9:
        raise ValueError('probabilities must sum to 1')


def select_candidate(candidates, rng):
    """Weighted draw over the generated set (same rule as the product engine)."""
    u, cumulative = rng.random(), 0.0
    for c in candidates:
        cumulative += c['probability']
        if u < cumulative:
            return c
    return candidates[-1]


# --------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------
def load_api_key(credentials_path, service=CREDENTIAL_SERVICE):
    """Return the api key for `service`. Never echoes the value."""
    try:
        with open(credentials_path, 'r', encoding='utf-8') as fh:
            doc = json.load(fh)
    except FileNotFoundError:
        raise SystemExit('credentials file not found: %s' % credentials_path)
    except json.JSONDecodeError:
        raise SystemExit('credentials file is not valid JSON: %s' % credentials_path)
    entries = doc.get('credentials') if isinstance(doc, dict) else doc
    if not isinstance(entries, list):
        raise SystemExit('unexpected credentials layout (no credentials list)')
    for entry in entries:
        if isinstance(entry, dict) and entry.get('service') == service:
            key = entry.get('api_key')
            if not isinstance(key, str) or not key:
                raise SystemExit('credential %s has an empty api_key' % service)
            return key
    raise SystemExit('credential service not found: %s' % service)


def build_prompt(facts_doc):
    facts = facts_doc['facts']
    lines = []
    for f in facts:
        lines.append('- %s: %s' % (f['id'], f['text']))
    return (
        'You write candidate posts for one X account. The fact sheet is the ONLY source of '
        'claims: never invent numbers, dates, product names, users, quotes, events or outcomes. '
        'If a sentence is not supported by a listed fact, do not write it.\n'
        'Return JSON only, no prose and no code fence:\n'
        '{"candidates":[{"id":"a","kind":"insight","text":"...","probability":0.4,"fact_ids":["F1"]}]}\n'
        'Rules:\n'
        '- 2..8 candidates.\n'
        '- Exactly one candidate with kind "none" and empty text (the option not to post now).\n'
        '- probability: float greater than 0, all probabilities sum to 1.\n'
        '- kind is one of: insight, question, humor, resource, thread, none.\n'
        '- text: %s language, at most %d characters, no hashtags, no links, no emoji strings, '
        'first line stands alone (X truncates the rest).\n'
        '- fact_ids: ids of the facts the text relies on; an empty list only if the text makes '
        'no factual claim.\n'
        '- No fabricated premises: do not assume a reader, a metric or a result that is not in '
        'the facts. No medical, crisis or guaranteed-outcome claims. No engaging-with-me asks '
        'that imply relationships that do not exist.\n'
        'Post shape wanted: %s\n'
        'Account: %s\n'
        'Fact sheet:\n%s'
    ) % (facts_doc.get('language', 'en'), MAX_TEXT, facts_doc.get('topic', 'one honest lesson from our own numbers'),
         facts_doc.get('account', ACCOUNT), '\n'.join(lines))


def finish_reason(raw):
    try:
        return raw['choices'][0].get('finish_reason')
    except (KeyError, IndexError, TypeError, AttributeError):
        return None


def parse_model_response(raw):
    """Accept an OpenRouter response, a {"text": ...} stub, or bare candidates JSON."""
    if not isinstance(raw, dict):
        raise ValueError('model response must be an object')
    if 'candidates' in raw:
        return raw['candidates']
    if 'choices' in raw:
        try:
            content = raw['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError):
            raise ValueError('model response has no message content')
        return parse_model_content(content)
    if 'text' in raw:
        return parse_model_content(raw['text'])
    raise ValueError('unrecognised model response')


def parse_model_content(content):
    if not isinstance(content, str) or not content.strip():
        raise ValueError('model returned empty content')
    text = content.strip()
    if text.startswith('```'):
        text = re.sub(r'^```[a-zA-Z]*\n', '', text)
        text = re.sub(r'\n?```$', '', text).strip()
    try:
        doc = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find('{'), text.rfind('}')
        if start < 0 or end <= start:
            raise ValueError('model content is not JSON')
        doc = json.loads(text[start:end + 1])
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict) and 'candidates' in doc:
        return doc['candidates']
    raise ValueError('model JSON has no candidates')


def call_openrouter(prompt, api_key, model=DEFAULT_MODEL, timeout=90):
    body = json.dumps({
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'You output strict JSON only.'},
            {'role': 'user', 'content': prompt},
        ],
        # Reasoning models (deepseek-v4.1-flash) spend completion tokens on
        # reasoning before any content; 1200 came back with empty content.
        'max_tokens': 4000,
        'temperature': 0.7,
        'usage': {'include': True},
    }).encode('utf-8')
    request = urllib.request.Request(
        OPENROUTER_URL, data=body,
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key,
                 'HTTP-Referer': 'https://aniccaai.com', 'X-Title': 'anicca-engine-x-post'})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detail = ''
        try:
            detail = exc.read().decode('utf-8', 'replace')[:300]
        except Exception:
            pass
        # never includes the Authorization header
        raise RuntimeError('OpenRouter HTTP %s: %s' % (exc.code, detail))
    except urllib.error.URLError as exc:
        raise RuntimeError('OpenRouter unreachable: %s' % exc.reason)


def usage_of(raw):
    usage = (raw or {}).get('usage') or {}
    cost = usage.get('cost')
    return {
        'tokens_in': usage.get('prompt_tokens'),
        'tokens_out': usage.get('completion_tokens'),
        'cost_usd': cost if isinstance(cost, (int, float)) and not isinstance(cost, bool) else None,
        'cost_basis': 'openrouter usage.cost' if isinstance(cost, (int, float)) and not isinstance(cost, bool)
        else 'unreported by provider (not estimated)',
    }


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------
def make_variant_id(chosen, facts_doc, now_utc):
    seed = '|'.join([CHANNEL, facts_doc.get('topic', ''), chosen['text']])
    digest = hashlib.sha256(seed.encode('utf-8')).hexdigest()[:8]
    return 'xp-%s-%s' % (now_utc.strftime('%Y%m%dT%H%M%SZ'), digest)


def build_record(chosen, candidates, facts_doc, model, usage, variant_id, now_utc, attempts):
    return {
        'variant_id': variant_id,
        'channel': CHANNEL,
        'created_at': now_utc.isoformat(timespec='seconds'),
        'account': facts_doc.get('account', ACCOUNT),
        'language': facts_doc.get('language', 'en'),
        'topic': facts_doc.get('topic', ''),
        'kind': chosen['kind'],
        'text': chosen['text'],
        'chars': len(chosen['text']),
        'over_280': len(chosen['text']) > 280,
        'assigned_probability': chosen['probability'],
        'chosen_id': chosen['id'],
        'facts_used': chosen.get('fact_ids', []),
        'candidates': candidates,
        'model': model,
        'backend': 'openrouter',
        'policy_version': 'engine-x-post-v1',
        'tokens_in': usage['tokens_in'],
        'tokens_out': usage['tokens_out'],
        'cost_usd': usage['cost_usd'],
        'cost_basis': usage['cost_basis'],
        'generation_attempts': attempts,
        'posted': False,
        'source': 'team/scripts/engine_x_draft.py',
    }


def append_jsonl(path, record):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=False) + '\n')


def draft_block(record, jst_label, fixture=False):
    used = ', '.join(record['facts_used']) if record['facts_used'] else 'none (no factual claim)'
    cost = ('$%s' % record['cost_usd']) if record['cost_usd'] is not None else 'unreported'
    return (
        '\n## %s @x-operator DRAFT from ENG-3 (@pickle common engine, channel=x_post, OE-P1c)%s\n'
        '%s\n\n'
        'Engine: variant_id=%s · model=%s (OpenRouter, base, not fine-tuned) · candidates=%d '
        '(one none, probability sum 1) · chosen kind=%s · assigned_probability=%s · '
        'tokens in/out=%s/%s · cost=%s · chars=%d%s\n'
        'Not posted. X Operator still runs post-gate / x_presim and the dupe check before publishing; '
        'this is an engine candidate, not a verified post.\n'
        'Facts used: %s\n'
        'Record: team/state/engine-x-drafts.jsonl (%s)\n'
    ) % (
        jst_label, ' (FIXTURE - offline test output, no model call)' if fixture else '',
        record['text'], record['variant_id'], record['model'], len(record['candidates']),
        record['kind'], record['assigned_probability'], record['tokens_in'], record['tokens_out'],
        cost, record['chars'], ' [over 280]' if record['over_280'] else '',
        used, record['variant_id'])


def append_block(path, block):
    with open(path, 'a', encoding='utf-8') as fh:
        fh.write(block)


# --------------------------------------------------------------------------
def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(os.path.dirname(here))
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--facts', help='fact sheet JSON ({topic, language, account, facts:[{id,text}]})')
    p.add_argument('--fixture', help='offline model response JSON (skips the API call and the key)')
    p.add_argument('--credentials', default=os.path.join(repo, 'credentials.json'))
    p.add_argument('--model', default=DEFAULT_MODEL)
    p.add_argument('--state', default=os.path.join(repo, 'team/state/engine-x-drafts.jsonl'))
    p.add_argument('--inbox', default=os.path.join(repo, 'team/inbox/x-operator.md'))
    p.add_argument('--seed', type=int, default=None, help='deterministic draw for a reproducible run')
    p.add_argument('--retries', type=int, default=1, help='extra generation attempts on an invalid set')
    p.add_argument('--no-write', action='store_true', help='validate and print the record without writing')
    args = p.parse_args(argv)

    if not args.facts and not args.fixture:
        p.error('give --facts to generate, or --fixture for an offline check')
    fact_ids = None
    if args.facts:
        with open(args.facts, encoding='utf-8') as fh:
            facts_doc = json.load(fh)
        if not isinstance(facts_doc.get('facts'), list) or not facts_doc['facts']:
            p.error('fact sheet must contain a non-empty facts list')
        for f in facts_doc['facts']:
            if set(f) - {'id', 'text', 'source'} or not isinstance(f.get('id'), str) or not isinstance(f.get('text'), str):
                p.error('each fact needs string id and text')
        if len(set(f['id'] for f in facts_doc['facts'])) != len(facts_doc['facts']):
            p.error('duplicate fact ids')
    else:
        facts_doc = {'topic': 'fixture', 'language': 'en', 'account': ACCOUNT,
                     'facts': [{'id': 'F1', 'text': 'fixture fact'}]}
    fact_ids = [f['id'] for f in facts_doc['facts']]

    rng = random.Random(args.seed)
    now = datetime.now(timezone.utc)
    attempts, candidates, raw, usage, chosen = 0, None, None, usage_of(None), None

    if args.fixture:
        with open(args.fixture, encoding='utf-8') as fh:
            raw = json.load(fh)
        candidates = parse_model_response(raw)
        usage = usage_of(raw)
        validate_candidates(candidates, fact_ids)
        chosen = select_candidate(candidates, rng)
        attempts = 1
    else:
        prompt = build_prompt(facts_doc)
        key = load_api_key(args.credentials)
        last = None
        for attempts in range(1, max(0, args.retries) + 2):
            raw = call_openrouter(prompt, key, args.model)
            usage = usage_of(raw)
            try:
                candidates = parse_model_response(raw)
                validate_candidates(candidates, fact_ids)
            except ValueError as exc:
                last = '%s (finish_reason=%s, completion_tokens=%s)' % (
                    exc, finish_reason(raw), (usage_of(raw)['tokens_out']))
                continue
            chosen = select_candidate(candidates, rng)
            break
        if chosen is None:
            print('engine_x_draft: FAIL closed - no valid candidate set after %d attempt(s): %s'
                  % (attempts, last), file=sys.stderr)
            return 3

    variant_id = make_variant_id(chosen, facts_doc, now)
    record = build_record(chosen, candidates, facts_doc, args.model, usage, variant_id, now, attempts)
    # file timestamps in this repo are JST
    jst_label = now.astimezone(ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M JST')

    if args.no_write:
        print(json.dumps({k: record[k] for k in ('variant_id', 'text', 'tokens_in', 'tokens_out', 'cost_usd', 'chars')},
                         ensure_ascii=False, indent=1))
        return 0

    append_jsonl(args.state, record)
    append_block(args.inbox, draft_block(record, jst_label, fixture=bool(args.fixture)))
    print('engine_x_draft: OK variant_id=%s chosen=%s chars=%d tokens=%s/%s cost=%s -> %s'
          % (variant_id, chosen['id'], len(chosen['text']), usage['tokens_in'], usage['tokens_out'],
             usage['cost_usd'], args.state))
    return 0


if __name__ == '__main__':
    sys.exit(main())
