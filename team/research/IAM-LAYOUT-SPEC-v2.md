# I am (id 874656917) en-US screenshot layout spec → Anicca treatment-iam-v2

Measured 2026-11-11 14:35–14:50 JST by Grok Bot 参謀 from the live US listing (iTunes lookup `screenshotUrls`, max size). Machine-readable: `anicca-aso/iam-layout-spec.json` (copy: `team/research/iam-layout-spec.json`). Measurer: `anicca-aso/v2tools/measure.py`.

## Winner spec (base canvas 1242×2688, APP_IPHONE_65)
| Item | I am (measured) |
|---|---|
| Canvas | 1242×2688 (6.5"), 9 slides |
| Background | solid, no gradient. light (235,222,214) / mauve (123,103,101) / dark (68,54,52) |
| Headline | 2 lines on every slide, centred at x=621, no tracking |
| Font | proprietary-looking grotesk; nearest free = **Red Hat Display wght 700–725** (x-height 62, cap 84, ascender 87, stem 15 px) |
| Size / weight used | 120 px / wght 725 |
| Baselines | line 1 y=295, line 2 y=424.5 (pitch ≈130). I am's own slides vary 292–295 |
| Text colour | (68,54,51) on light, white on mauve/dark, (235,222,214) on dark slide 7 |
| Device | flat white outline, no shadow, bleeds off bottom. outer x 56–1186 (w 1131), top y 582, outer radius 194 (fit err 0.65 px) |
| Bezel | top 42, sides 48 → screen x 104–1138 (w 1035), top 624, inner radius 146 |
| Side buttons | left 3 (T+447 h88, T+616 h177, T+842 h176), right 1 (T+738 h280), 9 px wide |
| Margins | headline top 207, device side 56, gap last baseline → device 157 |

Not copied: I am logo, illustrations, affirmation text, headline wording.

## Generator
ParthJadhav/app-store-screenshots was cloned and read (`/workspace/tools/app-store-screenshots`). It scaffolds an interactive Next.js editor; it does not give a headless, pixel-exact, measurable render. So v2 uses one PIL template (`anicca-aso/v2tools/render_v2.py`). Every slide reads the same `iam-layout-spec.json` plus `v2tools/slides.json`. Per slide only the copy, background key and source screen change. Export sizes follow that repo's list and ASC: APP_IPHONE_65 1242×2688 (the winner's size) and APP_IPHONE_67 1320×2868 (Anicca's current slot), each rendered natively at k = W/1242.

## Anicca v2 copy (en-US)
1 A kind line / every morning · 2 Swipe a new / affirmation · 3 Save the lines / you love · 4 Pick a calm / background · 5 Share a line / as an image · 6 Gentle daily / reminders · 7 One card / at your pace · 8 Clear price / before you pay
Screens are the real 1.9.x app captures from control-live (3 card screens plus the Theme sheet). Card screens: width-fit, with the bottom 25% background band extended to the bleed. Theme sheet: cover-fit. Background sequence = I am slides 1–8.

## Verification (`v2tools/verify_v2.py` → `treatment-iam-v2/verify-report.json`): PASS
Uniformity spread across the 8 slides (1242×2688, px): {"stem_px": 2.0, "frame_top": 0.0, "frame_left": 0.0, "frame_right": 0.0, "bezel_top": 0.0, "bezel_side": 0.0, "line1_baseline": 1.0, "line2_baseline": 1.0, "line_pitch": 2.0, "x_height": 1.0, "line_count": 0}
Max |Δ| vs I am (px): {"stem_px": 1.0, "frame_top": 0.0, "frame_left": 1.0, "frame_right": 0.5, "bezel_top": 0.0, "line1_baseline": 1.0, "line2_baseline": 1.5, "line_pitch": 2.0, "x_height": 1.38, "bezel_side": 0.0, "center_x": 3.5}
Frame and bezel are 0–1 px. Headline baselines, x-height and stem are ≤2 px. Ink-box centre is ≤3.5 px: text is advance-centred at exactly 621, and the remainder is glyph shape. Font, size and weight are one value for all slides by construction.
`ascx.sh screenshots validate`: IPHONE_65 and IPHONE_67, 8/8 ok, no issues.
Side-by-side: `team/research/ANICCA-VS-IAM-FIRST3-v2.jpg`.

## Export rule (2026-11-12, X scout)
App Store Connect rejects screenshot PNGs that carry an alpha channel. Before upload, flatten every slide to RGB (JPEG or alpha-free PNG) and check with `python3 -c "from PIL import Image;print(Image.open(f).mode)"` (must be RGB). Source: https://x.com/escstk/status/2120534034166009911
