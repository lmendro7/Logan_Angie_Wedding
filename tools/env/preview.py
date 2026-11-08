"""Compose the garden exactly as the game places it, for review images.

    python3 tools/env/preview.py

Uses the same object positions as src/main.js (ENV_OBJECTS) and the cast's
standing frames. Writes docs/art/env/garden-preview.png and bedroom-preview.png.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ENV = ROOT / 'public' / 'env'
SPR = ROOT / 'public' / 'sprites'
OUT = ROOT / 'docs' / 'art' / 'env'

# (image, left, top, base y for depth) — keep in step with src/main.js.
OBJECTS = [('house', 278, 610, 780), ('blossom', 534, 176, 265), ('bench', 122, 451, 480),
           ('arch', 294, 47, 152), ('gate-closed', 352, 187, 216)]
OBJECTS += [('tree', x - 36, y + 32 - 89, y + 32) for y in range(90, 880, 115) for x in (39, 728)]
CAST = [('ryan', 510, 610), ('sophie', 230, 480), ('mother', 445, 365), ('father', 485, 365),
        ('angie', 384, 115), ('logan', 384, 820)]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    g = Image.open(ENV / 'garden.png').convert('RGBA')
    items = []
    for name, x, y, depth in OBJECTS:
        items.append((depth, Image.open(ENV / f'{name}.png').convert('RGBA'), x, y))
    fountain = Image.open(ENV / 'fountain.png').convert('RGBA').crop((0, 0, 90, 84))
    items.append((342, fountain, 155, 259))
    for cid, x, y in CAST:
        sheet = Image.open(SPR / f'{cid}.png').convert('RGBA')
        items.append((y, sheet.crop((0, 0, 16, 32)), x - 8, y - 31))
    ring = Image.open(ENV / 'ring.png').convert('RGBA').crop((0, 0, 13, 13))
    for x, y in ((245, 350), (590, 290)):
        items.append((y, ring, x - 6, y - 7))
    for _, im, x, y in sorted(items, key=lambda t: t[0]):
        g.alpha_composite(im, (x, y))
    g.save(OUT / 'garden-preview.png')
    b = Image.open(ENV / 'bedroom.png').convert('RGBA')
    b.alpha_composite(Image.open(SPR / 'logan.png').convert('RGBA').crop((0, 0, 16, 32)), (136, 179))
    b.save(OUT / 'bedroom-preview.png')


if __name__ == '__main__':
    main()
