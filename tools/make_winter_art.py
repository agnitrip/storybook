"""Draws simple placeholder pictures for "The Winter Wonderland" (Lake Tahoe).

Reuses the sisters from make_sleepover_art.py so everyone looks the same
across books. Swap any page for Adhuna's drawing in stories.js.

Run: python3 tools/make_winter_art.py
"""
import os
import random

from make_placeholder_art import cloud
from make_sleepover_art import (HEAD_Y, SISTERS, face, label, lightbulb, person, shout,
                                sleeping_head, top_of_head)

OUT = os.path.join(os.path.dirname(__file__), "..", "stories", "winter-wonderland", "pages")

SISTERS["jyotisko"] = dict(s=0.66, pj="#42A5F5", pants="#1565C0", style="boy", accent="#FFD54F")

SNOW = "#F4FAFF"
SNOW_SHADOW = "#D6E8F5"
BLOCK_LINE = "#B3D4EA"
SHAPE_COLORS = ["#64B5F6", "#BA68C8", "#F06292", "#4DB6AC", "#FFB74D"]

_clip = 0


def next_id(prefix):
    global _clip
    _clip += 1
    return f"{prefix}{_clip}"


# ---------- outdoors ----------

def pine(x, y, s=1.0):
    tiers = "".join(
        f'<polygon points="{-w},{ty} {w},{ty} 0,{ty - h}" fill="#2E7D4F"/>'
        f'<polygon points="{-w * 0.45},{ty - h * 0.55} {w * 0.45},{ty - h * 0.55} 0,{ty - h}" fill="{SNOW}"/>'
        f'<path d="M{-w} {ty} q{w / 2} -10 {w} 0 q{w / 2} -10 {w} 0" fill="{SNOW}"/>'
        for w, h, ty in [(60, 70, -30), (48, 64, -80), (34, 56, -126)])
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-8" y="-34" width="16" height="36" fill="#6D4C41"/>'
            f"{tiers}</g>")


def flakes(rng, n=26):
    return "".join(f'<circle cx="{rng.randint(10, 790)}" cy="{rng.randint(10, 440)}" r="{rng.choice([3, 4, 5])}" fill="#fff" opacity=".9"/>'
                   for _ in range(n))


def snow_mounds(rng):
    out = ""
    for x in range(40, 800, 110):
        x += rng.randint(-20, 20)
        out += f'<ellipse cx="{x}" cy="{rng.randint(560, 588)}" rx="{rng.randint(30, 50)}" ry="10" fill="{SNOW_SHADOW}"/>'
    for _ in range(6):  # footprints
        fx, fy = rng.randint(60, 740), rng.randint(552, 590)
        out += f'<ellipse cx="{fx}" cy="{fy}" rx="6" ry="4" fill="{SNOW_SHADOW}"/><ellipse cx="{fx + 14}" cy="{fy + 6}" rx="6" ry="4" fill="{SNOW_SHADOW}"/>'
    return out


def tahoe_bg(rng, edge_pines=True):
    sky_id = next_id("sky")
    out = (
        f'<defs><linearGradient id="{sky_id}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#4FB0F0"/><stop offset="1" stop-color="#BFE6FF"/></linearGradient></defs>'
        f'<rect width="800" height="600" fill="url(#{sky_id})"/>'
        '<circle cx="680" cy="86" r="62" fill="#FFF3B0" opacity=".6"/><circle cx="680" cy="86" r="42" fill="#FFD84D"/>'
        + cloud(rng.randint(40, 160), 70, 1.0) + cloud(rng.randint(360, 480), 50, 0.8)
        # mountains with snowy caps
        + '<path d="M-20 330 L120 180 L230 300 L360 150 L500 300 L620 190 L820 330Z" fill="#7C93B8"/>'
        + '<path d="M120 180 L95 207 L120 200 L140 210Z M360 150 L325 190 L352 180 L372 196 L395 188Z M620 190 L592 220 L618 212 L640 222Z" fill="#fff"/>'
        # Lake Tahoe
        + '<rect y="318" width="800" height="54" fill="#2F86D6"/>'
        + "".join(f'<path d="M{x} {y} h{w}" stroke="#BFE3FF" stroke-width="3" stroke-linecap="round"/>'
                  for x, y, w in [(80, 334, 40), (260, 350, 60), (470, 330, 34), (600, 356, 50), (380, 362, 28)])
        + "".join(pine(x, 330, 0.32) for x in range(10, 800, 34))
        # snowy ground
        + f'<path d="M0 380 Q200 350 400 372 T800 366 V600 H0Z" fill="{SNOW_SHADOW}"/>'
        + f'<path d="M0 420 Q240 392 520 414 T800 406 V600 H0Z" fill="{SNOW}"/>'
        + "".join(pine(x, rng.randint(410, 424), rng.uniform(0.55, 0.75)) for x in (150, 300, 520, 640))
        + snow_mounds(rng)
    )
    if edge_pines:
        out += pine(rng.randint(20, 50), 590, 1.6) + pine(rng.randint(750, 780), 590, 1.6)
    return out + flakes(rng)


