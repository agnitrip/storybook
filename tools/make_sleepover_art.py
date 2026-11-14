"""Draws simple placeholder pictures for "The Big Sleepover".

Same idea as make_placeholder_art.py: swap any page for Adhuna's drawing
by changing that page's `image` in stories.js.

Run: python3 tools/make_sleepover_art.py
"""
import os
import random

from make_placeholder_art import FALL_CANOPY, bee, cloud, flower, tree

OUT = os.path.join(os.path.dirname(__file__), "..", "stories", "big-sleepover", "pages")

SKIN = "#E2A97E"
SKIN_EDGE = "#9A6440"
HAIR = "#2B1B12"
MOUTH = "#6B2B2B"
CUSHIONS = ["#FF8A80", "#80CBC4", "#FFD54F", "#B39DDB", "#81D4FA", "#F48FB1", "#AED581"]

SISTERS = {
    "dibhai": dict(s=1.15, pj="#8E6CCF", pants="#6A4FB0", style="long", accent="#FFD54F"),
    "chhuti": dict(s=1.05, pj="#2BB3A3", pants="#1E8C80", style="braid", accent="#FF80AB"),
    "mithi": dict(s=1.0, pj="#F06292", pants="#C2185B", style="pony", accent="#FFEB3B"),
    "bonu": dict(s=0.82, pj="#FFC93C", pants="#E0A800", style="short", accent="#FF5252"),
    "mom": dict(s=1.45, pj="#43A047", pants="#43A047", style="bun", accent="#FFD54F", dress=True),
}

HEAD_Y = -174  # head centre, in a person's own units (feet at 0)


# ---------- people ----------

def hair_back(style, accent):
    """Hair that sits behind the head and body."""
    shape = {
        "long": '<path d="M-40 -8 C-50 30 -48 72 -40 94 Q0 102 40 94 C48 72 50 30 40 -8Z"/>',
        "braid": '<path d="M-40 -8 C-46 20 -42 40 -34 46 L34 46 C42 40 46 20 40 -8Z"/>',
        "pony": '<path d="M-38 -8 C-42 14 -38 30 -30 34 L30 34 C38 30 42 14 38 -8Z"/>'
                '<path d="M22 -38 C64 -44 72 20 52 84 C44 60 42 12 18 -18Z"/>',
        "short": '<path d="M-42 -6 C-46 20 -42 38 -30 40 L30 40 C42 38 46 20 42 -6Z"/>',
        "bun": '<circle cx="0" cy="-44" r="19"/>',
    }[style]
    tie = f'<circle cx="24" cy="-34" r="7" fill="{accent}"/>' if style == "pony" else ""
    return f'<g fill="{HAIR}">{shape}</g>{tie}'


