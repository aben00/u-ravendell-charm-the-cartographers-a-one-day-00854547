#!/usr/bin/env python3
"""Draw the treasure map entry for Charm the Cartographers.

Renders a deterministic 1024x1024 PNG of a fictional island,
"The Isle of Wren's Regret", with seven labeled places, a compass rose,
a dashed route to the X, a sea serpent, a galleon and small jokes.
Run: python3 draw.py  -> writes entry.png next to this file.
Deterministic: fixed seed, no timestamps, no external input.
"""
import math
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
SEED = 20261124
rng = random.Random(SEED)

PARCH = (239, 219, 169)      # parchment
PARCH_D = (228, 203, 144)    # darker parchment
LAND = (216, 190, 128)       # island fill
LAND_D = (198, 168, 104)
INK = (59, 42, 24)           # dark brown ink
INK_SOFT = (96, 70, 38)
RED = (178, 52, 32)          # treasure red
BLUE = (58, 96, 110)         # sea ink
GREEN = (74, 102, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    p = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(p, size)
    except OSError:
        return ImageFont.load_default()


SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SERIF_BI = lambda s: font("DejaVuSerif-BoldItalic.ttf", s)


def chaikin(points, rounds=2):
    """Smooth a closed polygon by corner cutting."""
    pts = list(points)
    for _ in range(rounds):
        out = []
        n = len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            out.append((0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]))
            out.append((0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1]))
        pts = out
    return pts


