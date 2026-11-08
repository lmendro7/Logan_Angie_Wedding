"""Dialogue portraits: the detailed models, shown beside the speaker's name.

    python3 tools/sprites/portraits.py

Logan: his approved model with the white shirt and bow tie (from
docs/art/board-sprites-01). Angie: her approved model with glasses, plus her veil (Lucas, November 8). Ryan: his approved
design board. Sophie and the parents have no detailed model yet, so their
map sprite is enlarged as a stand-in until their models are made.
Writes public/portraits/<id>.png (crisp pixel art; scale with nearest-neighbour).
"""
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public' / 'portraits'
BOARDS = ROOT / 'docs' / 'art' / 'board-sprites-01'
SIZE = 96          # square portrait, px


def fit(img, scale):
    img = img.crop(img.getbbox())
    big = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    canvas = Image.new('RGBA', (SIZE, SIZE))
    canvas.alpha_composite(big, ((SIZE - big.width) // 2, SIZE - big.height))
    return canvas


def angie_portrait(glasses=True):
    """Angie's model with her veil. Lucas (Nov 8): the portrait keeps her glasses;
    only the map sprite drops them. glasses=False keeps the removal step for reference."""
    img = Image.open(BOARDS / 'angie-front.png').convert('RGBA')
    px = img.load()
    if not glasses:
        remove_glasses(px)
    add_veil(img, px)
    return img


def remove_glasses(px):
    skin, skin_sh, eye, lash = (249, 207, 158), (231, 178, 126), (58, 38, 26), (40, 26, 18)
    for y in range(11, 20):                     # glasses frames and lens tint -> skin
        for x in range(8, 20):
            r, g, b, a = px[x, y]
            if not a:
                continue
            lum, sat = (r + g + b) / 3, (max(r, g, b) - min(r, g, b)) / max(r, g, b, 1)
            dark = lum < 115
            brown_edge = y >= 12 and r > 120 and g < 120 and b < 80 and r - b > 60
            grey = y >= 12 and sat < 0.32 and 95 < lum < 225
            mid_brown = y >= 16 and r > 150 and 95 < g < 175 and b < 130 and r - b > 55 and not (r > 200 and g < 160)
            if dark or brown_edge or grey or mid_brown:
                px[x, y] = skin if 13 <= y <= 17 else skin_sh
    for xy in [(10, 14), (11, 14), (10, 15), (11, 15), (16, 14), (17, 14), (16, 15), (17, 15)]:
        px[xy] = eye
    for xy in [(9, 13), (10, 13), (11, 13), (16, 13), (17, 13), (18, 13)]:
        px[xy] = lash


def add_veil(img, px):
    veil, veil_sh = (248, 245, 238), (222, 216, 204)
    w, h = img.size
    for x in range(w):                          # veil band across the top of her hair
        for y in (2, 3):
            if px[x, y][3]:
                px[x, y] = veil if y == 2 else veil_sh
    for y in range(4, h):                       # veil falling along both sides
        row = [x for x in range(w) if px[x, y][3]]
        if row:
            px[row[0], y] = veil_sh
            px[row[-1], y] = veil_sh
            if len(row) > 2:
                px[row[1], y] = veil
                px[row[-2], y] = veil


def from_extraction(name, rows):
    pose = Image.open(BOARDS / name).convert('RGBA')
    return pose.crop((0, 0, pose.width, rows))


def ryan_from_board():
    board = Image.open(ROOT / 'docs/art/ryan-approved-01/ryan-review.png').convert('RGB')
    crop = np.asarray(board.crop((70, 250, 260, 500))).astype(int)        # front view, cap to chest
    bg = np.median(crop[:4].reshape(-1, 3), axis=0)
    alpha = (np.abs(crop - bg).sum(axis=2) > 40) * 255
    img = Image.fromarray(np.dstack([crop, alpha]).astype(np.uint8), 'RGBA')
    img = img.crop(img.getbbox())
    # The board is enlarged pixel art; bring it back to a crisp grid, then up to portrait size.
    small = img.resize((round(img.width / 6), round(img.height / 6)), Image.NEAREST)
    return small


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fit(from_extraction('logan-shirt-front.png', 31), 3).save(OUT / 'logan.png')
    fit(angie_portrait().crop((0, 0, 27, 32)), 3).save(OUT / 'angie.png')
    fit(ryan_from_board(), 2).save(OUT / "ryan.png")
    sheets = ROOT / 'public' / 'sprites'
    for cid in ('sophie', 'mother', 'father'):
        sprite = Image.open(sheets / f'{cid}.png').convert('RGBA').crop((0, 0, 16, 18))
        fit(sprite, 5).save(OUT / f'{cid}.png')


if __name__ == '__main__':
    main()
