"""Variations around simple style 13 (handheld RPG, pastel) for Lucas to compare.

    python3 tools/sprites/similar_13.py

Lucas liked style 13 but it was "not exactly" right, so each variation changes
one thing at a time: pastel strength, outline, eyes, body height or colour mood.
Writes docs/art/simple-styles-01/logan-style13-variations.png.
"""
import colorsys
import sys
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from styles import B_EYE_VARIANTS, STYLES, font            # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs' / 'art' / 'simple-styles-01'
HB = STYLES[1]                      # handheld base, 16 x 24
EYES = {label.split(' · ')[0]: (f, s) for label, f, s in B_EYE_VARIANTS}
FLAT = {'h': 'H', 'J': 'H', 'L': 'H', 'r': 's', 'B': 'b', 'c': 'b', 'V': 'W', 'n': 'N', 'o': 'O'}


def body(rows, height):
    """Taller (+3 rows) or shorter (-2 rows) body; the head is unchanged."""
    rows = list(rows)
    if height == 'tall':
        return rows[:16] + [rows[15]] + rows[16:20] + [rows[20], rows[20]] + rows[20:]
    if height == 'short':
        return rows[:16] + rows[17:20] + rows[21:]
    return rows


def pastel_fn(amount, sat=0.6, hue_shift=None):
    def fn(r, g, b):
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if hue_shift:
            h = (h + hue_shift[0]) % 1 if s > .08 else h
        l2 = l * (1 - amount) + amount * .97
        r2, g2, b2 = colorsys.hls_to_rgb(h, l2, s * sat)
        if hue_shift:                                   # gentle colour cast
            r2, g2, b2 = (min(1, r2 + hue_shift[1][0]), min(1, g2 + hue_shift[1][1]), min(1, b2 + hue_shift[1][2]))
        return int(r2 * 255), int(g2 * 255), int(b2 * 255)
    return fn


