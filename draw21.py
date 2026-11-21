#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: a 1024x1024 newspaper front page.

One image summing up the world news of Saturday 21 November 2026, drawn
with Pillow (dev-time only; the shipped entry.png is what main.ts copies).
Every story below was checked against reporting dated 21 November 2026
(see SOURCES at the bottom of the image). Claims are marked [CLAIM].
Run: python3 draw21.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (253, 253, 247)
INK = (17, 17, 17)
MUTED = (85, 85, 85)
NAVY = (14, 27, 51)
GOLD = (232, 163, 23)
RED = (178, 34, 34)
CARD_LINE = (170, 170, 160)
OCEAN = (215, 232, 243)
LAND = (233, 220, 195)
LAND_LINE = (184, 166, 126)

DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"


def font(size, bold=False, serif=False, italic=False):
    if serif:
        path = DJ + ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf")
    elif italic:
        path = LB + "LiberationSans-Italic.ttf"
    elif bold:
        path = DJ + "DejaVuSans-Bold.ttf"
    else:
        path = DJ + "DejaVuSans.ttf"
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# region colours
C = {
    "ASIA": (214, 110, 20),
    "MIDEAST": (178, 34, 34),
    "EUROPE": (46, 111, 183),
    "NAM": (123, 94, 167),
    "SAM": (39, 174, 96),
    "OCEANIA": (22, 160, 133),
    "GLOBAL": (102, 102, 102),
}

# (n, place, region, category, headline, body, source, lat, lon or None)
LEADS = [
    (1, "ANTALYA", "ASIA", "CLIMATE",
     "COP31 runs into overtime",
     "Negotiators work an extra day after the draft drops all mention of coal, oil and gas, and the $120bn adaptation figure.",
     "AP; Reuters", 36.9, 30.7),
    (2, "RIYADH", "MIDEAST", "WAR",
     "Three Houthi missiles shot down over Riyadh",
     "Air defences destroy three ballistic missiles fired at the capital early on Saturday \u2014 the third night of alerts in a row. No casualties.",
     "Reuters; AFP", 24.7, 46.7),
    (3, "JUN\u00cdN, PERU", "SAM", "QUAKE",
     "M6.7 quake shakes central Peru",
     "The tremor strikes at 19:09 local time near Carhuamayo, 108 km deep, and is felt in Lima. No deaths or serious damage; USGS issues a green alert.",
     "USGS; IGP", -10.9, -76.0),
]

MEDIUMS = [
    (4, "MERCURY", "GLOBAL", "SPACE",
     "BepiColombo fires into Mercury orbit",
     "At 19:24 CET the ESA\u2013JAXA probe fires its thrusters to enter Mercury's orbit.",
     "ESA", None, None),
    (5, "POLAND", "EUROPE", "WAR",
     "Russian missile lands in Poland",
     "A missile lands in Nowy Lipowiec in the barrage on Ukraine; NATO calls it a grave violation.",
     "Reuters", 50.3, 22.9),
    (6, "NEW YORK", "NAM", "MARKETS",
     "Wall Street slides into correction",
     "S&P 500 \u22123.7%, Nasdaq \u22125.3% in an AI selloff; Nvidia falls 13.8% as the SEC probes its accounts.",
     "CNBC; Reuters", 40.7, -74.0),
    (7, "WASHINGTON", "NAM", "COURTS",
     "SEC charges $560m AI Ponzi scheme",
     "Backward Hat Capital is accused of raising $560m from 2,000 investors in a fake AI forex fund.",
     "SEC", 38.9, -77.0),
    (8, "KHARG ISLAND", "MIDEAST", "ENERGY",
     "Iranian tankers mass to test US blockade",
     "Satellite data show 14+ Iranian tankers gathering at Kharg Island to sail as a convoy.",
     "Reports", 29.2, 50.3),
    (9, "WASHINGTON", "NAM", "TECH",
     "Trump threatens tax on AI data centres abroad",
     "He vows to bar US firms from building AI data centres abroad and impose a \u201ctremendous tax\u201d.",
     "Reuters", 38.9, -77.0),
    (10, "LOS ANGELES", "NAM", "COURTS",
     "Palisades Fire arsonist convicted",
     "A jury convicts Jonathan Rinderknecht of starting the Palisades Fire in Los Angeles.",
     "AP", 34.0, -118.2),
    (11, "WORLD", "GLOBAL", "BUSINESS",
     "GTA VI takes $3.8bn in one day",
     "Rockstar's sequel posts the biggest entertainment launch in history on day one.",
     "Industry reports", None, None),
    (12, "US", "NAM", "COURTS",
     "Judge approves $7.25bn Bayer payout",
     "A judge signs off the $7.25bn settlement of claims that weedkiller Roundup causes cancer.",
     "Reuters", None, None),
    (13, "WELLINGTON", "OCEANIA", "SPORT",
     "KL Rahul completes the SENA set",
     "His Wellington 100 makes him the first Indian opener with Test centuries in all four SENA countries.",
     "AP", -41.3, 174.8),
]

