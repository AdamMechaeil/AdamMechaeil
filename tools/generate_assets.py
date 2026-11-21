"""Generates the terminal-style SVGs in ../assets (dark + light variants).

Run from anywhere:  python tools/generate_assets.py
Edit THEMES for colors, BARS for section prompts, phrases in banner() for the typing lines.
"""
import os
from xml.sax.saxutils import escape

OUT = r"D:\Study\Projects\github-readme\AdamMechaeil\assets"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0E1210", edge="#3E6B4F", green="#6A9A78", silver="#C3C8CE",
                 gold="#C9A24B", dim="#7C8A81", name="#C3C8CE", dot2="#C3C8CE", dot2o="0.6"),
    "light": dict(bg="#F4F6F2", edge="#2F5D44", green="#2F5D44", silver="#1F2A23",
                  gold="#9A7420", dim="#5E6B63", name="#1F2A23", dot2="#5E6B63", dot2o="0.7"),
}
MONO = "Consolas,'SFMono-Regular','Courier New',monospace"
SANS = "'Segoe UI',Helvetica,Arial,sans-serif"
W = 900


def banner(th, c):
    H, FS, CW, X0, Y = 260, 22, 13.2, 60, 188
    phrases = ["Full Stack Engineer", "Building production-grade web platforms",
               "Trainer: 500+ students taught", "Open to roles overseas"]
    TYPE_DT, HOLD, ERASE_DT, GAP = 0.07, 1.6, 0.03, 0.4
    segs, t = [], 0.0
    for p in phrases:
        n = len(p)
        s = t
        he = s + n * TYPE_DT + HOLD
        ee = he + n * ERASE_DT
        segs.append((p, s, he, ee))
        t = ee + GAP
    TOTAL = round(t, 3)

    def frames(p, s, he):
        n = len(p)
        pts = [(0.0, 0)] + [(s + k * TYPE_DT, k) for k in range(1, n + 1)]
        pts += [(he + k * ERASE_DT, n - k) for k in range(1, n + 1)]
        return [(min(a, TOTAL), b) for a, b in pts] + [(TOTAL, 0)]

    def anim(attr, fr, conv):
        kt = ";".join(f"{min(a / TOTAL, 1):.5f}" for a, _ in fr)
        vals = ";".join(conv(b) for _, b in fr)
        return (f'<animate attributeName="{attr}" dur="{TOTAL}s" repeatCount="indefinite" '
                f'calcMode="discrete" keyTimes="{kt}" values="{vals}"/>')

    defs, body = [], []
    for i, (p, s, he, ee) in enumerate(segs):
        fr = frames(p, s, he)
        defs.append(f'<clipPath id="c{i}"><rect x="{X0}" y="{Y-30}" height="44" width="0">'
                    f'{anim("width", fr, lambda k: f"{k*CW:.1f}")}</rect></clipPath>')
        body.append(f'<text x="{X0}" y="{Y}" font-family="{MONO}" font-size="{FS}" fill="{c["silver"]}" '
                    f'clip-path="url(#c{i})" xml:space="preserve">{escape(p)}</text>')
        op = [(0.0, 0), (s, 1), (ee, 0), (TOTAL, 0)]
        body.append(
            f'<rect y="{Y-22}" width="10" height="26" fill="{c["gold"]}" x="{X0}" opacity="0">'
            f'{anim("x", fr, lambda k: f"{X0+k*CW:.1f}")}'
            f'<animate attributeName="opacity" dur="{TOTAL}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(f"{a/TOTAL:.5f}" for a, _ in op)}" values="{";".join(str(v) for _, v in op)}"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Adam Mechaeil, Full Stack Engineer">
<defs><linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{c['edge']}"/><stop offset="0.6" stop-color="{c['gold']}"/><stop offset="1" stop-color="{c['edge']}" stop-opacity="0"/></linearGradient>{"".join(defs)}</defs>
<rect width="{W}" height="{H}" rx="14" fill="{c['bg']}"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="none" stroke="{c['edge']}" stroke-width="2"/>
<circle cx="34" cy="34" r="5" fill="{c['green']}"/><circle cx="54" cy="34" r="5" fill="{c['dot2']}" opacity="{c['dot2o']}"/><circle cx="74" cy="34" r="5" fill="{c['gold']}"/>
<text x="{W/2}" y="39" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c['dim']}">zsh — 80x24</text>
<text x="{W-40}" y="39" text-anchor="end" font-family="{MONO}" font-size="14" fill="{c['dim']}">~/adam-mechaeil</text>
<text x="{X0}" y="112" font-family="{SANS}" font-size="52" font-weight="700" letter-spacing="4" fill="{c['name']}">ADAM MECHAEIL</text>
<rect x="{X0}" y="128" width="180" height="3" rx="1.5" fill="url(#line)"/>
<text x="{X0-28}" y="{Y}" font-family="{MONO}" font-size="{FS}" fill="{c['green']}">&gt;</text>
{"".join(body)}
</svg>
'''


def bar(cmd, c):
    H = 42
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(cmd)}">
<rect width="{W}" height="{H}" rx="8" fill="{c['bg']}"/>
<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="7.5" fill="none" stroke="{c['edge']}" stroke-width="1.5"/>
<circle cx="22" cy="21" r="4.5" fill="{c['green']}"/><circle cx="40" cy="21" r="4.5" fill="{c['dot2']}" opacity="{c['dot2o']}"/><circle cx="58" cy="21" r="4.5" fill="{c['gold']}"/>
<text x="84" y="27" font-family="{MONO}" font-size="17" xml:space="preserve"><tspan fill="{c['green']}" font-weight="700">adam@dev</tspan><tspan fill="{c['dim']}">:</tspan><tspan fill="{c['gold']}">~</tspan><tspan fill="{c['dim']}">$ </tspan><tspan fill="{c['silver']}">{escape(cmd)}</tspan></text>
<text x="{W-20}" y="26" text-anchor="end" font-family="{MONO}" font-size="14" fill="{c['dim']}"><tspan fill="{c['green']}">&#10003;</tspan> exit 0 · zsh</text>
</svg>
'''


