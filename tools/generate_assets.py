#!/usr/bin/env python3
"""Generates the pixel-art SVGs used by README.md.

No fonts, no external services: letters are drawn from a 5x7 bitmap font.
Edit the texts or colors below, run `python tools/generate_assets.py`, commit assets/.
"""
import os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

FONT = {
"A": ".###.|#...#|#...#|#####|#...#|#...#|#...#", "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
"C": ".###.|#...#|#....|#....|#....|#...#|.###.", "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
"E": "#####|#....|#....|####.|#....|#....|#####", "F": "#####|#....|#....|####.|#....|#....|#....",
"G": ".###.|#...#|#....|#.###|#...#|#...#|.###.", "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
"I": ".###.|..#..|..#..|..#..|..#..|..#..|.###.", "J": "..###|...#.|...#.|...#.|...#.|#..#.|.##..",
"K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#", "L": "#....|#....|#....|#....|#....|#....|#####",
"M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#", "N": "#...#|##..#|#.#.#|#..##|#...#|#...#|#...#",
"O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.", "P": "####.|#...#|#...#|####.|#....|#....|#....",
"Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#", "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
"S": ".####|#....|#....|.###.|....#|....#|####.", "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
"U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.", "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
"W": "#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#", "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
"Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..", "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
" ": ".....|.....|.....|.....|.....|.....|.....", "&": ".##..|#..#.|#.#..|.#...|#.#.#|#..#.|.##.#",
"'": "..#..|..#..|.#...|.....|.....|.....|.....", ">": "#....|.#...|..#..|...#.|..#..|.#...|#....",
"-": ".....|.....|.....|.###.|.....|.....|.....", ".": ".....|.....|.....|.....|.....|.##..|.##..",
}
GLYPHS = {k: v.split("|") for k, v in FONT.items()}
assert all(len(g) == 7 and all(len(r) == 5 for r in g) for g in GLYPHS.values())

BG, PANEL, BORDER, MUTED = "#0f0f1b", "#1a1c2c", "#566c86", "#a7b3c6"
YELLOW, CYAN, GREEN, TEAL, RED = "#ffcd75", "#41a6f6", "#38b764", "#257179", "#b13e53"
PALETTE = {"H": RED, "h": "#5d275d", "S": YELLOW, "E": BG, "B": CYAN, "b": "#3b5dc9", "W": "#f4f4f4"}
SPRITE = [
".......HH.......", "......HHHH......", ".....HHHHHH.....", "....HHHhHHHH....",
"...HHHHHHHHHH...", "..hhhhhhhhhhhh..", "....SSSSSSSS....", "....SEESSEES....",
"....SSSSSSSS....", ".....SSWWSS.....", "....BBBBBBBB....", "...BBBBBbBBBB...",
"..SBBBBBbBBBBS..", "...BBBBBbBBBB...", "...bbbbbbbbbb...", "....bb....bb....",
]

def text(s, x, y, scale, fill):
    d, cx = [], x
    for ch in s:
        for r, row in enumerate(GLYPHS[ch]):
            c = 0
            while c < 5:
                if row[c] == "#":
                    a = c
                    while c < 5 and row[c] == "#":
                        c += 1
                    d.append(f"M{cx + a * scale} {y + r * scale}h{(c - a) * scale}v{scale}h-{(c - a) * scale}z")
                else:
                    c += 1
        cx += 6 * scale
    return f'<path fill="{fill}" d="{"".join(d)}"/>'

def width(s, scale):
    return len(s) * 6 * scale - scale

def rect(x, y, w, h, fill):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'

def frame(w, h, fill):
    return rect(0, 0, w, h, BORDER) + rect(4, 4, w - 8, h - 8, fill)

def svg(w, h, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{title}" shape-rendering="crispEdges"><title>{title}</title>{body}</svg>\n')

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

def banner():
    w, h = 880, 260
    b = frame(w, h, BG)
    rnd, stars = random.Random(7), []
    while len(stars) < 26:
        x, y, s = rnd.randrange(600, 860, 4), rnd.randrange(16, 210, 4), rnd.choice([4, 4, 8])
        if not (660 < x < 860 and 52 < y < 226):
            stars.append(rect(x, y, s, s, rnd.choice(["#333c57", BORDER, MUTED])))
    b += "".join(stars)
    b += text("FULLSTACK", 40, 36, 8, YELLOW) + text("WEB DEVELOPER", 40, 108, 6, CYAN)
    b += text("SOFTWARE HOUSES & REMOTE TEAMS", 40, 176, 3, MUTED)
    b += rect(4, 224, w - 8, 4, GREEN) + rect(4, 228, w - 8, h - 232, TEAL)
    for r, row in enumerate(SPRITE):
        c = 0
        while c < 16:
            if row[c] != ".":
                a, ch = c, row[c]
                while c < 16 and row[c] == ch:
                    c += 1
                b += rect(690 + a * 10, 64 + r * 10, (c - a) * 10, 10, PALETTE[ch])
            else:
                c += 1
    save("banner.svg", svg(w, h, "Fullstack web developer for software houses and remote teams", b))

def header(name, label, color):
    w, h = 880, 56
    b = frame(w, h, PANEL) + rect(20, 20, 16, 16, color) + text(label, 52, 14, 4, YELLOW)
    for i, c in enumerate([RED, YELLOW, GREEN, CYAN]):
        b += rect(w - 28 - i * 16, 24, 8, 8, c)
    save(name, svg(w, h, label.title(), b))

def status(name, label, color):
    w, h = 280, 40
    b = frame(w, h, BG) + rect(14, 12, 16, 16, color) + rect(18, 16, 8, 8, "#f4f4f4")
    b += text(label, 44, 13, 2, color)
    save(name, svg(w, h, label.title(), b))

def button(name, label):
    w, h = 268, 52
    b = rect(6, 6, w, h, "#000000") + rect(0, 0, w, h, YELLOW)
    b += text(label, (w - width(label, 3)) // 2, 15, 3, BG)
    save(name, svg(w + 6, h + 6, label.title(), b))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner()
    status("status-open.svg", "OPEN FOR PROJECTS", GREEN)
    status("status-busy.svg", "FULLY BOOKED", YELLOW)
    button("btn-email.svg", "> EMAIL ME")
    for fn, label, col in [("h-what-i-do.svg", "WHAT I DO", CYAN), ("h-tech-stack.svg", "TECH STACK", GREEN),
                           ("h-case-studies.svg", "CASE STUDIES", YELLOW), ("h-why-trust.svg", "WHY TRUST ME", RED),
                           ("h-latest.svg", "LATEST ACTIVITY", CYAN), ("h-lets-build.svg", "LET'S BUILD", GREEN)]:
        header(fn, label, col)
    print("assets generated in", os.path.normpath(OUT))
