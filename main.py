#!/usr/bin/env python3
"""THE DAILY SIGNAL - Friday, 27 November 2026.

Draws a one-page newspaper that sums up the day's world news in a
single 1024x1024 PNG and writes it to /output/entry.png.

Every story on the page is real news, reported by Reuters, BBC News,
AP and CNN on 26 November 2026 (27 November in eastern time zones)
and collected in the project's lab notes before the build.

The drawing is fully deterministic: fixed layout, fixed text, no
randomness, no timestamps, no network. Two runs write identical
bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- setup

W, H = 1024, 1024
MARGIN = 36
RIGHT = W - MARGIN

PAPER = (246, 241, 231)
INK = (26, 26, 26)
MUTED = (92, 101, 112)
NAVY = (15, 35, 64)
NAVY_SOFT = (32, 52, 79)
RED = (179, 32, 44)
GOLD = (227, 185, 62)
WHITE = (255, 255, 255)
CARD_BG = (255, 255, 255)
CARD_LINE = (216, 210, 196)
PANEL_BG = (237, 241, 244)
WATER = (188, 211, 220)
LAND = (228, 214, 176)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_OBLIQUE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"


def font(path, size):
    """Load a TrueType font, falling back to Pillow's default."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real glyph metrics. Deterministic."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, line_height):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_height
    return y


# ---------------------------------------------------------------- content

DATE_LINE = "FRIDAY, 27 NOVEMBER 2026"
TAG_LINE = "WORLD EDITION  -  ALL THE DAY'S NEWS IN ONE IMAGE"

HERO_KICKER = "TOP STORY  -  KUWAIT / MIDDLE EAST"
HERO_HEADLINE = (
    "Two Italians Killed in Kuwait Drone Strike; "
    "Iran Denies Involvement"
)
HERO_SUMMARY = (
    "Technicians for Rheinmetall Italia died at an air-defence "
    "surveillance station hit by drones on Thursday. Italy and "
    "Kuwait blamed Iran; Tehran denied any role and offered a "
    "joint investigation."
)
HERO_BYLINE = "KUWAIT CITY / ROME - reporting by Reuters, BBC News and CNN"

CARDS = [
    {
        "label": "UKRAINE  -  BLACK SEA",
        "color": (32, 90, 138),
        "title": "Russia Hits Two Grain Ships Near Odesa",
        "body": (
            "Two foreign cargo ships carrying more than 100,000 "
            "tonnes of grain were attacked overnight near the "
            "Black Sea port, Ukraine's prime minister said."
        ),
    },
    {
        "label": "EGYPT  -  CAIRO",
        "color": (168, 91, 18),
        "title": "Cairo Fuel Tanker Fire Kills 31",
        "body": (
            "A fuel tanker overturned in rush hour on the Ring "
            "Road in Giza, burning 27 vehicles. A speeding driver "
            "who clipped it has been arrested."
        ),
    },
    {
        "label": "INDONESIA  -  WEST JAVA",
        "color": (30, 122, 76),
        "title": "Bogor Mine Flood: 13 Dead, 13 Missing",
        "body": (
            "Torrential rain flooded an illegal gold mine 100 "
            "metres deep in West Java. Rescuers found 13 bodies "
            "and searched for 13 more miners."
        ),
    },
    {
        "label": "HEALTH  -  AFRICA",
        "color": (14, 124, 134),
        "title": "$40 HIV Prevention Jab Reaches Africa",
        "body": (
            "The first generic lenacapavir shipment reached "
            "Zambia, with Uganda next. Two injections a year, "
            "nearly 100% effective, at $40 a year."
        ),
    },
]

TICKER = (
    "US tariffs proposed on 14 partners: China 20%, EU 15%  \u2022  "
    "Guinea-Bissau vote delayed to 2028  \u2022  "
    "Serbia presidential vote Dec 27  \u2022  "
    "Macy's 100th parade moved to Saturday  \u2022  "
    "Bank of Korea rate up to 3.25%  \u2022  "
    "Bangkok refinery blast injures 9"
)

FOOTER_LEFT = "Sources: Reuters \u2022 BBC News \u2022 AP \u2022 CNN \u2022 Global Fund"
FOOTER_RIGHT = "Drawn in code - Python + Pillow \u2022 No photos"


# ---------------------------------------------------------------- drawing

