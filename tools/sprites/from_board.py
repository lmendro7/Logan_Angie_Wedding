"""Turn an approved four-view character board into crisp game-scale sprites.

    python3 tools/sprites/from_board.py

For each board: lift every pose off its mint panel (flood fill from the panel
edge), keep the figure, shrink by SCALE with an area filter, snap alpha to
on/off and the colours to a small palette. Writes docs/art/board-sprites-01/.
"""
from collections import deque
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs' / 'art' / 'board-sprites-01'
SCALE = 4.5          # board pixels per sprite pixel (same for every character)
COLOURS = 24
PANELS = {'front': (72, 300, 540, 724), 'right': (612, 300, 1078, 724),
          'back': (72, 772, 540, 1202), 'left': (612, 772, 1078, 1202)}
BOARDS = {
    'angie': ROOT / 'docs/art/angie-approved-01/angie-review.png',
    'logan': ROOT / 'docs/art/logan-approved-01/logan-review.png',
}


def lift(panel):
    """RGBA figure: remove the panel background by flood fill from the border."""
    a = np.asarray(panel.convert('RGB')).astype(int)
    h, w, _ = a.shape
    bg = np.median(np.concatenate([a[2, :], a[-3, :], a[:, 2], a[:, -3]]), axis=0)
    near = np.abs(a - bg).sum(axis=2) < 70
    seen = np.zeros((h, w), bool)
    q = deque([(y, x) for y in range(h) for x in (0, w - 1)] + [(y, x) for x in range(w) for y in (0, h - 1)])
    while q:
        y, x = q.popleft()
        if 0 <= y < h and 0 <= x < w and not seen[y, x] and near[y, x]:
            seen[y, x] = True
            q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    fg = ~seen
    # Keep the largest connected blob (drops the panel's text label).
    lab = np.zeros((h, w), int); n = 0; sizes = {}
    for y0 in range(h):
        for x0 in range(w):
            if fg[y0, x0] and not lab[y0, x0]:
                n += 1; q = deque([(y0, x0)]); lab[y0, x0] = n; c = 0
                while q:
                    y, x = q.popleft(); c += 1
                    for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= yy < h and 0 <= xx < w and fg[yy, xx] and not lab[yy, xx]:
                            lab[yy, xx] = n; q.append((yy, xx))
                sizes[n] = c
    keep = lab == max(sizes, key=sizes.get)
    rgba = np.dstack([a, keep * 255]).astype(np.uint8)
    img = Image.fromarray(rgba, 'RGBA')
    return img.crop(img.getbbox())


def shrink(fig):
    w, h = round(fig.width / SCALE), round(fig.height / SCALE)
    a = np.asarray(fig).astype(float)
    a[..., :3] *= a[..., 3:4] / 255          # premultiply so the edge does not pick up background
    small = np.asarray(Image.fromarray(a.astype(np.uint8), 'RGBA').resize((w, h), Image.BOX)).astype(float)
    alpha = small[..., 3]
    rgb = np.where(alpha[..., None] > 0, small[..., :3] * 255 / np.maximum(alpha[..., None], 1), 0)
    out = np.dstack([np.clip(rgb, 0, 255), (alpha > 110) * 255]).astype(np.uint8)
    on = out[..., 3] > 0
    for y in range(out.shape[0]):
        for x in range(out.shape[1]):
            if on[y, x] and out[y, x, :3].mean() > 185:
                nb = sum(on[yy, xx] for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1))
                         if 0 <= yy < out.shape[0] and 0 <= xx < out.shape[1])
                if nb <= 2:
                    out[y, x, 3] = 0
    return Image.fromarray(out, 'RGBA')


def quantise(sprites):
    """Shared palette across a character's poses so they stay consistent."""
    strip = Image.new('RGBA', (sum(s.width for s in sprites), max(s.height for s in sprites)))
    x = 0
    for s in sprites:
        strip.paste(s, (x, 0)); x += s.width
    pal = strip.convert('RGB').quantize(COLOURS, method=Image.Quantize.MEDIANCUT)
    out = []
    for s in sprites:
        q = s.convert('RGB').quantize(palette=pal, dither=Image.Dither.NONE).convert('RGBA')
        q.putalpha(s.getchannel('A'))
        out.append(q)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for who, path in BOARDS.items():
        board = Image.open(path).convert('RGB')
        poses = [shrink(lift(board.crop(box))) for box in PANELS.values()]
        poses = quantise(poses)
        for name, img in zip(PANELS, poses):
            img.save(OUT / f'{who}-{name}.png')
        print(who, [p.size for p in poses])


if __name__ == '__main__':
    main()


# ----------------------------------------------- Logan revision: white shirt
# Lucas asked for the white shirt and black bow tie without the jacket.
# Per view: jacket rows, the existing light shirt strip (x range), and bow-tie pixels.
LOGAN_SHIRT = {
    'front': {'rows': (21, 39), 'strip': (9, 15), 'belt': 40, 'chest': (25, 32),
              'bow': [(9, 22), (14, 22), (9, 23), (10, 23), (11, 23), (12, 23), (13, 23), (14, 23),
                      (9, 24), (10, 24), (13, 24), (14, 24)]},
    'right': {'rows': (20, 39), 'strip': (8, 14), 'belt': 40, 'chest': (24, 32),
              'bow': [(10, 22), (11, 22), (12, 22), (11, 23), (12, 23)]},
    'back': {'rows': (18, 39), 'strip': None, 'belt': 40, 'chest': (22, 32), 'bow': []},
    'left': {'rows': (17, 39), 'strip': (3, 8), 'belt': 40, 'chest': (24, 32),
             'bow': [(5, 22), (6, 22), (7, 22), (5, 23), (6, 23)]},
}
SHIRT_RAMP = [(150, 146, 138), (196, 192, 183), (226, 223, 215), (246, 244, 238), (253, 252, 249)]
OUTLINE = (58, 54, 50)
BOW = (22, 22, 26)
BELT = (30, 28, 30)


