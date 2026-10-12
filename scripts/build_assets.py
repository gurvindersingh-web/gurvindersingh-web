#!/usr/bin/env python3
"""
Builds the hand-made SVGs for the profile README: hero, stack, footer.
Standard library only. Run from the repo root:  python scripts/build_assets.py

Rules baked in:
  * The base style of every element is its FINAL state. Animations only describe the way in,
    so prefers-reduced-motion (and any viewer that does not animate) sees the finished picture.
  * Anything that has to line up sits on a fixed grid (text-anchor=middle) or has textLength set,
    so the layout survives whatever fonts the viewer has installed.
  * No external fonts, images or scripts: GitHub's image proxy would block them.
"""
import html
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ── tokens ──────────────────────────────────────────────────────────────
GROUND = "#121212"   # hero / strip background
INK    = "#d4cebd"   # primary khaki
DIM    = "#8f8a7a"   # secondary text (5.4:1 on GROUND)
MID    = "#6b675b"   # structural labels (hexdump offsets)
FAINT  = "#3a3832"   # ambient texture only, never carries information
LINE   = "#2c2b27"   # 1px frame

MONO  = "'JetBrains Mono',ui-monospace,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SERIF = "'Playfair Display',Georgia,'Iowan Old Style','Times New Roman',serif"

CW, FS = 7.8, 13          # mono cell width / font size (advance = 0.6em)
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def esc(s):
    return html.escape(s, quote=False)


