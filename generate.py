#!/usr/bin/env python3
"""Draw the front page for the make.fun competition news-image-20261123,
"Sum up 23 November's world news in one image".

A newspaper-style front page drawn procedurally with PIL: a huge date
header over six captioned panels covering the defining stories of
Monday 23 November 2026, plus an "also today" ticker along the bottom.

Stories (reported 23 Nov 2026; SCMP, Yeni Safak, Economic Times, DZRH):
  1. COP31 climate talks in Antalya collapse with no deal: the EU and
     others reject a final text that omits any mention of
     transitioning away from fossil fuels.
  2. Ukraine says its sea drones sank a Russian warship at a base in
     Benghazi, Libya: seven unmanned boats destroyed a Ka-27
     helicopter and hit the cargo ship MV Angara; Libya files a UN
     complaint.
  3. Russian strikes kill at least 15 people in the Kyiv region.
  4. US Democrats clinch their biggest House majority in decades in
     the midterms, with the power to block Trump's agenda; Schumer
     led the party to a big Senate win.
  5. Trump says he is inclined to resume military strikes on Iran
     after the New Year if negotiations produce no agreement.
  6. The US seeks answers on Nvidia's chip sales to China, Treasury
     Secretary Bessent says, as Trump backs ousted CEO Jensen Huang
     and says the company should rehire him.
Ticker: 12,000 fans evacuated from a Manchester concert after a
substance release; Medvedev says Russia has the right, at times the
"obligation", to use nuclear weapons; French tear-gas complaints pass
10,000; Bangladesh vows to arrest Sheikh Hasina if she returns; NATO
fears a Russian nuclear-armed satellite.

Writes entry.png (1024x1024) beside this file. Deterministic.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

NAVY = (13, 21, 43)
GOLD = (233, 186, 82)
PAPER = (243, 239, 229)
INK = (17, 19, 25)
CAP_BG = (9, 13, 26)
CAP_SUB = (198, 207, 226)
WHITE = (250, 250, 248)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_w):
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, f, fill, tracking=10):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- panels

def panel_copcollapse(img, d, x, y, w, h):
    """The rejected final text, stamped NO DEAL."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 40, 26))
    px, py, pw, ph = x + 22, y + 18, w - 138, h - 40
    d.rectangle([px + 6, py + 6, px + pw + 6, py + ph + 6],
                fill=(10, 16, 12))
    d.rectangle([px, py, px + pw, py + ph], fill=(238, 236, 228))
    f = fit_font(d, "FINAL TEXT", BOLD, 19, pw - 24)
    d.text((px + 12, py + 10), "FINAL TEXT", font=f, fill=INK)
    d.line([px + 12, py + 38, px + pw - 12, py + 38], fill=(120, 120, 116),
           width=2)
    ly = py + 52
    for frac in (0.92, 0.84, 0.9):
        d.rectangle([px + 12, ly, px + 12 + (pw - 24) * frac, ly + 7],
                    fill=(168, 168, 162))
        ly += 18
    # the words that are not there, struck through in red
    f2 = fit_font(d, "FOSSIL FUELS", BOLD, 26, pw - 24)
    d.text((px + 12, ly + 4), "FOSSIL FUELS", font=f2, fill=(150, 40, 34))
    d.line([px + 10, ly + 19, px + pw - 10, ly + 19], fill=(214, 40, 40),
           width=5)
    ly += 46
    for frac in (0.88, 0.7):
        d.rectangle([px + 12, ly, px + 12 + (pw - 24) * frac, ly + 7],
                    fill=(168, 168, 162))
        ly += 18
    # a big rotated NO DEAL stamp across the page
    sw, sh = 250, 84
    stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([4, 4, sw - 5, sh - 5], outline=(198, 30, 30, 255),
                 width=6)
    sf = fit_font(sd, "NO DEAL", BOLD, 46, sw - 30)
    tw = sd.textlength("NO DEAL", font=sf)
    sd.text(((sw - tw) / 2, 14), "NO DEAL", font=sf, fill=(198, 30, 30, 255))
    stamp = stamp.rotate(14, expand=True, resample=Image.BILINEAR)
    img.paste(stamp, (int(px + pw - 196), int(py + ph - 94)), stamp)
    f3 = fit_font(d, "ANTALYA", BOLD, 18, 84)
    tw3 = d.textlength("ANTALYA", font=f3)
    d.text((x + w - 10 - tw3, y + 16), "ANTALYA", font=f3, fill=GOLD)
    f4 = fit_font(d, "COP31", BOLD, 18, 84)
    tw4 = d.textlength("COP31", font=f4)
    d.text((x + w - 10 - tw4, y + 40), "COP31", font=f4,
           fill=(220, 228, 214))