def face(style, mood, accent):
    """Face, fringe, and anything worn in front of the head."""
    if mood == "sleep":
        eyes = ('<path d="M-19 3 q6 6 12 0 M7 3 q6 6 12 0" fill="none" stroke="#3B2314" '
                'stroke-width="3" stroke-linecap="round"/>')
    else:
        eyes = "".join(
            f'<ellipse cx="{x}" cy="2" rx="7" ry="8" fill="#fff"/><circle cx="{x + 1}" cy="3" r="5" fill="#3B2314"/>'
            f'<circle cx="{x + 1}" cy="3" r="2.4" fill="#000"/><circle cx="{x + 3}" cy="0.5" r="1.8" fill="#fff"/>'
            for x in (-13, 13))
    brows = ('<path d="M-20 -11 q7 -4 13 0 M7 -11 q7 -4 13 0" fill="none" stroke="#2B1B12" stroke-width="2.5" stroke-linecap="round"/>'
             if mood not in ("sad", "cry") else
             '<path d="M-20 -9 q7 -5 13 -3 M7 -12 q7 1 13 3" fill="none" stroke="#2B1B12" stroke-width="2.5" stroke-linecap="round"/>')
    line = 'fill="none" stroke="#5A2E22" stroke-width="3" stroke-linecap="round"'
    mouth = {
        "happy": f'<path d="M-8 19 Q0 27 8 19" {line}/>',
        "big": f'<path d="M-10 18 Q0 33 10 18Z" fill="{MOUTH}"/><path d="M-6 26 Q0 30 6 26" fill="#F48FB1"/>',
        "sad": f'<path d="M-8 25 Q0 17 8 25" {line}/>',
        "cry": f'<path d="M-8 25 Q0 17 8 25" {line}/>'
               '<path d="M-16 11 q-4 8 0 11 q4 -3 0 -11Z M16 11 q-4 8 0 11 q4 -3 0 -11Z" fill="#6EC6FF"/>',
        "oh": f'<ellipse cx="0" cy="22" rx="4.5" ry="5.5" fill="{MOUTH}"/>',
        "flat": f'<path d="M-7 22 H7" {line}/>',
        "sleep": f'<path d="M-4 21 Q0 24 4 21" {line}/>',
    }[mood]
    if style == "short":
        fringe = "M-38 2 C-42 -50 42 -50 38 2 C30 -12 14 -15 0 -13 C-14 -15 -30 -12 -38 2Z"
    else:
        fringe = "M-38 0 C-42 -50 42 -50 38 0 C34 -20 18 -28 2 -26 C-10 -16 -26 -12 -38 0Z"
    strands = ('<path d="M-38 -4 C-43 16 -41 34 -36 46 L-29 43 C-33 27 -33 10 -31 -6Z"/>'
               '<path d="M38 -4 C43 16 41 34 36 46 L29 43 C33 27 33 10 31 -6Z"/>') if style != "bun" else ""
    extra = ""
    if style == "long":
        extra = f'<path d="M-37 -14 C-30 -44 30 -44 37 -14" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>'
    elif style == "braid":
        extra = ("".join(f'<ellipse cx="{30 + i * 2}" cy="{50 + i * 15}" rx="9" ry="10" fill="{HAIR}"/>' for i in range(5))
                 + f'<rect x="31" y="118" width="14" height="7" rx="3" fill="{accent}"/>'
                 + f'<path d="M34 125 l-4 12 M38 125 v13 M42 125 l4 12" stroke="{HAIR}" stroke-width="3" stroke-linecap="round"/>')
    elif style == "short":
        extra = f'<rect x="-30" y="-24" width="16" height="6" rx="3" fill="{accent}" transform="rotate(-20 -22 -21)"/>'
    return (
        f'<circle cx="-34" cy="6" r="7" fill="{SKIN}"/><circle cx="34" cy="6" r="7" fill="{SKIN}"/>'
        f'<ellipse rx="34" ry="36" fill="{SKIN}" stroke="#C98A62" stroke-width="2"/>'
        f"{brows}{eyes}"
        '<path d="M-2 11 q2 3 5 0" fill="none" stroke="#B57552" stroke-width="2.5" stroke-linecap="round"/>'
        '<circle cx="-22" cy="14" r="5.5" fill="#F48FB1" opacity=".55"/><circle cx="22" cy="14" r="5.5" fill="#F48FB1" opacity=".55"/>'
        f"{mouth}"
        f'<g fill="{HAIR}"><path d="{fringe}"/>{strands}</g>{extra}'
    )


def head(style, mood, accent="#FFD54F"):
    return hair_back(style, accent) + face(style, mood, accent)


ARM_ENDS = {  # (end x, end y, control x factor, control y) for the right arm; left mirrors
    "down": (38, -64, 1.6, -95),
    "up": (50, -192, 2.2, -150),
    "hold": (12, -84, 2.0, -92),
    "hips": (30, -70, 2.6, -100),
}


def arm(side, pose, color):
    ex, ey, cf, cy = ARM_ENDS[pose]
    sx = 24 * side
    return (f'<path d="M{sx} -120 Q{sx * cf} {cy} {ex * side} {ey}" fill="none" stroke="{color}" '
            f'stroke-width="12" stroke-linecap="round"/><circle cx="{ex * side}" cy="{ey}" r="7" fill="{SKIN}"/>')