def write(name, svg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{name:12} {len(svg):>7,} bytes")


def shift_x(markup, dx):
    """Offset every x="…" in a markup string (used to lay out looping marquee copies)."""
    return re.sub(r'\bx="(-?[\d.]+)"', lambda m: f'x="{float(m.group(1)) + dx:.1f}"', markup)


# ── hero ────────────────────────────────────────────────────────────────
def hero():
    W, H = 880, 364
    X0 = 48
    PAYLOAD = b"Gurvinder Singh\nfull-stack developer\nautomation engineer\nArch + Hyprland\n"
    rows = [PAYLOAD[i:i + 16] for i in range(0, len(PAYLOAD), 16)]
    y0, pitch = 238, 20

    T0, STEP1, STEP2 = 0.55, 0.10, 0.03      # sweep start, per-byte delay (row 1), per-byte delay (rows 2+)
    sweep = 16 * STEP1                        # 1.6s: name wipe and row-1 decode run together
    NAME_X, NAME_W = 48, 640

    # ambient stream on the right edge: real bytes of the stack names, scrolling up
    stream_src = ("react19 spring-boot python scapy linux hyprland arch docker fastapi vite "
                  "gsap rust ebpf kubernetes tailwind nginx mysql java typescript ").encode()
    per, SP, sx = 5, 22, 742
    srows = [stream_src[i:i + per] for i in range(0, len(stream_src) - per + 1, per)]
    stream = []
    for rep in range(2):
        for i, r in enumerate(srows):
            y = 40 + (rep * len(srows) + i) * SP
            stream.append(f'<text x="{sx}" y="{y}" textLength="{per * 3 * CW - CW:.1f}">'
                          f'{" ".join(f"{b:02x}" for b in r)}</text>')
    loop_h = len(srows) * SP

    el = []
    banner = "tcpdump: listening on wlan0mon, link-type IEEE802_11_RADIO (802.11 plus radiotap header)"
    el.append(f'<text class="ban" x="{X0}" y="40" font-size="11" fill="{DIM}" '
              f'textLength="{len(banner) * 6.6:.1f}" lengthAdjust="spacing">{esc(banner)}</text>')

    # selected-row band, like Wireshark's highlighted bytes
    bw = 78 * CW + 16
    el.append(f'<g class="band"><rect x="{X0 - 8}" y="{y0 - 14}" width="{bw:.1f}" height="20" fill="{INK}" fill-opacity=".07"/>'
              f'<rect x="{X0 - 8}" y="{y0 - 14}" width="2" height="20" fill="{INK}"/></g>')

    # hexdump -C rows (hex is real: it is the payload above)
    k = 0
    for r, chunk in enumerate(rows):
        y = y0 + r * pitch
        cls = "hs" if r == 0 else "hx"
        rd = T0 if r == 0 else T0 + sweep + 0.05 + k * STEP2
        el.append(f'<text class="of d" x="{X0}" y="{y}" textLength="{8 * CW:.1f}" style="animation-delay:{rd:.2f}s">{r * 16:08x}</text>')
        for i, b in enumerate(chunk):
            d = T0 + i * STEP1 if r == 0 else T0 + sweep + 0.05 + k * STEP2
            if r != 0:
                k += 1
            col = 10 + 3 * i + (1 if i >= 8 else 0)
            cx = X0 + (col + 1) * CW
            el.append(f'<text class="{cls} d" x="{cx:.1f}" y="{y}" text-anchor="middle" style="animation-delay:{d:.2f}s">{b:02x}</text>')
            ch = chr(b) if 32 <= b < 127 else "."
            if ch != " ":
                gx = X0 + (61 + i + 0.5) * CW
                el.append(f'<text class="{cls} d" x="{gx:.1f}" y="{y}" text-anchor="middle" style="animation-delay:{d:.2f}s">{esc(ch)}</text>')
        el.append(f'<text class="o" x="{X0 + 60.5 * CW:.1f}" y="{y}" text-anchor="middle">|</text>')
        el.append(f'<text class="o" x="{X0 + (61 + len(chunk) + 0.5) * CW:.1f}" y="{y}" text-anchor="middle">|</text>')

    # closing offset line (total length) with a caret that waits for more input
    yf = y0 + len(rows) * pitch
    el.append(f'<text class="of" x="{X0}" y="{yf}" textLength="{8 * CW:.1f}">{len(PAYLOAD):08x}</text>')
    el.append(f'<rect class="caret" x="{X0 + 10 * CW:.1f}" y="{yf - 10}" width="{CW:.1f}" height="13" fill="{INK}"/>')

    # name, the wipe that uncovers it, and the sweep edge
    el.append(f'<text class="name" x="{NAME_X}" y="148" font-size="88" textLength="{NAME_W}" '
              f'lengthAdjust="spacingAndGlyphs">Gurvinder Singh</text>')
    cover_x, cover_w = NAME_X - 8, NAME_W + 20
    el.append(f'<rect class="cover" x="{cover_x}" y="70" width="{cover_w}" height="106" fill="{GROUND}"/>')
    el.append(f'<rect class="edge" x="{cover_x}" y="78" width="2" height="92" fill="{INK}"/>')
    sub = "Breaking things. Fixing things. Shipping things."
    el.append(f'<text class="sub" x="{NAME_X + 2}" y="194" font-size="22" font-style="italic" fill="{INK}" '
              f'textLength="{len(sub) * 9.6:.1f}" lengthAdjust="spacingAndGlyphs">{sub}</text>')

    css = f"""
text{{font-family:{MONO};font-size:{FS}px}}
.hs{{fill:{INK}}} .hx{{fill:{DIM}}} .of{{fill:{MID}}} .o{{fill:{FAINT}}}
.name{{font-family:{SERIF};font-size:88px;fill:{INK}}}
.sub{{font-family:{SERIF};font-size:22px;opacity:.85;animation:fade .8s ease-out {T0 + sweep + 0.2:.2f}s backwards}}
.strm text{{fill:{FAINT}}}
.d{{animation:dec .2s ease-out backwards}}
.ban{{font-size:11px;fill:{DIM};animation:fade .6s ease-out .1s backwards}}
.band{{animation:fade .4s ease-out .35s backwards}}
.cover{{transform-box:fill-box;transform-origin:right center;transform:scaleX(0);animation:cover {sweep}s linear {T0}s backwards}}
.edge{{opacity:0;animation:mv {sweep}s linear {T0}s backwards,vis {sweep}s linear {T0}s backwards}}
.caret{{animation:blink 1.1s steps(1) infinite}}
.strm{{animation:up {loop_h / 9:.0f}s linear infinite}}
@keyframes dec{{from{{opacity:.08}}}}
@keyframes fade{{from{{opacity:0}}}}
@keyframes cover{{from{{transform:scaleX(1)}}}}
@keyframes mv{{from{{transform:translateX(0)}}to{{transform:translateX({cover_w}px)}}}}
@keyframes vis{{0%{{opacity:0}}6%{{opacity:1}}94%{{opacity:1}}100%{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes up{{to{{transform:translateY(-{loop_h}px)}}}}
{REDUCED}"""

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Gurvinder Singh, full-stack developer and automation engineer</title>
<desc id="d">A packet capture decodes a hex payload into the name Gurvinder Singh, then the roles full-stack developer and automation engineer, and the setup Arch with Hyprland.</desc>
<style>{css}</style>
<defs>
<linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="#fff"/><stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="sm" maskUnits="userSpaceOnUse" x="730" y="16" width="140" height="330"><rect x="730" y="16" width="140" height="330" fill="url(#sg)"/></mask>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="6" fill="{GROUND}" stroke="{LINE}"/>
<g mask="url(#sm)"><g class="strm">{"".join(stream)}</g></g>
{"".join(el)}
</svg>
'''
    write("hero.svg", svg)


# ── stack ───────────────────────────────────────────────────────────────
def serif_w(s, size):
    """Rough Georgia-like advance width. textLength pins the real width; this only picks it."""
    narrow, wide = set("iljtfr.,: "), set("mwMW")
    tot = 0.0
    for c in s:
        if c in narrow:
            tot += 0.30
        elif c in wide:
            tot += 0.82
        elif c.isupper():
            tot += 0.68
        elif c.isdigit():
            tot += 0.62
        else:
            tot += 0.52
    return tot * size


def stack():
    W, H = 880, 140
    SIZE, GAP, PAD = 38, 56, 24
    use = ["React 19", "Spring Boot", "Python", "Scapy", "Linux", "Java", "TypeScript", "JavaScript",
           "C++", "FastAPI", "Node", "Vite", "GSAP", "Tailwind", "Docker", "Nginx", "MySQL",
           "Raspberry Pi", "Git", "Arch", "Hyprland"]
    learn = ["Rust", "Kubernetes", "eBPF", "LLM fine-tuning"]

    def cycle(items, cls, y):
        x, out = float(PAD), []
        for it in items:
            w = serif_w(it, SIZE)
            out.append(f'<text class="{cls}" x="{x:.1f}" y="{y}" font-size="{SIZE}" textLength="{w:.1f}" '
                       f'lengthAdjust="spacingAndGlyphs">{esc(it)}</text>')
            x += w + GAP
            out.append(f'<rect x="{x - GAP / 2 - 1:.1f}" y="{y - 26}" width="2" height="26" fill="{FAINT}"/>')
        return "".join(out), x - PAD          # markup, width of one cycle

    m1, w1 = cycle(use, "s", 52)
    m2, w2 = cycle(learn, "o", 112)
    row1 = m1 + shift_x(m1, w1)                          # slides left by one cycle
    row2 = "".join(shift_x(m2, i * w2) for i in range(3))  # slides right by one cycle

    css = f"""
text{{font-family:{SERIF}}}
.s{{fill:{INK}}}
.o{{fill:none;stroke:{INK};stroke-width:1;stroke-linejoin:round}}
.r1{{animation:l {w1 / 70:.0f}s linear infinite}}
.r2{{animation:r {w2 / 38:.0f}s linear infinite}}
@keyframes l{{to{{transform:translateX(-{w1:.1f}px)}}}}
@keyframes r{{from{{transform:translateX(-{w2:.1f}px)}}to{{transform:translateX(0)}}}}
{REDUCED}"""

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
<title id="t">Stack. Solid type, in daily use: {esc(", ".join(use))}. Outlined type, learning: {esc(", ".join(learn))}.</title>
<style>{css}</style>
<defs>
<linearGradient id="fx" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m"><rect x="0" y="0" width="{W}" height="{H}" fill="url(#fx)"/></mask>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="6" fill="{GROUND}" stroke="{LINE}"/>
<g mask="url(#m)">
<g class="r1">{row1}</g>
<g class="r2">{row2}</g>
</g>
</svg>
'''
    write("stack.svg", svg)


# ── footer ──────────────────────────────────────────────────────────────
def footer():
    W, H = 880, 150
    lines = [("^C", DIM), ("1 packet captured", INK), ("1 packet received by filter", DIM),
             ("0 packets dropped by kernel", DIM)]
    el = [f'<text x="48" y="{40 + i * 22}" fill="{c}">{esc(t)}</text>' for i, (t, c) in enumerate(lines)]
    py = 40 + len(lines) * 22 + 10
    prompt = "apkx@arch ~ $"
    el.append(f'<text x="48" y="{py}" fill="{DIM}">{prompt}</text>')
    el.append(f'<rect class="caret" x="{48 + (len(prompt) + 1) * CW:.1f}" y="{py - 10}" width="{CW:.1f}" height="13" fill="{INK}"/>')
    css = f"""
text{{font-family:{MONO};font-size:{FS}px}}
.caret{{animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
{REDUCED}"""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="End of capture: 1 packet captured, 0 packets dropped by kernel.">
<style>{css}</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="6" fill="{GROUND}" stroke="{LINE}"/>
{"".join(el)}
</svg>
'''
    write("footer.svg", svg)


if __name__ == "__main__":
    hero()
    stack()
    footer()