def draw_masthead(draw):
    draw.rectangle([0, 0, W, 126], fill=NAVY)
    draw.rectangle([0, 126, W, 132], fill=RED)
    title_font = font(SERIF_BOLD, 49)
    draw.text((W // 2, 13), "THE DAILY SIGNAL", font=title_font,
              fill=WHITE, anchor="ma")
    date_font = font(SANS_BOLD, 15)
    draw.text((W // 2, 76), DATE_LINE, font=date_font,
              fill=GOLD, anchor="ma")
    tag_font = font(SANS, 12)
    draw.text((W // 2, 100), TAG_LINE, font=tag_font,
              fill=(201, 212, 226), anchor="ma")


def draw_hero_panel(draw):
    """Right-hand panel: schematic Gulf map plus the key numbers."""
    x0, y0, x1, y1 = 652, 148, RIGHT, 500
    draw.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=NAVY_SOFT,
                   width=2)
    draw.rectangle([x0, y0, x1, y0 + 30], fill=NAVY)
    draw.text((x0 + 14, y0 + 8), "THE GULF - AT A GLANCE",
              font=font(SANS_BOLD, 13), fill=WHITE)

    # Schematic map (positions approximate, not to scale).
    mx0, my0, mx1, my1 = x0 + 12, y0 + 42, x1 - 12, y0 + 170
    draw.rectangle([mx0, my0, mx1, my1], fill=WATER)
    # Arabian landmass, lower left.
    draw.polygon(
        [(mx0, my0 + 62), (mx0 + 58, my0 + 44), (mx0 + 118, my0 + 50),
         (mx0 + 168, my0 + 74), (mx0 + 188, my1), (mx0, my1)],
        fill=LAND,
    )
    # Iranian landmass, upper right.
    draw.polygon(
        [(mx0 + 168, my0), (mx1, my0), (mx1, my0 + 58),
         (mx0 + 232, my0 + 52), (mx0 + 196, my0 + 30)],
        fill=LAND,
    )
    draw.text((mx0 + 16, my1 - 24), "SAUDI ARABIA",
              font=font(SANS_BOLD, 10), fill=(110, 96, 58))
    draw.text((mx1 - 52, my0 + 8), "IRAN",
              font=font(SANS_BOLD, 10), fill=(110, 96, 58))
    draw.text((mx0 + 128, my0 + 82), "Persian Gulf",
              font=font(SANS_OBLIQUE, 11), fill=(52, 92, 110))
    # Kuwait, at the head of the Gulf.
    kx, ky = mx0 + 172, my0 + 60
    draw.ellipse([kx - 8, ky - 8, kx + 8, ky + 8], fill=RED,
                 outline=WHITE, width=2)
    draw.text((kx - 64, ky - 24), "KUWAIT",
              font=font(SANS_BOLD, 12), fill=RED)
    draw.text((x0 + 14, my1 + 6),
              "Schematic map - positions approximate, not to scale.",
              font=font(SANS, 10), fill=MUTED)

    # Key numbers.
    stats = [
        ("2", "Italian technicians killed at the station"),
        ("4", "people wounded in the first reports"),
        ("1", "air-defence surveillance station struck"),
    ]
    sy = y0 + 206
    num_font = font(SERIF_BOLD, 28)
    lab_font = font(SANS, 13)
    for i, (num, label) in enumerate(stats):
        if i:
            draw.line([x0 + 14, sy - 6, x1 - 14, sy - 6],
                      fill=CARD_LINE, width=1)
        draw.text((x0 + 16, sy), num, font=num_font, fill=NAVY)
        lines = wrap(draw, label, lab_font, 218)
        draw_lines(draw, x0 + 72, sy + 1, lines, lab_font, INK, 16)
        sy += 44


def draw_hero(draw):
    draw.text((MARGIN, 148), HERO_KICKER, font=font(SANS_BOLD, 16),
              fill=RED)
    head_font = font(SERIF_BOLD, 42)
    lines = wrap(draw, HERO_HEADLINE, head_font, 592)
    y = draw_lines(draw, MARGIN, 174, lines, head_font, INK, 52)
    body_font = font(SANS, 18)
    lines = wrap(draw, HERO_SUMMARY, body_font, 592)
    y = draw_lines(draw, MARGIN, y + 14, lines, body_font, INK, 27)
    draw.text((MARGIN, y + 12), HERO_BYLINE, font=font(SANS, 12),
              fill=MUTED)
    draw_hero_panel(draw)
    draw.line([MARGIN, 518, RIGHT, 518], fill=NAVY, width=2)


def draw_card(draw, x, y, w, h, card):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG,
                   outline=CARD_LINE, width=1)
    draw.rectangle([x, y, x + w, y + 5], fill=card["color"])
    draw.text((x + 16, y + 15), card["label"],
              font=font(SANS_BOLD, 12), fill=card["color"])
    title_font = font(SERIF_BOLD, 22)
    lines = wrap(draw, card["title"], title_font, w - 32)
    ty = draw_lines(draw, x + 16, y + 36, lines[:2], title_font, INK, 27)
    body_font = font(SANS, 15)
    lines = wrap(draw, card["body"], body_font, w - 32)
    draw_lines(draw, x + 16, ty + 8, lines[:3],
               body_font, (52, 58, 66), 20)


def draw_cards(draw):
    cw, ch, gap = 470, 166, 12
    positions = [
        (MARGIN, 532),
        (MARGIN + cw + gap, 532),
        (MARGIN, 532 + ch + gap),
        (MARGIN + cw + gap, 532 + ch + gap),
    ]
    for (x, y), card in zip(positions, CARDS):
        draw_card(draw, x, y, cw, ch, card)


def draw_ticker(draw):
    y0, y1 = 890, 962
    draw.rounded_rectangle([MARGIN, y0, RIGHT, y1], radius=8, fill=NAVY)
    draw.text((MARGIN + 16, y0 + 8), "LATEST",
              font=font(SANS_BOLD, 12), fill=GOLD)
    tick_font = font(SANS_BOLD, 13)
    lines = wrap(draw, TICKER, tick_font, RIGHT - MARGIN - 32)
    draw_lines(draw, MARGIN + 16, y0 + 28, lines[:2], tick_font,
               WHITE, 20)


def draw_footer(draw):
    foot_font = font(SANS, 12)
    draw.text((MARGIN, 978), FOOTER_LEFT, font=foot_font, fill=MUTED)
    draw.text((RIGHT, 978), FOOTER_RIGHT, font=foot_font, fill=MUTED,
              anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero(draw)
    draw_cards(draw)
    draw_ticker(draw)
    draw_footer(draw)
    out_dir = os.environ.get("ENTRY_OUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
