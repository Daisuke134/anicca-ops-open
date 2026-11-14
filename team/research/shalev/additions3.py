import re
p='docs/books/the-art-of-ai-monks-en.md'; t=open(p).read()
def ins_before(anchor, block):
    global t
    assert t.count(anchor)==1, anchor
    t=t.replace(anchor, block.strip('\n')+'\n\n'+anchor)

ins_before('## Chapter 4. Yang Mun and Shalev Hani', '''
### The creator's pre-history, 2023–2024

A history without a "first" still has people in it. The third research pass (23 October 2026) read back Shalev Hani's earliest public posts. They show that the robe came after a long run of other experiments. In December 2023 he described taking a POV app's TikTok and Instagram accounts to tens of millions of views in 60 days. His rule then was one he would repeat for years: most new videos should be remakes of earlier winners with a changed hook. [S57]

In March 2024 he described five months of AI-made TikTok Shop videos with more than 20 million views and "five figures in profit." Two months later he advised beginners to put "may," "might," and "potentially" before any claim. [S55], [S56] In April 2026 he summarized his background himself. He was an early student of the Creators Corner program from July 2023, he says, and before Yang Mun he had worked with more than 100 brands and made more than 3,000 AI videos. "Yang Mun wasn't luck. He was year 3." [S51] These are self-descriptions, not audited résumés. They still change the shape of the story. The monk was a new costume on an older craft: rewriting proven hooks, matching visuals to a script, and connecting attention to a product.
''')

ins_before('### What a creator can actually take away', '''
### The earlier record, January–April 2026

The second pass covered the creator's posts from April to October 2026. The third pass adds the months before that, when Yang Mun was still his. Each line is his own dated claim. [S47]–[S51]

- **23 January 2026.** "Everyone is copying this AI character... I'm the one behind it." He listed 400 million-plus organic views, "$300k Profit (90 Days)," and 5 million followers. [S47]
- **3 February 2026.** He published a tool breakdown: a locked character image, a custom deep voice slowed by about 10 percent ("Wisdom sounds better when it's slow"), and a lip-sync step. It closes with "Tools create content. Systems create cash." The article links to his paid blueprint. [S48]
- **12 February 2026.** He wrote that he had turned down a $325,000 cash offer for Yang Mun at nearly 6 million followers. [S49] This is the creator's own record of the rejected offer that Columbia News Service reported in March. [S02] Five months later he sold the character for $170,000. [S35] The record does not explain the difference, and we do not guess.
- **14 April 2026.** "I Tested 200+ AI Scripts" named three formulas he credits with about 70 million views. They are summarized in Chapter 5. [S50]

His figures also change wording over time. In May 2026 one post says "$500k PROFIT" across seven characters. An article title from the same month says "$467K in 7 months." [S58], [S59] Read beside the April article's revenue account [S31], these are further reasons to keep the revenue-versus-profit question open.
''')

ins_before('## Chapter 6. From Scroll to Store', '''
### Three formulas the creator published

In an April 2026 article, Hani names three script structures that he says outperformed more than 200 others. [S50] They are worth studying as structures. Each comes with a caveat.

1. **The reframe.** Do not tell viewers to stop a habit they feel guilty about. Redirect it: "If you're going to overthink… then overthink the positive." He reports 24 million views for that line. The viewer is understood rather than attacked.
2. **"You're doing it wrong."** Take an ordinary daily act, say it has been done wrong all along, and list fixes. His example is drinking water, with a reported 23 million views. This formula is the most likely to slide into unsupported health claims. Use it for harmless tasks, such as packing a bag or starting an email, and keep any health statement within what a qualified source supports (Chapter 9).
3. **Validation.** Teach nothing new. Say clearly what the audience already feels: "Keep it private until it's permanent." He reports 22.4 million views. "You're not the teacher here. You're the mirror."

The view counts are his. The structures fit the one-message pattern observed in Chapter 4, and they make a reasonable brief for an original character: one feeling, one turn, one usable action.
''')