# (n, place, region, one-line story, source, lat, lon or None)
ALSO = [
    (14, "KRYVYI RIH", "EUROPE", "Russian double-tap kills 2, injures 42, incl. 4 children", "Vilkul", 47.9, 33.4),
    (15, "HODEIDAH", "MIDEAST", "Saudi strikes hit Yemeni cities; 41 dead claimed, unverified [CLAIM]", "Reports", 14.8, 42.9),
    (16, "SHENZHEN", "ASIA", "Trump and Xi agree humans stay in the loop on military AI", "Bessent", 22.5, 114.1),
    (17, "CRYPTO", "GLOBAL", "Binance hacker moves ~$594m in ETH in two days", "Cointelegraph", None, None),
    (18, "CRYPTO", "GLOBAL", "Wrapped Monero token XMR1 \u221299% after a $13.5m hack", "Decrypt", None, None),
    (19, "LONDON", "EUROPE", "Russell Brand appeals as his 10-year sentence begins", "UK press", 51.5, -0.1),
    (20, "COPENHAGEN", "EUROPE", "Denmark expels a Russian diplomat over an alleged murder plot", "Reuters", 55.7, 12.6),
    (21, "HAVANA", "NAM", "US woman freed after 10 years in Cuba; no swap reported", "Reports", 23.1, -82.4),
    (22, "NEW YORK", "NAM", "Indian man gets 19 years in Sikh separatist murder plot", "US court", 40.7, -74.0),
    (23, "EUROPE", "EUROPE", "Cost-of-living protests spread across the continent into Saturday", "AP", None, None),
    (24, "TEHRAN", "MIDEAST", "Trump in no rush on Iran; a decision may wait until 2027", "Press", 35.7, 51.4),
    (25, "NEW DELHI", "ASIA", "Record \u20b91.22 lakh crore flows into Indian shares in November", "Depositories", 28.6, 77.2),
    (26, "NEW YORK", "NAM", "Mamdani sets 2032 as the date to close Rikers Island", "City Hall", 40.7, -74.0),
    (27, "KATHMANDU", "ASIA", "Nepal's PM Balen heads to Delhi on his first foreign trip", "Govt", 27.7, 85.3),
    (28, "TURIN", "EUROPE", "Zverev beats Fils to reach the ATP Finals semi-finals", "ATP", 45.1, 7.7),
    (29, "LAS VEGAS", "NAM", "Rain soaks F1 practice; Russell goes fastest", "F1", 36.2, -115.1),
    (30, "BHOPAL", "ASIA", "India women beat Malaysia 4\u20131 in their hockey opener", "Hockey India", 23.3, 77.4),
    (31, "VIENNA", "EUROPE", "Austria says its foreign ministry website was hacked", "Ministry", 48.2, 16.4),
    (32, "LONDON", "EUROPE", "Lauren Price becomes undisputed world champion", "BBC", 51.5, -0.1),
    (33, "SAN FRANCISCO", "NAM", "OpenAI launches MedChemBench; GPT-6.2 Astra scores 84.5%", "OpenAI", 37.8, -122.4),
    (34, "SAN FRANCISCO", "NAM", "Thinking Machines releases Inkling 2 Mini with Hugging Face", "HF", 37.8, -122.4),
    (35, "SAN FRANCISCO", "NAM", "AWS ships Textract Insights for verifiable AI documents", "AWS", 37.8, -122.4),
    (36, "WASHINGTON", "NAM", "Disclosure: Trump's account made 751 trades in Nvidia, Palantir, SpaceX", "Filing", 38.9, -77.0),
]