def person(who, x, y, arms="down", mood="happy", right_arm=None):
    p = SISTERS[who]
    s = p["s"]
    if p.get("dress"):
        lower = (f'<path d="M-30 -100 L-46 -6 L46 -6 L30 -100Z" fill="{p["pj"]}"/>'
                 '<ellipse cx="-14" cy="-2" rx="12" ry="6" fill="#5D4037"/><ellipse cx="14" cy="-2" rx="12" ry="6" fill="#5D4037"/>')
    else:
        lower = (f'<rect x="-17" y="-62" width="13" height="60" rx="5" fill="{p["pants"]}"/>'
                 f'<rect x="4" y="-62" width="13" height="60" rx="5" fill="{p["pants"]}"/>'
                 '<ellipse cx="-12" cy="-2" rx="11" ry="6" fill="#fff" stroke="#ccc" stroke-width="2"/>'
                 '<ellipse cx="12" cy="-2" rx="11" ry="6" fill="#fff" stroke="#ccc" stroke-width="2"/>')
    body = (f'<path d="M-24 -128 Q0 -136 24 -128 Q34 -124 32 -110 L32 -56 L-32 -56 L-32 -110 Q-34 -124 -24 -128Z" fill="{p["pj"]}"/>'
            f'<path d="M-10 -130 Q0 -122 10 -130" fill="none" stroke="#ffffff88" stroke-width="3"/>'
            '<g fill="#fff" opacity=".35"><circle cx="-12" cy="-104" r="4"/><circle cx="10" cy="-90" r="4"/>'
            '<circle cx="-6" cy="-72" r="4"/><circle cx="16" cy="-116" r="3"/></g>')
    neck = f'<rect x="-8" y="-150" width="16" height="26" rx="6" fill="{SKIN}"/>'
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<g transform="translate(0 {HEAD_Y})">{hair_back(p["style"], p["accent"])}</g>'
        f'{lower}{neck}{body}'
        f'{arm(-1, arms, p["pj"])}{arm(1, right_arm or arms, p["pj"])}'
        f'<g transform="translate(0 {HEAD_Y})">{face(p["style"], mood, p["accent"])}</g></g>'
    )


def hand_y(who, y):
    return y - 84 * SISTERS[who]["s"]


def top_of_head(who, y):
    return y - 220 * SISTERS[who]["s"]


def sleeping_head(who, x, y):
    p = SISTERS[who]
    return f'<g transform="translate({x} {y}) scale(0.85)">{head(p["style"], "sleep", p["accent"])}</g>'


# ---------- things ----------

def cushion(x, y, w, h, color, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot})">'
            f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="{h / 2.4}" fill="{color}" stroke="#00000022" stroke-width="3"/>'
            f'<path d="M{-w / 2 + 10} 0 H{w / 2 - 10}" stroke="#ffffff66" stroke-width="3" stroke-dasharray="6 8"/>'
            f'<circle r="4" fill="#00000033"/></g>')


def cushion_pile(rng, cx, base, width, rows):
    out = ""
    for r in range(rows):
        n = max(1, int(width / 90) - r)
        span = (n - 1) * 80
        for i in range(n):
            out += cushion(cx - span / 2 + i * 80 + rng.randint(-8, 8), base - 18 - r * 34,
                           96, 40, rng.choice(CUSHIONS), rng.randint(-12, 12))
    return out


def cushion_stack(rng, x, base, count, w=110):
    return "".join(cushion(x + rng.randint(-6, 6), base - 14 - i * 26, w, 30, rng.choice(CUSHIONS), rng.randint(-5, 5))
                   for i in range(count))


def mug(x, y, color, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M-8 -40 q-6 -10 0 -18 q6 -8 0 -16 M8 -40 q-6 -10 0 -18 q6 -8 0 -16" fill="none" stroke="#ffffffcc" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M16 -24 q16 0 16 12 q0 12 -16 12" fill="none" stroke="{color}" stroke-width="6"/>'
            f'<rect x="-18" y="-32" width="36" height="34" rx="6" fill="{color}"/>'
            '<ellipse cx="0" cy="-32" rx="18" ry="5" fill="#6D3B1F"/>'
            '<rect x="-12" y="-40" width="10" height="9" rx="3" fill="#fff"/><rect x="1" y="-42" width="10" height="9" rx="3" fill="#FFE4EC"/>'
            "</g>")


def lightbulb(x, y):
    rays = "".join(f'<path d="M0 0 L0 -12" transform="translate(0 -6) rotate({a}) translate(0 -26)" stroke="#FFC107" stroke-width="3" stroke-linecap="round"/>'
                   for a in (-60, -30, 0, 30, 60))
    return (f'<g transform="translate({x} {y})">{rays}'
            '<circle cx="0" cy="-6" r="16" fill="#FFF176" stroke="#F9A825" stroke-width="3"/>'
            '<rect x="-7" y="8" width="14" height="10" rx="2" fill="#9E9E9E"/></g>')


def confetti(rng, n=30):
    colors = ["#FF5252", "#FFD740", "#40C4FF", "#69F0AE", "#E040FB", "#FF6E40"]
    return "".join(f'<rect x="{rng.randint(20, 780)}" y="{rng.randint(60, 300)}" width="9" height="14" rx="2" '
                   f'fill="{rng.choice(colors)}" transform="rotate({rng.randint(0, 90)} {rng.randint(20, 780)} {rng.randint(60, 300)})"/>'
                   for _ in range(n))


