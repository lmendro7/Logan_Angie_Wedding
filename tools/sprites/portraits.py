"""Dialogue portraits: the detailed models, shown beside the speaker's name.

    python3 tools/sprites/portraits.py

Logan: his approved model with the white shirt and bow tie (from
docs/art/board-sprites-01). Angie: her approved model. Ryan: his approved
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
    fit(from_extraction('angie-front.png', 32), 3).save(OUT / 'angie.png')
    fit(ryan_from_board(), 2).save(OUT / "ryan.png")
    sheets = ROOT / 'public' / 'sprites'
    for cid in ('sophie', 'mother', 'father'):
        sprite = Image.open(sheets / f'{cid}.png').convert('RGBA').crop((0, 0, 16, 18))
        fit(sprite, 5).save(OUT / f'{cid}.png')


if __name__ == '__main__':
    main()
