#!/usr/bin/env python3
"""Compose the news-image-20261117 front page.

One 1024x1024 PNG: a newspaper front page summing up Tuesday 17 November
2026. All text is drawn with PIL (crisp, never garbled); the four photo
panels are original AI-generated illustrations in assets/ (generated for
this entry, not copied from anywhere). The world map is drawn from
Natural Earth country outlines (assets/world.geo.json, public domain data).
"""
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (20, 20, 20)
GREY = (90, 88, 82)
RED = (163, 22, 33)
RULE = (20, 20, 20)
SEA = (214, 226, 232)
LAND = (198, 192, 176)

FDIR = "/usr/share/fonts/truetype/liberation/"
def serif_b(sz): return ImageFont.truetype(FDIR + "LiberationSerif-Bold.ttf", sz)
def serif(sz): return ImageFont.truetype(FDIR + "LiberationSerif-Regular.ttf", sz)
def serif_i(sz): return ImageFont.truetype(FDIR + "LiberationSerif-Italic.ttf", sz)
def sans_b(sz): return ImageFont.truetype(FDIR + "LiberationSans-Bold.ttf", sz)
def sans(sz): return ImageFont.truetype(FDIR + "LiberationSans-Regular.ttf", sz)
def sans_i(sz): return ImageFont.truetype(FDIR + "LiberationSans-Italic.ttf", sz)

ASSETS = "assets/"
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 20            # side margin
CW = W - 2 * MX    # content width = 984

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def tracked(text, font, cx, y, fill, tracking=6):
    """Draw text centred on cx with letter tracking."""
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w + tracking

def rule(y, weight=2):
    d.line([(MX, y), (W - MX, y)], fill=RULE, width=weight)

# ---------- masthead ----------
d.line([(0, 8), (W, 8)], fill=RULE, width=4)
d.text((W / 2, 16), "THE WORLD IN ONE DAY", font=serif_b(60),
       fill=INK, anchor="ma")
rule(92, 2)
tracked("TUESDAY, 17 NOVEMBER 2026", sans_b(28), W / 2, 100, RED, tracking=7)
d.text((W / 2, 136), "The day's world news — six continents, in one picture",
       font=serif_i(18), fill=GREY, anchor="ma")
rule(160, 3)

# ---------- lead story: Kerch Bridge ----------
d.text((MX, 172), "EUROPE  ·  THE WAR IN UKRAINE", font=sans_b(19), fill=RED)
d.text((MX, 196), "THE BRIDGE IS DOWN", font=serif_b(56), fill=INK)
y = 252
sub = ("Ukraine destroys a span of the Kerch Bridge in an overnight strike, "
       "halting road and rail traffic to Crimea — hours after Russian "
       "missiles hit Kyiv's two river bridges.")
for line in wrap(sub, serif(22), CW):
    d.text((MX, y), line, font=serif(22), fill=INK)
    y += 26
kerch = Image.open(ASSETS + "media-generation-kerch-bridge-0-24f526c7-b240-4575-8b9c-787722b260f7.webp").convert("RGB")
kerch = ImageOps.fit(kerch, (CW, 160), method=Image.LANCZOS, centering=(0.5, 0.42))
img.paste(kerch, (MX, 312))
d.text((MX, 478), "A span of the Kerch Bridge lies in the strait after Tuesday's strike. "
       "Kyiv says the operation took weeks to prepare; Moscow vows to rebuild.",
       font=sans_i(14), fill=GREY)
rule(500, 2)

# ---------- second row: three photo stories + world map, four columns ----------
y0 = 512
COLW, GAP = 234, 16
x1, x2, x3, x4 = MX, MX + COLW + GAP, MX + 2 * (COLW + GAP), MX + 3 * (COLW + GAP)

def photo_col(x, webp, headline, summary, head_font):
    p = Image.open(ASSETS + webp).convert("RGB")
    p = ImageOps.fit(p, (COLW, 90), method=Image.LANCZOS, centering=(0.5, 0.45))
    img.paste(p, (x, y0))
    yy = y0 + 98
    d.text((x, yy), headline, font=head_font, fill=INK)
    yy += 30
    n = 0
    for line in wrap(summary, sans(13), COLW):
        d.text((x, yy), line, font=sans(13), fill=INK)
        yy += 16
        n += 1
    return n

