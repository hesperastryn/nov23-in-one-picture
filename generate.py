#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page as a single PNG.

Layout: masthead on top, six story panels in a 2x3 grid (kicker,
headline, short body, then a slim motif strip along the panel bottom),
and a two-line ticker at the very bottom. All drawing is procedural
PIL work driven by the story table below.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (246, 241, 230)
INK = (28, 26, 24)
ACCENT = (156, 32, 28)
BODY_INK = (52, 48, 44)
PANEL_BG = (252, 249, 242)
PANEL_LINE = (120, 112, 98)
SEA = (70, 110, 140)
TICKER_BG = (28, 26, 24)
TICKER_FG = (246, 241, 230)
TICKER_HEAD = (232, 176, 92)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_width, step, max_lines):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width)[:max_lines]:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


# ------------------------------------------------------- motif sketches
# Each motif gets a slim strip box (about 200 x 46) at a panel's bottom.

def motif_no_deal(draw, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.rounded_rectangle([cx - 52, cy - 14, cx + 52, cy + 14], radius=5,
                           outline=ACCENT, width=3)
    f = font(SANS_BOLD, 17)
    label = "NO DEAL"
    tw = draw.textlength(label, font=f)
    draw.text((cx - tw / 2, cy - 9), label, font=f, fill=ACCENT)
    draw.line([x0 + 8, cy + 16, cx - 62, cy + 16], fill=BODY_INK, width=2)
    draw.line([cx + 62, cy - 16, x1 - 8, cy - 16], fill=BODY_INK, width=2)


def motif_drones(draw, box):
    x0, y0, x1, y1 = box
    horizon = y0 + 20
    for i in range(3):
        yy = horizon + 8 + i * 7
        draw.line([x0 + 6, yy, x1 - 6, yy], fill=SEA, width=2)
    sx = x0 + 66
    draw.polygon([(sx, horizon), (sx + 76, horizon), (sx + 66, horizon - 9),
                  (sx + 9, horizon - 9)], fill=INK)
    draw.rectangle([sx + 30, horizon - 19, sx + 48, horizon - 9], fill=INK)
    draw.line([sx + 39, horizon - 28, sx + 39, horizon - 19], fill=INK, width=2)
    for i in range(7):
        dx = x0 + 10 + i * 26
        dy = horizon + 22 + (i % 2) * 6
        draw.polygon([(dx, dy), (dx + 12, dy + 3), (dx, dy + 6)], fill=ACCENT)


def motif_strikes(draw, box):
    x0, y0, x1, y1 = box
    base = y1 - 2
    for bx, bh in [(x0 + 8, 18), (x0 + 52, 27), (x0 + 102, 21), (x0 + 148, 30)]:
        draw.rectangle([bx, base - bh, bx + 32, base], outline=INK, width=2)
    for i in range(3):
        sx = x0 + 30 + i * 56
        draw.line([sx, y0 + 2, sx + 22, y0 + 26], fill=ACCENT, width=3)
        draw.ellipse([sx + 19, y0 + 23, sx + 29, y0 + 33], fill=ACCENT)
    cx, cy = x0 + 118, y0 + 34
    for ang in range(0, 360, 45):
        draw.line([cx, cy, cx + 10 * math.cos(math.radians(ang)),
                   cy + 10 * math.sin(math.radians(ang))], fill=ACCENT, width=2)


def motif_capitol(draw, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    base = y1 - 2
    draw.pieslice([cx - 30, base - 46, cx + 30, base - 4], 180, 360,
                  outline=INK, width=3)
    draw.line([cx, base - 50, cx, base - 38], fill=INK, width=3)
    draw.rectangle([cx - 52, base - 10, cx + 52, base], fill=INK)
    for i in range(5):
        px = cx - 42 + i * 21
        draw.line([px, base - 28, px, base - 10], fill=INK, width=3)
    draw.line([cx - 52, base - 28, cx + 52, base - 28], fill=INK, width=3)
    f = font(SANS_BOLD, 12)
    label = "* * *"
    tw = draw.textlength(label, font=f)
    draw.text((x0 + 8, y0 + 2), label, font=f, fill=ACCENT)
    draw.text((x1 - 8 - tw, y0 + 2), label, font=f, fill=ACCENT)


def motif_iran(draw, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=ACCENT, width=3)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=ACCENT)
    pts = [(x0 + 12, cy + 14), (x0 + 58, cy + 4), (x0 + 68, cy + 9),
           (x0 + 30, cy + 19)]
    draw.polygon(pts, fill=INK)
    pts2 = [(x1 - 68, cy - 12), (x1 - 22, cy - 18), (x1 - 12, cy - 13),
            (x1 - 50, cy - 6)]
    draw.polygon(pts2, fill=INK)


def motif_chip(draw, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    half = 17
    draw.rectangle([cx - half, cy - half, cx + half, cy + half],
                   outline=INK, width=3)
    draw.rectangle([cx - 7, cy - 7, cx + 7, cy + 7], outline=ACCENT, width=2)
    for i in range(-1, 2):
        off = i * 12
        draw.line([cx - half - 8, cy + off, cx - half, cy + off], fill=INK, width=3)
        draw.line([cx + half, cy + off, cx + half + 8, cy + off], fill=INK, width=3)
        draw.line([cx + off, cy - half - 8, cx + off, cy - half], fill=INK, width=3)
        draw.line([cx + off, cy + half, cx + off, cy + half + 8], fill=INK, width=3)
    f = font(SERIF_BOLD, 22)
    draw.text((cx + half + 16, cy - 13), "?", font=f, fill=ACCENT)
    draw.text((x0 + 10, cy - 11), "AI", font=font(SANS_BOLD, 15), fill=BODY_INK)


STORIES = [
    ("CLIMATE SUMMIT",
     "No Deal in Antalya as COP31 Collapses",
     "The EU and other blocs reject a final text that drops any mention "
     "of transitioning away from fossil fuels. Overtime ends with no deal.",
     motif_no_deal),
    ("BLACK SEA / LIBYA",
     "Ukraine Sea Drones Sink Russian Warship at Benghazi",
     "Seven sea drones hit a Russian base in Benghazi, sinking a warship "
     "and destroying a Ka-27 helicopter. Libya files a UN complaint.",
     motif_drones),
    ("UKRAINE",
     "Russian Strikes Kill at Least 15 in Kyiv Region",
     "Another night of Russian strikes on the Kyiv region leaves at "
     "least fifteen dead, as air defences engage waves of missiles.",
     motif_strikes),
    ("US MIDTERMS",
     "Democrats Win Biggest House Majority in Decades",
     "Democrats clinch a historic House majority while Schumer leads a "
     "big Senate win, redrawing the map for the next Congress.",
     motif_capitol),
    ("IRAN",
     "Trump: Strikes on Iran May Resume After New Year",
     "Trump says he is inclined to resume military strikes on Iran "
     "after the New Year if negotiations fail to produce a deal.",
     motif_iran),
    ("CHIPS / TRADE",
     "US Seeks Answers on Nvidia Chip Sales to China",
     "Bessent presses for answers on Nvidia sales to China as Trump "
     "backs ousted CEO Jensen Huang and urges his rehiring.",
     motif_chip),
]

TICKER = [
    "12,000 fans evacuated from Manchester concert",
    "Medvedev floats a nuclear \u201cobligation\u201d",
    "French tear-gas complaints pass 10,000",
    "Bangladesh vows Hasina arrest",
    "NATO fears a Russian nuclear satellite",
]


def masthead(draw):
    draw.rectangle([0, 0, W, H], fill=PAPER)
    f_title = font(SERIF_BOLD, 54)
    title = "THE DAILY SYNTHESIS"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, 24), title, font=f_title, fill=INK)
    f_date = font(SANS_BOLD, 25)
    date = "23 NOVEMBER 2026  ·  MONDAY"
    tw = draw.textlength(date, font=f_date)
    draw.text(((W - tw) / 2, 94), date, font=f_date, fill=ACCENT)
    draw.line([36, 134, W - 36, 134], fill=INK, width=4)
    draw.line([36, 142, W - 36, 142], fill=INK, width=1)