def label(x, y, text):
    w = 16 + len(text) * 13
    return (f'<rect x="{x - w / 2}" y="{y - 22}" width="{w}" height="32" rx="16" fill="#fff" stroke="#E0C9B0" stroke-width="3"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Comic Sans MS, Chalkboard, sans-serif" '
            f'font-size="20" font-weight="700" fill="#3A2A1A">{text}</text>')


def shout(x, y, text, size=34):
    w = size * 0.62 * len(text) + 36
    return (f'<rect x="{x - w / 2}" y="{y - size}" width="{w}" height="{size * 1.5}" rx="{size * 0.75}" fill="#fff" stroke="#FFB300" stroke-width="4"/>'
            f'<text x="{x}" y="{y + size * 0.18}" text-anchor="middle" font-family="Comic Sans MS, Chalkboard, sans-serif" '
            f'font-size="{size}" font-weight="700" fill="#E53935">{text}</text>')


def teddy(x, y):
    b = "#B07A4A"
    return (f'<g transform="translate({x} {y})">'
            f'<circle cx="-20" cy="-72" r="10" fill="{b}"/><circle cx="20" cy="-72" r="10" fill="{b}"/>'
            f'<ellipse cx="0" cy="-20" rx="28" ry="24" fill="{b}"/><circle cx="0" cy="-58" r="22" fill="{b}"/>'
            '<ellipse cx="0" cy="-52" rx="9" ry="7" fill="#E8C9A0"/><circle cx="0" cy="-55" r="3" fill="#222"/>'
            '<circle cx="-8" cy="-63" r="3" fill="#222"/><circle cx="8" cy="-63" r="3" fill="#222"/></g>')


def ball(x, y):
    return (f'<g transform="translate({x} {y})"><circle cx="0" cy="-18" r="18" fill="#FF7043"/>'
            '<path d="M-18 -18 H18 M0 -36 V0" stroke="#fff" stroke-width="3"/></g>')


# ---------- the room ----------

def palm(x, y, s, trunk="#8D6E4A", leaves="#3E8E41"):
    fronds = "".join(f'<ellipse cx="0" cy="-36" rx="11" ry="40" transform="rotate({a})" fill="{leaves}"/>'
                     for a in (-110, -70, -35, 0, 35, 70, 110))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M0 0 Q14 -110 4 -220" fill="none" stroke="{trunk}" stroke-width="16" stroke-linecap="round"/>'
            f'<g transform="translate(4 -220)">{fronds}</g></g>')


def apartments(x, y, w, h, night):
    wall, lit, dark = ("#3A4466", "#FFE082", "#2A3150") if night else ("#E8D3B5", "#9FD3F5", "#9FD3F5")
    out = f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{wall}"/><rect x="{x - 8}" y="{y - h - 12}" width="{w + 16}" height="14" fill="{"#2A3150" if night else "#B5653A"}"/>'
    for r, wy in enumerate(range(y - h + 22, y - 30, 60)):
        for c, wx in enumerate(range(x + 18, x + w - 30, 54)):
            on = night and (r + c) % 3 != 0
            out += f'<rect x="{wx}" y="{wy}" width="32" height="36" rx="3" fill="{lit if on else dark}"/>'
    return out


def window_view(night):
    """Looking out of the San Jose apartment: neighbours' apartments, palms, and the hills with the observatory."""
    if night:
        stars = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#FFF9C4"/>' for x, y in
                        [(90, 80), (220, 160), (330, 60), (480, 140), (120, 230), (420, 210), (560, 70)])
        return ('<rect width="800" height="600" fill="#1F2B5C"/>' + stars
                + '<circle cx="640" cy="140" r="70" fill="#FFF3B0"/><circle cx="676" cy="114" r="62" fill="#1F2B5C"/>'
                + '<path d="M0 360 Q160 300 330 330 Q480 250 620 300 T800 320 V600 H0Z" fill="#2C3A63"/>'
                + '<path d="M470 268 a16 16 0 0 1 32 0Z" fill="#9AA6C8"/>'
                + apartments(30, 600, 290, 190, True) + apartments(600, 600, 200, 150, True)
                + palm(420, 600, 1.3, "#1B2440", "#1B2440") + palm(500, 600, 1.0, "#1B2440", "#1B2440"))
    return ('<rect width="800" height="600" fill="#5DB7F2"/>'
            '<circle cx="680" cy="100" r="60" fill="#FFD84D"/>' + cloud(60, 110, 1.5) + cloud(330, 70, 1.2)
            + '<path d="M0 360 Q160 300 330 330 Q480 250 620 300 T800 320 V600 H0Z" fill="#D8B46A"/>'
            + '<path d="M0 400 Q200 350 400 380 T800 370 V600 H0Z" fill="#C49A52"/>'
            + '<rect x="470" y="262" width="40" height="18" fill="#fff"/><path d="M466 264 a24 24 0 0 1 48 0Z" fill="#fff" stroke="#CFD8DC" stroke-width="3"/>'
            + apartments(30, 600, 290, 190, False) + apartments(600, 600, 200, 150, False)
            + tree(380, 600, 1.4, "#E4572E") + palm(440, 600, 1.3) + palm(510, 600, 1.0) + tree(740, 600, 1.1, "#6CC24A"))