NUMBERS = [
    ("3", "Houthi missiles downed over Riyadh", "Reuters"),
    ("M6.7", "Peru quake, no deaths reported", "USGS"),
    ("\u22123.7%", "S&P 500 slides into correction", "CNBC"),
    ("19:24 CET", "BepiColombo's Mercury burn", "ESA"),
    ("3rd draft", "COP31 text due Saturday", "AP"),
    ("$3.8bn", "GTA VI's first-day sales", "Industry"),
]

REGIONS = [("ASIA", 5), ("MIDEAST", 4), ("EUROPE", 8), ("N. AMERICA", 13),
           ("S. AMERICA", 1), ("OCEANIA", 1), ("GLOBAL", 4)]

NOT_TODAY = [
    ("FRI 20 NOV", "Kyiv's overnight barrage: 7 killed, 3 bridges hit"),
    ("FRI 20 NOV", "Cyclone Akvan's landfall in Odisha"),
    ("FRI 20 NOV", "UK\u2013EU summit deals on food, carbon, youth mobility"),
    ("THU 19 NOV", "ICJ rules Myanmar committed genocide, 9\u20136"),
    ("THU 19 NOV", "Anthropic's $81.3bn Nasdaq debut"),
    ("THU 19 NOV", "Trump\u2013Xi\u2013Putin summit in Shenzhen"),
    ("THU 19 NOV", "Houthi missile hits Riyadh's PIF tower"),
    ("FRI 20 NOV", "US adds four Iranians to the OFAC sanctions list"),
]

# Simplified continent outlines as (lon, lat) points.
NA = [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-100, 68),
      (-90, 66), (-85, 66), (-82, 70), (-75, 68), (-68, 62), (-65, 60),
      (-60, 58), (-55, 52), (-60, 47), (-65, 45), (-70, 42), (-74, 39),
      (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-89, 29), (-94, 29),
      (-97, 26), (-102, 24), (-106, 22), (-105, 20), (-100, 18), (-95, 16),
      (-90, 14), (-86, 12), (-83, 9), (-79, 8), (-78, 7), (-81, 9),
      (-85, 11), (-90, 14), (-95, 16), (-100, 18), (-105, 20), (-110, 24),
      (-114, 29), (-118, 33), (-122, 37), (-124, 42), (-124, 48), (-128, 52),
      (-135, 58), (-145, 60), (-152, 58), (-158, 56), (-164, 58), (-168, 66)]
SA = [(-79, 9), (-76, 11), (-72, 12), (-68, 11), (-62, 9), (-58, 6),
      (-52, 5), (-50, 1), (-46, -2), (-42, -4), (-37, -6), (-35, -9),
      (-38, -14), (-40, -20), (-42, -23), (-48, -27), (-52, -32), (-57, -38),
      (-62, -40), (-65, -43), (-68, -48), (-69, -52), (-71, -54), (-73, -50),
      (-73, -44), (-73, -37), (-72, -30), (-70, -22), (-70, -18), (-73, -16),
      (-77, -12), (-80, -6), (-81, -1), (-80, 3), (-79, 7), (-79, 9)]
AF = [(-17, 15), (-16, 20), (-15, 25), (-12, 28), (-9, 32), (-5, 35),
      (-1, 35), (3, 37), (9, 37), (11, 34), (15, 32), (20, 32), (25, 31),
      (30, 31), (32, 29), (34, 27), (35, 23), (37, 18), (39, 15), (41, 12),
      (44, 11), (48, 11), (51, 11), (48, 7), (44, 2), (41, -3), (40, -8),
      (39, -13), (37, -18), (34, -22), (32, -27), (29, -31), (26, -34),
      (21, -35), (18, -32), (16, -28), (14, -22), (13, -16), (12, -10),
      (11, -5), (9, 1), (8, 4), (4, 6), (-2, 5), (-8, 4), (-13, 8),
      (-16, 11), (-17, 15)]
