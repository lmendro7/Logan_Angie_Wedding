"""Style-mix round 1: our own character style, mixing Stardew-like traits.

    python3 tools/sprites/style_mix.py

Lucas (November 8, 2026): "make our own style of characters ... mixing
Stardew art styles till we get one we like". Logan (white shirt, bow tie) is
drawn larger than the 16 x 24 sprites so he is less blocky, in two body
shapes, each with six treatments that vary one trait family at a time:
outline, shading depth, eyes, blush, colour warmth. All pixels are original.
Writes docs/art/style-mix/round-1.png.
"""
import colorsys
import sys
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from styles import font                    # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'docs' / 'art' / 'style-mix'

PAL = {
    'x': '#2a1d1b',
    'h': '#5a4330', 'H': '#8a6a4c', 'J': '#ae8c66', 'L': '#ccb088',
    'S': '#f6d2ad', 's': '#e4b08a', 'r': '#cf9373', 'p': '#f0a9a0',
    'w': '#ffffff', 'i': '#7a5a3c', 'E': '#2b1d16', 'B': '#5a4330',
    'b': '#94603a', 'c': '#6e4428', 'd': '#b07a4c',
    'W': '#fbfaf6', 'V': '#dcd8cf', 'U': '#bdb7ab', 'X': '#18181d',
    'N': '#30313a', 'n': '#22232a', 'K': '#3b2a20', 'Y': '#d1aa4c', 'O': '#1c1c21', 'o': '#3c3c46',
}

# Classic proportions, 24 x 48: head about 40% of the height.
CLASSIC = [
    "........xxxxxxxx........",
    "......xxJLLJJHHHxx......",
    ".....xHJLLLJJHHHHHx.....",
    "....xHHJJLJJHHHHhHHx....",
    "....xHHHJJHHHHhHHhHx....",
    "...xhHHHHHHHHhHHHhHHx...",
    "...xhhHHHHHhHHHHhhHhx...",
    "...xhhhSSSSSSSSSShhhx...",
    "...xhhSSSSSSSSSSSShhx...",
    "...xhsSBBBSSSSBBBSshx...",
    "...xsSSwiiSSSSiiwSSsx...",
    "...xsSSwEiSSSSiEwSSsx...",
    "...xsSSSSSSrrSSSSSSsx...",
    "...xspSSSSSrrSSSSSpsx...",
    "...xcdSSSSSSSSSSSSdcx...",
    "...xcbdSSSSSSSSSSdbcx...",
    "....xcbbbbdrrdbbbbcx....",
    "....xccbbbbbbbbbbccx....",
    ".....xccbbbbbbbbccx.....",
    "......xxccbbbbccxx......",
    "........xsSSSSsx........",
    "...xVWWWWWWXXWWWWWWVx...",
    "..xVWWWWWXXXXXXWWWWWVx..",
    "..xVWWWWWWXXXXWWWWWWVx..",
    "..xVWWxWWWWVVWWWWxWWVx..",
    "..xVWWxWWWWWVWWWWxWWVx..",
    "..xVWUxWWWWWVWWWWxUWVx..",
    "..xVWUxVWWWWVWWWVxUWVx..",
    "..xVWUxVWWWWVWWWVxUWVx..",
    "..xVWUxVWWWWVWWWVxUWVx..",
    "..xVVUxVWWWWVWWWVxUVVx..",
    "..xsSSxVWWWWVWWWVxSSsx..",
    "..xsSSxVVWWWVWWVVxSSsx..",
    "..xxssxKKKKKYKKKKxssxx..",
    "...xxxxNNNNNNNNNNxxxx...",
    "......xNNNNNNNNNNx......",
    "......xNNNNNnNNNNx......",
    "......xNNNNxxNNNNx......",
    "......xNNNnxxnNNNx......",
    "......xNNNnxxnNNNx......",
    "......xNNNnxxnNNNx......",
    "......xNNNnxxnNNNx......",
    "......xNNNnxxnNNNx......",
    "......xNNNnxxnNNNx......",
    ".....xOOOOoxxoOOOOx.....",
    ".....xOOOOOxxOOOOOx.....",
    ".....xxxxxxxxxxxxxx.....",
    "........................",
]
# Rounder: same head, shorter body (24 x 40).
ROUNDER = CLASSIC[:21] + [CLASSIC[n] for n in (21, 22, 23, 24, 26, 28, 30, 31, 33)] + \
          [CLASSIC[n] for n in (34, 35, 37, 38, 40, 44, 45, 46)] + [CLASSIC[47], CLASSIC[47]]