def room(night=False, door=None):
    """door: None, 'closed', or 'open'."""
    bunting_colors = ["#FF5252", "#FFD740", "#40C4FF", "#69F0AE", "#E040FB"]
    flags = "".join(
        f'<polygon points="{x - 16},{24 + abs(400 - x) * -0.03 + 18} {x + 16},{24 + abs(400 - x) * -0.03 + 18} {x},{24 + abs(400 - x) * -0.03 + 50}" '
        f'fill="{bunting_colors[i % 5]}"/>'
        for i, x in enumerate(range(300, 800, 52)))
    out = (
        '<rect width="800" height="600" fill="#FFE9D6"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#FFD9BD"/>' for x in range(30, 800, 60) for y in range(40, 470, 60))
        # window
        + '<rect x="34" y="64" width="232" height="182" rx="8" fill="#fff" stroke="#E0C9B0" stroke-width="6"/>'
        + f'<svg x="46" y="76" width="208" height="158" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid slice">{window_view(night)}</svg>'
        + '<path d="M150 76 V234 M46 155 H254" stroke="#fff" stroke-width="8"/>'
        + '<path d="M22 56 H280" stroke="#A1683A" stroke-width="8" stroke-linecap="round"/>'
        + '<path d="M26 60 q20 60 0 196 h28 q-14 -100 10 -196Z" fill="#F48FB1"/>'
        + '<path d="M274 60 q-20 60 0 196 h-28 q14 -100 -10 -196Z" fill="#F48FB1"/>'
        # bunting
        + '<path d="M290 40 Q545 70 800 40" fill="none" stroke="#A1683A" stroke-width="3"/>' + flags
        # framed picture of the bee story
        + '<rect x="326" y="86" width="120" height="96" rx="6" fill="#A1683A"/>'
        + '<rect x="336" y="96" width="100" height="76" fill="#BFE6FF"/>'
        + f'<g transform="translate(336 96) scale(0.125)">{flower(500, 250, 1.4, "smile", 230)}{bee(250, 180, 1.4)}</g>'
        # shelf
        + '<rect x="590" y="160" width="180" height="10" rx="3" fill="#A1683A"/>'
        + "".join(f'<rect x="{x}" y="{160 - h}" width="16" height="{h}" rx="3" fill="{c}"/>'
                  for x, h, c in [(600, 52, "#EF5350"), (618, 44, "#42A5F5"), (636, 56, "#66BB6A"), (654, 40, "#FFCA28"), (672, 50, "#AB47BC")])
        + '<path d="M716 160 L708 128 H752 L744 160Z" fill="#E07A5F"/>'
        + '<ellipse cx="722" cy="118" rx="12" ry="20" fill="#66BB6A"/><ellipse cx="740" cy="114" rx="11" ry="22" fill="#4CAF50"/>'
        # floor and rug
        + '<rect y="470" width="800" height="130" fill="#C68B59"/>'
        + "".join(f'<path d="M0 {y} H800" stroke="#B07746" stroke-width="2"/>' for y in (500, 535, 570))
        + '<ellipse cx="400" cy="548" rx="340" ry="46" fill="#5C6BC0"/>'
        + '<ellipse cx="400" cy="548" rx="300" ry="36" fill="#7986CB"/>'
        + '<ellipse cx="400" cy="548" rx="250" ry="26" fill="#9FA8DA"/>'
    )
    if door == "closed":
        out += ('<rect x="640" y="250" width="130" height="222" rx="4" fill="#A1683A"/>'
                '<rect x="656" y="268" width="98" height="80" rx="4" fill="#8D5A30"/><rect x="656" y="366" width="98" height="90" rx="4" fill="#8D5A30"/>'
                '<circle cx="752" cy="362" r="7" fill="#FFD54F"/>')
    elif door == "open":
        out += ('<rect x="634" y="244" width="142" height="228" fill="#7A4E2D"/>'
                '<rect x="640" y="250" width="130" height="222" fill="#8ED0F7"/>'
                + f'<g transform="translate(640 250)">{palm(80, 170, 0.62)}{tree(28, 170, 0.75, "#F3A712")}</g>'
                '<rect x="640" y="410" width="130" height="62" fill="#CFC8BE"/>'
                '<path d="M640 380 H770 M640 410 H770" stroke="#90A4AE" stroke-width="5"/>'
                + "".join(f'<path d="M{x} 380 V410" stroke="#90A4AE" stroke-width="4"/>' for x in range(652, 770, 18))
                + '<polygon points="770,250 800,236 800,486 770,472" fill="#A1683A"/>')
    return out


