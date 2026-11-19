#!/usr/bin/env python3
"""
Builds the Omarchy plugin contribution cards for the profile README.

Produces two assets (2x, dark theme):
  assets/omarchy-plugins-row.png    three connected cards for wide screens
  assets/omarchy-plugins-stack.png  vertically connected cards for narrow screens

Run from the repo root:
    python scripts/build_plugin_cards.py

Requires Pillow (with Raqm for the Gurmukhi sample).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ── palette (matches the README blue theme) ─────────────────────────────
BG_TOP, BG_BOT = "#0b1424", "#0f1b30"
CARD_BG = "#0b1220"
BORDER = "#243550"
GRID = "#16243a"
INK = "#f8fafc"
DIM = "#8aa0bd"
FAINT = "#5b7291"
ACCENT = "#60a5fa"
ACCENT2 = "#3b82f6"
AMBER = "#fbbf24"
SLATE = "#94a3b8"

# ── geometry (2x) ───────────────────────────────────────────────────────
CARD_W, CARD_H = 496, 392
ART_H = 286
GAP_X, GAP_Y = 24, 80
CONNECTOR_H = 148
RAIL_Y = 48

FONT_DIR = "/usr/share/fonts"


def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)


SG_BOLD = "OTF/SpaceGrotesk-Bold.otf"
SG_SEMI = "OTF/SpaceGrotesk-SemiBold.otf"
SG_REG = "OTF/SpaceGrotesk-Regular.otf"
MONO = "TTF/JetBrainsMonoNerdFont-Regular.ttf"
MONO_BOLD = "TTF/JetBrainsMonoNerdFont-Bold.ttf"
GURMUKHI = "noto/NotoSansGurmukhiUI-Bold.ttf"


def vgrad(w, h, top, bottom):
    im = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(im)
    t = tuple(int(top[i : i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(bottom[i : i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        k = y / max(h - 1, 1)
        d.line(
            [(0, y), (w, y)],
            fill=tuple(round(t[i] + (b[i] - t[i]) * k) for i in range(3)),
        )
    return im


def grid(im, step=28, color=GRID):
    d = ImageDraw.Draw(im)
    w, h = im.size
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=color, width=1)
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=color, width=1)


def dot_grid(im, step=22, color=GRID, r=1):
    d = ImageDraw.Draw(im)
    w, h = im.size
    for y in range(10, h, step):
        for x in range(10, w, step):
            d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def glow(im, box, color, blur):
    rgb = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=rgb + (90,))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    im.alpha_composite(layer)


def art_base():
    art = vgrad(CARD_W, ART_H, BG_TOP, BG_BOT).convert("RGBA")
    return art


def art_header(art, plugin_id, version="v1.0.0"):
    d = ImageDraw.Draw(art)
    d.text((24, 20), plugin_id, font=font(MONO, 15), fill=FAINT, anchor="lt")
    d.text((CARD_W - 24, 20), version, font=font(MONO, 13), fill="#3f5573", anchor="rt")


# ── card art: System Stats ──────────────────────────────────────────────
def art_system_stats():
    art = art_base()
    grid(art, 28)
    art_header(art, "gurvindersingh-web.system-stats")

    d = ImageDraw.Draw(art)
    pills = [
        ("CPU", "44%", ACCENT),
        ("MEM", "22%", ACCENT2),
        ("DISK", "19m", "#38bdf8"),
        ("TEMP", "59\u00b0", "#a5b4fc"),
    ]
    pw, ph, gap = 108, 62, 8
    x0 = (CARD_W - (len(pills) * pw + (len(pills) - 1) * gap)) // 2
    y0 = 92
    for i, (label, value, tint) in enumerate(pills):
        x = x0 + i * (pw + gap)
        d.rounded_rectangle(
            [x, y0, x + pw, y0 + ph], radius=14, fill="#15243c", outline="#27405f", width=2
        )
        d.ellipse([x + 12, y0 + 12, x + 18, y0 + 18], fill=tint)
        d.text((x + 26, y0 + 10), label, font=font(MONO, 13), fill="#7f9cc0", anchor="lt")
        d.text((x + 12, y0 + 28), value, font=font(MONO_BOLD, 25), fill=INK, anchor="lt")

    # cpu history sparkline with a soft area fill
    sx0, sx1 = 28, CARD_W - 28
    d.line([(sx0, 250), (sx1, 250)], fill="#22334d", width=2)
    for gy in (206, 228):
        d.line([(sx0, gy), (sx1, gy)], fill="#182741", width=1)
    pts = [
        (0.00, 0.55), (0.10, 0.48), (0.20, 0.66), (0.30, 0.58), (0.40, 0.76),
        (0.50, 0.52), (0.60, 0.62), (0.70, 0.44), (0.80, 0.57), (0.90, 0.40),
        (1.00, 0.50),
    ]
    line_pts = [(sx0 + (sx1 - sx0) * px, 250 - 48 * py) for px, py in pts]
    area = Image.new("RGBA", art.size, (0, 0, 0, 0))
    ImageDraw.Draw(area).polygon(line_pts + [(sx1, 250), (sx0, 250)], fill=ACCENT + "26")
    art.alpha_composite(area)
    d.line(line_pts, fill=ACCENT, width=4, joint="curve")
    d.text((sx0, 210), "cpu load", font=font(MONO, 12), fill="#55708f", anchor="lt")
    d.text((sx1, 210), "60s", font=font(MONO, 12), fill="#55708f", anchor="rt")
    return art


# ── card art: Zoom Lens ─────────────────────────────────────────────────
def art_zoom_lens():
    art = art_base()
    grid(art, 30)
    art_header(art, "zoom-lens.magnifier")

    d = ImageDraw.Draw(art)
    cx, cy, r = 190, 166, 92
    glow(art, [cx - r - 26, cy - r - 26, cx + r + 26, cy + r + 26], "#1d4ed8", 26)

    # opaque lens content: magnified interface grid and text bars
    inner = Image.new("RGBA", art.size, "#08101e")
    di = ImageDraw.Draw(inner)
    for gx in range(cx - r, cx + r + 1, 48):
        di.line([(gx, cy - r), (gx, cy + r)], fill="#193253", width=3)
    for gy in range(cy - r, cy + r + 1, 48):
        di.line([(cx - r, gy), (cx + r, gy)], fill="#193253", width=3)
    bars = [
        (cx - 62, cy - 54, 104, "#2f5f9e"),
        (cx - 62, cy - 28, 132, "#24476f"),
        (cx - 62, cy - 2, 78, "#2f5f9e"),
        (cx - 62, cy + 24, 116, "#24476f"),
        (cx - 62, cy + 50, 58, "#315b8a"),
    ]
    for x, y, w, col in bars:
        di.rounded_rectangle([x, y, x + w, y + 11], radius=5, fill=col)
    di.rectangle([cx + 58, cy + 24, cx + 62, cy + 36], fill=ACCENT)
    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    art.paste(inner, (0, 0), mask)

    # lens rings
    d.ellipse([cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12], outline="#1e3a5f", width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ACCENT, width=6)
    d.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], outline="#2f5f9e", width=2)
    d.arc([cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18], 200, 320, fill="#dbeafe", width=4)

    # zoom badge
    d.rounded_rectangle(
        [cx - 42, cy + 58, cx + 42, cy + 86], radius=7, fill="#0b1424", outline="#2f5f9e", width=2
    )
    d.text((cx, cy + 72), "1.75\u00d7", font=font(MONO_BOLD, 16), fill="#dbeafe", anchor="mm")

    # crosshair ticks
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        x1, y1 = cx + dx * (r + 20), cy + dy * (r + 20)
        x2, y2 = cx + dx * (r + 38), cy + dy * (r + 38)
        d.line([(x1, y1), (x2, y2)], fill=ACCENT, width=4)

    # keycaps
    ky = 142
    d.rounded_rectangle([338, ky, 420, ky + 40], radius=8, fill="#13223a", outline="#2f4a6d", width=2)
    d.text((379, ky + 20), "SUPER", font=font(MONO, 15), fill="#c9dcf5", anchor="mm")
    d.text((430, ky + 20), "+", font=font(MONO, 18), fill=FAINT, anchor="mm")
    d.rounded_rectangle([442, ky, 478, ky + 40], radius=8, fill="#13223a", outline="#2f4a6d", width=2)
    d.text((460, ky + 20), "Z", font=font(MONO_BOLD, 16), fill=INK, anchor="mm")
    d.text((408, ky + 56), "toggle lens", font=font(MONO, 12), fill=DIM, anchor="mt")
    d.text((408, ky + 78), "esc to close", font=font(MONO, 12), fill="#55708f", anchor="mt")
    return art


# ── card art: Omarchy Translator ────────────────────────────────────────
def art_translator():
    art = art_base()
    dot_grid(art, 22)
    art_header(art, "gurvindersingh-web.omalation")

    cx, cy = CARD_W // 2, 168
    glow(art, [cx - 190, cy - 120, cx + 190, cy + 120], "#1d4ed8", 28)

    d = ImageDraw.Draw(art)
    x0, y0, x1, y1 = 44, 44, CARD_W - 44, ART_H - 26
    d.rounded_rectangle(
        [x0, y0, x1, y1], radius=16, fill="#101d33", outline="#2b4160", width=2
    )
    # header
    d.text(
        (x0 + 20, y0 + 16),
        "TRANSLATE \u2192 PUNJABI",
        font=font(MONO, 15),
        fill=ACCENT,
        anchor="lt",
    )
    d.text(
        (x1 - 20, y0 + 16),
        "EN \u2192 PA",
        font=font(MONO, 13),
        fill="#5b7291",
        anchor="rt",
    )
    d.line([(x0 + 20, y0 + 42), (x1 - 20, y0 + 42)], fill="#22344f", width=2)
    # source
    d.text((x0 + 20, y0 + 54), "hi", font=font(MONO, 24), fill="#94a3b8", anchor="lt")
    d.text(
        (x1 - 20, y0 + 62), "source", font=font(MONO, 11), fill="#445a75", anchor="rt"
    )
    # result
    d.text(
        (x0 + 20, y0 + 94),
        "\u0a38\u0a24 \u0a38\u0a4d\u0a30\u0a40 \u0a05\u0a15\u0a3e\u0a32",
        font=font(GURMUKHI, 46),
        fill=INK,
        anchor="lt",
        language="pa",
    )
    d.line([(x0 + 20, y1 - 46), (x1 - 20, y1 - 46)], fill="#22344f", width=2)
    d.text(
        (x0 + 20, y1 - 34),
        "COPIED TO CLIPBOARD",
        font=font(MONO, 12),
        fill=ACCENT,
        anchor="lt",
    )
    d.text(
        (x1 - 20, y1 - 34), "\u2713", font=font(MONO_BOLD, 16), fill=ACCENT, anchor="rt"
    )
    return art


# ── card shell ──────────────────────────────────────────────────────────
def chip(im, status, color):
    label = status.upper()
    f = font(MONO, 16)
    tw = f.getlength(label)
    w = int(tw + 44)
    x1, y1 = CARD_W - 22, 372
    x0, y0 = x1 - w, y1 - 32
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(
        [x0, y0, x1, y1], radius=8, fill="#050b16", outline="#2b4160", width=2
    )
    d.ellipse([x0 + 14, y0 + 12, x0 + 24, y0 + 22], fill=color)
    d.text((x0 + 32, y0 + 8), label, font=f, fill=color, anchor="lt")
    return w


def card(art, title, subtitle, status, status_color):
    im = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    im.alpha_composite(art, (0, 0))

    # fade art into the footer
    fade = Image.new("RGBA", (CARD_W, 70), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fade)
    for y in range(70):
        fd.line([(0, y), (CARD_W, y)], fill=(11, 18, 32, round(255 * (y / 69))))
    im.alpha_composite(fade, (0, ART_H - 70))

    d = ImageDraw.Draw(im)
    d.rectangle([0, ART_H, CARD_W, CARD_H], fill=CARD_BG)
    d.line([(0, ART_H), (CARD_W, ART_H)], fill=BORDER, width=2)

    d.text((24, 300), title, font=font(SG_SEMI, 38), fill=INK, anchor="lt")
    d.text((24, 348), subtitle, font=font(SG_REG, 19), fill=DIM, anchor="lt")
    chip(im, status, status_color)

    # chamfered frame
    c = 14
    pts = [
        (c, 0),
        (CARD_W, 0),
        (CARD_W, CARD_H - c),
        (CARD_W - c, CARD_H),
        (0, CARD_H),
        (0, c),
        (c, 0),
    ]
    d.line(pts, fill=BORDER, width=2)
    return im


# ── connectors ──────────────────────────────────────────────────────────
def line(d, pts, color="#334155", width=3):
    d.line(pts, fill=color, width=width, joint="curve")


def row_image(cards):
    w = len(cards) * CARD_W + (len(cards) - 1) * GAP_X
    h = CONNECTOR_H + CARD_H
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    centers = [i * (CARD_W + GAP_X) + CARD_W // 2 for i in range(len(cards))]
    line(d, [(centers[0], RAIL_Y), (centers[-1], RAIL_Y)])
    for c in centers:
        line(d, [(c, RAIL_Y), (c, CONNECTOR_H)])
    mid = centers[len(centers) // 2]
    line(d, [(mid, 0), (mid, RAIL_Y)])
    for c in centers:
        line(
            d,
            [(c - 16, CONNECTOR_H - 10), (c + 16, CONNECTOR_H - 10)],
            color=ACCENT,
            width=4,
        )
    line(d, [(mid - 12, 14), (mid + 12, 14)], color=ACCENT, width=4)
    line(
        d, [(centers[0] + 40, RAIL_Y), (centers[0] + 92, RAIL_Y)], color=ACCENT, width=4
    )
    line(
        d,
        [(centers[-1] - 92, RAIL_Y), (centers[-1] - 40, RAIL_Y)],
        color=ACCENT,
        width=4,
    )
    for i, c in enumerate(cards):
        im.alpha_composite(c, (i * (CARD_W + GAP_X), CONNECTOR_H))
    return im


def stack_image(cards):
    h = CONNECTOR_H + len(cards) * CARD_H + (len(cards) - 1) * GAP_Y
    im = Image.new("RGBA", (CARD_W, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    mid = CARD_W // 2
    line(d, [(mid, 0), (mid, CONNECTOR_H)])
    line(d, [(mid - 12, 14), (mid + 12, 14)], color=ACCENT, width=4)
    y = CONNECTOR_H
    for i, c in enumerate(cards):
        if i:
            line(d, [(mid, y - GAP_Y), (mid, y)])
            line(
                d,
                [(mid - 14, y - GAP_Y // 2), (mid + 14, y - GAP_Y // 2)],
                color=ACCENT,
                width=4,
            )
        im.alpha_composite(c, (0, y))
        y += CARD_H + GAP_Y
    return im


def main():
    cards = [
        card(
            art_system_stats(),
            "System Stats",
            "Waybar-style system stats",
            "verified",
            ACCENT,
        ),
        card(
            art_zoom_lens(),
            "Zoom Lens",
            "Desktop magnifier for Hyprland",
            "listed",
            SLATE,
        ),
        card(
            art_translator(),
            "Omarchy Translator",
            "Selection, clipboard or typing",
            "in review",
            AMBER,
        ),
    ]
    os.makedirs(OUT, exist_ok=True)
    for name, im in (
        ("omarchy-plugins-row.png", row_image(cards)),
        ("omarchy-plugins-stack.png", stack_image(cards)),
    ):
        path = os.path.join(OUT, name)
        im.save(path, optimize=True)
        print(f"{name:28} {im.size[0]}x{im.size[1]}  {os.path.getsize(path):,} bytes")


if __name__ == "__main__":
    main()
