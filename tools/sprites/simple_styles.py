"""Draft Logan's simple map sprite in 24 styles so Lucas can pick one.

    python3 tools/sprites/simple_styles.py

Plan (Lucas, November 8, 2026): very simple sprites walk the map; the detailed
models appear beside the speaker's name in conversations. Logan's approved
model is the reference: short dirty-blond hair, short beard, white shirt and
black bow tie (his preferred look), black trousers and shoes.

Seven hand-drawn base figures (different sizes and proportions) are combined
with outline, shading and palette treatments. All art is original, in the
spirit of genres, not copied from any game.
Writes docs/art/simple-styles-01/logan-simple-styles.png.
"""
import colorsys
import sys
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from characters import FB_LEGS, LOGAN, SIDE_LEGS          # noqa: E402
from styles import BASE, STYLES, font                      # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs' / 'art' / 'simple-styles-01'

# ------------------------------------------------------------- base figures
RYANLIKE = {
    'front': LOGAN['front'][:13] + [
        "...VWWXXXXWWV...",
        "...VWWWWWWWWV...",
        "...VWWWWWWWWV...",
        "....VWWWWWWV....",
        "....VWWWWWWV....",
        "....VWWWWWWV....",
        "....VWWWWWWV....",
        "....VWWWWWWV....",
        "....SWWWWWWS....",
        ".....KKKYKK.....",
        ".....NNNNNN.....",
        ".....NNNNNN.....",
    ] + FB_LEGS[0],
    'side': LOGAN['side'][:13] + [
        "......VWWWX.....",
        "......VWWWX.....",
        "......VWWWW.....",
        "......WVVWW.....",
        "......WVVWW.....",
        "......WVVWW.....",
        "......WVVWW.....",
        "......WVVWW.....",
        "......WSSWW.....",
        "......KKKKY.....",
        "......NNNNN.....",
        "......NNNNN.....",
    ] + SIDE_LEGS[0],
}
CHIBI16 = {
    'front': [
        ".....xxxxxx.....",
        "...xxHHJJHHxx...",
        "..xHHJJJJHHHHx..",
        "..xHHHHHHHHHHx..",
        "..xhSSSSSSSShx..",
        "..xSSESSSSESSx..",
        "..xsbSSSSSSbsx..",
        "...xbbBBBBbbx...",
        "..xWWWWXXWWWWx..",
        ".xVWWWWWWWWWWVx.",
        ".xSWWWWWWWWWWSx.",
        "..xNKKKYKKKKNx..",
        "...xNNNxxNNNx...",
        "...xNNNxxNNNx...",
        "..xOOOOxxOOOOx..",
        "..xxxxxxxxxxxx..",
    ],
    'side': [
        "....xxxxxx......",
        "...xHHJJHHxx....",
        "..xHHHHJJJHHx...",
        "..xhHHHHHHHHHx..",
        "..xhhsSSSSSESx..",
        "..xhhsSSSSSESSx.",
        "...xhbbSSSbbx...",
        "....xbbbbbbx....",
        "....xWWWWXXx....",
        "....xVWWWWWx....",
        "....xVSSWWWx....",
        "....xKKKKKYx....",
        ".....xNNNNx.....",
        ".....xNNNNx.....",
        "....xOOOOOOx....",
        "....xxxxxxxx....",
    ],
}
MICRO = {
    'front': [
        "....hHHh....",
        "...hHJJHh...",
        "..hHHHHHHh..",
        "..hSSSSSSh..",
        "..hSESSESh..",
        "..sbSSSSbs..",
        "...bbBBbb...",
        "....bSSb....",
        "..WWWXXWWW..",
        ".SWWWWWWWWS.",
        ".SWWWWWWWWS.",
        "..NKKYKKKN..",
        "...NN..NN...",
        "...NN..NN...",
        "..OOO..OOO..",
        "..OOO..OOO..",
    ],
    'side': [
        "...hHHHh....",
        "..hHHJJHh...",
        "..hHHHHHHh..",
        "..hhHHSSSS..",
        "..hhSSSSES..",
        "..hhsSSSSSS.",
        "...hbbSSbb..",
        "....bbbbb...",
        "....WWWXX...",
        "....WWWWW...",
        "....WSSWW...",
        "....KKKKY...",
        "....NNNN....",
        "....NNNN....",
        "....OOOOO...",
        "....OOOOO...",
    ],
}
BASES = {
    'ryanlike': (RYANLIKE, BASE),
    'cozy': (STYLES[0], STYLES[0]['palette']),
    'handheld': (STYLES[1], STYLES[1]['palette']),
    'retro': (STYLES[2], STYLES[2]['palette']),
    'hibit': (STYLES[3], STYLES[3]['palette']),
    'chibi': (CHIBI16, {**BASE, 'x': '#202020'}),
    'micro': (MICRO, BASE),
}