def earmuffs(who, x, y, color):
    s = SISTERS[who]["s"]
    hy = y + HEAD_Y * s
    return (f'<path d="M{x - 36 * s} {hy - 4 * s} C{x - 34 * s} {hy - 52 * s} {x + 34 * s} {hy - 52 * s} {x + 36 * s} {hy - 4 * s}" '
            f'fill="none" stroke="#555" stroke-width="{4 * s}"/>'
            f'<circle cx="{x - 36 * s}" cy="{hy + 4 * s}" r="{12 * s}" fill="{color}"/><circle cx="{x + 36 * s}" cy="{hy + 4 * s}" r="{12 * s}" fill="{color}"/>')


def scarf(who, x, y, color):
    s = SISTERS[who]["s"]
    ny = y - 134 * s
    return (f'<rect x="{x - 26 * s}" y="{ny}" width="{52 * s}" height="{14 * s}" rx="{6 * s}" fill="{color}"/>'
            f'<rect x="{x + 8 * s}" y="{ny + 8 * s}" width="{12 * s}" height="{34 * s}" rx="{4 * s}" fill="{color}"/>')


WINTER = {  # earmuff + scarf colours per kid
    "dibhai": ("#FFD54F", "#FFD54F"),
    "chhuti": ("#FF80AB", "#FF80AB"),
    "mithi": ("#FFFFFF", "#FFEB3B"),
    "bonu": ("#FF5252", "#FF5252"),
    "jyotisko": ("#FFB74D", "#FFB74D"),
}


def kid(who, x, y, arms="down", mood="happy", right_arm=None):
    muff, sc = WINTER[who]
    return person(who, x, y, arms, mood, right_arm) + scarf(who, x, y, sc) + earmuffs(who, x, y, muff)


def snowman(x, y, s=1.0, hat="#333"):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="-36" r="40" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="3"/>'
            f'<circle cx="0" cy="-98" r="30" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="3"/>'
            f'<circle cx="0" cy="-146" r="24" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="3"/>'
            '<circle cx="-8" cy="-150" r="3.5" fill="#222"/><circle cx="8" cy="-150" r="3.5" fill="#222"/>'
            '<polygon points="0,-144 22,-140 0,-138" fill="#FF8A00"/>'
            '<path d="M-8 -134 Q0 -128 8 -134" fill="none" stroke="#222" stroke-width="2.5"/>'
            '<circle cx="0" cy="-104" r="3.5" fill="#222"/><circle cx="0" cy="-90" r="3.5" fill="#222"/>'
            '<path d="M-28 -100 L-60 -126 M-48 -116 L-56 -132 M28 -100 L60 -126 M48 -116 L58 -130" stroke="#6D4C41" stroke-width="4" stroke-linecap="round"/>'
            '<rect x="-26" y="-126" width="52" height="10" rx="5" fill="#E53935"/><rect x="10" y="-120" width="10" height="26" rx="4" fill="#E53935"/>'
            f'<rect x="-20" y="-172" width="40" height="6" fill="{hat}"/><rect x="-13" y="-196" width="26" height="26" fill="{hat}"/>'
            "</g>")


