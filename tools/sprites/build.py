"""Render every character's map sprite sheet and the review images.

    python3 tools/sprites/build.py

Writes public/sprites/<id>.png (runtime sheets) and review images in
docs/art/sprites-01/. Requires Pillow.

Sheet layout: 16x32 px frames; rows = down, right, up, left;
columns = stand, step A, step B. Feet touch the bottom row (origin 0.5, 1).
"""
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageFont

from characters import CHARACTERS

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / 'public' / 'sprites'
REVIEW = ROOT / 'docs' / 'art' / 'sprites-01'
W, H = 16, 32
TOP_ROWS = 25


def frame(rows, palette, who):
    assert len(rows) == H, (who, len(rows))
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == W, (who, y, row)
        for x, ch in enumerate(row):
            if ch == '.':
                continue
            assert ch in palette, (who, y, ch)
            img.putpixel((x, y), ImageColor.getrgb(palette[ch]) + (255,))
    return img


def frames_for(cid):
    c = CHARACTERS[cid]
    for view in ('front', 'back', 'side'):
        assert len(c[view]) == TOP_ROWS, (cid, view, len(c[view]))
    fb, side = c['legs']
    pal = c['palette']
    down = [frame(c['front'] + legs, pal, cid) for legs in fb]
    up = [frame(c['back'] + legs, pal, cid) for legs in fb]
    right = [frame(c['side'] + legs, pal, cid) for legs in side]
    left = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in right]
    return [down, right, up, left]


def sheet_for(rows):
    sheet = Image.new('RGBA', (W * 3, H * 4), (0, 0, 0, 0))
    for r, frames in enumerate(rows):
        for c, f in enumerate(frames):
            sheet.paste(f, (c * W, r * H))
    return sheet


def scaled(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def font(size):
    for name in ('DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def shadow(draw, cx, base, k):
    draw.ellipse([cx - 7 * k, base - 2 * k, cx + 7 * k, base + 2 * k], fill=(38, 60, 48, 70))


def main():
    RUNTIME.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    all_rows = {}
    for cid in CHARACTERS:
        rows = frames_for(cid)
        all_rows[cid] = rows
        sheet = sheet_for(rows)
        sheet.save(RUNTIME / f'{cid}.png', optimize=True)
        scaled(sheet, 8).save(REVIEW / f'{cid}-sheet-x8.png', optimize=True)

    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    ids = list(CHARACTERS)

    # Per-character review: four views at 8x, Ryan alongside, walk frames, game scale.
    for cid in ids:
        if cid == 'ryan':
            continue
        c, rows = CHARACTERS[cid], all_rows[cid]
        k = 8
        rv = Image.new('RGBA', (1150, 1000), BG)
        d = ImageDraw.Draw(rv, 'RGBA')
        d.text((50, 36), f"{c['name']} — map sprite", font=font(40), fill=INK)
        d.text((50, 92), c['status'], font=font(20), fill=MUTED)
        for r, lab in enumerate(['FRONT', 'RIGHT', 'BACK', 'LEFT']):
            x0 = 50 + r * 175
            d.text((x0 + 64 - d.textlength(lab, font=font(18)) / 2, 140), lab, font=font(18), fill=INK)
            rv.alpha_composite(scaled(rows[r][0], k), (x0, 170))
        d.text((790, 140), 'RYAN (approved)', font=font(18), fill=MUTED)
        rv.alpha_composite(scaled(all_rows['ryan'][0][0], k), (830, 170))
        d.text((50, 450), 'Walk frames', font=font(24), fill=INK)
        for r in range(4):
            for col in range(3):
                rv.alpha_composite(scaled(rows[r][col], 3), (50 + r * 270 + col * 60, 490))
        d.text((50, 620), 'Game scale beside Ryan: 1× (current zoom), 2×, 3×', font=font(24), fill=INK)
        for j, s in enumerate([1, 2, 3]):
            gx, gy, gw, gh = 50 + j * 350, 665, 320, 200
            d.rectangle([gx, gy, gx + gw, gy + gh], fill='#97b779')
            for n, who in enumerate([cid, 'ryan']):
                cx = gx + gw // 2 - 14 * s + n * 28 * s
                base = gy + gh // 2 + 16 * s
                shadow(d, cx, base, s)
                rv.alpha_composite(scaled(all_rows[who][0][0], s), (cx - 8 * s, base - 32 * s))
        rv.convert('RGB').save(REVIEW / f'{cid}-review.png', optimize=True)

    # Lineup board: every character, four directions, 6x, plus game scale.
    k = 6
    cell = W * k + 20
    board = Image.new('RGBA', (900, 150 + len(ids) * (H * k + 60) + 300), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 36), 'Map sprites 01 — all characters', font=font(40), fill=INK)
    d.text((40, 92), '16 × 32 px · front, right, back, left · shown 6×', font=font(20), fill=MUTED)
    y = 150
    for cid in ids:
        c = CHARACTERS[cid]
        d.text((40, y), f"{c['name']}  ·  {c['status']}", font=font(20), fill=INK)
        for r in range(4):
            board.alpha_composite(scaled(all_rows[cid][r][0], k), (40 + r * cell, y + 34))
        y += H * k + 60
    d.text((40, y), 'Actual game scale (1×) and 2×', font=font(24), fill=INK)
    for j, s in enumerate([1, 2]):
        gx, gy, gw, gh = 40, y + 44 + j * 110, 4 * cell, 96 if s == 1 else 100
        gy = y + 44 if s == 1 else y + 120
        gh = 60 if s == 1 else 110
        d.rectangle([gx, gy, gx + gw, gy + gh], fill='#97b779')
        for i, cid in enumerate(ids):
            cx = gx + 30 * s + i * (22 * s + 14)
            base = gy + gh - 10
            shadow(d, cx, base, s)
            board.alpha_composite(scaled(all_rows[cid][0][0], s), (cx - 8 * s, base - 32 * s))
    board.convert('RGB').save(REVIEW / 'sprites-review.png', optimize=True)

    # Walking GIF: each character walking toward the viewer and to the right.
    k, pad = 4, 10
    gif = []
    for i in [1, 0, 2, 0]:
        canvas = Image.new('RGBA', (len(ids) * 2 * (W * k + pad) + pad, H * k + 2 * pad), '#97b779')
        dd = ImageDraw.Draw(canvas, 'RGBA')
        for n, cid in enumerate(ids):
            for m, r in enumerate((0, 1)):
                x0 = pad + (2 * n + m) * (W * k + pad)
                shadow(dd, x0 + W * k // 2, pad + H * k, k)
                canvas.alpha_composite(scaled(all_rows[cid][r][i], k), (x0, pad))
        gif.append(canvas.convert('RGB'))
    gif[0].save(REVIEW / 'sprites-walking.gif', save_all=True, append_images=gif[1:], duration=170, loop=0)


if __name__ == '__main__':
    main()