ins_before('## Chapter 10. Build a Different Character', '''
### What the creator says about labels, care, and calls to action

Three more of the creator's posts, from January to May 2026, turn into concrete obligations. [S52]–[S54]

In January he wrote that a new character "clearly labeled as AI in the bio" still made sales, because "people are impulsive they don't read." [S52] If the person running a character expects buyers not to read a label, that label is not meaningful disclosure. Disclosure belongs where the decision is made: in the video, in the caption, and at checkout.

In May he wrote that his AI monk "has helped more people with their mental health than most real therapists on Instagram. He's not real. But the messages I get from his followers are." [S54] Messages from people in distress are a responsibility, not a metric. A character that receives them needs a human escalation path and crisis resources, and it must never present itself as therapy.

Also in May, he argued that a wave of account bans was driven less by AI detection than by incentivized "comment YES" calls to action. [S53] Platform rules on engagement bait are part of the ethics too. When an account is banned, the people who trusted it lose their way back to it.

The wider question about "fake people" is not whether a character may be fictional. Fiction, parable, and the teaching persona are old. The questions are these: can the audience understand what is speaking to them, does the advice survive qualified review, and is a vulnerable viewer treated as a person rather than a conversion?
''')

ins_before('## Appendix C. References', '''
A third pass on 23 October 2026 extended the read-back to the creator's original posts and articles from December 2023 to May 2026, about 130 more posts. S47–S59 cite them. Like S31–S46, they establish what he published and when. They do not audit revenue, profit, ownership, or sale terms.
''')

REFS = [
 ('S47','2014732472664076414','“Everyone is copying this AI character” post','23 January 2026','Creator claims of 400M+ views, $300k profit in 90 days and 5M followers.'),
 ('S48','2018725900959822131','“The exact blueprint I used to build Yang Mun into a $300k profit machine”, X article','3 February 2026','Creator tool and voice workflow; links to a paid blueprint.'),
 ('S49','2021989884882244010','post on declining a $325,000 offer','12 February 2026','Creator statement; same figure as reported in S02.'),
 ('S50','2044099931494068455','“I Tested 200+ AI Scripts. These 3 Formulas Got 70 Million Views”, X article','14 April 2026','Creator-reported view counts for three script structures.'),
 ('S51','2049166336002343021','background post (“Yang Mun was luck bro”)','28 April 2026','Self-described training, brand work and video count.'),
 ('S52','2012564307071127718','post on sales from a character labeled as AI','17 January 2026','Creator claim; sales figure unverified.'),
 ('S53','2052265003051524464','post on account bans and calls to action','7 May 2026','Creator interpretation of platform enforcement.'),
 ('S54','2056389501816303742','post on followers’ mental-health messages','18 May 2026','Creator statement; messages not reviewed.'),
 ('S55','1765717627110895699','thread on AI TikTok Shop content','7 March 2024','Earlier creator claim of 20M+ views and five-figure profit.'),
 ('S56','1785762655623434673','thread item on cautious claim wording','1 May 2024','Creator advice to qualify claims with “may,” “might,” “potentially.”'),
 ('S57','1732500936596082750','thread on growing a POV app’s accounts in 60 days','6 December 2023','Creator claims of 30M Instagram and 15M TikTok views; advice to remake winners.'),
 ('S58','2056718288823198031','post summarizing seven characters and “$500k PROFIT”','19 May 2026','Creator claim using “profit”; compare S31 and S59.'),
 ('S59','2052024190547710355','“AI Monk + Claude = $467K in 7 months”, X article','6 May 2026','Creator title figure differing from S31 and S58.'),
]
sec='### Creator’s earlier publications (third pass, read back 23 October 2026)\n\n'+'\n\n'.join(f'**{r}. Shalev Hani, {ti}.** Published {d}; read back 23 October 2026 via the X API. {n} Creator statement, not an audit. [Source][{r}]' for r,i,ti,d,n in REFS)+'\n\n'
ins_before('[S01]: https://www.heygen.com/customer-stories/yangmun', sec)
t=t.rstrip('\n')+'\n'+'\n'.join(f'[{r}]: https://x.com/shalevhvs/status/{i}' for r,i,*_ in REFS)+'\n'
open(p,'w').write(t)
import json; json.dump(REFS,open('/tmp/refs3.json','w'))
print('ok')
