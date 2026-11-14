"""Draws simple placeholder pictures for "The Bee and the Flower".

Swap any page for Adhuna's own drawing by dropping a photo into the
story's pages/ folder and pointing that page's `image` at it in stories.js.

Run: python3 tools/make_placeholder_art.py
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "..", "stories", "bee-and-flower", "pages")

BEE_YELLOW = "#FFD23F"
INK = "#222"
PETAL_RED = "#E53935"
PETAL_EDGE = "#B71C1C"
CENTER_YELLOW = "#FFC93C"
STEM = "#4CAF50"

_clip_id = 0


def page(body, bg):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">{bg}{body}</svg>\n'


FALL_CANOPY = ["#E4572E", "#F3A712", "#C0392B", "#E9C46A", "#D9822B"]
SPRING_CANOPY = ["#6CC24A", "#4FAE3A", "#8FD45E", "#F7A8C4"]


def sky(top, bottom):
    return (
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
        '<rect width="800" height="600" fill="url(#sky)"/>'
        '<circle cx="680" cy="86" r="62" fill="#FFF3B0" opacity=".6"/>'
        '<circle cx="680" cy="86" r="44" fill="#FFD84D"/>'
    )


def cloud(x, y, s=1.0):
    puffs = [(0, 0, 40, 24), (34, -14, 34, 28), (70, -2, 38, 24), (36, 8, 56, 20)]
    return f'<g transform="translate({x} {y}) scale({s})" fill="#fff" opacity=".95">' + "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>' for cx, cy, rx, ry in puffs) + "</g>"


def tree(x, y, s, color):
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        '<rect x="-8" y="-72" width="16" height="74" rx="4" fill="#7A4E2D"/>'
        f'<circle cx="0" cy="-104" r="46" fill="{color}"/>'
        f'<circle cx="-32" cy="-80" r="32" fill="{color}"/><circle cx="32" cy="-80" r="32" fill="{color}"/>'
        '<circle cx="-12" cy="-116" r="14" fill="#fff" opacity=".18"/>'
        "</g>"
    )


def flock(x, y):
    return "".join(
        f'<path d="M{x + dx} {y + dy} q7 -8 14 0 q7 -8 14 0" fill="none" stroke="#4A5A6A" stroke-width="2.5" stroke-linecap="round"/>'
        for dx, dy in [(0, 0), (34, 12), (-30, 16)]
    )


def tuft(x, y, color):
    return (f'<path d="M{x - 10} {y} L{x - 14} {y - 22} M{x} {y} L{x} {y - 28} M{x + 10} {y} L{x + 15} {y - 20}" '
            f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>')


def rock(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="26" ry="16" fill="#9AA3AB"/>'
            '<ellipse cx="-6" cy="-5" rx="10" ry="5" fill="#C3CAD0"/></g>')


def mushroom(x, y):
    return (f'<g transform="translate({x} {y})"><rect x="-5" y="-18" width="10" height="18" rx="4" fill="#F5E6CC"/>'
            '<path d="M-18 -16 Q0 -40 18 -16Z" fill="#D63A2F"/>'
            '<circle cx="-7" cy="-24" r="3" fill="#fff"/><circle cx="6" cy="-27" r="2.5" fill="#fff"/></g>')


def pumpkin(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<ellipse cx="-12" cy="-16" rx="16" ry="18" fill="#F08A24"/><ellipse cx="12" cy="-16" rx="16" ry="18" fill="#F08A24"/>'
            '<ellipse cx="0" cy="-16" rx="14" ry="19" fill="#F59E3C"/>'
            '<path d="M0 -34 Q2 -42 8 -44" stroke="#4E7A2A" stroke-width="4" fill="none" stroke-linecap="round"/></g>')


def acorn(x, y):
    return (f'<g transform="translate({x} {y})"><ellipse cx="0" cy="-6" rx="7" ry="9" fill="#9C6B30"/>'
            '<path d="M-9 -10 Q0 -20 9 -10Z" fill="#6B4423"/></g>')


def daisy(x, y):
    petals = "".join(f'<ellipse cx="0" cy="-7" rx="3.5" ry="7" transform="rotate({a})" fill="#fff"/>' for a in range(0, 360, 45))
    return f'<g transform="translate({x} {y})">{petals}<circle r="4" fill="#FFC93C"/></g>'


def scenery_back(rng, spring):
    canopy = SPRING_CANOPY if spring else FALL_CANOPY
    out = "".join(cloud(x, y, s) for x, y, s in
                  [(rng.randint(30, 160), rng.randint(50, 90), 0.9),
                   (rng.randint(300, 460), rng.randint(40, 80), 0.7),
                   (rng.randint(520, 600), rng.randint(150, 190), 0.6)])
    if not spring:
        out += flock(rng.randint(200, 520), rng.randint(110, 150))
    out += f'<path d="M0 430 Q150 390 320 420 T640 410 T800 400 V600 H0Z" fill="{"#B5E08C" if spring else "#E9B676"}"/>'
    for i, x in enumerate(range(20, 800, 70)):
        out += tree(x + rng.randint(-18, 18), 440 + rng.randint(-14, 6), rng.uniform(0.45, 0.7), canopy[(i + rng.randint(0, 3)) % len(canopy)])
    return out


def scenery_front(rng, spring):
    if spring:
        items = [lambda x, y: tuft(x, y, "#4E9A2E"), lambda x, y: daisy(x, y - 6), rock]
    else:
        items = [lambda x, y: tuft(x, y, "#C9A33B"), rock, mushroom, pumpkin, acorn,
                 lambda x, y: leaf(x, y - 4, rng.randint(0, 180), rng.choice(FALL_CANOPY), 0.7)]
    out = ""
    for x in range(30, 800, 64):
        out += rng.choice(items)(x + rng.randint(-14, 14), 576 + rng.randint(-8, 10))
    return out


def bush(x, y, s, colors):
    blobs = [(-26, 0, 22), (0, -12, 26), (26, 0, 22), (0, 6, 22)]
    return f'<g transform="translate({x} {y}) scale({s})">' + "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{colors[i % len(colors)]}"/>' for i, (cx, cy, r) in enumerate(blobs)) + "</g>"


def fence(x, y, posts=4):
    out = f'<g transform="translate({x} {y})">'
    out += f'<rect x="0" y="-30" width="{(posts - 1) * 30 + 8}" height="6" fill="#A8794A"/>'
    out += f'<rect x="0" y="-16" width="{(posts - 1) * 30 + 8}" height="6" fill="#A8794A"/>'
    out += "".join(f'<rect x="{i * 30}" y="-40" width="8" height="40" rx="2" fill="#C49461"/>' for i in range(posts))
    return out + "</g>"


def hay_bale(x, y):
    return (f'<g transform="translate({x} {y})"><rect x="-30" y="-36" width="60" height="36" rx="12" fill="#E6C15A"/>'
            '<path d="M-20 -26 h40 M-22 -16 h44 M-20 -6 h40" stroke="#C9A33B" stroke-width="3"/></g>')


def barn(x, y, s=0.5):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<rect x="-50" y="-70" width="100" height="70" fill="#C0392B"/>'
            '<polygon points="-60,-70 0,-115 60,-70" fill="#8E2A20"/>'
            '<rect x="-18" y="-44" width="36" height="44" fill="#fff"/>'
            '<path d="M-18 -44 L18 0 M18 -44 L-18 0" stroke="#C0392B" stroke-width="5"/></g>')


def butterfly_small(x, y, color):
    return (f'<g transform="translate({x} {y})"><ellipse cx="-7" cy="0" rx="8" ry="11" fill="{color}"/>'
            f'<ellipse cx="7" cy="0" rx="8" ry="11" fill="{color}"/><rect x="-1.5" y="-9" width="3" height="18" rx="1.5" fill="#333"/></g>')


# Pages whose own drawing already fills one side, so the big framing tree stays off that side.
SKIP_EDGE_TREE = {"05": "right"}


def scenery_mid(rng, spring, page_id):
    canopy = SPRING_CANOPY if spring else FALL_CANOPY
    bushes = ["#4FAE3A", "#6CC24A"] if spring else ["#C0392B", "#D9822B", "#E9C46A"]
    out = ""
    for _ in range(3):
        out += bush(rng.randint(60, 740), rng.randint(486, 506), rng.uniform(0.7, 1.0), bushes)
    extra = [lambda: fence(rng.randint(120, 560), 512, rng.randint(3, 5))]
    if not spring:
        extra.append(lambda: hay_bale(rng.randint(150, 650), 514))
    for make in rng.sample(extra, len(extra)):
        out += make()
    return out


def edge_trees(rng, spring, page_id):
    canopy = SPRING_CANOPY if spring else FALL_CANOPY
    out = ""
    if SKIP_EDGE_TREE.get(page_id) != "left":
        out += tree(rng.randint(20, 50), 572, rng.uniform(1.5, 1.75), rng.choice(canopy[:3]))
    if SKIP_EDGE_TREE.get(page_id) != "right":
        out += tree(rng.randint(750, 780), 572, rng.uniform(1.5, 1.75), rng.choice(canopy[:3]))
    return out


def air(rng, spring):
    if spring:
        return "".join(butterfly_small(rng.randint(120, 680), rng.randint(220, 330), rng.choice(["#FFB347", "#B39DDB", "#81D4FA"]))
                       for _ in range(3))
    return "".join(leaf(rng.randint(60, 740), rng.randint(180, 420), rng.randint(0, 180), rng.choice(FALL_CANOPY), 0.8)
                   for _ in range(6))


def fall_bg(rng, page_id):
    far_barn = barn(rng.choice([rng.randint(200, 300), rng.randint(470, 560)]), 432) if rng.random() < 0.6 else ""
    return (
        sky("#4FB0F0", "#A6DAFA") + scenery_back(rng, spring=False) + far_barn
        + '<path d="M0 470 Q200 420 400 460 T800 450 V600 H0Z" fill="#D9934E"/>'
        + scenery_mid(rng, False, page_id)
        + '<path d="M0 520 Q260 490 520 520 T800 510 V600 H0Z" fill="#B8733A"/>'
        + edge_trees(rng, False, page_id) + air(rng, False)
    )


def spring_bg(rng, page_id):
    return (
        sky("#3FA9F0", "#A6DAFA") + scenery_back(rng, spring=True)
        + '<path d="M0 440 Q200 400 400 430 T800 420 V600 H0Z" fill="#9BDB72"/>'
        + scenery_mid(rng, True, page_id)
        + '<path d="M0 500 Q260 470 520 500 T800 490 V600 H0Z" fill="#7CC456"/>'
        + edge_trees(rng, True, page_id) + air(rng, True)
    )


def bee(x, y, s=1.0, mood="happy", flip=False, pollen=False, hold_tummy=False):
    global _clip_id
    _clip_id += 1
    cid = f"beebody{_clip_id}"
    sx = -s if flip else s
    mouths = {
        "happy": '<path d="M50 4 Q58 12 66 4" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>',
        "sad": '<path d="M50 10 Q58 2 66 10" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>',
        "wow": '<ellipse cx="58" cy="7" rx="5" ry="6" fill="#222"/>',
        "yum": '<path d="M49 3 Q58 15 67 3Z" fill="#222"/><path d="M54 8 Q58 12 62 8" fill="#FF7A8A"/>',
    }
    legs = "".join(
        f'<path d="M{lx} 28 L{lx - 4} 44" stroke="#222" stroke-width="4" stroke-linecap="round"/>'
        for lx in (-20, -2, 16)
    )
    dust = ""
    if pollen:
        dust = "".join(
            f'<circle cx="{lx - 4}" cy="44" r="6" fill="#FFB000" stroke="#E08E00" stroke-width="1.5"/>'
            for lx in (-20, -2, 16)
        )
    arms = ""
    if hold_tummy:
        arms = '<path d="M30 6 Q14 22 -2 18" fill="none" stroke="#222" stroke-width="4" stroke-linecap="round"/>'
    return (
        f'<g transform="translate({x} {y}) scale({sx} {s})">'
        f'<defs><clipPath id="{cid}"><ellipse cx="0" cy="0" rx="48" ry="34"/></clipPath></defs>'
        '<ellipse cx="-10" cy="-40" rx="20" ry="30" transform="rotate(-25 -10 -40)" fill="#E3F4FF" opacity=".9" stroke="#7FB7D9" stroke-width="3"/>'
        '<ellipse cx="14" cy="-42" rx="18" ry="28" transform="rotate(20 14 -42)" fill="#E3F4FF" opacity=".9" stroke="#7FB7D9" stroke-width="3"/>'
        f"{legs}{dust}"
        '<polygon points="-46,-6 -64,0 -46,6" fill="#222"/>'
        f'<ellipse cx="0" cy="0" rx="48" ry="34" fill="{BEE_YELLOW}"/>'
        f'<g clip-path="url(#{cid})"><rect x="-26" y="-40" width="13" height="80" fill="#222"/>'
        '<rect x="-3" y="-40" width="13" height="80" fill="#222"/><rect x="20" y="-40" width="10" height="80" fill="#222"/></g>'
        '<ellipse cx="0" cy="0" rx="48" ry="34" fill="none" stroke="#222" stroke-width="4"/>'
        '<path d="M40 -26 Q34 -50 24 -56" fill="none" stroke="#222" stroke-width="3"/><circle cx="24" cy="-56" r="5" fill="#222"/>'
        '<path d="M54 -26 Q60 -50 70 -54" fill="none" stroke="#222" stroke-width="3"/><circle cx="70" cy="-54" r="5" fill="#222"/>'
        f'<circle cx="52" cy="-4" r="25" fill="{BEE_YELLOW}" stroke="#222" stroke-width="4"/>'
        '<circle cx="60" cy="-11" r="5" fill="#222"/><circle cx="62" cy="-13" r="1.8" fill="#fff"/>'
        '<circle cx="66" cy="2" r="5" fill="#FF9AA8" opacity=".8"/>'
        f"{mouths[mood]}{arms}"
        "</g>"
    )


def flower(x, y, s=1.0, face=None, stem_h=200):
    petals = "".join(
        f'<ellipse cx="0" cy="-40" rx="22" ry="38" transform="rotate({a})" '
        f'fill="{PETAL_RED}" stroke="{PETAL_EDGE}" stroke-width="3"/>'
        for a in range(0, 360, 45)
    )
    faces = {
        "smile": '<circle cx="-10" cy="-6" r="4.5" fill="#222"/><circle cx="10" cy="-6" r="4.5" fill="#222"/>'
                 '<path d="M-11 7 Q0 17 11 7" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>',
        "talk": '<circle cx="-10" cy="-6" r="4.5" fill="#222"/><circle cx="10" cy="-6" r="4.5" fill="#222"/>'
                '<ellipse cx="0" cy="10" rx="6" ry="5" fill="#222"/>',
    }
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M0 0 Q-8 {stem_h / 2} 0 {stem_h}" fill="none" stroke="{STEM}" stroke-width="9" stroke-linecap="round"/>'
        f'<ellipse cx="-24" cy="{stem_h * 0.55}" rx="26" ry="11" transform="rotate(-30 -24 {stem_h * 0.55})" fill="{STEM}"/>'
        f'<ellipse cx="22" cy="{stem_h * 0.7}" rx="24" ry="10" transform="rotate(30 22 {stem_h * 0.7})" fill="{STEM}"/>'
        f"{petals}"
        f'<circle cx="0" cy="0" r="30" fill="{CENTER_YELLOW}" stroke="#E0A800" stroke-width="3"/>'
        f'{faces.get(face, "")}'
        "</g>"
    )


def dry_stem(x, y, h=150, lean=30):
    return (
        f'<path d="M{x} {y} Q{x - 6} {y - h / 2} {x + lean} {y - h}" fill="none" stroke="#8D6E4A" stroke-width="7" stroke-linecap="round"/>'
        f'<circle cx="{x + lean}" cy="{y - h}" r="9" fill="#7A5C3C"/>'
    )


def leaf(x, y, rot, color, s=1.0):
    return (
        f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
        f'<path d="M0 -22 Q18 -6 0 24 Q-18 -6 0 -22Z" fill="{color}"/>'
        '<path d="M0 -18 V20" stroke="#00000033" stroke-width="2"/></g>'
    )


def falling_leaves(spots):
    colors = ["#E4572E", "#F3A712", "#C0392B", "#E9C46A", "#D9822B"]
    return "".join(leaf(x, y, r, colors[i % len(colors)]) for i, (x, y, r) in enumerate(spots))


def flight_path(d):
    return f'<path d="{d}" fill="none" stroke="#6B4F2A" stroke-width="3" stroke-dasharray="4 12" stroke-linecap="round" opacity=".6"/>'


def squirrel(x, y):
    return (
        f'<g transform="translate({x} {y})">'
        '<path d="M-40 40 C-130 30 -140 -90 -60 -110 C-20 -120 -10 -70 -50 -60 C-80 -50 -70 0 -30 10Z" fill="#B5652B" stroke="#7A3E15" stroke-width="4"/>'
        '<ellipse cx="0" cy="20" rx="46" ry="56" fill="#A0522D" stroke="#7A3E15" stroke-width="4"/>'
        '<ellipse cx="6" cy="34" rx="26" ry="34" fill="#E8B98A"/>'
        '<circle cx="12" cy="-50" r="36" fill="#A0522D" stroke="#7A3E15" stroke-width="4"/>'
        '<polygon points="-12,-80 -4,-104 6,-82" fill="#A0522D" stroke="#7A3E15" stroke-width="4"/>'
        '<polygon points="20,-82 32,-104 38,-78" fill="#A0522D" stroke="#7A3E15" stroke-width="4"/>'
        '<circle cx="24" cy="-56" r="5" fill="#222"/><circle cx="26" cy="-58" r="1.8" fill="#fff"/>'
        '<circle cx="30" cy="-36" r="14" fill="#C27A48"/><circle cx="44" cy="-46" r="4" fill="#222"/>'
        '<g transform="translate(26 8)"><ellipse cx="0" cy="8" rx="13" ry="16" fill="#9C6B30"/>'
        '<path d="M-15 0 Q0 -16 15 0Z" fill="#6B4423"/><path d="M0 -10 V-16" stroke="#6B4423" stroke-width="3"/></g>'
        '<path d="M8 4 Q22 12 36 4" fill="none" stroke="#7A3E15" stroke-width="5" stroke-linecap="round"/>'
        "</g>"
    )


def baby_elephant(x, y):
    grey, edge = "#A9B4C2", "#6F7C8C"
    legs = "".join(
        f'<rect x="{lx}" y="40" width="34" height="62" rx="12" fill="{grey}" stroke="{edge}" stroke-width="4"/>'
        for lx in (-80, -36, 30, 70)
    )
    return (
        f'<g transform="translate({x} {y})">'
        f'<path d="M-112 0 Q-140 10 -134 40" fill="none" stroke="{edge}" stroke-width="5" stroke-linecap="round"/>'
        f"{legs}"
        f'<ellipse cx="0" cy="10" rx="115" ry="72" fill="{grey}" stroke="{edge}" stroke-width="4"/>'
        f'<circle cx="-112" cy="-20" r="1" fill="{grey}"/>'
        f'<circle cx="104" cy="-44" r="62" fill="{grey}" stroke="{edge}" stroke-width="4"/>'
        f'<path d="M140 -10 Q170 30 160 70 Q156 90 176 92" fill="none" stroke="{edge}" stroke-width="30" stroke-linecap="round"/>'
        f'<path d="M140 -10 Q170 30 160 70 Q156 90 176 92" fill="none" stroke="{grey}" stroke-width="22" stroke-linecap="round"/>'
        f'<path d="M80 -90 C10 -110 -10 -10 40 10 C70 20 90 -20 80 -90Z" fill="#C3CCD8" stroke="{edge}" stroke-width="4"/>'
        '<path d="M64 -70 C36 -74 30 -20 52 -8" fill="none" stroke="#F2B8C6" stroke-width="10" stroke-linecap="round" opacity=".8"/>'
        '<circle cx="124" cy="-58" r="6" fill="#222"/><circle cx="126" cy="-60" r="2" fill="#fff"/>'
        '<circle cx="134" cy="-32" r="9" fill="#F2B8C6" opacity=".8"/>'
        '<path d="M118 -20 Q126 -12 136 -18" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>'
        "</g>"
    )


def tree_with_bird(x, y):
    return (
        f'<g transform="translate({x} {y})">'
        '<path d="M120 400 L130 -40 L170 -40 L190 400Z" fill="#7A4E2D"/>'
        '<path d="M140 60 Q40 50 -120 70" fill="none" stroke="#7A4E2D" stroke-width="22" stroke-linecap="round"/>'
        '<circle cx="150" cy="-60" r="90" fill="#E07A2E" opacity=".9"/><circle cx="60" cy="-30" r="60" fill="#F2A541" opacity=".9"/>'
        '<g transform="translate(-50 -22) scale(1.5)">'
        '<ellipse cx="0" cy="0" rx="46" ry="40" fill="#4A90E2" stroke="#2A5E9E" stroke-width="4"/>'
        '<ellipse cx="8" cy="12" rx="26" ry="22" fill="#BFDDF7"/>'
        '<path d="M-30 -4 Q-60 10 -40 30 Q-20 20 -14 6Z" fill="#3A78C2"/>'
        '<circle cx="18" cy="-14" r="5" fill="#222"/><circle cx="20" cy="-16" r="1.8" fill="#fff"/>'
        '<polygon points="40,-10 66,-2 40,6" fill="#F59E0B" stroke="#C47A06" stroke-width="2"/>'
        '<path d="M62 -2 C74 10 60 20 72 30 C80 38 70 46 76 52" fill="none" stroke="#F28AA0" stroke-width="7" stroke-linecap="round"/>'
        '<path d="M-6 38 V54 M8 38 V54" stroke="#C47A06" stroke-width="4"/>'
        "</g></g>"
    )


def big_leaf(x, y):
    return (
        f'<g transform="translate({x} {y})">'
        '<path d="M-170 0 Q-60 -120 170 -20 Q60 70 -170 0Z" fill="#9C6B3A" stroke="#6E4824" stroke-width="5"/>'
        '<path d="M-160 0 Q0 -30 160 -20" fill="none" stroke="#6E4824" stroke-width="4"/>'
        '<path d="M-60 -10 L-30 -50 M10 -18 L40 -56 M70 -20 L100 -48 M-40 -6 L-10 26 M30 -14 L60 22" stroke="#6E4824" stroke-width="3"/>'
        "</g>"
    )


def leaf_pile(x, y):
    spots = [(-150, 10, 20), (-100, -10, -40), (-40, 20, 70), (30, -8, 10), (90, 14, -60),
             (150, 0, 40), (-120, 30, 100), (0, 30, -20), (120, 34, 80), (-70, 40, 15), (60, 40, -100)]
    colors = ["#E4572E", "#F3A712", "#C0392B", "#E9C46A", "#D9822B", "#9C6B3A"]
    return "".join(leaf(x + dx, y + dy, r, colors[i % len(colors)], 1.6) for i, (dx, dy, r) in enumerate(spots))


def heart(x, y, s=1.0, color="#FF6B81"):
    return (f'<path transform="translate({x} {y}) scale({s})" '
            f'd="M0 10 C-24 -8 -14 -28 0 -16 C14 -28 24 -8 0 10Z" fill="{color}"/>')


def sparkles(spots):
    return "".join(
        f'<path transform="translate({x} {y})" d="M0 -12 L3 -3 L12 0 L3 3 L0 12 L-3 3 L-12 0 L-3 -3Z" fill="#FFE066" stroke="#E0A800" stroke-width="1.5"/>'
        for x, y in spots
    )


def grumble(x, y):
    return (f'<path d="M{x} {y} q8 -10 16 0 t16 0 t16 0" fill="none" stroke="#8B4513" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M{x + 6} {y + 16} q8 -10 16 0 t16 0" fill="none" stroke="#8B4513" stroke-width="3" stroke-linecap="round"/>')


PAGES = {
    "01": ("fall", flower(470, 250, 1.4, "smile", 230) + bee(300, 180, 1.3, "happy")
           + heart(390, 110, 1.4) + falling_leaves([(90, 120, 20), (700, 260, -30), (150, 360, 60)])),
    "02": ("fall", flight_path("M60 330 Q200 160 330 260 T560 220")
           + bee(600, 210, 1.3, "happy") + falling_leaves([(120, 120, 20), (300, 90, -30), (720, 330, 50), (470, 380, 10)])
           + dry_stem(140, 480, 120, 20) + dry_stem(700, 470, 110, -25)),
    "03": ("fall", dry_stem(150, 490, 150, 30) + dry_stem(260, 480, 130, -20) + dry_stem(560, 480, 140, 35)
           + dry_stem(680, 490, 120, -30)
           + falling_leaves([(100, 100, 30), (220, 220, -40), (360, 80, 60), (620, 140, -10), (720, 250, 45), (470, 60, 15), (520, 300, -60)])
           + bee(400, 260, 1.5, "sad", hold_tummy=True) + grumble(370, 340)),
    "04": ("fall", squirrel(540, 360) + bee(220, 220, 1.2, "wow")
           + leaf(440, 470, 30, "#9C6B3A", 1.4) + leaf(640, 480, -20, "#E4572E", 1.4)),
    "05": ("fall", tree_with_bird(500, 200) + bee(180, 230, 1.2, "wow")),
    "06": ("fall", baby_elephant(470, 380) + bee(170, 200, 1.2, "wow")
           + leaf(330, 500, 30, "#9C6B3A", 1.4) + falling_leaves([(120, 380, 20), (700, 120, -30), (360, 90, 60)])),
    "07": ("fall", big_leaf(400, 470) + bee(400, 395, 1.4, "sad")
           + falling_leaves([(120, 100, 20), (690, 140, -30), (240, 220, 60), (600, 260, 30)])),
    "08": ("fall", leaf_pile(420, 470) + flower(430, 330, 1.0, "talk", 150) + leaf_pile(430, 500)
           + bee(270, 140, 1.2, "wow")),
    "09": ("fall", flower(400, 260, 1.5, "smile", 230) + bee(400, 175, 1.1, "yum", pollen=True)
           + sparkles([(260, 140), (540, 120), (300, 300), (520, 310)])),
    "10": ("fall", flower(480, 250, 1.4, "talk", 230) + bee(270, 230, 1.2, "happy", pollen=True)
           + heart(380, 130, 1.6)),
    "11": ("fall", flower(140, 300, 0.9, None, 180) + flower(400, 330, 0.9, None, 160) + flower(660, 290, 0.9, None, 190)
           + flight_path("M140 250 Q270 120 400 280 T660 240")
           + bee(540, 150, 1.0, "happy", pollen=True)),
    "12": ("spring", "".join(flower(x, y, s, "smile", h) for x, y, s, h in
                               [(90, 400, .6, 140), (210, 360, .75, 180), (340, 410, .6, 140), (470, 370, .8, 170),
                                (600, 410, .6, 140), (720, 370, .75, 180), (150, 470, .5, 120), (400, 480, .5, 110), (650, 480, .5, 110)])
           + bee(400, 170, 1.2, "happy") + heart(300, 120) + heart(500, 110)),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (season, body) in PAGES.items():
        # Seed by page number so each page gets its own scenery but reruns are stable.
        rng = random.Random(int(name))
        spring = season == "spring"
        bg = (spring_bg(rng, name) if spring else fall_bg(rng, name)) + scenery_front(rng, spring)
        with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
            f.write(page(body, bg))
    print(f"wrote {len(PAGES)} pages to {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
