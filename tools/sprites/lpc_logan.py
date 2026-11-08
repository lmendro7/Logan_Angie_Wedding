"""Build Logan's original-style (LPC) walking sprite.

    python3 tools/sprites/lpc_logan.py /path/to/Universal-LPC-Spritesheet-Character-Generator
    python3 tools/sprites/lpc_logan.py <lpc checkout> --candidates <out.png>

The checkout must be at the commit pinned in docs/art/logan-draft-01/recipe.json.
BUILD selects the parts. Hair and beard are recoloured to colours taken from
reference photos (kept out of the repository); the darkest stock skin shade is
softened. Writes docs/art/logan-lpc-01/ (sheet, recipe with credits, previews).
The composition is CC-BY-SA 4.0; recipe.json lists every layer's credits.
"""
import csv
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / 'docs' / 'art' / 'logan-draft-01' / 'recipe.json'
OUT = ROOT / 'docs' / 'art' / 'logan-lpc-01'
SRC = Path(sys.argv[1])
SS = 'spritesheets/'

# Bottom-to-top layer stacks. 'hair'/'beard'/'skin' mark layers to recolour.
BUILDS = {
    # Revision 1-2: the draft 01 broad adult body.
    'adult': [
        ('body/bodies/male/light.png', 'skin'),
        ('feet/shoes/male/black.png', None),
        ('legs/formal/male/black.png', None),
        ('torso/clothes/longsleeve/formal/male/white.png', None),
        ('torso/jacket/collared/male/black.png', None),
        ('neck/tie/bowtie/adult/black.png', None),
        ('head/heads/human/male/light.png', 'skin'),
        ('eyes/human/adult/brown.png', None),
        ('beards/beard/medium/light_brown.png', 'beard'),
        ('hair/cowlick/adult/light_brown.png', 'hair'),
    ],
    # Revision 3: younger. Slim body, smaller head, trimmed beard, slim shirt,
    # open black cardigan standing in for the jacket, slim trousers.
    'young': [
        ('body/bodies/teen/light.png', 'skin'),
        ('feet/shoes/female/black.png', None),
        ('legs/formal/thin/black.png', None),
        ('torso/clothes/longsleeve/longsleeve2_buttoned/teen/white.png', None),
        ('torso/clothes/longsleeve/longsleeve2_cardigan/teen/black.png', 'open'),
        ('neck/tie/bowtie/adult/black.png', None),
        ('head/heads/human/male_small/light.png', 'skin'),
        ('beards/beard/trimmed/light_brown.png', 'beard'),
        ('hair/cowlick/adult/light_brown.png', 'hair'),
    ],
}
BUILD = 'young'

LPC_RAMP = [(26, 14, 4), (48, 27, 7), (96, 53, 15), (125, 69, 19), (174, 104, 42), (200, 141, 88)]
# From the reference photos: light ash-brown hair, lighter on top; warmer ginger-brown beard.
HAIR_RAMP = [(28, 21, 16), (58, 45, 34), (92, 72, 52), (124, 99, 72), (160, 131, 96), (198, 170, 128)]
BEARD_RAMP = [(30, 18, 10), (66, 40, 22), (104, 64, 36), (136, 88, 52), (170, 116, 72), (204, 150, 100)]
# The stock darkest skin shade reads as bright red at this size.
SKIN_MAP = {(153, 66, 60): (164, 100, 80), (204, 134, 101): (214, 150, 118),
            # The small head carries its own blue eyes; make them brown.
            (42, 60, 73): (66, 44, 30), (86, 134, 174): (92, 62, 40), (87, 206, 228): (128, 90, 60)}


def recolour_map(img, table):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in table:
                px[x, y] = table[(r, g, b)] + (a,)
    return img


TABLES = {'hair': dict(zip(LPC_RAMP, HAIR_RAMP)), 'beard': dict(zip(LPC_RAMP, BEARD_RAMP)), 'skin': SKIN_MAP}


def credits_for(rel):
    """Credits row whose filename is the longest prefix of the layer path."""
    best = None
    with open(SRC / 'CREDITS.csv', newline='') as f:
        for row in csv.DictReader(f):
            name = row['filename'].rstrip('/')
            if rel.startswith(name + '/') or rel.startswith(name + '.') or rel == name:
                if best is None or len(name) > len(best['filename']):
                    best = row
    if best is None:
        return None
    urls = [best[k] for k in best if k.startswith('url') and best[k]]
    return {'file': best['filename'], 'notes': best['notes'],
            'authors': [a.strip() for a in best['authors'].split(',')],
            'licenses': [l.strip() for l in best['licenses'].split(',')], 'urls': urls}