# one headline size for all three photo columns: largest (<=22) that fits
heads = ["MINES IN THE STRAIT", "THE SUMMIT IS SET", "QUAKE OFF TUAL"]
hsize = 22
while hsize > 16 and any(d.textlength(t, font=serif_b(hsize)) > COLW for t in heads):
    hsize -= 1
hf = serif_b(hsize)
n1 = photo_col(x1, "media-generation-hormuz-tanker-0-adb2675a-763c-4bfd-be3c-58b5354ab2f3.webp",
               "MINES IN THE STRAIT",
               "Mines hit tankers near Hormuz; they catch fire. "
               "A third US carrier reaches the Gulf.", hf)
n2 = photo_col(x2, "media-generation-shenzhen-summit-0-be44ab1d-51cd-447c-9e02-d4882bff7d75.webp",
               "THE SUMMIT IS SET",
               "China confirms Xi, Trump and Putin meet in Shenzhen "
               "on Thursday, on the APEC sidelines.", hf)
n3 = photo_col(x3, "media-generation-quake-tual-0-3d809ee4-d514-4fce-935c-c52e827891ca.webp",
               "QUAKE OFF TUAL",
               "Magnitude 6.6 quake near Tual, Indonesia; "
               "no tsunami threat.", hf)

# world map panel, fourth column. Narrower than round 2 (234px); the map
# carries dots only — markers 1/2/7 sit too close together in Europe for
# leader labels at this width, so the legend below carries the numbering.
d.text((x4, y0), "WHERE IT HAPPENED", font=sans_b(15), fill=RED)
map_box = (x4, y0 + 26, x4 + COLW, y0 + 26 + 90)
map_img = Image.new("RGB", (COLW, 90), SEA)
md = ImageDraw.Draw(map_img)
geo = json.load(open(ASSETS + "world.geo.json"))
mw, mh = COLW - 2, 88
def proj(lon, lat):
    return (1 + (lon + 170) / 360 * mw,
            1 + (75 - lat) / 130 * mh)
def draw_poly(coords):
    pts = [proj(lon, lat) for lon, lat in coords]
    if len(pts) > 2:
        md.polygon(pts, fill=LAND)
for feat in geo["features"]:
    g = feat["geometry"]
    if g["type"] == "Polygon":
        draw_poly(g["coordinates"][0])
    elif g["type"] == "MultiPolygon":
        for poly in g["coordinates"]:
            draw_poly(poly[0])
markers = [
    ("1", 36.6, 45.3), ("2", 30.5, 50.4), ("3", 56.3, 26.6),
    ("4", 114.1, 22.5), ("5", 139.7, 35.7), ("6", -77.0, 38.9),
    ("7", 6.1, 46.2), ("8", 30.1, -1.9),
]
for num, lon, lat in markers:
    px, py = proj(lon, lat)
    md.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
               outline=(255, 255, 255), width=1)
img.paste(map_img, (map_box[0], map_box[1]))
d.rectangle(map_box, outline=RULE, width=1)
ly = y0 + 122
d.text((x4, ly), "1 Kerch · 2 Kyiv · 3 Hormuz", font=sans(11), fill=GREY)
d.text((x4, ly + 14), "4 Shenzhen · 5 Tokyo", font=sans(11), fill=GREY)
d.text((x4, ly + 28), "6 Washington · 7 Geneva · 8 Kigali", font=sans(11), fill=GREY)
rule(700, 2)
print("photo headline size:", hsize, "| summary lines:", n1, n2, n3)

