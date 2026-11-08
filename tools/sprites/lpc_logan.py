"""Rebuild Logan's original-style (LPC) walking sprite to match his approved board.

    python3 tools/sprites/lpc_logan.py /path/to/Universal-LPC-Spritesheet-Character-Generator

The checkout must be at the commit pinned in docs/art/logan-draft-01/recipe.json.
Starts from that draft recipe, swaps the buzzcut for the "cowlick" hair (compact,
lifted, brushed-back top with short sides), and recolours the hair and trimmed
beard to the muted dirty blond sampled from docs/art/logan-approved-01.
Writes docs/art/logan-lpc-01/ (sheet, recipe with credits, previews).
The composition is CC-BY-SA 4.0; see the recipe for each layer's credits.
"""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / 'docs' / 'art' / 'logan-draft-01' / 'recipe.json'
OUT = ROOT / 'docs' / 'art' / 'logan-lpc-01'
SRC = Path(sys.argv[1])

HAIR_STYLE = 'cowlick'
BEARD_STYLE = 'medium'
LPC_RAMP = [(26, 14, 4), (48, 27, 7), (96, 53, 15), (125, 69, 19), (174, 104, 42), (200, 141, 88)]
# Colours taken from the reference photos (kept out of the repo):
# light ash-brown hair, lighter on top; warmer ginger-brown beard.
HAIR_RAMP = [(28, 21, 16), (58, 45, 34), (92, 72, 52), (124, 99, 72), (160, 131, 96), (198, 170, 128)]
# Softer skin shadows: the stock darkest shade reads as bright red at this size.
SKIN_MAP = {(153, 66, 60): (164, 100, 80), (204, 134, 101): (214, 150, 118)}
BEARD_RAMP = [(30, 18, 10), (66, 40, 22), (104, 64, 36), (136, 88, 52), (170, 116, 72), (204, 150, 100)]


def hair_path(style):
    for sub in ('adult', 'male'):
        p = f'spritesheets/hair/{style}/{sub}/light_brown.png'
        if (SRC / p).exists():
            return p
    raise FileNotFoundError(style)


HAIR_CREDITS = [{
    'file': 'hair/cowlick',
    'notes': 'Original by bluecarrot16, animated by ElizaWy.',
    'authors': ['ElizaWy', 'bluecarrot16'],
    'licenses': ['CC0'],
    'urls': ['https://opengameart.org/content/lpc-hair',
             'https://github.com/ElizaWy/LPC/blob/main/Characters/Hair',
             'https://opengameart.org/content/expanded-universal-lpc-spritesheet-idle-run-jump-lpc-revised-combat-and-assets'],
}]


def recolour(img, ramp):
    table = dict(zip(LPC_RAMP, ramp))
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in table:
                px[x, y] = table[(r, g, b)] + (a,)
    return img


def recolour_map(img, table):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in table:
                px[x, y] = table[(r, g, b)] + (a,)
    return img


def compose(hair_style, beard_style, crop):
    recipe = json.loads(DRAFT.read_text())
    layers = []
    for layer in recipe['layers']:
        if 'spritesheets/hair/' in layer['path']:
            layer = {'path': hair_path(hair_style), 'definition': f'sheet_definitions/hair_{hair_style}.json',
                     'credits': HAIR_CREDITS if hair_style == 'cowlick' else 'see CREDITS.csv for hair/' + hair_style,
                     'recolour': 'hair'}
        elif 'spritesheets/beards/' in layer['path']:
            layer = {**layer, 'path': f'spritesheets/beards/beard/{beard_style}/light_brown.png', 'recolour': 'beard'}
        layers.append(layer)
    sheet = Image.new('RGBA', (crop[2] - crop[0], crop[3] - crop[1]))
    for layer in layers:
        part = Image.open(SRC / layer['path']).convert('RGBA').crop(crop)
        if layer.get('recolour') == 'hair':
            part = recolour(part, HAIR_RAMP)
        elif layer.get('recolour') == 'beard':
            part = recolour(part, BEARD_RAMP)
        elif '/heads/' in layer['path'] or '/bodies/' in layer['path']:
            part = recolour_map(part, SKIN_MAP)
        sheet.alpha_composite(part)
    return sheet, layers


def font(size):
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
    except OSError:
        return ImageFont.load_default()