# ---------- pages ----------

def p01(rng):
    return (room() + cushion_pile(rng, 400, 540, 520, 4)
            + person("dibhai", 150, 560, "up", "big") + person("chhuti", 290, 572, "up", "big")
            + person("mithi", 520, 572, "up", "big") + person("bonu", 660, 566, "up", "big") + confetti(rng))


def p02(rng):
    xs = [("dibhai", 160, "Dibhai"), ("chhuti", 315, "Chhuti Didi"), ("mithi", 470, "Mithi"), ("bonu", 620, "Chithi Bonu")]
    return (room() + teddy(740, 540)
            + "".join(person(w, x, 545, "down", "happy", right_arm="up" if w == "mithi" else None) for w, x, _ in xs)
            + "".join(label(x, 588, name) for _, x, name in xs))


def p03(rng):
    return (room() + confetti(rng, 40) + shout(400, 236, "Yay, sleepover!")
            + person("dibhai", 170, 555, "up", "big") + person("chhuti", 320, 560, "up", "big")
            + person("mithi", 470, 560, "up", "big") + person("bonu", 610, 556, "up", "big")
            + ball(730, 560))


def p04(rng):
    return (room() + cushion_pile(rng, 470, 545, 420, 4)
            + person("dibhai", 130, 560, "hold", "big") + person("chhuti", 250, 566, "hold", "oh")
            + person("mithi", 700, 566, "hold", "big") + person("bonu", 560, 572, "up", "big")
            + cushion(250, hand_y("chhuti", 566), 70, 34, "#FFD54F"))


def p05(rng):
    return (room() + cushion_stack(rng, 730, 560, 9, 96)
            + person("dibhai", 150, 556, "down", "sad") + person("chhuti", 270, 560, "hips", "sad")
            + person("mithi", 390, 560, "down", "sad")
            + person("bonu", 600, 564, "hold", "happy") + cushion_stack(rng, 600, 564, 4))


def p06(rng):
    return (room() + cushion_stack(rng, 740, 560, 8, 90)
            + person("dibhai", 120, 556, "down", "oh") + person("chhuti", 215, 560, "down", "sad")
            + person("mithi", 310, 560, "down", "sad")
            + person("mom", 470, 562, "hips", "flat") + person("bonu", 630, 566, "hold", "happy")
            + cushion_stack(rng, 630, 566, 4))


def p07(rng):
    return (room(door="open")
            + person("dibhai", 140, 556, "down", "happy") + person("mithi", 260, 560, "down", "happy")
            + person("chhuti", 370, 560, "down", "oh") + person("mom", 520, 562, "hold", "flat")
            + person("bonu", 705, 470, "down", "cry")
            + lightbulb(140, top_of_head("dibhai", 556) - 18) + lightbulb(260, top_of_head("mithi", 560) - 18)
            + lightbulb(520, top_of_head("mom", 562) - 18) + cushion_pile(rng, 640, 590, 200, 1))


def p08(rng):
    return (room() + teddy(740, 545) + cushion_pile(rng, 120, 590, 200, 1)
            + person("dibhai", 200, 556, "down", "happy") + person("mithi", 390, 560, "hold", "big")
            + person("chhuti", 570, 560, "hips", "oh")
            + mug(390, hand_y("mithi", 560) + 14, "#FF7043") + lightbulb(390, top_of_head("mithi", 560) - 20))