def bezier(p0, p1, p2, n=14):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def label(d, xy, text, fnt, fill=INK, anchor="mm", halo=True):
    if halo:
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1),
                       (-2, -2), (2, 2)):
            d.text((xy[0] + dx, xy[1] + dy), text, font=fnt, fill=PARCH, anchor=anchor)
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def dashed(d, points, fill=INK_SOFT, width=3, dash=12, gap=8):
    """Draw a dashed polyline through points."""
    for a, b in zip(points, points[1:]):
        x0, y0 = a
        x1, y1 = b
        total = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(total // (dash + gap)))
        for i in range(n + 1):
            t0 = i * (dash + gap) / total
            t1 = min(1.0, t0 + dash / total)
            if t0 >= 1:
                break
            d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                    (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
                   fill=fill, width=width)


def wave(d, x, y, s=1.0, fill=BLUE):
    """A little hand-drawn wave squiggle."""
    d.arc([x - 14 * s, y - 8 * s, x + 2 * s, y + 8 * s], 200, 340, fill=fill, width=2)
    d.arc([x - 2 * s, y - 8 * s, x + 14 * s, y + 8 * s], 200, 340, fill=fill, width=2)


def gull(d, x, y, s=1.0):
    d.line([(x - 10 * s, y - 4 * s), (x, y + 3 * s), (x + 10 * s, y - 4 * s)],
           fill=INK_SOFT, width=2)


def palm(d, x, y, s=1.0, lean=0.0):
    """A small palm tree with drooping bezier fronds."""
    top = (x + 26 * s * math.sin(math.radians(lean)), y - 34 * s)
    d.line([(x, y), top], fill=INK, width=max(2, int(3 * s)))
    for ang in (-75, -40, -8, 28, 62):
        a = math.radians(ang)
        tip = (top[0] + 24 * s * math.sin(a), top[1] + 16 * s * math.cos(a) - 6 * s)
        ctrl = (top[0] + 16 * s * math.sin(a), top[1] - 12 * s)
        d.line(bezier(top, ctrl, tip), fill=GREEN, width=2)
    d.ellipse([top[0] - 4 * s, top[1] - 2 * s, top[0] + 4 * s, top[1] + 6 * s],
              fill=GREEN)


def mountain(d, cx, base_y, w, h):
    pts = [(cx - w, base_y), (cx, base_y - h), (cx + w, base_y)]
    d.polygon(pts, fill=LAND_D, outline=INK, width=3)
    cap = [(cx - w * 0.32, base_y - h * 0.68), (cx, base_y - h),
           (cx + w * 0.32, base_y - h * 0.68),
           (cx + w * 0.14, base_y - h * 0.58), (cx, base_y - h * 0.66),
           (cx - w * 0.14, base_y - h * 0.58)]
    d.polygon(cap, fill=(250, 244, 224), outline=INK, width=2)
    for i in range(1, 4):
        t = i / 4
        x = cx + w * t
        y = base_y - h * (1 - t)
        d.line([(x, y), (x - 12, y + 16)], fill=INK_SOFT, width=2)


def lighthouse(d, x, y, s=1.0):
    """A ruined lighthouse: tapered tower, broken top, tiny flag."""
    d.polygon([(x - 12 * s, y), (x - 8 * s, y - 52 * s),
               (x + 8 * s, y - 52 * s), (x + 12 * s, y)],
              fill=(242, 232, 200), outline=INK, width=3)
    d.line([(x - 8 * s, y - 52 * s), (x - 2 * s, y - 58 * s),
            (x + 3 * s, y - 50 * s), (x + 8 * s, y - 56 * s)],
           fill=INK, width=3)
    d.rectangle([x - 4 * s, y - 16 * s, x + 4 * s, y], outline=INK, width=2)
    d.ellipse([x - 3 * s, y - 38 * s, x + 3 * s, y - 32 * s], outline=INK, width=2)
    d.line([(x + 2 * s, y - 58 * s), (x + 2 * s, y - 72 * s)], fill=INK, width=2)
    d.polygon([(x + 2 * s, y - 72 * s), (x + 20 * s, y - 68 * s), (x + 2 * s, y - 64 * s)],
              fill=RED, outline=INK)


def ship(d, x, y, s=1.0):
    """A small galleon under sail."""
    d.polygon([(x - 34 * s, y), (x + 34 * s, y), (x + 24 * s, y + 14 * s),
               (x - 24 * s, y + 14 * s)], fill=INK_SOFT, outline=INK, width=2)
    d.line([(x - 6 * s, y), (x - 6 * s, y - 40 * s)], fill=INK, width=2)
    d.line([(x + 12 * s, y), (x + 12 * s, y - 30 * s)], fill=INK, width=2)
    d.polygon([(x - 6 * s, y - 40 * s), (x - 26 * s, y - 8 * s), (x - 6 * s, y - 8 * s)],
              fill=(250, 244, 224), outline=INK, width=2)
    d.polygon([(x + 12 * s, y - 30 * s), (x + 28 * s, y - 6 * s), (x + 12 * s, y - 6 * s)],
              fill=(250, 244, 224), outline=INK, width=2)
    d.polygon([(x - 6 * s, y - 40 * s), (x + 2 * s, y - 38 * s), (x - 6 * s, y - 32 * s)],
              fill=RED, outline=INK)


def serpent(d, x, y, s=1.0):
    """A friendly sea serpent: three humps and a curious head."""
    for hx in (x - 56 * s, x - 18 * s, x + 20 * s):
        d.arc([hx - 16 * s, y - 14 * s, hx + 16 * s, y + 14 * s], 180, 360,
              fill=BLUE, width=3)
    d.line([(x + 34 * s, y - 2 * s), (x + 52 * s, y - 30 * s)], fill=BLUE, width=3)
    d.ellipse([x + 44 * s, y - 46 * s, x + 66 * s, y - 24 * s], outline=BLUE, width=3)
    d.ellipse([x + 59 * s, y - 40 * s, x + 63 * s, y - 36 * s], fill=INK)
    d.arc([x + 48 * s, y - 34 * s, x + 62 * s, y - 22 * s], 15, 165, fill=BLUE, width=2)


def compass(d, cx, cy, r):
    """An eight-point compass rose."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - r * 0.72, cy - r * 0.72, cx + r * 0.72, cy + r * 0.72],
              outline=INK_SOFT, width=1)
    for ang in range(0, 360, 45):
        a = math.radians(ang - 90)
        tip = (cx + r * 0.98 * math.cos(a), cy + r * 0.98 * math.sin(a))
        base1 = (cx + r * 0.14 * math.cos(a + 0.35), cy + r * 0.14 * math.sin(a + 0.35))
        base2 = (cx + r * 0.14 * math.cos(a - 0.35), cy + r * 0.14 * math.sin(a - 0.35))
        fill = INK if ang % 90 == 0 else INK_SOFT
        d.polygon([tip, base1, base2], fill=fill, outline=INK)
    for letter, ang in (("N", -90), ("E", 0), ("S", 90), ("W", 180)):
        a = math.radians(ang)
        lx = cx + (r + 22) * math.cos(a)
        ly = cy + (r + 22) * math.sin(a)
        d.text((lx, ly), letter, font=SERIF_B(26), fill=INK, anchor="mm")
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED, outline=INK, width=2)


def draw():
    img = Image.new("RGB", (W, H), PARCH)
    d = ImageDraw.Draw(img)

    # --- parchment texture: fine speckles only ---
    for _ in range(2600):
        x, y = rng.randrange(W), rng.randrange(H)
        shade = rng.choice([PARCH_D, (244, 228, 186), (222, 196, 138)])
        d.point((x, y), fill=shade)
    # a few very soft blotches, kept away from the title band
    blotch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blotch)
    for _ in range(6):
        x, y = rng.randrange(80, W - 80), rng.randrange(220, H - 80)
        r = rng.randrange(24, 70)
        bd.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7],
                   fill=(206, 178, 118, 26))
    blotch = blotch.filter(ImageFilter.GaussianBlur(18))
    img.paste(Image.alpha_composite(img.convert("RGBA"), blotch).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    # --- light vignette, soft edge ---
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-60, -60, W + 60, H + 60], fill=70)
    vig = vig.filter(ImageFilter.GaussianBlur(140))
    dark = Image.new("RGB", (W, H), (120, 92, 50))
    img.paste(Image.blend(img, dark, 0.30), (0, 0), vig)
    d = ImageDraw.Draw(img)

    # --- frame ---
    d.rectangle([22, 22, W - 22, H - 22], outline=INK, width=4)
    d.rectangle([34, 34, W - 34, H - 34], outline=INK_SOFT, width=2)
    for cx, cy in ((22, 22), (W - 22, 22), (22, H - 22), (W - 22, H - 22)):
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=INK, width=3)

    # --- title cartouche (top centre) ---
    d.text((512, 76), "THE ISLE OF WREN'S REGRET", font=SERIF_B(36),
           fill=INK, anchor="mm")
    d.line([(272, 102), (752, 102)], fill=INK_SOFT, width=2)
    d.text((512, 128), "survey'd by Capt. Marrow — who never came back (twice)",
           font=SERIF_I(21), fill=INK_SOFT, anchor="mm")

    # --- sea doodles ---
    for x, y, s in ((120, 300, 1.1), (150, 520, 0.9), (110, 850, 1.0),
                    (880, 420, 1.0), (920, 640, 0.9), (760, 940, 1.1),
                    (300, 940, 0.9), (900, 300, 0.8), (120, 180, 0.9)):
        wave(d, x, y, s)
    for x, y in ((180, 220), (880, 330), (950, 780), (90, 640), (700, 180)):
        gull(d, x, y, 0.9)
    ship(d, 150, 690, 1.05)
    wave(d, 150, 712, 1.3)
    serpent(d, 830, 890, 1.0)
    d.text((838, 940), "Here be dragons (retired)", font=SERIF_I(19),
           fill=BLUE, anchor="mm")

    # --- compass rose (top right) ---
    compass(d, 870, 196, 56)

    # --- the island ---
    island = chaikin([
        (330, 330), (420, 292), (520, 296), (610, 318), (690, 372),
        (726, 448), (700, 528), (724, 606), (688, 688), (636, 762),
        (556, 806), (462, 824), (376, 800), (306, 748), (252, 676),
        (236, 596), (262, 528), (228, 470), (258, 408), (286, 372),
    ])
    d.polygon(island, fill=LAND, outline=INK, width=4)
    inner = [((x - 512) * 0.94 + 512, (y - 580) * 0.94 + 580) for x, y in island]
    d.line(inner + [inner[0]], fill=INK_SOFT, width=1)
    for _ in range(500):
        ang = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, 1) ** 0.5
        x = 512 + rr * 210 * math.cos(ang)
        y = 580 + rr * 235 * math.sin(ang)
        d.point((int(x), int(y)), fill=LAND_D)

    # --- Gullwhisper Cove (west bay) ---
    d.arc([200, 456, 264, 520], 250, 120, fill=BLUE, width=3)
    d.arc([214, 474, 250, 502], 200, 340, fill=BLUE, width=2)
    label(d, (128, 420), "Gullwhisper", SERIF_I(26), anchor="mm")
    label(d, (128, 448), "Cove", SERIF_I(26), anchor="mm")
    d.line([(168, 448), (228, 478)], fill=INK_SOFT, width=2)
    d.ellipse([226, 476, 232, 482], fill=INK)

    # --- The Ruined Lighthouse (north point) ---
    lighthouse(d, 352, 356, 1.0)
    label(d, (352, 268), "The Ruined", SERIF_I(25), anchor="mm")
    label(d, (352, 294), "Lighthouse", SERIF_I(25), anchor="mm")
    d.line([(352, 306), (352, 330)], fill=INK_SOFT, width=2)

    # --- Mount Grumble (centre) ---
    mountain(d, 512, 628, 78, 96)
    label(d, (512, 500), "Mount Grumble", SERIF_I(26), anchor="mm")
    d.line([(512, 514), (512, 532)], fill=INK_SOFT, width=2)
    for hx, hy in ((430, 640), (600, 648), (470, 668), (560, 676)):
        d.arc([hx - 16, hy - 10, hx + 16, hy + 10], 180, 360, fill=INK_SOFT, width=2)

    # --- Palm Grove of Second Chances (east) ---
    palm(d, 636, 500, 1.0, lean=-8)
    palm(d, 668, 512, 0.85, lean=10)
    palm(d, 606, 514, 0.75, lean=-16)
    label(d, (742, 452), "Palm Grove of", SERIF_I(24), anchor="mm")
    label(d, (742, 480), "Second Chances", SERIF_I(24), anchor="mm")
    d.line([(700, 470), (676, 496)], fill=INK_SOFT, width=2)

    # --- The Giggling Tide Pools (south shore) ---
    for cx, cy, r in ((452, 786, 14), (486, 800, 11), (520, 788, 13)):
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7],
                  outline=BLUE, width=2)
        d.arc([cx - r + 4, cy - 3, cx + r - 4, cy + 4], 200, 340, fill=BLUE, width=2)
    label(d, (512, 884), "The Giggling Tide Pools", SERIF_I(25), anchor="mm")
    d.line([(500, 872), (492, 812)], fill=INK_SOFT, width=2)

    # --- Wreck of the Polite Pirate (south-east shore) ---
    d.polygon([(648, 716), (706, 700), (700, 720), (656, 730)],
              fill=INK_SOFT, outline=INK, width=2)
    d.line([(684, 704), (676, 664)], fill=INK, width=3)
    d.line([(676, 664), (692, 656)], fill=INK, width=2)
    d.polygon([(676, 664), (694, 660), (676, 652)], fill=RED, outline=INK)
    label(d, (806, 742), "Wreck of the", SERIF_I(24), anchor="mm")
    label(d, (806, 770), "Polite Pirate", SERIF_I(24), anchor="mm")
    d.line([(758, 756), (706, 716)], fill=INK_SOFT, width=2)

    # --- dashed route: cove -> mountain -> X ---
    route = [(252, 486), (330, 540), (420, 566), (470, 600),
             (540, 622), (586, 646)]
    dashed(d, route, fill=INK_SOFT, width=3)
    for t in (0.25, 0.5, 0.75):
        i = int(t * (len(route) - 1))
        x0, y0 = route[i]
        d.ellipse([x0 - 3, y0 - 5, x0 + 3, y0 + 5], outline=INK_SOFT, width=2)

    # --- X: Captain Wren's Treasure ---
    d.line([(588, 628), (624, 664)], fill=RED, width=7)
    d.line([(624, 628), (588, 664)], fill=RED, width=7)
    d.ellipse([600, 640, 612, 652], outline=RED, width=3)
    label(d, (706, 596), "Captain Wren's", SERIF_BI(25), fill=RED, anchor="mm")
    label(d, (706, 624), "Treasure", SERIF_BI(25), fill=RED, anchor="mm")
    d.text((606, 692), "X marks the spot (obviously)", font=SERIF_I(18),
           fill=INK_SOFT, anchor="mm")

    # --- scale bar (bottom left, inside frame) ---
    d.line([(70, 916), (190, 916)], fill=INK, width=3)
    for x in (70, 110, 150, 190):
        d.line([(x, 910), (x, 922)], fill=INK, width=3)
    d.text((130, 936), "0 ——— 3 leagues", font=SERIF_I(19), fill=INK, anchor="mm")
    d.text((130, 958), "(a league is however far", font=SERIF_I(16),
           fill=INK_SOFT, anchor="mm")
    d.text((130, 976), "you feel like walking)", font=SERIF_I(16),
           fill=INK_SOFT, anchor="mm")
    d.text((512, 952), "Do not feed the kraken. · No refunds on cursed gold.",
           font=SERIF_I(16), fill=INK_SOFT, anchor="mm")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True, compress_level=9)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    draw()