def main():
    recipe = json.loads(DRAFT.read_text())
    crop = tuple(recipe['source_crop'])
    if len(sys.argv) > 2 and sys.argv[2] == '--candidates':
        candidates(crop)
        return
    sheet, layers = compose(HAIR_STYLE, BEARD_STYLE, crop)

    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT / 'logan-walk.png', optimize=True)
    out_recipe = {**recipe, 'status': 'original-style rebuild for review; not integrated into live game',
                  'changes': recipe['changes'] + f' Hair swapped to {HAIR_STYLE}, beard to {BEARD_STYLE}; hair and beard recoloured from reference-photo colours.',
                  'layers': layers}
    (OUT / 'recipe.json').write_text(json.dumps(out_recipe, indent=1) + '\n')

    def tile(row, col=0):
        return sheet.crop((col * 64, row * 64, (col + 1) * 64, (row + 1) * 64))

    # Review board: approved board crop, four directions, walk cycle, game scale with Ryan.
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    board = Image.new('RGBA', (1150, 1060), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((50, 36), 'Logan — original-style walking sprite', font=font(40), fill=INK)
    d.text((50, 92), 'Rebuilt from the LPC layers behind the approved board · 64 × 64 frames · shown 4×', font=font(20), fill=MUTED)
    approved = Image.open(ROOT / 'docs/art/logan-approved-01/logan-review.png').convert('RGBA').crop((70, 300, 540, 724))
    approved = approved.resize((282, 254), Image.LANCZOS)
    board.alpha_composite(approved, (50, 150))
    d.text((50, 412), 'Approved board (front)', font=font(16), fill=MUTED)
    for n, (row, lab) in enumerate([(2, 'FRONT'), (3, 'RIGHT'), (0, 'BACK'), (1, 'LEFT')]):
        x0 = 360 + n * 190
        d.text((x0 + 70, 140), lab, font=font(18), fill=INK)
        board.alpha_composite(tile(row).resize((256, 256), Image.NEAREST), (x0 - 30, 160))
    d.text((50, 460), 'Walk cycle, facing right (8 frames per direction)', font=font(24), fill=INK)
    for col in range(1, 9):
        board.alpha_composite(tile(3, col).resize((128, 128), Image.NEAREST), (20 + (col - 1) * 138, 500))
    d.text((50, 650), 'Game scale beside Ryan (current garden zoom 1×, then 2×)', font=font(24), fill=INK)
    ryan = Image.open(ROOT / 'public/sprites/ryan.png').convert('RGBA').crop((0, 0, 16, 32))
    for j, s in enumerate([1, 2]):
        gx, gy, gw, gh = 50 + j * 540, 700, 500, 300
        d.rectangle([gx, gy, gx + gw, gy + gh], fill='#97b779')
        base = gy + gh // 2 + 30 * s
        for cx, img, fh in [(gx + gw // 2 - 30 * s, tile(2), 64), (gx + gw // 2 + 30 * s, ryan, 32)]:
            d.ellipse([cx - 8 * s, base - 2 * s, cx + 8 * s, base + 2 * s], fill=(38, 60, 48, 70))
            off = 2 if fh == 64 else 0   # LPC feet sit ~2 px above the frame bottom
            big = img.resize((img.width * s, img.height * s), Image.NEAREST)
            board.alpha_composite(big, (cx - big.width // 2, base - (fh - off) * s))
    board.convert('RGB').save(OUT / 'logan-lpc-review.png', optimize=True)

    frames = []
    for row in (2, 3, 0, 1):
        for col in range(1, 9):
            f = Image.new('RGBA', (64 * 4, 64 * 4), '#97b779')
            f.alpha_composite(tile(row, col).resize((256, 256), Image.NEAREST))
            frames.append(f.convert('RGB'))
    frames[0].save(OUT / 'logan-walking.gif', save_all=True, append_images=frames[1:], duration=110, loop=0)


def candidates(crop):
    """Grid of haircut x beard options, front and right views, for choosing."""
    hairs = ['cowlick', 'flat_top_fade', 'spiked', 'messy2', 'parted2', 'plain']
    beards = ['trimmed', 'medium']
    k = 3
    img = Image.new('RGBA', (60 + len(hairs) * 2 * 64 * k, 60 + len(beards) * 64 * k), '#e9eedb')
    d = ImageDraw.Draw(img)
    for i, h in enumerate(hairs):
        d.text((60 + i * 128 * k + 10, 10), h, font=font(18), fill='#14634a')
        for j, b in enumerate(beards):
            sheet, _ = compose(h, b, crop)
            for v, row in enumerate((2, 3)):
                t = sheet.crop((0, row * 64, 64, row * 64 + 64)).resize((64 * k, 64 * k), Image.NEAREST)
                img.alpha_composite(t, (60 + i * 128 * k + v * 64 * k - 20, 40 + j * 64 * k))
    for j, b in enumerate(beards):
        d.text((4, 40 + j * 64 * k + 90), b, font=font(14), fill='#14634a')
    out = Path(sys.argv[3])
    img.convert('RGB').save(out)


if __name__ == '__main__':
    main()