def earthy(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    r2, g2, b2 = colorsys.hls_to_rgb(h, l * .9 + .04, s * .45)
    return int(r2 * 255), int(g2 * 255), int(b2 * 255)


def make(opts):
    eye_f, eye_s = EYES.get(opts.get('eyes', '1'), ({}, {}))
    pal = {**HB['palette'], 'i': '#6b4a32', 'u': '#5f7d94'}
    out = []
    for view, swap in (('front', eye_f), ('side', eye_s)):
        rows = [swap.get(n, r) for n, r in enumerate(HB[view])]
        rows = body(rows, opts.get('height'))
        if opts.get('flat'):
            rows = [''.join(FLAT.get(c, c) for c in r) for r in rows]
        fn = opts.get('fn')
        img = Image.new('RGBA', (len(rows[0]), len(rows)))
        px = img.load()
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == '.' or (ch == 'x' and opts.get('outline') == 'none'):
                    continue
                rgb = ImageColor.getrgb(pal[ch])
                if ch == 'x':
                    if opts.get('outline') == 'dark':
                        rgb = (52, 40, 38)
                    elif opts.get('outline') == 'soft':
                        rgb = None                       # filled in below
                    elif fn:
                        rgb = fn(*rgb)
                elif fn:
                    rgb = fn(*rgb)
                if rgb:
                    px[x, y] = rgb + (255,)
        if opts.get('outline') == 'soft':                # darker shade of the neighbouring colour
            for y, row in enumerate(rows):
                for x, ch in enumerate(row):
                    if ch != 'x':
                        continue
                    nbs = [px[xx, yy] for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                           if 0 <= xx < img.width and 0 <= yy < img.height and rows[yy][xx] not in '.x']
                    if nbs:
                        r, g, b = (sum(n[i] for n in nbs) // len(nbs) for i in range(3))
                        px[x, y] = (int(r * .55), int(g * .48), int(b * .48), 255)
                    else:
                        px[x, y] = (70, 56, 52, 255)
        out.append(img)
    return out


PASTEL = pastel_fn(.45)
MEDIUM = pastel_fn(.25, .75)
VARIATIONS = [
    ('13 as shown', 'Pastel, outline washed to grey', {'fn': PASTEL}),
    ('Pastel + dark outline', 'Same pastel, crisp brown-black outline', {'fn': PASTEL, 'outline': 'dark'}),
    ('Medium + dark outline', 'Medium pastel: less washed out, stands off the grass', {'fn': MEDIUM, 'outline': 'dark'}),
    ('Medium + soft outline', 'Outline is a darker shade of each colour', {'fn': MEDIUM, 'outline': 'soft'}),
    ('Pastel, no outline', 'Softest, most minimal', {'fn': MEDIUM, 'outline': 'none'}),
    ('Pastel, two-tone', 'One colour per part, dark outline', {'fn': MEDIUM, 'outline': 'dark', 'flat': True}),
    ('Big friendly eyes', 'Medium pastel, taller eyes, brows up', {'fn': MEDIUM, 'outline': 'dark', 'eyes': '5'}),
    ('Blue-grey eyes', 'Medium pastel, iris + shine', {'fn': MEDIUM, 'outline': 'dark', 'eyes': '4'}),
    ('Brown eyes + shine', 'Medium pastel, warm iris', {'fn': MEDIUM, 'outline': 'dark', 'eyes': '3'}),
    ('Happy eyes', 'Medium pastel, smiling (^ ^)', {'fn': MEDIUM, 'outline': 'dark', 'eyes': '6'}),
    ('Taller body', '16×27, longer shirt and legs', {'fn': MEDIUM, 'outline': 'dark', 'height': 'tall'}),
    ('Shorter, chibier', '16×22, even rounder', {'fn': MEDIUM, 'outline': 'dark', 'height': 'short'}),
    ('Warm pastel', 'Peachy, golden cast', {'fn': pastel_fn(.3, .75, (0.0, (.04, .01, -.03))), 'outline': 'soft'}),
    ('Cool pastel', 'Minty, blue cast', {'fn': pastel_fn(.3, .7, (0.0, (-.03, .01, .05))), 'outline': 'soft'}),
    ('Muted earthy', 'Desaturated, not lightened', {'fn': earthy, 'outline': 'dark'}),
    ('Full colour (style 12)', 'Original handheld colours, for reference', {}),
    ('Tall + big eyes', 'Medium pastel, 16×27, big friendly eyes', {'fn': MEDIUM, 'outline': 'dark', 'height': 'tall', 'eyes': '5'}),
    ('Soft outline + blue eyes', 'Medium pastel, gentle outline, iris + shine', {'fn': MEDIUM, 'outline': 'soft', 'eyes': '4'}),
]


def main():
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    cols, cw, ch = 6, 300, 370
    rows_n = (len(VARIATIONS) + cols - 1) // cols
    board = Image.new('RGBA', (40 + cols * cw, 150 + rows_n * ch), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), f'Logan — {len(VARIATIONS)} variations on style 13', font=font(42), fill=INK)
    d.text((40, 88), 'Each changes one thing: pastel strength, outline, eyes, body height or colour mood. '
                     'Small figure = true size at 2× on grass.', font=font(18, False), fill=MUTED)
    for i, (name, blurb, opts) in enumerate(VARIATIONS):
        front, side = make(opts)
        x0, y0 = 40 + (i % cols) * cw, 150 + (i // cols) * ch
        d.text((x0, y0), f'{chr(65 + i)}. {name}', font=font(18), fill=INK)
        d.text((x0, y0 + 25), blurb, font=font(13, False), fill=MUTED)
        panel = Image.new('RGBA', (cw - 20, 230), '#97b779')
        k = 8
        for m, img in enumerate((front, side)):
            big = img.resize((img.width * k, img.height * k), Image.NEAREST)
            panel.alpha_composite(big, (m * 140 + 6, 230 - 6 - big.height))
        board.alpha_composite(panel, (x0, y0 + 48))
        strip = Image.new('RGBA', (cw - 20, 72), '#97b779')
        small = front.resize((front.width * 2, front.height * 2), Image.NEAREST)
        strip.alpha_composite(small, ((cw - 20) // 2 - small.width // 2, 72 - 6 - small.height))
        board.alpha_composite(strip, (x0, y0 + 282))
    board.convert('RGB').save(OUT / 'logan-style13-variations.png', optimize=True)


if __name__ == '__main__':
    main()
