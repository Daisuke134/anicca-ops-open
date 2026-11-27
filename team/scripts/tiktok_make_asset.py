#!/usr/bin/env python3
"""Build a TikTok-ready 1080x1920 asset from an existing vertical demo clip.

Why: the shipped demo clips end on an Instagram end card (aniccaai.com/go/anicca?ct=ig_*),
which would mis-attribute TikTok taps. This trims the clip before that card and appends a
TikTok end card with the right ct tag. Deterministic, no network, no LLM.

Usage:
  python3 team/scripts/tiktok_make_asset.py \
      --source marketing/demo-videos/anicca-living-home-2026-11-18.mp4 \
      --trim 11.6 --ct tiktok_tt_daily --out assets/tiktok/tt-affirmation-2026-11-28.mp4

Requires ffmpeg + Pillow. Never prints secrets.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def end_card(path: str, ct: str) -> None:
    img = Image.new("RGB", (W, H), (0x1B, 0x24, 0x30))
    d = ImageDraw.Draw(img)

    def center(text, font, y, fill):
        bb = d.textbbox((0, 0), text, font=font)
        d.text(((W - (bb[2] - bb[0])) / 2, y), text, font=font, fill=fill)

    center("Anicca", ImageFont.truetype(BOLD, 160), 620, (255, 255, 255))
    center("Words that meet you where you are", ImageFont.truetype(REG, 50), 840, (0xD9, 0xDE, 0xE5))
    btn, fb = "Free on the App Store", ImageFont.truetype(BOLD, 62)
    bb = d.textbbox((0, 0), btn, font=fb)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x0, y0 = (W - tw) / 2 - 34, 1000
    x1, y1 = (W + tw) / 2 + 34, y0 + th + 56
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, outline=(0x5A, 0x66, 0x78),
                        width=3, fill=(0x2E, 0x3A, 0x4A))
    d.text(((W - tw) / 2, y0 + 28 - bb[1]), btn, font=fb, fill=(255, 255, 255))
    center(f"aniccaai.com/go/anicca?ct={ct}", ImageFont.truetype(REG, 40), 1165, (0xB9, 0xC2, 0xCE))
    img.save(path)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--source", required=True)
    a.add_argument("--trim", type=float, required=True, help="seconds of source to keep (cut before the IG end card)")
    a.add_argument("--ct", default="tiktok_tt_daily")
    a.add_argument("--card-seconds", type=float, default=3.0)
    a.add_argument("--out", required=True)
    args = a.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        card_png = os.path.join(td, "card.png")
        card_mp4 = os.path.join(td, "card.mp4")
        part = os.path.join(td, "part.mp4")
        lst = os.path.join(td, "list.txt")
        end_card(card_png, args.ct)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", card_png,
             "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
             "-t", str(args.card_seconds), "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", card_mp4])
        run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-t", str(args.trim), "-i", args.source,
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
             "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", part])
        with open(lst, "w") as fh:
            fh.write(f"file '{part}'\nfile '{card_mp4}'\n")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k", args.out])

    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", args.out], capture_output=True, text=True).stdout.strip()
    print(f"BUILT {args.out} duration={dur}s ct={args.ct}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