# ------------------------------------------------------------- treatments
FLAT = {'h': 'H', 'J': 'H', 'L': 'H', 'r': 's', 'B': 'b', 'c': 'b', 'V': 'W', 'n': 'N', 'o': 'O'}


def grid(rows, flat=False, no_outline=False):
    out = []
    for row in rows:
        if flat:
            row = ''.join(FLAT.get(c, c) for c in row)
        if no_outline:
            row = row.replace('x', '.')
        out.append(row)
    return out


def render(rows, pal):
    w = len(rows[0])
    img = Image.new('RGBA', (w, len(rows)))
    for y, row in enumerate(rows):
        assert len(row) == w, (y, row)
        for x, ch in enumerate(row):
            if ch != '.':
                img.putpixel((x, y), ImageColor.getrgb(pal[ch]) + (255,))
    return img


def add_outline(img, tinted=False, colour=(32, 26, 26)):
    w, h = img.size
    big = Image.new('RGBA', (w + 2, h + 2))
    big.paste(img, (1, 1))
    src = big.copy().load()
    px = big.load()
    for y in range(h + 2):
        for x in range(w + 2):
            if src[x, y][3]:
                continue
            nbs = [src[xx, yy] for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                   if 0 <= xx < w + 2 and 0 <= yy < h + 2 and src[xx, yy][3]]
            if nbs:
                if tinted:
                    r, g, b = (sum(n[i] for n in nbs) // len(nbs) for i in range(3))
                    px[x, y] = (int(r * .45), int(g * .4), int(b * .4), 255)
                else:
                    px[x, y] = colour + (255,)
    return big


def tint_existing(rows, pal):
    """Replace the dark 'x' outline with a darker shade of the colour beside it."""
    img = render(rows, pal)
    px = img.load()
    w, h = img.size
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != 'x':
                continue
            nbs = [px[xx, yy] for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                   if 0 <= xx < w and 0 <= yy < h and rows[yy][xx] not in '.x']
            if nbs:
                r, g, b = (sum(n[i] for n in nbs) // len(nbs) for i in range(3))
                px[x, y] = (int(r * .5), int(g * .45), int(b * .45), 255)
    return img


def recolour(img, fn):
    img = img.copy()
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = fn(r, g, b) + (255,)
    return img


def lum(r, g, b):
    return 0.3 * r + 0.59 * g + 0.11 * b


def gameboy(r, g, b):
    ramp = [(15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)]
    return ramp[min(3, int(lum(r, g, b) / 64))]


def pastel(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    r2, g2, b2 = colorsys.hls_to_rgb(h, min(1, l * .55 + .42), s * .6)
    return int(r2 * 255), int(g2 * 255), int(b2 * 255)


def sepia(r, g, b):
    v = lum(r, g, b) / 255
    return int(40 + 200 * v), int(26 + 170 * v), int(18 + 120 * v)


def warm(r, g, b):
    return min(255, int(r * 1.08 + 10)), int(g * .98), int(b * .8)


def cool(r, g, b):
    return int(r * .86), int(g * .95), min(255, int(b * 1.12 + 12))


def onebit(r, g, b):
    return (20, 20, 24) if lum(r, g, b) < 120 else (246, 244, 236)


def ink(r, g, b):
    v = lum(r, g, b)
    if v < 70:
        return (27, 27, 31)
    if r > 200 and g > 150 and r - b > 45:   # skin stays a light peach
        return (243, 214, 188)
    if r > g + 25 and v < 190:          # warm browns: hair, beard
        return (150, 98, 58) if v < 120 else (196, 140, 88)
    return (242, 237, 226) if v > 170 else (214, 205, 188)


# name, blurb, base, options
STYLE_LIST = [
    ('Ryan match', '16×32, no outline, like approved Ryan', 'ryanlike', {}),
    ('Ryan match + outline', '16×32, adds a dark outline', 'ryanlike', {'outline': 'dark'}),
    ('Ryan + soft outline', '16×32, outline tinted to each colour', 'ryanlike', {'outline': 'tinted'}),
    ('Ryan match, two-tone', '16×32, one colour per part', 'ryanlike', {'flat': True}),
    ('Ryan match, warm', '16×32, golden-hour palette', 'ryanlike', {'fn': warm}),
    ('Cozy farm', '16×32, dark outline, eye whites, 3–4 tones', 'cozy', {}),
    ('Cozy farm, soft outline', '16×32, outline tinted per colour', 'cozy', {'tint': True}),
    ('Cozy farm, no outline', '16×32, shading only', 'cozy', {'no_outline': True}),
    ('Pastel cozy', '16×32, soft pastel palette', 'cozy', {'tint': True, 'fn': pastel}),
    ('Sepia storybook', '16×32, old-photo tones', 'cozy', {'fn': sepia}),
    ('Ink & paper', '16×32, black ink, cream paper', 'cozy', {'fn': ink}),
    ('Handheld RPG', '16×24, big head, bold outline', 'handheld', {}),
    ('Handheld RPG, pastel', '16×24, softer colours', 'handheld', {'fn': pastel}),
    ('Handheld, cool evening', '16×24, blue-shifted palette', 'handheld', {'fn': cool}),
    ('Pocket green', '16×24, four greens (old handheld)', 'handheld', {'fn': gameboy}),
    ('Chibi 16×16', 'Tiny overworld figure, outline', 'chibi', {}),
    ('Chibi 16×16, flat', 'No outline, one tone per part', 'chibi', {'flat': True, 'no_outline': True}),
    ('Chibi, pocket green', '16×16, four greens', 'chibi', {'fn': gameboy}),
    ('Chibi, soft outline', '16×16, outline tinted per colour', 'chibi', {'tint': True}),
    ('Micro 12×16', 'Smallest; no outline', 'micro', {}),
    ('Micro 12×16, outlined', 'Smallest, with outline', 'micro', {'outline': 'dark'}),
    ('Retro 8-bit', '16×24, four flat colours', 'retro', {}),
    ('Retro 8-bit, outlined', '16×24, adds a black outline', 'retro', {'outline': 'dark'}),
    ('Detailed hi-bit', '24×40, most detailed option', 'hibit', {}),
]


def make(base, opts):
    figure, pal = BASES[base]
    out = []
    for view in ('front', 'side'):
        rows = grid(figure[view], opts.get('flat'), opts.get('no_outline'))
        img = tint_existing(rows, pal) if opts.get('tint') else render(rows, pal)
        if opts.get('outline'):
            img = add_outline(img, tinted=opts['outline'] == 'tinted')
        if opts.get('fn'):
            img = recolour(img, opts['fn'])
        out.append(img)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    cols, cw, ch = 6, 300, 400
    rows_n = (len(STYLE_LIST) + cols - 1) // cols
    board = Image.new('RGBA', (40 + cols * cw, 150 + rows_n * ch), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), f'Logan — {len(STYLE_LIST)} simple map-sprite styles', font=font(42), fill=INK)
    d.text((40, 88), 'Front and side enlarged to a similar height; the small figure below each is true size at 2×. '
                     'Detailed models stay for the dialogue portraits.', font=font(18, False), fill=MUTED)
    for i, (name, blurb, base, opts) in enumerate(STYLE_LIST):
        front, side = make(base, opts)
        x0, y0 = 40 + (i % cols) * cw, 150 + (i // cols) * ch
        d.text((x0, y0), f'{i + 1}. {name}', font=font(19), fill=INK)
        d.text((x0, y0 + 26), blurb, font=font(13, False), fill=MUTED)
        panel = Image.new('RGBA', (cw - 20, 250), '#97b779')
        k = max(1, min(220 // front.height, (cw - 40) // 2 // front.width))
        for m, img in enumerate((front, side)):
            big = img.resize((img.width * k, img.height * k), Image.NEAREST)
            px = m * (cw - 20) // 2 + ((cw - 20) // 2 - big.width) // 2
            panel.alpha_composite(big, (px, 250 - 12 - big.height))
        board.alpha_composite(panel, (x0, y0 + 50))
        strip = Image.new('RGBA', (cw - 20, 86), '#97b779')
        small = front.resize((front.width * 2, front.height * 2), Image.NEAREST)
        strip.alpha_composite(small, ((cw - 20) // 2 - small.width // 2, 86 - 4 - small.height))
        board.alpha_composite(strip, (x0, y0 + 304))
    board.convert('RGB').save(OUT / 'logan-simple-styles.png', optimize=True)


if __name__ == '__main__':
    main()