def panel_warship(img, d, x, y, w, h):
    """Sea drones converge on a warship in Benghazi harbour."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 66))
    sea = y + h * 0.58
    d.rectangle([x, sea, x + w, y + h], fill=(16, 48, 80))
    for i in range(9):  # wave ticks
        wx = x + 12 + (i * 71) % int(w - 26)
        wy = sea + 14 + (i * 29) % int(h * 0.3)
        d.line([wx, wy, wx + 15, wy], fill=(92, 142, 192), width=2)
    # the warship: hull, superstructure, mast
    hx, hy = x + w * 0.3, sea - 6
    hw = w * 0.62
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 20, hy + 22),
               (hx + 12, hy + 22)], fill=(24, 28, 38))
    d.rectangle([hx + hw * 0.3, hy - 26, hx + hw * 0.52, hy],
                fill=(52, 58, 72))
    d.rectangle([hx + hw * 0.56, hy - 16, hx + hw * 0.7, hy],
                fill=(52, 58, 72))
    d.line([hx + hw * 0.4, hy - 26, hx + hw * 0.4, hy - 48],
           fill=(200, 204, 212), width=3)
    d.line([hx + hw * 0.4, hy - 48, hx + hw * 0.52, hy - 40],
           fill=(200, 204, 212), width=2)
    # blast where a drone boat reached the stern
    bx, by = hx + 6, hy - 2
    star(d, bx, by, 21, (255, 140, 60))
    star(d, bx, by, 11, (255, 220, 140))
    for i in range(3):  # smoke puffs
        sx = bx - 6 - i * 12
        sy = by - 18 - i * 14
        d.ellipse([sx - 9, sy - 7, sx + 9, sy + 7], fill=(150, 150, 158))
    # three unmanned boats with wakes, closing in
    for i, (fx, fy) in enumerate([(0.1, 0.74), (0.34, 0.86), (0.62, 0.78)]):
        cx, cy = x + w * fx, y + h * fy
        d.polygon([(cx, cy), (cx + 30, cy + 4), (cx + 24, cy + 12),
                   (cx + 4, cy + 12)], fill=(10, 12, 16))
        d.line([cx - 26, cy + 8, cx - 2, cy + 6], fill=(210, 226, 240),
               width=2)
        d.line([cx - 20, cy + 13, cx - 2, cy + 11], fill=(160, 190, 220),
               width=2)
    f = fit_font(d, "BENGHAZI · LIBYA", BOLD, 20, w * 0.62)
    d.text((x + 14, y + 12), "BENGHAZI · LIBYA", font=f,
           fill=(255, 196, 110))
    f2 = fit_font(d, "7 SEA DRONES", REG, 16, w * 0.5)
    d.text((x + 14, y + 40), "7 SEA DRONES", font=f2,
           fill=(190, 208, 230))


def panel_kyiv(img, d, x, y, w, h):
    """Night over the capital region; two missile arcs come down."""
    bands = [(26, 24, 48), (44, 30, 58), (74, 40, 62), (110, 56, 62)]
    bh = h / len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=col)
    for sx, sy in [(0.12, 0.1), (0.3, 0.05), (0.55, 0.14), (0.78, 0.07),
                   (0.9, 0.18), (0.42, 0.2)]:
        star(d, x + w * sx, y + h * sy, 3, (220, 224, 235))
    for x0, drop in ((0.06, 0.5), (0.52, 0.42)):
        arc = [(x + w * x0 + t * w * 0.3,
                y + 10 + (t * t) * h * drop) for t in
               [i / 20.0 for i in range(21)]]
        d.line(arc, fill=(255, 226, 170), width=3)
        ex, ey = arc[-1]
        star(d, ex, ey, 16, (255, 140, 60))
        star(d, ex, ey, 8, (255, 220, 140))
    # skyline
    base = y + h
    heights = [0.3, 0.46, 0.24, 0.38, 0.52, 0.28, 0.42, 0.33, 0.26]
    bx = x
    for i, hf in enumerate(heights):
        bw = w / len(heights)
        bhh = h * hf
        d.rectangle([bx, base - bhh, bx + bw - 2, base], fill=(10, 9, 16))
        for wy in range(int(base - bhh) + 8, int(base) - 8, 14):
            if (i * 7 + wy) % 3:
                d.point((bx + 5 + (wy % 9), wy), fill=(245, 205, 110))
        bx += bw
    f = fit_font(d, "KYIV REGION", BOLD, 22, w * 0.55)
    tw = d.textlength("KYIV REGION", font=f)
    d.text((x + w - 14 - tw, y + 10), "KYIV REGION", font=f,
           fill=(255, 236, 205))


def panel_capitol(img, d, x, y, w, h):
    """The Capitol dome over a blue field, stars above."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 32, 74))
    for i in range(2):  # stars across the top right, clear of the title
        sx = x + w * (0.81 + 0.11 * i)
        star(d, sx, y + 22, 6, (240, 240, 245))
    cx = x + w / 2
    base = y + h - 14
    # building body and wings
    d.rectangle([x + 18, base - 46, x + w - 18, base], fill=(226, 228, 234))
    d.rectangle([x + w * 0.3, base - 66, x + w * 0.7, base],
                fill=(232, 234, 240))
    # columns
    for i in range(7):
        cxx = x + w * 0.33 + i * (w * 0.34) / 6
        d.line([cxx, base - 60, cxx, base - 8], fill=(150, 154, 168),
               width=3)
    # the dome: stacked arcs and a spire
    d.pieslice([cx - 62, base - 142, cx + 62, base - 40], 180, 360,
               fill=(238, 240, 246))
    d.pieslice([cx - 38, base - 158, cx + 38, base - 90], 180, 360,
               fill=(226, 230, 240))
    d.rectangle([cx - 5, base - 184, cx + 5, base - 152],
                fill=(238, 240, 246))
    star(d, cx, base - 191, 5, GOLD)
    # red and gold stripes under the steps
    d.rectangle([x + 18, base, x + w - 18, base + 5], fill=(178, 34, 52))
    f = fit_font(d, "HOUSE MAJORITY", BOLD, 22, w * 0.66)
    d.text((x + 14, y + 12), "HOUSE MAJORITY", font=f, fill=WHITE)