def p09(rng):
    counter = ('<rect x="120" y="444" width="560" height="100" rx="10" fill="#F3E5D8"/>'
               '<rect x="108" y="434" width="584" height="20" rx="8" fill="#BCAAA4"/>'
               '<rect x="160" y="466" width="140" height="64" rx="8" fill="#E9D6C4"/><rect x="330" y="466" width="140" height="64" rx="8" fill="#E9D6C4"/>'
               '<rect x="500" y="466" width="140" height="64" rx="8" fill="#E9D6C4"/>')
    pan = ('<g transform="translate(180 434)"><rect x="-34" y="-30" width="68" height="30" rx="6" fill="#90A4AE"/>'
           '<rect x="30" y="-24" width="50" height="8" rx="4" fill="#455A64"/><ellipse cx="0" cy="-30" rx="34" ry="6" fill="#6D3B1F"/></g>')
    bag = ('<g transform="translate(620 434)"><path d="M-26 0 L-22 -56 H22 L26 0Z" fill="#fff" stroke="#F48FB1" stroke-width="3"/>'
           '<rect x="-14" y="-40" width="12" height="10" rx="3" fill="#FFE4EC"/><rect x="2" y="-30" width="12" height="10" rx="3" fill="#FFE4EC"/></g>')
    return (room() + person("dibhai", 250, 520, "down", "big") + person("chhuti", 400, 524, "down", "big")
            + person("mithi", 550, 524, "down", "big")
            + counter + pan + mug(300, 434, "#42A5F5") + mug(400, 434, "#AB47BC") + mug(500, 434, "#FF7043") + bag)


def p10(rng):
    return (room(door="open") + shout(705, 222, "Ding-dong!", 26)
            + person("dibhai", 150, 556, "hold", "big") + mug(150, hand_y("dibhai", 556) + 14, "#42A5F5")
            + person("chhuti", 280, 560, "hold", "happy") + mug(280, hand_y("chhuti", 560) + 14, "#AB47BC")
            + person("mithi", 410, 560, "hold", "big") + mug(410, hand_y("mithi", 560) + 14, "#FF7043")
            + person("bonu", 560, 566, "hold", "big") + mug(560, hand_y("bonu", 566) + 14, "#66BB6A"))


def p11(rng):
    blanket = ('<path d="M290 352 Q420 300 560 352 L572 420 Q420 380 278 420Z" fill="#4FC3F7"/>'
               + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" opacity=".7"/>' for x, y in
                         [(320, 370), (370, 350), (420, 340), (470, 350), (520, 365), (350, 395), (450, 375), (500, 395)]))
    return (room() + person("bonu", 425, 560, "up", "big")
            + cushion_stack(rng, 320, 560, 7, 90) + cushion_stack(rng, 530, 560, 7, 90) + blanket
            + person("dibhai", 140, 556, "up", "big") + person("mithi", 230, 566, "hold", "big", right_arm="up")
            + person("chhuti", 660, 560, "up", "big") + teddy(760, 560) + ball(600, 590) + confetti(rng, 16))


