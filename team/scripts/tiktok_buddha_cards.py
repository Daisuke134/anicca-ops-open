#!/usr/bin/env python3
"""Render a 5-card JA affirmation carousel (1080x1920) for @anicca_buddha.

Format copied from the logged JA winner @motto_app_jp https://www.instagram.com/p/DfZaqRRD-uF/
(10-card list carousel: number + one line per card, app promo at the end) — Anicca posts 5 cards.

Usage:
  python3 team/scripts/tiktok_buddha_cards.py \
      --lines-file team/distribution/shortform/buddha-lines-2026-11-28.json \
      --out-dir assets/tiktok/buddha-cards/2026-11-28
Lines file: {"title": "...", "lines": ["...", "..."]} (5 lines recommended)
"""
from __future__ import annotations

import argparse
import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
import os as _os
W3 = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
W6 = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
if not _os.path.exists(W6):  # Linux box fallback (Noto Sans CJK)
    W3 = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    W6 = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def background(seed: int) -> Image.Image:
    warm = seed % 2 == 0
    top = (238, 231, 220) if warm else (232, 236, 231)
    bot = (212, 205, 196) if warm else (206, 215, 209)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    blob = Image.new("L", (W, H), 0)
    ImageDraw.Draw(blob).ellipse([W * 0.15, H * 0.08, W * 0.95, H * 0.55], fill=90)
    blob = blob.filter(ImageFilter.GaussianBlur(160))
    return Image.composite(Image.new("RGB", (W, H), (255, 250, 242)), img, blob)


def wrap(d: ImageDraw.ImageDraw, text: str, font, maxw: int) -> list[str]:
    out: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            if d.textlength(cur + ch, font=font) <= maxw:
                cur += ch
            else:
                out.append(cur)
                cur = ch
        out.append(cur)
    return out


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--lines-file", required=True)
    a.add_argument("--out-dir", required=True)
    a.add_argument("--footer", default="Anicca — 今日の言葉")
    args = a.parse_args()

    data = json.load(open(args.lines_file, encoding="utf-8"))
    lines = data["lines"]
    os.makedirs(args.out_dir, exist_ok=True)
    paths = []
    for i, txt in enumerate(lines, 1):
        img = background(i)
        d = ImageDraw.Draw(img)
        f = ImageFont.truetype(W6, 86)
        small = ImageFont.truetype(W3, 44)
        d.text((96, 150), f"{i:02d}", font=ImageFont.truetype(W6, 58), fill=(120, 132, 120))
        rows = wrap(d, txt, f, 880)
        lh = 126
        y = (H - lh * len(rows)) // 2 - 40
        for r in rows:
            d.text(((W - d.textlength(r, font=f)) / 2, y), r, font=f, fill=(46, 52, 46))
            y += lh
        d.text(((W - d.textlength(args.footer, font=small)) / 2, H - 230), args.footer,
               font=small, fill=(110, 118, 110))
        p = os.path.join(args.out_dir, f"{i:02d}.png")
        img.save(p)
        paths.append(p)
    print(json.dumps({"cards": paths, "title": data.get("title", "")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