def open_front(part):
    """Cut a 4 px opening down the cardigan's front so it reads as an open jacket."""
    px = part.load()
    for col in range(part.width // 64):
        for y in range(128 + 34, 128 + 47):          # row 2 = facing the viewer
            for x in range(col * 64 + 30, col * 64 + 34):
                px[x, y] = (0, 0, 0, 0)
    return part


def compose(layers, crop):
    sheet = Image.new('RGBA', (crop[2] - crop[0], crop[3] - crop[1]))
    for rel, kind in layers:
        part = Image.open(SRC / SS / rel).convert('RGBA').crop(crop)
        if kind == 'open':
            part = open_front(part)
        elif kind:
            part = recolour_map(part, TABLES[kind])
        sheet.alpha_composite(part)
    return sheet


def font(size):
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
    except OSError:
        return ImageFont.load_default()


def tiles(sheet):
    return lambda row, col=0: sheet.crop((col * 64, row * 64, (col + 1) * 64, (row + 1) * 64))


def main():
    recipe = json.loads(DRAFT.read_text())
    crop = tuple(recipe['source_crop'])
    if len(sys.argv) > 2 and sys.argv[2] == '--candidates':
        candidates(crop)
        return
    layers = BUILDS[BUILD]
    sheet = compose(layers, crop)
    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT / 'logan-walk.png', optimize=True)
    out_recipe = {k: recipe[k] for k in ('source_repository', 'source_commit', 'source_license_choice',
                                         'composite_artwork_license', 'license_url', 'frame_width',
                                         'frame_height', 'columns', 'rows', 'source_crop')}
    out_recipe.update({
        'status': f'original-style rebuild "{BUILD}" for review; not integrated into live game',
        'changes': 'Layer composition; four-direction walk frames only; hair, beard and skin-shadow '
                   'recolouring (see tools/sprites/lpc_logan.py). No photo pixels used. '
                   'Preview enlargements use nearest-neighbour scaling.',
        'layers': [{'path': SS + rel, 'recolour': kind, 'credits': credits_for(rel)} for rel, kind in layers],
    })
    (OUT / 'recipe.json').write_text(json.dumps(out_recipe, indent=1) + '\n')

    tile = tiles(sheet)
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    board = Image.new('RGBA', (1150, 1060), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((50, 36), 'Logan — original-style walking sprite', font=font(40), fill=INK)
    d.text((50, 92), f'Build "{BUILD}" · LPC layers · 64 × 64 frames · shown 4×', font=font(20), fill=MUTED)
    approved = Image.open(ROOT / 'docs/art/logan-approved-01/logan-review.png').convert('RGBA').crop((70, 300, 540, 724))
    board.alpha_composite(approved.resize((282, 254), Image.LANCZOS), (50, 150))
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

    close = Image.new('RGBA', (4 * 320, 320), '#97b779')
    for n, row in enumerate((2, 3, 0, 1)):
        close.alpha_composite(tile(row).resize((320, 320), Image.NEAREST), (n * 320, 0))
    close.convert('RGB').save(OUT / 'logan-closeup.png', optimize=True)

    frames = []
    for row in (2, 3, 0, 1):
        for col in range(1, 9):
            f = Image.new('RGBA', (256, 256), '#97b779')
            f.alpha_composite(tile(row, col).resize((256, 256), Image.NEAREST))
            frames.append(f.convert('RGB'))
    frames[0].save(OUT / 'logan-walking.gif', save_all=True, append_images=frames[1:], duration=110, loop=0)


def candidates(crop):
    """Previous adult build beside younger variants, front and right views."""
    young = BUILDS['young']
    swap = lambda old, new: [(new if r == old else r, k) for r, k in young]
    variants = [
        ('previous (adult)', BUILDS['adult']),
        ('young, trimmed beard', young),
        ('young, medium beard', swap('beards/beard/trimmed/light_brown.png', 'beards/beard/medium/light_brown.png')),
        ('young, no cardigan', [l for l in young if 'cardigan' not in l[0]]),
    ]
    k = 4
    img = Image.new('RGBA', (len(variants) * 2 * 64 * k + 40, 64 * k + 60), '#e9eedb')
    d = ImageDraw.Draw(img)
    for i, (label, layers) in enumerate(variants):
        tile = tiles(compose(layers, crop))
        d.text((20 + i * 128 * k + 10, 10), label, font=font(20), fill='#14634a')
        for v, row in enumerate((2, 3)):
            img.alpha_composite(tile(row).resize((64 * k, 64 * k), Image.NEAREST), (20 + i * 128 * k + v * 64 * k, 44))
    img.convert('RGB').save(Path(sys.argv[3]))


if __name__ == '__main__':
    main()