def panel_deadline(img, d, x, y, w, h):
    """A New Year calendar page, its first day circled in red."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 30, 30))
    px, py, pw, ph = x + 62, y + 18, w - 124, h - 56
    d.rectangle([px + 6, py + 6, px + pw + 6, py + ph + 6],
                fill=(16, 10, 10))
    d.rectangle([px, py, px + pw, py + ph], fill=(240, 238, 232))
    d.rectangle([px, py, px + pw, py + 40], fill=(178, 34, 52))
    f = fit_font(d, "JANUARY", BOLD, 24, pw - 20)
    tw = d.textlength("JANUARY", font=f)
    d.text((px + (pw - tw) / 2, py + 7), "JANUARY", font=f, fill=WHITE)
    f2 = fit_font(d, "1", SERIF, 104, pw - 30)
    tw2 = d.textlength("1", font=f2)
    d.text((px + (pw - tw2) / 2, py + 46), "1", font=f2, fill=INK)
    # the red circle around the day
    d.ellipse([px + 28, py + 48, px + pw - 28, py + ph - 14],
              outline=(214, 40, 40), width=6)
    # binder rings
    for fx in (0.3, 0.7):
        rx = px + pw * fx
        d.ellipse([rx - 7, py - 9, rx + 7, py + 9], outline=(200, 204, 210),
                  width=4)
    f3 = fit_font(d, "NEW YEAR", BOLD, 20, w * 0.5)
    tw3 = d.textlength("NEW YEAR", font=f3)
    d.text((x + (w - tw3) / 2, y + h - 30), "NEW YEAR", font=f3,
           fill=(255, 190, 120))


def panel_chip(img, d, x, y, w, h):
    """A giant AI chip under a magnifying glass."""
    d.rectangle([x, y, x + w, y + h], fill=(14, 26, 30))
    cx, cy, cs = x + w * 0.44, y + h * 0.46, 118
    # circuit traces out to the edges
    for (tx, ty) in [(0.08, 0.16), (0.86, 0.2), (0.1, 0.82), (0.88, 0.8),
                     (0.64, 0.05), (0.94, 0.52)]:
        ex, ey = x + w * tx, y + h * ty
        d.line([cx, cy, ex, cy], fill=(40, 90, 84), width=3)
        d.line([ex, cy, ex, ey], fill=(40, 90, 84), width=3)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(70, 160, 148))
    # pins
    for i in range(6):
        off = -cs / 2 + 14 + i * (cs - 28) / 5
        d.rectangle([cx + off - 4, cy - cs / 2 - 16, cx + off + 4,
                     cy - cs / 2], fill=(196, 200, 206))
        d.rectangle([cx + off - 4, cy + cs / 2, cx + off + 4,
                     cy + cs / 2 + 16], fill=(196, 200, 206))
        d.rectangle([cx - cs / 2 - 16, cy + off - 4, cx - cs / 2,
                     cy + off + 4], fill=(196, 200, 206))
        d.rectangle([cx + cs / 2, cy + off - 4, cx + cs / 2 + 16,
                     cy + off + 4], fill=(196, 200, 206))
    # chip body
    d.rectangle([cx - cs / 2, cy - cs / 2, cx + cs / 2, cy + cs / 2],
                fill=(26, 34, 44), outline=(150, 200, 190), width=3)
    d.rectangle([cx - cs / 4, cy - cs / 4, cx + cs / 4, cy + cs / 4],
                outline=(90, 170, 158), width=2)
    f = fit_font(d, "AI", BOLD, 44, cs / 2)
    tw = d.textlength("AI", font=f)
    d.text((cx - tw / 2, cy - 26), "AI", font=f, fill=(160, 235, 220))
    # magnifying glass, lower right
    gx, gy, gr = x + w * 0.76, y + h * 0.66, 40
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr],
              outline=(232, 234, 238), width=7)
    d.line([gx + gr * 0.68, gy + gr * 0.68, gx + gr * 1.25, gy + gr * 1.25],
           fill=(232, 234, 238), width=9)
    f2 = fit_font(d, "?", BOLD, 44, 40)
    d.text((gx - 11, gy - 24), "?", font=f2, fill=(255, 214, 130))
    f3 = fit_font(d, "CHINA SALES", BOLD, 20, w * 0.55)
    d.text((x + 14, y + 12), "CHINA SALES", font=f3, fill=(190, 235, 225))


PANELS = [
    (panel_copcollapse, "COP31 TALKS COLLAPSE, NO DEAL",
     "EU rejects a final text with no fossil-fuel transition"),
    (panel_warship, "UKRAINE SINKS RUSSIAN WARSHIP",
     "Sea drones hit Benghazi base; a helicopter destroyed"),
    (panel_kyiv, "RUSSIAN STRIKES KILL 15 NEAR KYIV",
     "Overnight barrage hits the capital region, Kyiv says"),
    (panel_capitol, "DEMOCRATS CLINCH THE HOUSE",
     "Biggest House majority in decades curbs Trump's agenda"),
    (panel_deadline, "TRUMP WARNS IRAN ON STRIKES",
     "May resume attacks after New Year if talks fail"),
    (panel_chip, "US PROBES NVIDIA CHINA SALES",
     "Bessent seeks answers; Trump backs ousted CEO Huang"),
]

TICKER = ("ALSO TODAY:  12,000 fans evacuated from Manchester concert  •  "
          "Medvedev talks of a nuclear 'obligation'  •  French tear-gas "
          "complaints pass 10,000  •  Bangladesh vows to arrest Hasina "
          "if she returns  •  NATO fears a nuclear-armed Russian satellite")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 158], fill=NAVY)
    f_kick = font(BOLD, 21)
    tracked(d, (30, 20), "THE DAY IN ONE PICTURE", f_kick, GOLD, 8)
    f_day = fit_font(d, "MONDAY", BOLD, 30, 260)
    tw = d.textlength("MONDAY", font=f_day)
    d.text((W - 30 - tw, 16), "MONDAY", font=f_day, fill=WHITE)
    f_date = fit_font(d, "23 NOVEMBER 2026", SERIF, 84, W - 60)
    d.text((28, 52), "23 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.rectangle([0, 152, W, 158], fill=GOLD)

    # panel grid
    mx, gap = 26, 14
    pw = (W - 2 * mx - 2 * gap) // 3
    ph = 368
    top = 172
    for i, (draw_fn, head, sub) in enumerate(PANELS):
        col, row = i % 3, i // 3
        px = mx + col * (pw + gap)
        py = top + row * (ph + gap)
        cap_h = 96
        d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255))
        draw_fn(img, d, px, py, pw, ph - cap_h)
        cy = py + ph - cap_h
        d.rectangle([px, cy, px + pw, py + ph], fill=CAP_BG)
        fh = fit_font(d, head, BOLD, 25, pw - 20)
        lines = wrap(d, head, fh, pw - 20)
        if len(lines) > 1:
            fh = fit_font(d, head, BOLD, 21, pw - 20)
            lines = wrap(d, head, fh, pw - 20)
        ly = cy + 9
        for ln in lines[:2]:
            d.text((px + 10, ly), ln, font=fh, fill=WHITE)
            ly += fh.size + 3
        fs = font(REG, 17)
        for ln in wrap(d, sub, fs, pw - 20)[:2]:
            d.text((px + 10, ly), ln, font=fs, fill=CAP_SUB)
            ly += 21

    # ticker (shrink the font until the whole ticker fits on two lines)
    ty = top + 2 * ph + gap + 12
    d.rectangle([0, ty, W, H], fill=NAVY)
    tsize = 20
    while tsize > 12:
        ft = font(REG, tsize)
        lines = wrap(d, TICKER, ft, W - 52)
        if len(lines) <= 2:
            break
        tsize -= 1
    ly = ty + 12
    for ln in lines[:2]:
        d.text((26, ly), ln, font=ft, fill=(226, 231, 242))
        ly += tsize + 6

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
