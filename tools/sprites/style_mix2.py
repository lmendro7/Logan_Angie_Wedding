"""Style-mix round 2: simple, comforting Stardew x Pokémon characters.

    python3 tools/sprites/style_mix2.py

Lucas (November 8, 2026): round 1 was not what he imagined; he likes
Stardew's simple, comforting designs, mixed with Pokémon. So: rounded heads,
soft outlines, gentle 2-3 tone shading, simple faces with blush (Stardew),
and chibi proportions, clean colours and shiny eyes (Pokémon). All original.
Writes docs/art/style-mix/round-2.png.
"""
import sys
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from styles import font                    # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'docs' / 'art' / 'style-mix'

# Logan, 16 x 32, Stardew-like proportions with a rounded head.
BASE = [
    "................",
    ".....xxxxxx.....",
    "....xHHJJHHx....",
    "...xHHJJJJHHx...",
    "..xHHHHHHHHHHx..",
    "..xHHHHHHHHHHx..",
    "..xhHSSSSSSHhx..",
    "..xhSSSSSSSShx..",
    "..xsSESSSSESsx..",
    "..xsSESSSSESsx..",
    "..xspSSSSSSpsx..",
    "..xcbSSSSSSbcx..",
    "...xbbSSSSbbx...",
    "....xbbbbbbx....",
    ".....xxSSxx.....",
    "...xWWWXXWWWx...",
    "..xVWWWWWWWWVx..",
    "..xVWWWWWWWWVx..",
    "..xVWWWWWWWWVx..",
    "..xVWWWWWWWWVx..",
    "..xVWWWWWWWWVx..",
    "..xsVWWWWWWVsx..",
    "..xxKKKKYKKKxx..",
    "...xNNNNNNNNx...",
    "...xNNNNNNNNx...",
    "...xNNNxxNNNx...",
    "...xNNnxxnNNx...",
    "...xNNnxxnNNx...",
    "...xNNnxxnNNx...",
    "..xOOOoxxoOOOx..",
    "..xxxxxxxxxxxx..",
    "................",
]
SHINE_EYES = {8: "..xsSwESSwESsx..", 9: "..xsSEESSEESsx.."}
BIG_HEAD = {4: ".xHHHHHHHHHHHHx.", 5: ".xHHHHHHHHHHHHx.", 6: ".xhHSSSSSSSSHhx.", 7: ".xhSSSSSSSSSShx.",
            8: ".xsSSESSSSESSsx.", 9: ".xsSSESSSSESSsx.", 10: ".xspSSSSSSSSpsx.", 11: ".xcbSSSSSSSSbcx.",
            12: "..xbbSSSSSSbbx..", 13: "...xbbbbbbbbx..."}
BIG_HEAD_SHINE = {8: ".xsSwESSSSwESsx.", 9: ".xsSEESSSSEESsx."}

SOFT = {   # Stardew-like: warm, gentle, soft brown outline
    'x': '#4a3328', 'h': '#7a5a3e', 'H': '#9a7350', 'J': '#bd9670',
    'S': '#f7d6b5', 's': '#e8b893', 'p': '#f2aeae', 'E': '#3a2a22', 'w': '#ffffff',
    'b': '#9a6a42', 'c': '#7c5232',
    'W': '#fbf8f1', 'V': '#e0d8c9', 'X': '#2b2a33', 'K': '#5a3e2c', 'Y': '#e3c06a',
    'N': '#3d3d4c', 'n': '#2e2e3a', 'O': '#3a2e2a', 'o': '#5a4a44',
}
BRIGHT = {**SOFT,   # Pokémon-like: cleaner, brighter, bolder outline
    'x': '#2e2220', 'h': '#6e4e30', 'H': '#94693f', 'J': '#c49660',
    'S': '#ffd9b3', 's': '#f0b48c', 'p': '#ff9e9e',
    'W': '#ffffff', 'V': '#d6dce8', 'N': '#2f3650', 'n': '#232840', 'O': '#262a36', 'o': '#454b5c'}


def build(rows, swaps=(), drop=()):
    out = list(rows)
    for sw in swaps:
        for n, r in sw.items():
            out[n] = r
    return [r for n, r in enumerate(out) if n not in drop]


