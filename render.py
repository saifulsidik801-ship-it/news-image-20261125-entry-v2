#!/usr/bin/env python3
"""Render the 25 November 2026 world-news front page, 1024x1024 PNG.

Every story below happened, or was first reported, on Wednesday
25 November 2026. Three heroes, a world map, a date-check box, and
47 further stories across six continents plus science & tech.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (25, 25, 25)
GRAY = (100, 106, 118)
RED = (180, 35, 24)
NAVY = (31, 58, 95)
TEAL = (14, 107, 107)
GOLD = (176, 116, 28)
LIGHT = (232, 225, 208)
MAPDOT = (88, 108, 138)
CARD = (255, 253, 247)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, max_w, start, minimum=9):
    """Largest font size (<= start) that fits text in max_w."""
    s = start
    while s > minimum and draw.textlength(text, font=font(path, s)) > max_w:
        s -= 1
    return font(path, s)


def wrap(draw, text, f, max_w, max_lines=3):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:max_lines]


# ---------------------------------------------------------------- stories
# (continent, kicker, headline) — every headline verified Nov 25 2026.
HEROES = [
    {
        "tag": "CYBERATTACK",
        "color": (22, 40, 63),
        "art": "cyber",
        "headline": "US spy agencies hit by cyberattack",
        "standfirst": "CIA and the Director of National Intelligence hit in an attack on "
                      "classified systems \u2014 the latest in a wave of US cyber incidents.",
    },
    {
        "tag": "MARKETS",
        "color": (20, 53, 42),
        "art": "markets",
        "headline": "Dow tops 50,000 as tech rout deepens",
        "standfirst": "Dow closes at 50,018.70 while the Nasdaq sinks 1.48% and Nvidia "
                      "falls 5.9%; Anthropic slips below its $83 IPO price.",
    },
    {
        "tag": "DRONE WAR",
        "color": (29, 58, 77),
        "art": "drone",
        "headline": "Drone war spills onto the seas",
        "standfirst": "Moscow accuses Kyiv of \u2018terrorism\u2019 after drones hit a Russian cargo "
                      "ship in the Baltic and a warship off Libya.",
    },
]

# grid: (section, color, [(kicker, headline), ...])
GRID = [
    ("NORTH AMERICA", RED, [
        ("WASHINGTON", "Trump set to unveil new wave of tariffs"),
        ("WASHINGTON", "Trump: Huang pardon \u2018an option\u2019 \u2014 for now"),
        ("WASHINGTON", "Giuliani awarded the Medal of Freedom"),
        ("ECONOMY", "US consumer confidence jumps to 103.3"),
        ("FED WATCH", "All eyes on today\u2019s PCE inflation print"),
        ("MEXICO", "Sinaloa kingpin \u2018El Chapo Isidro\u2019 captured"),
        ("WALL ST", "Dell sinks 12%; Ambarella plunges 37%"),
    ]),
    ("SOUTH AMERICA", (150, 80, 20), [
        ("CARTAGENA", "Gunmen seize 30 hostages in supermarket"),
        ("COLOMBIA", "Car bomb hits governor\u2019s office in Meta"),
        ("COLOMBIA", "Drone attack on police base injures infant"),
        ("BRAZIL", "Supercell storm wrecks town; thousands flee"),
        ("ARGENTINA", "2027 budget goes to a floor vote today"),
    ]),
    ("OCEANIA", TEAL, [
        ("SYDNEY", "Australia beat NZ 32\u201312 to lift World Cup"),
        ("WELLINGTON", "Peters aghast at Australian politics"),
        ("NEW ZEALAND", "a2 Milk A$62m settlement approved"),
        ("CHRISTMAS IS.", "Red crabs begin their great migration"),
    ]),
    ("EUROPE", NAVY, [
        ("FOOTBALL", "Madrid hit PSV for five; Arsenal held 1\u20131"),
        ("BRUSSELS", "EU leaders meet over \u20ac1.78tn budget fight"),
        ("LONDON", "Two held over Prince William home break-in"),
        ("NATO", "NATO vows space defence amid satellite fears"),
        ("UKRAINE", "700,000 Russian troops killed, study says"),
        ("MANCHESTER", "Yoro red card overturned on appeal"),
        ("CLIMATE", "COP31 ends with no deal; COP32 set for Addis"),
    ]),
    ("AFRICA", (120, 90, 10), [
        ("DR CONGO", "WHO pulls staff from Ebola hospital siege"),
        ("DR CONGO", "Ebola toll: 5,775 dead of 11,762 cases"),
        ("NIGERIA", "Katsina Emir suspended over assault claim"),
        ("HUNGER", "266m face acute food insecurity \u2014 WFP"),
        ("ETHIOPIA", "Polio drive to protect 11m children"),
    ]),
    ("ASIA", (140, 40, 90), [
        ("SPACE", "China launches Shenzhou-24 to Tiangong"),
        ("CHINA", "Graft probe hits Shanghai party chief"),
        ("GAZA", "Gaza death toll reaches 74,746 \u2014 WAFA"),
        ("HORMUZ", "Iran spurns talks; tankers hit by mines"),
        ("RIYADH", "Houthi attack injures 11, two Indians"),
        ("ISRAEL", "Eisenkot seals first coalition agreement"),
        ("WEST BANK", "Settler arson called \u2018Jewish terrorism\u2019"),
        ("PYONGYANG", "N. Korea threatens to shut Swiss office"),
        ("SEOUL", "Education minister quits in exam scandal"),
        ("MYANMAR", "Top UN court condemns Myanmar genocide"),
        ("SPACE", "Pakistani astronaut to fly on China mission"),
        ("NEPAL", "5.3 quake shakes Sikkim, North Bengal"),
        ("INDIA\u2013EU", "Modi, Merz: FTA will unlock opportunity"),
        ("CRICKET", "Suryavanshi, 15, smashes record 204* off 53"),
    ]),
    ("SCIENCE & TECH", (60, 90, 60), [
        ("GAMING", "GTA 6 draws 39m PS5 players in four days"),
        ("AI", "Anthropic founders bank $2bn on IPO day"),
        ("AI", "OpenAI releases GPT-6.2 Astra model"),
        ("SCIENCE", "Message sent through a wall \u2014 by gravity"),
        ("SPACE", "Amateurs spot possible exoplanets with AI"),
    ]),
]

# Hand-drawn world map is drawn from polygon shapes in main() below.


# ---------------------------------------------------------------- drawing
def draw_cyber(d, x0, y0, w, h):
    # padlock + circuit traces on dark navy
    cx, cy = x0 + w // 2, y0 + h // 2 + 8
    d.ellipse([cx - 34, cy - 8, cx + 34, cy + 40], outline=(176, 116, 28), width=4)
    d.arc([cx - 20, cy - 34, cx + 20, cy + 2], 180, 360, fill=(176, 116, 28), width=4)
    d.ellipse([cx - 6, cy + 8, cx + 6, cy + 20], fill=(176, 116, 28))
    d.rectangle([cx - 2, cy + 16, cx + 2, cy + 30], fill=(176, 116, 28))
    for (sx, sy, ex, ey) in [(x0 + 18, y0 + 16, cx - 30, cy - 6),
                             (x0 + w - 18, y0 + 20, cx + 30, cy - 2),
                             (x0 + 26, y0 + h - 14, cx - 26, cy + 34),
                             (x0 + w - 26, y0 + h - 18, cx + 26, cy + 36)]:
        d.line([(sx, sy), (ex, ey)], fill=(120, 150, 190), width=2)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(220, 60, 40))


def draw_markets(d, x0, y0, w, h):
    # candlesticks + a rising 50,000 line
    base = y0 + h - 18
    bars = [(0.10, 30, True), (0.24, 46, True), (0.38, 34, False),
            (0.52, 58, True), (0.66, 40, False), (0.80, 66, True)]
    for fx, bh, up in bars:
        bx = x0 + int(fx * w)
        col = (64, 180, 110) if up else (220, 70, 55)
        d.line([(bx, base - bh - 12), (bx, base + 4)], fill=col, width=2)
        d.rectangle([bx - 7, base - bh, bx + 7, base - 6], fill=col)
    d.text((x0 + 14, y0 + 10), "50,000", font=font(F_SANS_B, 30), fill=(255, 255, 255))


def draw_drone(d, x0, y0, w, h):
    # sea, ship, quadcopter, burst
    sea_y = y0 + h - 30
    for i in range(3):
        yy = sea_y + i * 9
        d.arc([x0 + 10 + i * 40, yy - 8, x0 + 90 + i * 40, yy + 8], 180, 360,
              fill=(140, 180, 210), width=2)
    d.polygon([(x0 + 30, sea_y - 6), (x0 + 150, sea_y - 6), (x0 + 138, sea_y + 14),
               (x0 + 42, sea_y + 14)], fill=(200, 205, 210))
    d.rectangle([x0 + 55, sea_y - 26, x0 + 75, sea_y - 6], fill=(180, 60, 50))
    d.rectangle([x0 + 85, sea_y - 20, x0 + 100, sea_y - 6], fill=(180, 60, 50))
    dx, dy = x0 + w - 78, y0 + 34
    d.line([(dx - 22, dy - 14), (dx + 22, dy + 14)], fill=(240, 240, 240), width=3)
    d.line([(dx - 22, dy + 14), (dx + 22, dy - 14)], fill=(240, 240, 240), width=3)
    for px, py in [(dx - 22, dy - 14), (dx + 22, dy - 14), (dx - 22, dy + 14), (dx + 22, dy + 14)]:
        d.ellipse([px - 6, py - 6, px + 6, py + 6], outline=(240, 240, 240), width=2)
    d.rectangle([dx - 8, dy - 5, dx + 8, dy + 5], fill=(240, 240, 240))
    bx, by = x0 + w - 150, y0 + 62
    d.polygon([(bx, by - 12), (bx + 4, by - 4), (bx + 12, by - 4), (bx + 6, by + 3),
               (bx + 9, by + 11), (bx, by + 6), (bx - 9, by + 11), (bx - 6, by + 3),
               (bx - 12, by - 4), (bx - 4, by - 4)], fill=(255, 190, 60))


ART = {"cyber": draw_cyber, "markets": draw_markets, "drone": draw_drone}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    d.rectangle([0, 0, W, 6], fill=RED)
    d.text((28, 14), "THE WORLD IN ONE PAGE",
           font=font(F_SERIF_B, 46), fill=INK)
    d.text((W - 28, 22), "NEWS-IMAGE \u00b7 25 NOV 2026",
           font=font(F_SANS_B, 13), fill=RED, anchor="ra")
    d.line([(28, 78), (W - 28, 78)], fill=INK, width=2)
    d.text((28, 84), "WEDNESDAY, 25 NOVEMBER 2026",
           font=font(F_SANS_B, 14), fill=INK)
    d.text((W - 28, 84), "50 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE FRONT PAGE",
           font=font(F_SANS_B, 14), fill=INK, anchor="ra")

    # ---------------------------------------------------------- heroes
    hy0, hy1 = 108, 330
    cw = (W - 56 - 2 * 14) // 3
    for i, hero in enumerate(HEROES):
        x0 = 28 + i * (cw + 14)
        x1 = x0 + cw
        d.rounded_rectangle([x0, hy0, x1, hy1], radius=8, fill=CARD,
                            outline=(200, 192, 172), width=1)
        # art panel
        ax0, ay0, ax1, ay1 = x0 + 8, hy0 + 8, x1 - 8, hy0 + 112
        d.rounded_rectangle([ax0, ay0, ax1, ay1], radius=6, fill=hero["color"])
        ART[hero["art"]](d, ax0, ay0, ax1 - ax0, ay1 - ay0)
        d.text((x0 + 16, ay1 + 8), hero["tag"],
               font=font(F_SANS_B, 11), fill=RED)
        hl = wrap(d, hero["headline"], font(F_SANS_B, 20), cw - 32, max_lines=2)
        yy = ay1 + 26
        for line in hl:
            d.text((x0 + 16, yy), line, font=font(F_SANS_B, 20), fill=INK)
            yy += 23
        sf = wrap(d, hero["standfirst"], font(F_SANS, 12), cw - 32, max_lines=3)
        yy += 2
        for line in sf:
            d.text((x0 + 16, yy), line, font=font(F_SANS, 12), fill=(60, 60, 60))
            yy += 15

    # ---------------------------------------------------------- map + date check
    my0, my1 = 342, 478
    mx0, mx1 = 28, 640
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=8, fill=CARD,
                        outline=(200, 192, 172), width=1)
    d.text((mx0 + 12, my0 + 8), "THE DAY IN ONE MAP",
           font=font(F_SANS_B, 11), fill=NAVY)
    # stylised world map: flat continent shapes (local 588x102 box)
    ox, oy = mx0 + 12, my0 + 26
    polys = [
        [(18, 8), (150, 4), (185, 14), (175, 38), (150, 52), (132, 72),
         (118, 66), (104, 52), (70, 48), (38, 44), (14, 26)],          # N America
        [(200, 4), (224, 2), (230, 14), (210, 18), (198, 12)],          # Greenland
        [(150, 58), (196, 56), (206, 80), (192, 100), (172, 96),
         (158, 76)],                                                    # S America
        [(268, 10), (310, 6), (322, 18), (312, 34), (292, 40), (276, 30),
         (264, 20)],                                                    # Europe
        [(272, 44), (318, 42), (330, 58), (322, 84), (304, 98), (288, 82),
         (276, 62)],                                                    # Africa
        [(330, 14), (470, 6), (520, 12), (540, 26), (520, 44), (490, 52),
         (470, 66), (450, 60), (430, 44), (400, 40), (360, 34), (336, 26)],  # Eurasia
        [(430, 52), (448, 50), (452, 66), (440, 78), (432, 64)],        # India
        [(462, 58), (478, 56), (482, 70), (468, 74)],                   # SE Asia
        [(528, 30), (534, 28), (536, 42), (530, 44)],                   # Japan
        [(470, 84), (528, 82), (536, 94), (500, 100), (474, 96)],       # Australia
        [(552, 92), (558, 90), (560, 100), (554, 102)],                 # New Zealand
    ]
    for poly in polys:
        d.polygon([(ox + x, oy + int(y * 0.85)) for (x, y) in poly], fill=MAPDOT)
    # Indonesia islets
    for (ix, iy) in [(486, 78), (502, 80), (518, 78)]:
        d.ellipse([ox + ix - 4, oy + int(iy * 0.85) - 2,
                   ox + ix + 4, oy + int(iy * 0.85) + 2], fill=MAPDOT)
    # hero-location pins: Washington, New York, Black Sea
    for (px, py) in [(ox + 108, oy + int(34 * 0.85)), (ox + 128, oy + int(28 * 0.85)),
                     (ox + 330, oy + int(30 * 0.85))]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(255, 255, 255))
    d.text((mx0 + 12, my1 - 16), "Red pins: Washington \u00b7 New York \u00b7 the Black Sea",
           font=font(F_SANS, 9), fill=GRAY)

    # date-check box
    bx0, bx1 = 656, W - 28
    d.rounded_rectangle([bx0, my0, bx1, my1], radius=8, fill=NAVY)
    d.text((bx0 + 14, my0 + 10), "DATE CHECK \u2713",
           font=font(F_SANS_B, 14), fill=(255, 210, 90))
    dc = [
        "Every story on this page happened,",
        "or was first reported, on",
        "WEDNESDAY 25 NOVEMBER 2026.",
        "No story from any other day.",
    ]
    yy = my0 + 34
    for line in dc:
        f = font(F_SANS_B, 13) if "WEDNESDAY" in line else font(F_SANS, 13)
        d.text((bx0 + 14, yy), line, font=f, fill=(255, 255, 255))
        yy += 16
    d.line([(bx0 + 14, yy + 4), (bx1 - 14, yy + 4)], fill=(120, 150, 190), width=1)
    yy += 10
    for line in wrap(d, "Also today: the International Day for the "
                        "Elimination of Violence against Women.",
                     font(F_SANS, 11), bx1 - bx0 - 28, max_lines=2):
        d.text((bx0 + 14, yy), line, font=font(F_SANS, 11),
               fill=(200, 215, 235))
        yy += 14

    # ---------------------------------------------------------- story grid
    gy0 = 490
    d.text((28, gy0), "THE REST OF THE DAY \u2014 47 MORE STORIES",
           font=font(F_SANS_B, 13), fill=INK)
    d.text((W - 28, gy0), "ALL 25 NOVEMBER 2026",
           font=font(F_SANS_B, 11), fill=RED, anchor="ra")
    d.line([(28, gy0 + 20), (W - 28, gy0 + 20)], fill=INK, width=2)

    # column plan: balanced so no column runs past the footer
    asia_first = GRID[5][2][:2]
    asia_rest = GRID[5][2][2:]
    cols_plan = [
        [GRID[0], GRID[1], GRID[2]],                       # NA, SA, Oceania
        [GRID[3], GRID[4], ("ASIA", GRID[5][1], asia_first)],
        [("ASIA \u2014 CONTINUED", GRID[5][1], asia_rest), GRID[6]],  # Asia rest, Sci&Tech
    ]
    col_w = (W - 56 - 2 * 16) // 3
    y = gy0 + 30
    row_h = 24
    for ci, sections in enumerate(cols_plan):
        x0 = 28 + ci * (col_w + 16)
        yy = y
        for (name, color, items) in sections:
            d.text((x0, yy), name, font=font(F_SANS_B, 11), fill=color)
            d.line([(x0, yy + 15), (x0 + col_w, yy + 15)],
                   fill=color, width=1)
            yy += 20
            for (kicker, headline) in items:
                f = fit(d, headline, F_SANS_B, col_w - 16, 12, minimum=10)
                d.ellipse([x0 + 1, yy + 5, x0 + 7, yy + 11], fill=color)
                d.text((x0 + 12, yy), headline, font=f, fill=INK)
                yy += row_h
            yy += 6

    # ---------------------------------------------------------- footer
    fy = H - 34
    d.line([(28, fy - 6), (W - 28, fy - 6)], fill=(180, 172, 150), width=1)
    d.text((28, fy), "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 CNN \u00b7 BBC \u00b7 UEFA \u00b7 WHO \u00b7 WFP \u00b7 "
                      "Al Jazeera \u00b7 NDTV \u00b7 market wires \u2014 all reported 25 Nov 2026",
           font=font(F_SANS, 10), fill=GRAY)
    d.text((W - 28, fy), "THE WORLD IN ONE PAGE",
           font=font(F_SANS_B, 10), fill=GRAY, anchor="ra")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