def snow_shape(x, y, kind, color, s=1.0):
    path = {
        "star": "M0 -14 L4 -4 L14 -4 L6 2 L9 13 L0 6 L-9 13 L-6 2 L-14 -4 L-4 -4Z",
        "heart": "M0 10 C-18 -4 -10 -18 0 -9 C10 -18 18 -4 0 10Z",
        "circle": "M-11 0 a11 11 0 1 0 22 0 a11 11 0 1 0 -22 0",
        "fish": "M-14 0 Q-2 -12 10 0 Q-2 12 -14 0Z M10 0 L18 -8 L18 8Z",
    }[kind]
    return f'<path transform="translate({x} {y}) scale({s})" d="{path}" fill="#fff" stroke="{color}" stroke-width="3"/>'


def igloo(x, y, s=1.0, built=1.0, shapes=None):
    """built < 1 leaves the top unfinished. shapes: list of (dx, dy, kind)."""
    cid = next_id("igloo")
    dome = "M-160 0 A160 140 0 0 1 160 0Z"
    rows = "".join(f'<path d="M-160 {-h} H160" stroke="{BLOCK_LINE}" stroke-width="3"/>' for h in range(28, 140, 28))
    joints = "".join(f'<path d="M{jx + (14 if r % 2 else 0)} {-28 * r} v-28" stroke="{BLOCK_LINE}" stroke-width="3"/>'
                     for r in range(1, 5) for jx in range(-140, 160, 48))
    top_cut = -140 * built
    out = (f'<g transform="translate({x} {y}) scale({s})">'
           f'<defs><clipPath id="{cid}"><rect x="-170" y="{top_cut}" width="340" height="{150 - top_cut}"/></clipPath></defs>'
           f'<g clip-path="url(#{cid})"><path d="{dome}" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="4"/>'
           f'<g clip-path="url(#{cid})">{rows}{joints}</g></g>'
           f'<path d="M70 0 A54 62 0 0 1 178 0Z" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="4"/>'
           '<path d="M94 0 A30 40 0 0 1 154 0Z" fill="#46688C"/>')
    for dx, dy, kind in shapes or []:
        out += snow_shape(dx, dy, kind, SHAPE_COLORS[(dx + dy) % len(SHAPE_COLORS)])
    return out + "</g>"


def snowball(x, y, r=12, flying=False):
    trail = (f'<path d="M{x - r - 30} {y - 4} h22 M{x - r - 24} {y + 6} h18" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
             if flying else "")
    return trail + f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="2.5"/>'


def car(x, y, riders, front=""):
    """riders: list of (who, dx) seen through the back window; front: extra drawing for the front window."""
    heads = "".join(f'<g transform="translate({x + dx} {y - 150}) scale(0.7)">'
                    f'{face(SISTERS[who]["style"], "big", SISTERS[who]["accent"])}</g>' for who, dx in riders)
    return (f'<g>'
            f'<path d="M{x - 240} {y - 40} Q{x - 240} {y - 110} {x - 180} {y - 116} L{x - 130} {y - 200} '
            f'Q{x - 120} {y - 212} {x - 100} {y - 212} L{x + 120} {y - 212} Q{x + 140} {y - 212} {x + 150} {y - 200} '
            f'L{x + 200} {y - 116} Q{x + 250} {y - 110} {x + 250} {y - 40} Z" fill="#E53935"/>'
            f'<path d="M{x - 230} {y - 236} Q{x} {y - 262} {x + 230} {y - 236} L{x + 140} {y - 212} L{x - 120} {y - 212}Z" fill="{SNOW}"/>'
            f'<path d="M{x - 112} {y - 196} L{x - 150} {y - 124} H{x - 10} V{y - 196}Z" fill="#BFE6FF"/>'
            f'<path d="M{x + 10} {y - 196} V{y - 124} H{x + 180} L{x + 140} {y - 196}Z" fill="#BFE6FF"/>'
            f"{heads}{front}"
            f'<rect x="{x - 240}" y="{y - 120}" width="490" height="80" rx="20" fill="#E53935"/>'
            f'<path d="M{x} {y - 120} V{y - 50}" stroke="#B71C1C" stroke-width="4"/>'
            f'<rect x="{x - 40}" y="{y - 100}" width="26" height="6" rx="3" fill="#B71C1C"/><rect x="{x + 40}" y="{y - 100}" width="26" height="6" rx="3" fill="#B71C1C"/>'
            f'<circle cx="{x + 240}" cy="{y - 84}" r="9" fill="#FFF59D"/>'
            + "".join(f'<circle cx="{x + wx}" cy="{y - 36}" r="38" fill="#333"/><circle cx="{x + wx}" cy="{y - 36}" r="16" fill="#9E9E9E"/>'
                      for wx in (-150, 160))
            + "</g>")