def render(rows, opts):
    merge = {}
    if opts.get('tones') == 3:
        merge = {'L': 'J', 'U': 'V', 'd': 'b'}
    elif opts.get('tones') == 2:
        merge = {'L': 'H', 'J': 'H', 'h': 'H', 'U': 'V', 'd': 'b', 'c': 'b', 'r': 's', 'n': 'N', 'o': 'O'}
    if opts.get('eyes') == 'dots':
        merge.update({'w': 'S', 'i': 'E'})
    if not opts.get('blush', True):
        merge['p'] = 'S'
    pal = dict(PAL)
    if opts.get('warm'):
        for k, v in pal.items():
            r, g, b = ImageColor.getrgb(v)
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            r2, g2, b2 = colorsys.hls_to_rgb((h - 0.012) % 1, l, min(1, s * 1.15))
            pal[k] = '#%02x%02x%02x' % (min(255, int(r2 * 255 + 8)), int(g2 * 255), max(0, int(b2 * 255 - 10)))
    w, h = len(rows[0]), len(rows)
    img = Image.new('RGBA', (w, h))
    px = img.load()
    for y, row in enumerate(rows):
        assert len(row) == w, (y, row, len(row))
        for x, ch in enumerate(row):
            if ch == '.':
                continue
            ch = merge.get(ch, ch)
            if ch == 'x':
                continue
            px[x, y] = ImageColor.getrgb(pal[ch]) + (255,)
    mode = opts.get('outline', 'tinted')
    if mode != 'none':
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != 'x':
                    continue
                if mode == 'black':
                    px[x, y] = (24, 20, 20, 255)
                    continue
                nbs = [px[xx, yy] for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                       if 0 <= xx < w and 0 <= yy < h and px[xx, yy][3]]
                if nbs:
                    r, g, b = (sum(n[i] for n in nbs) // len(nbs) for i in range(3))
                    k = .42 if mode == 'tinted' else .62
                    px[x, y] = (int(r * k), int(g * k * .92), int(b * k * .9), 255)
                else:
                    px[x, y] = (42, 29, 27, 255)
        if mode == 'outer':                 # soft look: drop inner lines, keep the silhouette
            for y, row in enumerate(rows):
                for x, ch in enumerate(row):
                    if ch != 'x':
                        continue
                    touches_outside = any(not (0 <= xx < w and 0 <= yy < h) or rows[yy][xx] == '.'
                                          for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
                    if not touches_outside:
                        nbs = [px[xx, yy] for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                               if rows[yy][xx] not in '.x']
                        if nbs:
                            r, g, b = (sum(n[i] for n in nbs) // len(nbs) for i in range(3))
                            px[x, y] = (int(r * .8), int(g * .78), int(b * .78), 255)
    return img


TREATMENTS = [
    ('1', 'Full mix', 'tinted outline, 4 tones, eye whites, blush', {}),
    ('2', 'Bold outline', 'black outline, 4 tones, eye whites', {'outline': 'black', 'blush': False}),
    ('3', 'Soft', 'edge outline only, 3 tones, dot eyes', {'outline': 'outer', 'tones': 3, 'eyes': 'dots'}),
    ('4', 'Simple', 'tinted outline, 2 tones, dots', {'tones': 2, 'eyes': 'dots', 'blush': False}),
    ('5', 'Painterly', 'no outline, full shading', {'outline': 'none'}),
    ('6', 'Golden hour', 'warm colours, tinted outline, blush', {'warm': True}),
]
BASES = [('A', 'Classic 24 × 48', CLASSIC), ('B', 'Rounder 24 × 40', ROUNDER)]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    k, cw = 5, 250
    board = Image.new('RGBA', (60 + 6 * cw, 150 + 2 * 420), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Our own style — round 1', font=font(40), fill=INK)
    d.text((40, 86), 'Two body shapes (A, B) × six treatments (1–6). Name a pick like "A3", or mix: '
                     '"A1 with 3\'s eyes". Small figure = true size at 2×.', font=font(18, False), fill=MUTED)
    for bi, (bl, bname, rows) in enumerate(BASES):
        y0 = 150 + bi * 420
        d.text((40, y0), f'{bl} · {bname}', font=font(24), fill=INK)
        for ti, (tl, tname, blurb, opts) in enumerate(TREATMENTS):
            img = render(rows, opts)
            x0 = 40 + ti * cw
            d.text((x0, y0 + 36), f'{bl}{tl} · {tname}', font=font(17), fill=INK)
            d.text((x0, y0 + 60), blurb, font=font(11, False), fill=MUTED)
            panel = Image.new('RGBA', (cw - 14, 300), '#97b779')
            big = img.resize((img.width * k, img.height * k), Image.NEAREST)
            panel.alpha_composite(big, (12, 300 - 10 - big.height))
            small = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
            panel.alpha_composite(small, (cw - 14 - small.width - 12, 300 - 10 - small.height))
            board.alpha_composite(panel, (x0, y0 + 82))
    board.convert('RGB').save(OUT / 'round-1.png', optimize=True)


if __name__ == '__main__':
    main()