def panel(draw, box, story):
    x0, y0, x1, y1 = box
    kicker, headline, body, motif = story
    draw.rectangle(box, fill=PANEL_BG, outline=PANEL_LINE, width=2)
    pad = 16
    inner_w = (x1 - x0) - 2 * pad
    draw.text((x0 + pad, y0 + 10), kicker, font=font(SANS_BOLD, 14), fill=ACCENT)
    y = draw_wrapped(draw, (x0 + pad, y0 + 34), headline,
                     font(SERIF_BOLD, 24), INK, inner_w, 29, 2)
    draw_wrapped(draw, (x0 + pad, y + 6), body, font(SANS, 16), BODY_INK,
                 inner_w, 21, 3)
    motif(draw, (x0 + 128, y1 - 56, x1 - 128, y1 - 8))


def ticker(draw):
    y0 = H - 84
    draw.rectangle([0, y0, W, H], fill=TICKER_BG)
    draw.text((30, y0 + 10), "ALSO TODAY", font=font(SANS_BOLD, 15),
              fill=TICKER_HEAD)
    f_item = font(SANS, 15)
    text = "   •   ".join(TICKER)
    y = y0 + 34
    for line in wrap(draw, text, f_item, W - 60)[:2]:
        draw.text((30, y), line, font=f_item, fill=TICKER_FG)
        y += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    grid_top = 156
    grid_bottom = H - 100
    cols = [(36, 506), (518, 988)]
    row_h = (grid_bottom - grid_top) // 3
    idx = 0
    for r in range(3):
        for c in range(2):
            box = (cols[c][0], grid_top + r * row_h + 5,
                   cols[c][1], grid_top + (r + 1) * row_h - 5)
            panel(draw, box, STORIES[idx])
            idx += 1
    ticker(draw)
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        os.makedirs(out, exist_ok=True)
        path = os.path.join(out, "entry.png")
    else:
        path = "entry.png"
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