# ---------- inside the igloo ----------

def igloo_inside(rng):
    """A cut-away igloo standing in the Tahoe snow, so the sky and trees stay in the picture."""
    cid = next_id("inside")
    dome = "M40 600 V560 A360 450 0 0 1 760 560 V600Z"
    rows = "".join(f'<path d="M40 {y} H760" stroke="#C9E2F3" stroke-width="3"/>' for y in range(200, 560, 60))
    return (tahoe_bg(rng)
            + f'<defs><clipPath id="{cid}"><path d="{dome}"/></clipPath></defs>'
            + f'<path d="{dome}" fill="#E6F3FC"/>'
            + f'<g clip-path="url(#{cid})">{rows}'
            + f'<rect x="40" y="520" width="720" height="80" fill="{SNOW}"/>'
            + f'<ellipse cx="400" cy="572" rx="320" ry="22" fill="{SNOW_SHADOW}"/></g>'
            + f'<path d="M40 600 V560 A360 450 0 0 1 760 560 V600" fill="none" stroke="#fff" stroke-width="30"/>'
            + f'<path d="M25 600 V560 A375 465 0 0 1 775 560 V600" fill="none" stroke="{BLOCK_LINE}" stroke-width="3"/>'
            + f'<path d="M55 600 V560 A345 435 0 0 1 745 560 V600" fill="none" stroke="{BLOCK_LINE}" stroke-width="3"/>'
            + "".join(f'<circle cx="{rng.randint(80, 720)}" cy="{rng.randint(530, 590)}" r="3" fill="{BLOCK_LINE}"/>' for _ in range(10)))


def mini_bed(x, y, w=180, blanket="#BA68C8"):
    return (f'<rect x="{x - w / 2}" y="{y - 40}" width="{w}" height="40" rx="12" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="3"/>'
            f'<ellipse cx="{x - w / 2 + 34}" cy="{y - 42}" rx="28" ry="12" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="3"/>'
            f'<rect x="{x - w / 2 + 60}" y="{y - 48}" width="{w - 70}" height="22" rx="10" fill="{blanket}"/>')


def bag(x, y, color):
    return (f'<g transform="translate({x} {y})"><rect x="-26" y="-44" width="52" height="44" rx="8" fill="{color}"/>'
            '<path d="M-12 -44 Q0 -64 12 -44" fill="none" stroke="#5D4037" stroke-width="4"/></g>')


def jacket_pile(x, y):
    return (f'<g transform="translate({x} {y})"><path d="M-50 0 Q-40 -30 0 -26 Q40 -30 50 0Z" fill="#8E6CCF"/>'
            '<path d="M-40 -18 Q-20 -46 20 -40 Q40 -36 44 -18Z" fill="#2BB3A3"/>'
            '<path d="M-30 -36 Q0 -60 30 -42Z" fill="#F06292"/></g>')


def sand_toys(x, y):
    return (f'<g transform="translate({x} {y})"><path d="M-22 0 L-26 -40 H26 L22 0Z" fill="#FFB74D"/>'
            '<path d="M-24 -40 Q0 -64 24 -40" fill="none" stroke="#E65100" stroke-width="3"/>'
            '<path d="M40 0 l10 -26 l10 26Z" fill="#64B5F6"/><path d="M70 -2 C60 -24 90 -24 80 -2Z" fill="#F06292"/>'
            '<rect x="-60" y="-8" width="10" height="34" rx="3" fill="#4DB6AC" transform="rotate(-30 -55 0)"/></g>')


# ---------- pages ----------

def p01(rng):
    return (tahoe_bg(rng) + igloo(470, 520, 1.1, shapes=[(-60, -110, "star"), (20, -126, "heart"), (-120, -60, "circle")])
            + snowman(700, 560, 0.8)
            + kid("dibhai", 130, 560, "up", "big") + kid("mithi", 250, 572, "up", "big")
            + kid("chhuti", 360, 578, "down", "happy") + kid("bonu", 600, 584, "up", "big") + kid("jyotisko", 480, 588, "up", "big"))