EU = [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-4, 48),
      (-1, 49), (2, 51), (4, 53), (7, 54), (8, 57), (10, 59), (8, 58),
      (6, 60), (5, 62), (10, 64), (14, 67), (18, 69), (22, 70), (26, 71),
      (30, 70), (32, 68), (30, 66), (28, 62), (27, 59), (24, 58), (22, 57),
      (20, 54), (18, 54), (15, 54), (12, 54), (10, 54), (8, 53), (5, 53),
      (2, 51), (0, 49), (-2, 47), (-4, 44), (-6, 40), (-9, 37), (-10, 36)]
AS = [(60, 68), (65, 69), (70, 71), (75, 72), (80, 73), (85, 74),
      (90, 75), (95, 76), (100, 77), (105, 77), (110, 76), (115, 74),
      (120, 73), (125, 72), (130, 71), (135, 71), (140, 72), (145, 72),
      (150, 71), (155, 70), (160, 69), (165, 67), (170, 67), (175, 65),
      (178, 64), (172, 62), (168, 60), (162, 58), (158, 54), (156, 51),
      (152, 55), (148, 59), (144, 59), (142, 54), (140, 50), (138, 46),
      (135, 44), (132, 43), (130, 42), (128, 39), (126, 38), (124, 38),
      (122, 39), (120, 36), (121, 32), (120, 28), (118, 25), (115, 23),
      (112, 22), (109, 20), (107, 18), (105, 15), (104, 10), (103, 7),
      (101, 5), (99, 3), (98, 6), (97, 10), (96, 15), (94, 17), (92, 21),
      (90, 22), (88, 22), (86, 20), (84, 18), (82, 16), (80, 14), (80, 10),
      (78, 8), (77, 9), (76, 12), (75, 15), (74, 19), (72, 20), (70, 22),
      (68, 23), (66, 25), (64, 25), (62, 25), (60, 25), (58, 26), (56, 27),
      (54, 28), (52, 29), (50, 29), (48, 30), (48, 33), (47, 36), (44, 38),
      (42, 41), (40, 41), (38, 40), (36, 36), (38, 38), (40, 42), (44, 44),
      (48, 47), (52, 51), (55, 56), (58, 61), (60, 65), (58, 68), (52, 68),
      (45, 68), (38, 68), (32, 68), (28, 70), (35, 70), (42, 69), (50, 68),
      (60, 68)]
