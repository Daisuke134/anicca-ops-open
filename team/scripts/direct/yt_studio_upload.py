#!/usr/bin/env python3
"""Free YouTube Shorts path: upload through YouTube Studio in the box browser (signed-in session).

成田さん t4404u 2026-11-28: free direct path per account, no paid scheduler.
Opens its OWN new tab on the shared box Chrome (CDP 127.0.0.1:9223), closes it at the end.
Prints the watch URL. Never touches other tabs, never reads cookies.

  python3 team/scripts/direct/yt_studio_upload.py --file x.mp4 --title "..." --desc-file d.txt [--dry-run]
"""
import argparse, asyncio, re, sys
from playwright.async_api import async_playwright

async def run(a):
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp(a.cdp)
        ctx = b.contexts[0]
        pg = await ctx.new_page()
        try:
            await pg.goto("https://studio.youtube.com/", timeout=60000, wait_until="domcontentloaded")
            await pg.wait_for_timeout(5000)
            if "accounts.google.com" in pg.url:
                print("BLOCKED: YouTube Studio not signed in"); return 3
            await pg.click("#upload-icon", timeout=20000)
            fi = pg.locator("input[type=file]").first
            await fi.set_input_files(a.file, timeout=30000)
            title = pg.locator("#title-textarea #textbox, ytcp-social-suggestions-textbox#title-textarea #textbox").first
            await title.wait_for(timeout=60000)
            await pg.wait_for_timeout(2500)
            await title.click(); await pg.keyboard.press("Control+A"); await pg.keyboard.type(a.title[:100])
            desc = open(a.desc_file, encoding="utf-8").read().strip() if a.desc_file else ""
            if desc:
                d = pg.locator("#description-textarea #textbox").first
                await d.click(); await pg.keyboard.type(desc)
            await pg.locator("tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]").first.click(timeout=20000)
            for _ in range(3):
                await pg.click("#next-button", timeout=20000); await pg.wait_for_timeout(1500)
            vis = "PRIVATE" if a.dry_run else "PUBLIC"
            await pg.locator(f"tp-yt-paper-radio-button[name={vis}]").first.click(timeout=20000)
            await pg.wait_for_timeout(2000)
            await pg.screenshot(path="/tmp/yt-studio-vis.png")
            html = await pg.content()
            m = re.search(r'https://(?:youtu\.be|youtube\.com/shorts)/[\w-]{11}', html)
            link = m.group(0) if m else None
            # wait for upload to finish before publishing (done button enabled)
            for _ in range(120):
                dis = await pg.locator("#done-button").get_attribute("aria-disabled")
                if dis in (None, "false"): break
                await pg.wait_for_timeout(2000)
            await pg.click("#done-button", timeout=20000)
            await pg.wait_for_timeout(8000)
            await pg.screenshot(path="/tmp/yt-studio-after.png")
            print("UPLOADED", vis, link)
            return 0
        except Exception as e:
            await pg.screenshot(path="/tmp/yt-studio-err.png"); raise
        finally:
            await pg.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True); ap.add_argument("--title", required=True)
    ap.add_argument("--desc-file"); ap.add_argument("--cdp", default="http://127.0.0.1:9223")
    ap.add_argument("--dry-run", action="store_true")
    sys.exit(asyncio.run(run(ap.parse_args())))