def p02(rng):
    xs = [("dibhai", 130, "Dibhai"), ("chhuti", 270, "Chhuti Didi"), ("mithi", 410, "Mithi"),
          ("bonu", 545, "Chithi Bonu"), ("jyotisko", 670, "Jyotisko")]
    return (tahoe_bg(rng) + "".join(kid(w, x, 545, "down", "happy", right_arm="up" if w == "mithi" else None) for w, x, _ in xs)
            + "".join(label(x, 588, name) for _, x, name in xs))


def p03(rng):
    return (tahoe_bg(rng) + shout(400, 120, "Lake Tahoe!", 30)
            + kid("dibhai", 150, 560, "up", "big") + snowball(150, 300, 14)
            + kid("chhuti", 290, 570, "hold", "big") + kid("mithi", 430, 566, "up", "big")
            + kid("bonu", 560, 576, "up", "big") + kid("jyotisko", 670, 580, "hold", "big")
            + f'<path d="M520 590 q60 -10 120 0 l-10 14 h-100Z" fill="#E53935"/>')


def p04(rng):
    return (tahoe_bg(rng) + kid("dibhai", 160, 556, "down", "oh") + kid("chhuti", 300, 560, "hips", "oh")
            + kid("mithi", 480, 560, "hips", "big") + lightbulb(480, top_of_head("mithi", 560) - 26)
            + kid("bonu", 610, 566, "down", "happy") + kid("jyotisko", 700, 572, "down", "happy")
            + f'<g opacity=".55">{igloo(480, 340, 0.35)}</g>')


def p05(rng):
    block = lambda x, y: f'<rect x="{x - 22}" y="{y - 14}" width="44" height="28" rx="5" fill="#fff" stroke="{BLOCK_LINE}" stroke-width="3"/>'
    return (tahoe_bg(rng) + igloo(420, 520, 1.1, built=0.6)
            + kid("dibhai", 140, 560, "hold", "happy") + block(140, 470)
            + kid("mithi", 250, 568, "up", "big") + kid("chhuti", 640, 566, "hold", "happy") + block(640, 478)
            + kid("bonu", 740, 576, "hold", "big") + block(740, 504) + block(560, 556) + block(600, 580))


def p06(rng):
    return (igloo_inside(rng) + snowman(560, 560, 0.75)
            + kid("dibhai", 150, 556, "down", "oh") + kid("chhuti", 260, 560, "down", "oh")
            + kid("mithi", 420, 560, "hold", "big") + lightbulb(420, top_of_head("mithi", 560) - 26)
            + kid("bonu", 700, 566, "down", "happy"))


def p07(rng):
    return (igloo_inside(rng) + bag(90, 560, "#8D6E63") + bag(150, 566, "#5C6BC0") + jacket_pile(720, 560)
            + snowman(250, 520, 0.6) + snowman(420, 520, 0.55, "#5C6BC0") + snowman(590, 520, 0.6, "#E53935")
            + kid("dibhai", 190, 576, "hold", "big") + kid("chhuti", 340, 580, "hold", "big")
            + kid("mithi", 500, 580, "hold", "big") + kid("bonu", 640, 586, "hold", "big"))


def p08(rng):
    return (igloo_inside(rng) + snowman(140, 540, 0.6) + snowman(680, 540, 0.6, "#E53935")
            + kid("dibhai", 250, 560, "down", "happy") + kid("chhuti", 360, 564, "down", "oh")
            + kid("mithi", 480, 564, "hold", "big") + sand_toys(520, 590) + lightbulb(480, top_of_head("mithi", 564) - 26)
            + kid("bonu", 600, 570, "down", "happy"))


def p09(rng):
    return (igloo_inside(rng) + snowman(700, 540, 0.6)
            + mini_bed(260, 540, 360, "#BA68C8")
            + sleeping_head("dibhai", 150, 482) + sleeping_head("chhuti", 250, 482) + sleeping_head("bonu", 350, 486)
            + '<path d="M120 510 Q260 490 430 510 V530 H120Z" fill="#BA68C8"/>'
            + '<text x="320" y="420" font-family="Comic Sans MS, sans-serif" font-size="32" font-weight="700" fill="#7E57C2">Z z z</text>'
            + kid("mithi", 560, 572, "hold", "happy") + sand_toys(600, 590))