AU = [(114, -22), (114, -30), (115, -34), (118, -35), (124, -33), (129, -32),
      (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
      (153, -32), (153, -27), (150, -23), (147, -19), (146, -15), (142, -11),
      (141, -13), (137, -12), (136, -15), (135, -12), (132, -11), (130, -13),
      (128, -14), (126, -14), (124, -16), (122, -17), (120, -20), (117, -20),
      (114, -22)]



# ---------------------------------------------------------------- layout
MX = 12          # outer margin
CW = W - 2 * MX  # content width


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead band (navy), 0-108 ----
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((MX, 12), "ONE DAY  \u00b7  ONE PAGE", font=font(15, bold=True), fill=GOLD)
    right = "36 STORIES  \u00b7  7 REGIONS  \u00b7  1 DAY"
    d.text((W - MX - font(15, bold=True).getlength(right), 12), right,
           font=font(15, bold=True), fill=GOLD)
    d.text((MX, 30), "SATURDAY 21 NOVEMBER 2026", font=font(44, bold=True, serif=True),
           fill=(255, 255, 255))
    d.text((MX, 84),
           "The world in a single day \u2014 every story below happened, or was first reported, "
           "on Saturday 21 November 2026.",
           font=font(13, italic=True), fill=(200, 208, 220))

    # ---- key numbers strip, 114-174 ----
    y = 114
    bw = (CW - 5 * 6) // 6
    for i, (num, label, _src) in enumerate(NUMBERS):
        x = MX + i * (bw + 6)
        d.rectangle([x, y, x + bw, y + 60], outline=CARD_LINE, width=1, fill=(255, 255, 255))
        d.text((x + 8, y + 5), num, font=font(24, bold=True), fill=RED)
        for j, ln in enumerate(wrap(label, font(11), bw - 16)):
            d.text((x + 8, y + 33 + j * 12), ln, font=font(11), fill=INK)

    # ---- region bar, 180-204 ----
    y = 180
    d.rectangle([MX, y, MX + CW, y + 24], fill=NAVY)
    d.text((MX + 8, y + 4), "WHERE THE NEWS CAME FROM", font=font(13, bold=True), fill=GOLD)
    rx = MX + 235
    keymap = {"ASIA": "ASIA", "MIDEAST": "MIDEAST", "EUROPE": "EUROPE",
              "N. AMERICA": "NAM", "S. AMERICA": "SAM", "OCEANIA": "OCEANIA",
              "GLOBAL": "GLOBAL"}
    for name, count in REGIONS:
        col = C[keymap[name]]
        d.ellipse([rx, y + 7, rx + 10, y + 17], fill=col)
        t = f"{name} {count}"
        d.text((rx + 14, y + 4), t, font=font(12, bold=True), fill=(255, 255, 255))
        rx += 14 + font(12, bold=True).getlength(t) + 12

    # ---- lead cards, 208-370 ----
    y = 208
    lw = (CW - 2 * 10) // 3
    lh = 162
    for i, s in enumerate(LEADS):
        n, place, region, cat, head, body, src, _la, _lo = s
        x = MX + i * (lw + 10)
        col = C[region]
        d.rectangle([x, y, x + lw, y + lh], outline=CARD_LINE, width=1, fill=(255, 255, 255))
        d.rectangle([x, y, x + lw, y + 5], fill=col)
        d.text((x + 10, y + 11), f"{n}  \u00b7  {place}  \u00b7  {cat}",
               font=font(12, bold=True), fill=col)
        yy = block(d, x + 10, y + 30, wrap(head, font(23, bold=True), lw - 20),
                   font(23, bold=True), leading=26)
        block(d, x + 10, yy + 4, wrap(body, font(13), lw - 20), font(13), leading=16)
        d.text((x + 10, y + lh - 17), f"Sources: {src}", font=font(10, italic=True), fill=MUTED)

    # ---- medium cards, rows at 376 and 474, height 92 ----
    mw = (CW - 4 * 8) // 5
    mh = 92
    for row in range(2):
        yy = 376 + row * (mh + 6)
        for i in range(5):
            s = MEDIUMS[row * 5 + i]
            n, place, region, cat, head, body, src, _la, _lo = s
            x = MX + i * (mw + 8)
            col = C[region]
            d.rectangle([x, yy, x + mw, yy + mh], outline=CARD_LINE, width=1,
                        fill=(255, 255, 255))
            d.rectangle([x, yy, x + mw, yy + 4], fill=col)
            d.text((x + 8, yy + 8), f"{n} \u00b7 {place} \u00b7 {cat}",
                   font=font(10, bold=True), fill=col)
            y2 = block(d, x + 8, yy + 23, wrap(head, font(13, bold=True), mw - 16),
                       font(13, bold=True), leading=15)
            block(d, x + 8, y2 + 2, wrap(body, font(10), mw - 16), font(10), leading=12)

    # ---- map + "also on" list, headers at 572 ----
    y = 572
    d.text((MX, y), "WHERE IT HAPPENED \u2014 pins are story numbers",
           font=font(13, bold=True), fill=INK)
    d.text((MX + 440, y), "ALSO ON SATURDAY 21 NOVEMBER",
           font=font(13, bold=True), fill=INK)
    my = 592
    mh2 = 304
    d.rectangle([MX, my, MX + 424, my + mh2], outline=CARD_LINE, width=1, fill=OCEAN)

    def proj(lon, lat):
        px = MX + (lon + 170) / 360.0 * 424
        py = my + (78 - lat) / 136.0 * mh2
        return px, py

    for poly in (NA, SA, AF, EU, AS, AU):
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for lon, lat in [(-2, 54), (138, 37), (141, 41), (172, -41), (167, -45)]:
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=LAND, outline=LAND_LINE)
    # ocean labels last so continents never cover them
    d.text((MX + 150, my + 150), "ATLANTIC", font=font(11, italic=True), fill=(120, 140, 155))
    d.text((MX + 28, my + 200), "PACIFIC", font=font(11, italic=True), fill=(120, 140, 155))
    d.text((MX + 290, my + 245), "INDIAN", font=font(11, italic=True), fill=(120, 140, 155))

    placed = []
    all_stories = list(LEADS) + list(MEDIUMS)
    pin_items = [(s[0], s[7], s[8]) for s in all_stories if s[7] is not None]
    pin_items += [(s[0], s[5], s[6]) for s in ALSO if s[5] is not None]
    # same-location pins fan out in a small circle around the true spot
    nudges = [(0, 0), (13, -9), (-13, -9), (13, 9), (-13, 9), (0, -15), (0, 15), (19, 0)]
    seen_spots = {}
    for n, lat, lon in pin_items:
        base = proj(lon, lat)
        k = seen_spots.get((lat, lon), 0)
        seen_spots[(lat, lon)] = k + 1
        dx, dy = nudges[k % len(nudges)]
        px, py = base[0] + dx, base[1] + dy
        placed.append((px, py))
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        t = str(n)
        fnt = font(9, bold=True)
        d.text((px - fnt.getlength(t) / 2, py - 6), t, font=fnt, fill=(255, 255, 255))
    d.text((MX + 6, my + mh2 - 16), "Map positions approximate; dots are numbered to the stories.",
           font=font(10, italic=True), fill=MUTED)

    # also list: two columns, source inline, 2 lines max per item
    lx = MX + 440
    lw2 = (CW - 440) // 2 - 6
    for col_i in range(2):
        items = ALSO[:12] if col_i == 0 else ALSO[12:]
        xx = lx + col_i * (lw2 + 12)
        yy = my
        for n, place, _region, text, src, _la, _lo in items:
            full = f"{n}. {place} \u2014 {text} ({src})"
            lines = wrap(full, font(10), lw2)[:2]
            head = f"{n}. {place} \u2014 "
            first = lines[0]
            cut = min(len(head), len(first))
            d.text((xx, yy), first[:cut], font=font(10, bold=True), fill=INK)
            d.text((xx + font(10, bold=True).getlength(first[:cut]), yy),
                   first[cut:], font=font(10), fill=INK)
            yy += 13
            for ln in lines[1:]:
                d.text((xx, yy), ln, font=font(10), fill=INK)
                yy += 13

    # ---- date check box, 902-964 ----
    y = 902
    d.rectangle([MX, y, MX + CW, y + 64], outline=RED, width=2, fill=(255, 240, 240))
    d.text((MX + 8, y + 4), "\u2717  DATE CHECK \u2014 THESE ARE NOT ON 21 NOVEMBER:",
           font=font(13, bold=True), fill=RED)
    colw = CW // 2
    for i, (when, text) in enumerate(NOT_TODAY):
        xx = MX + 8 + (i // 4) * colw
        yy = y + 23 + (i % 4) * 10
        d.text((xx, yy), when, font=font(9, bold=True), fill=RED)
        d.text((xx + 72, yy), text, font=font(9), fill=INK)

    # ---- footer ----
    d.text((MX, 972),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 USGS \u00b7 ESA \u00b7 SEC \u00b7 CNBC \u00b7 BBC \u00b7 ATP \u00b7 F1 \u00b7 OpenAI \u00b7 "
           "Hugging Face \u00b7 AWS \u00b7 Cointelegraph \u00b7 Decrypt. Every story verified against reporting dated Saturday 21 November 2026.",
           font=font(10), fill=MUTED)
    d.text((MX, 985),
           "Claims are attributed, not stated as fact \u00b7 Drawn by an AI agent for make.fun \u00b7 news-image-20261121",
           font=font(10, italic=True), fill=MUTED)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