def divider(c):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="6" viewBox="0 0 {W} 6"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{c['edge']}" stop-opacity="0"/><stop offset="0.3" stop-color="{c['edge']}"/><stop offset="0.5" stop-color="{c['gold']}"/><stop offset="0.7" stop-color="{c['edge']}"/><stop offset="1" stop-color="{c['edge']}" stop-opacity="0"/></linearGradient></defs><rect y="2" width="{W}" height="2" rx="1" fill="url(#g)"/></svg>
'''


def footer(c):
    H = 42
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="adam@dev prompt">
<rect width="{W}" height="{H}" rx="8" fill="{c['bg']}"/>
<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="7.5" fill="none" stroke="{c['edge']}" stroke-width="1.5"/>
<text x="24" y="27" font-family="{MONO}" font-size="17" xml:space="preserve"><tspan fill="{c['green']}" font-weight="700">adam@dev</tspan><tspan fill="{c['dim']}">:</tspan><tspan fill="{c['gold']}">~</tspan><tspan fill="{c['dim']}">$ </tspan></text>
<rect x="186" y="12" width="10" height="20" fill="{c['gold']}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
<text x="{W-20}" y="26" text-anchor="end" font-family="{MONO}" font-size="14" fill="{c['dim']}">let's build something &#8629;</text>
</svg>
'''


BARS = {
    "about": "cat about.md",
    "open": "cat open_to.md",
    "exp": "cat experience.log",
    "own": "ls -l ./own-work",
    "stack": "cat stack.json",
    "now": "cat now.txt",
}

for th, c in THEMES.items():
    w = lambda name, s: open(os.path.join(OUT, f"{name}-{th}.svg"), "w", encoding="utf-8").write(s)
    w("banner", banner(th, c))
    w("divider", divider(c))
    w("footer", footer(c))
    for k, cmd in BARS.items():
        w(f"bar-{k}", bar(cmd, c))
print(sorted(os.listdir(OUT)))