def render(rows, pal, tinted=False):
    w, h = len(rows[0]), len(rows)
    img = Image.new('RGBA', (w, h))
    px = img.load()
    for y, row in enumerate(rows):
        assert len(row) == w, (y, row)
        for x, ch in enumerate(row):
            if ch not in '.x':
                px[x, y] = ImageColor.getrgb(pal[ch]) + (255,)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != 'x':
                continue
            if tinted:
                nbs = [px[xx, yy] for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                       if 0 <= xx < w and 0 <= yy < h and px[xx, yy][3]]
                if nbs:
                    r, g, b = (sum(n[i] for n in nbs) // len(nbs) for i in range(3))
                    px[x, y] = (int(r * .55), int(g * .48), int(b * .46), 255)
                    continue
            px[x, y] = ImageColor.getrgb(pal['x']) + (255,)
    return img


SHORT_BODY = (17, 19, 24, 27)            # 16 x 28: chibi, Pokémon-like
VARIANTS = [
    ('1', 'Stardew comfort', '16 × 32 · soft brown outline, dot eyes, blush', build(BASE), SOFT, False),
    ('2', 'Pokémon comfort', '16 × 28 · chibi body, brighter colours, shiny eyes', build(BASE, [SHINE_EYES], SHORT_BODY), BRIGHT, False),
    ('3', 'Even mix', '16 × 28 · chibi body, soft colours, shiny eyes', build(BASE, [SHINE_EYES], SHORT_BODY), SOFT, False),
    ('4', 'Extra soft', '16 × 32 · outline tinted to each colour', build(BASE), SOFT, True),
    ('5', 'Big round head', '16 × 28 · wider head, chibi body, shiny eyes', build(BASE, [BIG_HEAD, BIG_HEAD_SHINE], SHORT_BODY), SOFT, False),
    ('6', 'Big head, bright', '16 × 28 · wider head, Pokémon colours', build(BASE, [BIG_HEAD, BIG_HEAD_SHINE], SHORT_BODY), BRIGHT, False),
]


def scene(sprite, scale):
    """A small patch of garden so the style is judged in context."""
    w, h = 60, 46
    img = Image.new('RGBA', (w, h), '#97b779')
    d = ImageDraw.Draw(img)
    d.rectangle([0, 30, w, 38], fill='#d9bd87')
    for x, y in ((6, 6), (40, 10), (50, 24), (12, 40), (30, 4)):
        d.rectangle([x, y, x + 1, y], fill='#88aa70')
    for x in (44, 48, 52):
        d.rectangle([x, 14, x + 1, 15], fill='#eac4a4'); d.rectangle([x, 16, x, 18], fill='#648555')
    d.ellipse([22, 34, 34, 37], fill=(38, 60, 48, 80))
    img.alpha_composite(sprite, (20, 36 - sprite.height + 1))
    return img.resize((w * scale, h * scale), Image.NEAREST)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    cw = 300
    board = Image.new('RGBA', (60 + 3 * cw * 2 // 1 - 280, 150 + 2 * 470), BG)
    board = Image.new('RGBA', (40 + 3 * 520, 150 + 2 * 470), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Our own style — round 2: simple and comforting', font=font(38), fill=INK)
    d.text((40, 84), 'Stardew\'s soft, cosy look mixed with Pokémon\'s chibi shapes and clean colours. '
                     'Left: enlarged. Right: in a patch of garden at phone size.', font=font(18, False), fill=MUTED)
    for i, (num, name, blurb, rows, pal, tinted) in enumerate(VARIANTS):
        img = render(rows, pal, tinted)
        x0, y0 = 40 + (i % 3) * 520, 150 + (i // 3) * 470
        d.text((x0, y0), f'{num} · {name}', font=font(22), fill=INK)
        d.text((x0, y0 + 30), blurb, font=font(14, False), fill=MUTED)
        panel = Image.new('RGBA', (180, 360), '#97b779')
        big = img.resize((img.width * 10, img.height * 10), Image.NEAREST)
        panel.alpha_composite(big, (10, 360 - 12 - big.height))
        board.alpha_composite(panel, (x0, y0 + 60))
        board.alpha_composite(scene(img, 5), (x0 + 195, y0 + 60))
    board.convert('RGB').save(OUT / 'round-2.png', optimize=True)


if __name__ == '__main__':
    main()