# ---------- bottom grid: 12 stories, 4 x 3 ----------
stories = [
    ("KYIV", "Kyiv's bridges hit",
     "North and South crossings shut; heat, water and power cut."),
    ("WASHINGTON", "Pentagon fails audit",
     "Ninth year running; $4.8 trillion unverified."),
    ("WASHINGTON", "Testimony needs approval",
     "White House: agencies must clear staff evidence."),
    ("TECHNOLOGY", "AI chip loophole closing",
     "US acts to stop China renting its computing power."),
    ("EUROPE", "Five states plan Rwanda hub",
     "Joint return centre for rejected asylum seekers."),
    ("TOKYO", "Japan scrambles jets",
     "Two suspected Russian planes enter its airspace."),
    ("LONDON", "UK sanctions settler builders",
     "Eight firms hit over West Bank construction."),
    ("GENEVA", "128 states debate robot arms",
     "UN talks on a ban for lethal autonomous weapons."),
    ("YEMEN", "Houthis advance on Aden",
     "Government forces pull back from the Red Sea coast."),
    ("CLIMATE", "COP31 cash fight stalls",
     "Nepal seeks billions for the Himalayas as talks drag."),
    ("MARKETS", "Bitcoin at four-month low",
     "Slides near $62,000 as big buyers keep accumulating."),
    ("SPACE", "Voyager, one light-day out",
     "NASA probe now 25.9 billion km from Earth."),
]
GW = 234
for i, (tag, head, summ) in enumerate(stories):
    col, row = i % 4, i // 4
    gx = MX + col * (GW + 16)
    gy = 712 + row * 68
    d.text((gx, gy), tag, font=sans_b(13), fill=RED)
    d.text((gx, gy + 16), head, font=serif_b(18), fill=INK)
    for j, line in enumerate(wrap(summ, sans(13), GW)):
        d.text((gx, gy + 38 + j * 15), line, font=sans(13), fill=INK)
rule(924, 2)

# ---------- footer: in brief ----------
# 10 items — the quake moved up to a photo panel, so it leaves this strip.
# Set at 15px (was 12px) with bold kickers so the strip still reads as
# distinct news nuggets at ~300px wide. Word-level flow keeps each kicker
# bold while the text wraps across lines.
brief_items = [
    ("IRAN", "drones hit US radar base in Bahrain"),
    ("US INTEL", "alleged plot vs Trump officials"),
    ("MEASLES", "13 US babies born with it since 2025"),
    ("INDIA", "bus crash kills at least 6"),
    ("TARIFFS", "China–Canada agree cuts"),
    ("ISRAEL", "Netanyahu camp accused of tipping off arrests"),
    ("GAZA", "UK, Australia, Canada, Italy urge aid crossings open"),
    ("DEPARDIEU", "admits sexual assault charge in Paris"),
    ("JPMORGAN", "nationwide outage"),
    ("MOSCOW", "1,441 Ukrainian drones intercepted"),
]
BF = 15
label_f, kick_f, body_f, sep_f = sans_b(BF), sans_b(BF), sans(BF), sans(BF)
tokens = [("IN BRIEF:  ", label_f, RED)]
for i, (kick, text) in enumerate(brief_items):
    if i:
        tokens.append((" · ", sep_f, GREY))
    tokens.append((kick + ": ", kick_f, INK))
    tokens.append((text, body_f, INK))
words = []
for txt, font, fill in tokens:
    for w in txt.split(" "):
        if w:
            words.append((w, font, fill))
SPACE = d.textlength(" ", font=body_f)
lines, cur, cur_w = [], [], 0.0
for w, font, fill in words:
    ww = d.textlength(w, font=font)
    add = ww if not cur else SPACE + ww
    if cur and cur_w + add > CW:
        lines.append(cur)
        cur, cur_w = [(w, font, fill)], ww
    else:
        cur.append((w, font, fill))
        cur_w += add
if cur:
    lines.append(cur)
fy = 932
for line in lines:
    xx = MX
    for w, font, fill in line:
        d.text((xx, fy), w, font=font, fill=fill)
        xx += d.textlength(w, font=font) + SPACE
    fy += 19
print("brief lines:", len(lines), "| last bottom:", fy - 19 + BF)
d.line([(0, H - 8), (W, H - 8)], fill=RULE, width=4)

img.save("entry.png", optimize=True)
print("saved entry.png")