def is_jacket(rgb):
    r, g, b = rgb
    mx = max(rgb)
    return mx < 100 and (mx - min(rgb)) / max(mx, 1) < 0.25


def white_shirt(img, spec):
    px = img.load()
    w, h = img.size
    y0, y1 = spec['rows']
    c0, c1 = spec['chest']
    targets = []
    for y in range(y0, y1 + 1):
        for x in range(w):
            r, g, b, a = px[x, y]
            if not a:
                continue
            lum = (r + g + b) / 3
            in_strip = (spec['strip'] and spec['strip'][0] <= x <= spec['strip'][1]
                        and c0 - 2 <= y < y1 - 3)
            if is_jacket((r, g, b)):
                targets.append((x, y, lum))
            elif (in_strip and lum > 110) or c0 <= y <= c1:
                targets.append((x, y, None))          # old tie / shirt strip / speckle -> plain shirt
    lums = sorted(l for _, _, l in targets if l is not None)
    lo, hi = lums[len(lums) // 20], lums[-len(lums) // 20 - 1]
    shirt = set()
    for x, y, lum in targets:
        if lum is None:
            k = 3
        else:                                      # stretch jacket shading across the shirt ramp
            k = round((min(max(lum, lo), hi) - lo) / max(hi - lo, 1) * 3.4 + 0.6)
        px[x, y] = SHIRT_RAMP[min(4, k)] + (255,)
        shirt.add((x, y))
    for x, y in shirt:
        for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] == 0:
                px[x, y] = OUTLINE + (255,)
                break
    y = spec['belt']
    for x in range(w):
        r, g, b, a = px[x, y]
        if a and is_jacket((r, g, b)):
            px[x, y] = BELT + (255,)
    for x, y in spec['bow']:
        px[x, y] = BOW + (255,)
    return img


def logan_revision():
    for view, spec in LOGAN_SHIRT.items():
        img = Image.open(OUT / f'logan-{view}.png').convert('RGBA')
        white_shirt(img, spec).save(OUT / f'logan-shirt-{view}.png')


if __name__ == '__main__':
    logan_revision()


# ---------------------------------------------------- walking sheet (step + bob)
FRAME_W, FRAME_H = 32, 72
SHEETS = {
    # id: (pose file prefix, kind, rows below which legs/hem move, per view)
    'logan': ('logan-shirt-', 'legs', {'front': 42, 'back': 42, 'right': 42, 'left': 42}),
    'angie': ('angie-', 'gown', {'front': 58, 'back': 58, 'right': 58, 'left': 58}),
}
VIEW_ROWS = ['front', 'right', 'back', 'left']        # sheet rows: down, right, up, left


def step(img, view, kind, hip, side):
    """side = -1 or +1: which foot steps. Returns a new image (same size)."""
    w, h = img.size
    src = img.load()
    out = Image.new('RGBA', (w, h + 2))
    dst = out.load()
    cx = w / 2
    for y in range(h):
        for x in range(w):
            p = src[x, y]
            if not p[3]:
                continue
            nx, ny = x, y
            if y >= hip:
                depth = (y - hip) / max(h - hip, 1)
                if kind == 'gown':
                    nx = x + round(side * depth * 1.6)          # hem sways
                elif view in ('front', 'back'):
                    if (x < cx) == (side < 0):
                        ny = y - 2                               # lifted foot
                else:
                    if depth > 0.35:                             # lower legs stride apart
                        nx = x + (side if x < cx else -side) * (1 if depth < 0.7 else 2)
            if 0 <= nx < w:
                dst[nx, ny + 1] = p
    return out.crop((0, 0, w, h + 1))                            # body bobs up 1 px


def build_sheets():
    runtime = ROOT / 'public' / 'sprites'
    runtime.mkdir(parents=True, exist_ok=True)
    for cid, (prefix, kind, hips) in SHEETS.items():
        sheet = Image.new('RGBA', (FRAME_W * 3, FRAME_H * 4))
        for r, view in enumerate(VIEW_ROWS):
            pose = Image.open(OUT / f'{prefix}{view}.png').convert('RGBA')
            frames = [pose, step(pose, view, kind, hips[view], -1), step(pose, view, kind, hips[view], +1)]
            for c, f in enumerate(frames):
                x = c * FRAME_W + (FRAME_W - f.width) // 2
                y = r * FRAME_H + FRAME_H - 1 - f.height + (1 if c else 0)
                sheet.alpha_composite(f, (x, y))
        sheet.save(runtime / f'{cid}-board.png')
        # Review images.
        big = sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST)
        bg = Image.new('RGBA', big.size, '#97b779'); bg.alpha_composite(big)
        bg.convert('RGB').save(OUT / f'{cid}-sheet-x6.png')
        gif = []
        for col in (1, 0, 2, 0):
            fr = Image.new('RGBA', (FRAME_W * 4 * 5, FRAME_H * 5), '#97b779')
            for r in range(4):
                cell = sheet.crop((col * FRAME_W, r * FRAME_H, (col + 1) * FRAME_W, (r + 1) * FRAME_H))
                fr.alpha_composite(cell.resize((FRAME_W * 5, FRAME_H * 5), Image.NEAREST), (r * FRAME_W * 5, 0))
            gif.append(fr.convert('RGB'))
        gif[0].save(OUT / f'{cid}-walking.gif', save_all=True, append_images=gif[1:], duration=180, loop=0)


if __name__ == '__main__':
    build_sheets()