def p12(rng):
    table = ('<rect x="110" y="440" width="580" height="24" rx="10" fill="#8D5A3B"/>'
             '<rect x="140" y="462" width="22" height="80" rx="6" fill="#7A4A2E"/><rect x="638" y="462" width="22" height="80" rx="6" fill="#7A4A2E"/>')

    def plate(x, food):
        return f'<g transform="translate({x} 440)"><ellipse cx="0" cy="-4" rx="48" ry="12" fill="#fff" stroke="#ddd" stroke-width="2"/>{food}</g>'

    rice = plate(200, '<ellipse cx="0" cy="-14" rx="32" ry="16" fill="#FFFDF5" stroke="#EDE7D9" stroke-width="2"/>'
                      + "".join(f'<ellipse cx="{x}" cy="{y}" rx="3" ry="1.6" fill="#E8E0CC"/>' for x, y in [(-14, -18), (0, -22), (12, -16), (-4, -10), (18, -12)]))
    chicken = plate(330, "".join(f'<g transform="translate({x} -14) rotate({r})"><ellipse cx="0" cy="0" rx="18" ry="12" fill="#C0702E"/>'
                                 '<rect x="14" y="-3" width="16" height="6" rx="3" fill="#FFF8E1"/></g>' for x, r in [(-14, -10), (12, 20)]))
    mutton = ('<g transform="translate(470 440)"><path d="M-42 -26 Q-40 4 0 6 Q40 4 42 -26Z" fill="#fff" stroke="#ddd" stroke-width="2"/>'
              '<ellipse cx="0" cy="-26" rx="42" ry="9" fill="#B5532A"/>'
              '<circle cx="-14" cy="-28" r="7" fill="#7A3A1E"/><circle cx="8" cy="-27" r="8" fill="#7A3A1E"/><circle cx="24" cy="-25" r="5" fill="#7A3A1E"/></g>')
    soup = ('<g transform="translate(600 440)"><path d="M-36 -24 Q-34 4 0 6 Q34 4 36 -24Z" fill="#fff" stroke="#ddd" stroke-width="2"/>'
            '<ellipse cx="0" cy="-24" rx="36" ry="8" fill="#F2C14E"/><path d="M-6 -36 q-5 -8 0 -14 M6 -36 q-5 -8 0 -14" stroke="#ffffffcc" stroke-width="3" fill="none"/></g>')
    lemonade = "".join(f'<g transform="translate({x} 440)"><rect x="-12" y="-46" width="24" height="46" rx="4" fill="#FFF59D" stroke="#E0E0E0" stroke-width="2"/>'
                       '<circle cx="10" cy="-44" r="9" fill="#FFEB3B" stroke="#FBC02D" stroke-width="2"/></g>' for x in (265, 400, 535))
    return (room(night=True)
            + person("dibhai", 200, 520, "hold", "big") + person("chhuti", 330, 524, "hold", "happy")
            + person("mithi", 470, 524, "hold", "big") + person("bonu", 600, 528, "hold", "big")
            + table + rice + chicken + mutton + soup + lemonade)


def p13(rng):
    mat = ('<rect x="70" y="456" width="440" height="96" rx="12" fill="#FFE082"/>'
           + "".join(f'<path d="M{x} 456 V552" stroke="#FFCA28" stroke-width="6"/>' for x in range(100, 510, 40)))
    pillows = "".join(cushion(x, 462, 96, 40, c) for x, c in [(150, "#F48FB1"), (290, "#80CBC4"), (430, "#FFD54F")])
    heads = sleeping_head("dibhai", 150, 446) + sleeping_head("chhuti", 290, 446) + sleeping_head("bonu", 430, 446)
    blanket = ('<path d="M84 478 Q290 456 496 478 L500 548 H80Z" fill="#7E57C2"/>'
               + "".join(f'<path transform="translate({x} {y})" d="M0 -8 L2 -2 L8 0 L2 2 L0 8 L-2 2 L-8 0 L-2 -2Z" fill="#FFF59D"/>'
                         for x, y in [(130, 500), (210, 520), (300, 495), (380, 525), (450, 500)]))
    extra = "".join(cushion(x, y, 80, 34, rng.choice(CUSHIONS), r) for x, y, r in [(70, 560, -10), (520, 566, 14), (260, 576, -4)])
    bed = ('<rect x="560" y="300" width="20" height="240" rx="6" fill="#8D5A3B"/>'
           '<rect x="560" y="300" width="220" height="120" rx="16" fill="#A1683A"/>'
           '<rect x="566" y="410" width="214" height="60" rx="10" fill="#fff"/>'
           '<rect x="566" y="520" width="18" height="30" fill="#8D5A3B"/><rect x="758" y="520" width="18" height="30" fill="#8D5A3B"/>')
    bed_pillow = cushion(640, 396, 110, 44, "#fff")
    bed_head = sleeping_head("mithi", 640, 376)
    bed_blanket = '<path d="M566 420 Q680 404 784 420 L784 528 H566Z" fill="#F06292"/><path d="M566 440 Q680 424 784 440" stroke="#F8BBD0" stroke-width="6" fill="none"/>'
    zzz = ('<text x="330" y="380" font-family="Comic Sans MS, sans-serif" font-size="34" font-weight="700" fill="#7E57C2">Z z z</text>'
           '<text x="690" y="350" font-family="Comic Sans MS, sans-serif" font-size="30" font-weight="700" fill="#F06292">Z z z</text>')
    return room(night=True) + mat + pillows + heads + blanket + extra + bed + bed_pillow + bed_head + bed_blanket + zzz


PAGES = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13]


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, make in enumerate(PAGES, start=1):
        rng = random.Random(100 + i)
        with open(os.path.join(OUT, f"{i:02d}.svg"), "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">{make(rng)}</svg>\n')
    print(f"wrote {len(PAGES)} pages to {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