def p10(rng):
    shapes = [(-90, -100, "star"), (-30, -128, "heart"), (40, -124, "circle"), (100, -96, "fish"), (-130, -56, "heart")]
    return (tahoe_bg(rng) + igloo(400, 560, 1.4, shapes=shapes)
            + kid("mithi", 420, 382, "up", "big") + sand_toys(470, 384)
            + shout(640, 220, "Shapes!", 26))


def p11(rng):
    shapes = [(-90, -100, "star"), (-30, -128, "heart"), (40, -124, "circle"), (100, -96, "fish"), (-130, -56, "heart")]
    return (tahoe_bg(rng) + igloo(400, 500, 1.15, shapes=shapes) + shout(400, 200, "Wow, so cool!", 26)
            + kid("dibhai", 90, 572, "up", "big") + kid("chhuti", 195, 580, "up", "big") + kid("jyotisko", 300, 592, "up", "big")
            + kid("mithi", 640, 584, "hips", "big") + kid("bonu", 735, 588, "up", "big"))


def p12(rng):
    shapes = "".join(snow_shape(x, y, k, SHAPE_COLORS[i % 5]) for i, (x, y, k) in enumerate(
        [(120, 200, "star"), (240, 150, "heart"), (560, 150, "circle"), (690, 210, "fish"), (90, 330, "heart"),
         (720, 340, "star"), (520, 480, "star"), (610, 486, "heart"), (700, 482, "circle")]))
    return (igloo_inside(rng) + shapes + mini_bed(610, 546, 220, "#42A5F5")
            + kid("dibhai", 120, 560, "hold", "happy") + kid("chhuti", 230, 566, "hold", "happy")
            + kid("mithi", 340, 566, "hold", "big") + sand_toys(380, 590) + kid("bonu", 450, 572, "hold", "happy")
            + kid("jyotisko", 610, 500, "up", "big"))


def p13(rng):
    shiver = lambda x, y: f'<path d="M{x} {y} q6 -6 0 -12 q-6 -6 0 -12 M{x + 12} {y} q6 -6 0 -12 q-6 -6 0 -12" fill="none" stroke="#64B5F6" stroke-width="3"/>'
    return (igloo_inside(rng) + mini_bed(640, 546, 220, "#42A5F5") + sleeping_head("jyotisko", 580, 494)
            + '<path d="M600 516 Q660 504 740 516 V530 H600Z" fill="#42A5F5"/>'
            + '<text x="640" y="450" font-family="Comic Sans MS, sans-serif" font-size="28" font-weight="700" fill="#42A5F5">Z z z</text>'
            + kid("dibhai", 120, 560, "hold", "sad") + kid("chhuti", 240, 566, "hold", "sad")
            + kid("mithi", 360, 566, "hold", "sad") + kid("bonu", 470, 572, "hold", "sad")
            + shiver(70, 360) + shiver(300, 370) + shiver(520, 400))


def p14(rng):
    return (tahoe_bg(rng) + car(690, 600, []) + igloo(170, 470, 0.7)
            + kid("mithi", 300, 572, "up", "big") + snowball(410, 340, 13, True)
            + kid("dibhai", 520, 566, "up", "big") + snowball(440, 280, 12, True)
            + kid("chhuti", 410, 580, "hold", "big") + kid("bonu", 620, 586, "up", "big")
            + snowball(560, 300, 12) + snowball(250, 330, 11, True) + snowball(680, 380, 10))


def p15(rng):
    steam = "".join(f'<path d="M{x} 300 q-8 -14 0 -26 q8 -12 0 -24" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>' for x in (290, 340, 470))
    # Mom and Jyotisko (on her lap) are drawn into the front window before the car body covers their shoulders.
    front = (f'<g transform="translate(500 450) scale(0.72)">{face("bun", "happy", "#FFD54F")}</g>'
             f'<g transform="translate(470 470) scale(0.5)">{face("boy", "big", "#FFB74D")}</g>')
    return (tahoe_bg(rng)
            + car(400, 600, [("dibhai", -132), ("chhuti", -96), ("mithi", -60), ("bonu", -24)], front)
            + steam + shout(400, 230, "Ahh, warm!", 26))


PAGES = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15]


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, make in enumerate(PAGES, start=1):
        rng = random.Random(200 + i)
        with open(os.path.join(OUT, f"{i:02d}.svg"), "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">{make(rng)}</svg>\n')
    print(f"wrote {len(PAGES)} pages to {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
