"""Cozy Garden environment art: the garden, the house, the ceremony and the bedroom.

    python3 tools/env/build_env.py

Lucas (November 8, 2026) gave full creative freedom over the environment:
"make it cozy and comfortable". The approved layout is unchanged: every path,
obstacle, collision box, ring and NPC position matches src/world.js and the
old code-drawn scenery. Only the look changes. All art is original pixel art
painted here with deterministic randomness (same output every run).

Writes public/env/:
  garden.png (768 x 900 ground: grass, paths, ceremony floor, hedges, flowers)
  bedroom.png (360 x 400, furniture included)
  house.png, tree.png, blossom.png, bench.png, arch.png, gate-closed.png,
  gate-open.png, fountain.png (2 frames), butterfly.png (2 frames x 3 colours),
  ring.png (2 frames)
Tall objects are separate images so characters can walk in front of and behind them.
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public' / 'env'
R = random.Random(20261108)

# ------------------------------------------------------------------ palette
GRASS = ['#86b863', '#7cad5a', '#8fc06b', '#93c470']
GRASS_DARK, GRASS_TUFT, GRASS_LIGHT = '#6a9c4c', '#5e8f45', '#a6d17e'
DIRT, DIRT_SHADE, DIRT_LIGHT, DIRT_EDGE, PEBBLE = '#dcbc8c', '#caa674', '#e8cc9e', '#b98f5e', '#bfa07a'
HEDGE, HEDGE_D, HEDGE_L, HEDGE_HL = '#3f7046', '#2f5636', '#55894f', '#79aa62'
FLOWERS = [('#f4a6b8', '#e07b95'), ('#fff3a8', '#e8c95a'), ('#ffffff', '#e4e0f0'), ('#c9a8f0', '#a07ad8'),
           ('#ffb37a', '#e88a4e')]
OUTLINE = '#3b2722'

# Layout, copied from the approved map (src/world.js and the old scenery code).
PATHS = [(362, 190, 44, 455), (195, 590, 211, 40), (183, 335, 36, 286), (384, 380, 204, 38),
         (570, 286, 36, 132), (360, 780, 183, 53), (505, 610, 38, 223), (384, 610, 159, 35),
         (362, 833, 44, 67)]
CEREMONY = (264, 34, 242, 165)
HEDGES = [(250, 20, 270, 12), (250, 20, 12, 196), (508, 20, 12, 196), (250, 200, 110, 16), (408, 200, 112, 16)]
HOUSE = (290, 650, 190, 130)
FOUNTAIN = (161, 295, 78, 47)
BENCH = (124, 460, 58, 20)
BORDER_TREES = [(x, y) for y in range(90, 880, 115) for x in (39, 728)]
FLOWER_BEDS = [(120, 280), (290, 390), (610, 570), (270, 550), (625, 720), (140, 795), (470, 470), (650, 160),
               (90, 640), (230, 700), (660, 860), (110, 160), (620, 480)]


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def put(px, x, y, c, w=None, h=None):
    if (w is None or 0 <= x < w) and (h is None or 0 <= y < h):
        px[x, y] = rgb(c) + (255,)


def in_rect(x, y, r, pad=0):
    return r[0] - pad <= x < r[0] + r[2] + pad and r[1] - pad <= y < r[1] + r[3] + pad


# ------------------------------------------------------------------ garden ground
def garden():
    W, H = 768, 900
    img = Image.new('RGBA', (W, H))
    px = img.load()
    # Grass: one soft green with gentle, rounded patches (low-frequency waves),
    # lightly dithered at the patch edges, then tufts and tiny flowers.
    import math
    base, patch = rgb('#86b863'), rgb('#7fb05c')
    for y in range(H):
        for x in range(W):
            n = (math.sin(x / 37.0) + math.sin(y / 29.0 + x / 61.0) + math.sin((x + y) / 47.0)) / 3
            c = patch if n + (R.random() - .5) * .18 > .32 else base
            px[x, y] = c + (255,)
    for _ in range(2600):                                         # grass tufts
        x, y = R.randrange(2, W - 2), R.randrange(3, H)
        put(px, x, y, GRASS_TUFT, W, H); put(px, x - 1, y - 1, GRASS_TUFT, W, H); put(px, x + 1, y - 1, GRASS_TUFT, W, H)
        put(px, x, y - 2, GRASS_DARK, W, H)
    for _ in range(1400):
        put(px, R.randrange(W), R.randrange(H), GRASS_LIGHT, W, H)
    for _ in range(260):                                          # tiny wildflowers
        x, y = R.randrange(W), R.randrange(H)
        put(px, x, y, R.choice(['#ffffff', '#fff3a8', '#f7c6d6']), W, H)

    # Dirt paths with wobbly grassy edges, a darker rim and pebbles.
    path_mask = [[False] * W for _ in range(H)]
    for (x0, y0, w, h) in PATHS:
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if 0 <= x < W and 0 <= y < H:
                    path_mask[y][x] = True
    for y in range(H):                                            # wobble edges
        for x in range(W):
            if path_mask[y][x]:
                edge = any(not path_mask[yy][xx] for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                           if 0 <= xx < W and 0 <= yy < H)
                if edge and R.random() < .35 and not (y >= 833 and 362 <= x < 406):
                    path_mask[y][x] = 'grass'
    for y in range(H):
        for x in range(W):
            if path_mask[y][x] is True:
                c = DIRT if R.random() > .12 else (DIRT_SHADE if R.random() < .6 else DIRT_LIGHT)
                put(px, x, y, c)
    for y in range(H):                                            # rim
        for x in range(W):
            if path_mask[y][x] is True:
                if any(path_mask[yy][xx] is not True for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                       if 0 <= xx < W and 0 <= yy < H):
                    put(px, x, y, DIRT_EDGE)
    for _ in range(420):                                          # pebbles
        x, y = R.randrange(W), R.randrange(H)
        if path_mask[y][x] is True and path_mask[min(H - 1, y + 1)][x] is True:
            put(px, x, y, PEBBLE); put(px, x, y + 1, DIRT_EDGE)

    # Ceremony floor: cream stone tiles, a petal-strewn aisle runner.
    cx, cy, cw, ch = CEREMONY
    for y in range(cy, cy + ch):
        for x in range(cx, cx + cw):
            gx, gy = (x - cx) % 16, (y - cy) % 16
            base = '#ece2c8' if ((x - cx) // 16 + (y - cy) // 16) % 2 else '#e6dbbf'
            if gx == 0 or gy == 0:
                base = '#d6c9a8'
            elif gx == 1 or gy == 1:
                base = '#f5ecd6'
            put(px, x, y, base)
    for y in range(64, 199):                                      # aisle runner
        for x in range(368, 400):
            c = '#fbf7ee' if 370 <= x < 398 else '#e8b4c0'
            if x in (369, 398):
                c = '#d98ea2'
            put(px, x, y, c)
    for _ in range(70):
        x, y = R.randrange(366, 402), R.randrange(66, 198)
        put(px, x, y, R.choice(['#f4a6b8', '#f7c6d6', '#ffffff', '#e07b95']))
    for side in (296, 464):                                       # flower pots along the aisle
        for y in (92, 128, 164):
            for dx in range(-5, 6):
                for dy in range(0, 6):
                    put(px, side + dx, y + dy, '#c26a4a' if dy > 1 else '#a8553a')
            for dx, dy, c in ((-3, -3, '#f4a6b8'), (0, -5, '#ffffff'), (3, -3, '#f4a6b8'), (-1, -2, '#5f9a4f'),
                              (1, -2, '#5f9a4f'), (0, -1, '#4f8a45'), (-4, -1, '#5f9a4f'), (4, -1, '#5f9a4f'),
                              (-2, -4, '#fff3a8'), (2, -4, '#e07b95')):
                put(px, side + dx, y + dy, c)

    # Hedges: leafy walls with a lit top and a shadow at the base.
    for (x0, y0, w, h) in HEDGES:
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                put(px, x, y, HEDGE)
        for _ in range(w * h // 5):
            x, y = R.randrange(x0, x0 + w), R.randrange(y0, y0 + h)
            put(px, x, y, R.choice([HEDGE_L, HEDGE_L, HEDGE_D]))
        for x in range(x0, x0 + w):
            put(px, x, y0, HEDGE_HL); put(px, x, y0 + 1, HEDGE_L if R.random() < .6 else HEDGE_HL)
            put(px, x, y0 + h - 1, HEDGE_D)
            if y0 + h < H and not in_rect(x, y0 + h, CEREMONY):
                put(px, x, y0 + h, '#5e8f45')                    # soft shadow on the grass
        for y in range(y0, y0 + h):
            put(px, x0, y, HEDGE_D); put(px, x0 + w - 1, y, HEDGE_D)
        for _ in range(w * h // 60):                              # little white blossoms
            put(px, R.randrange(x0 + 1, x0 + w - 1), R.randrange(y0 + 1, y0 + h - 1), '#fbf3f6')

    # Flower beds: clusters of five-petal flowers with leaves.
    def flower(x, y, petal, centre):
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, -2), (-2, 0), (2, 0)):
            put(px, x + dx, y + dy, petal if abs(dx) + abs(dy) < 3 else petal, W, H)
        for dx, dy in ((-1, 1), (1, 1)):
            put(px, x + dx, y + dy, petal, W, H)
        put(px, x, y, centre, W, H)
        put(px, x, y + 2, '#4f8a45', W, H); put(px, x - 1, y + 3, '#5f9a4f', W, H); put(px, x + 1, y + 3, '#4f8a45', W, H)
    for (fx, fy) in FLOWER_BEDS:
        petal, centre = R.choice(FLOWERS)
        for _ in range(60):                                       # leafy base
            x, y = fx + R.randrange(-16, 17), fy + R.randrange(-8, 10)
            if ((x - fx) / 16) ** 2 + ((y - fy) / 9) ** 2 <= 1 and not any(in_rect(x, y, p, 3) for p in PATHS):
                put(px, x, y, R.choice(['#5f9a4f', '#6aa556', '#4f8a45']), W, H)
        for _ in range(20):
            x, y = fx + R.randrange(-14, 15), fy + R.randrange(-7, 8)
            if not any(in_rect(x, y, p, 3) for p in PATHS) and not in_rect(x, y, CEREMONY, 3):
                flower(x, y, petal, centre if R.random() < .7 else '#fff3a8')

    # Round bushes tucked beside the house, the ceremony hedge and the fence.
    def bush(cx, cy, r=8):
        for y in range(cy - r, cy + r):
            for x in range(cx - r - 3, cx + r + 3):
                e = ((x - cx) / (r + 3)) ** 2 + ((y - cy) / r) ** 2
                if e <= 1:
                    lit = (x - cx) + (y - cy) < -r * .4
                    c = '#79aa62' if lit else ('#3f7046' if e > .75 or (y - cy) > r * .4 else '#55894f')
                    put(px, x, y, c, W, H)
        for _ in range(r * 2):
            put(px, cx + R.randrange(-r, r), cy + R.randrange(-r + 2, r - 2), '#fbf3f6' if R.random() < .3 else '#3f7046', W, H)
    for (bx, by) in ((262, 760), (500, 600), (236, 222), (532, 222), (330, 872), (440, 872), (150, 560), (620, 300),
                     (95, 420), (660, 640)):
        bush(bx, by)

    # A low picket fence along the bottom edge (outside the walkable area).
    for x in range(0, W):
        if x % 6 in (0, 1, 2):
            for y in range(884, 898):
                put(px, x, y, '#f4ead7' if x % 6 != 2 else '#d9cdb6')
            put(px, x, 883, '#fbf6ea')
        put(px, x, 888, '#e0d4bc'); put(px, x, 893, '#e0d4bc')
    for y in range(884, 898):
        for x in range(362, 406):
            put(px, x, y, DIRT)                                   # gap where the path leaves
    return img


# ------------------------------------------------------------------ objects
def canvas(w, h):
    img = Image.new('RGBA', (w, h))
    return img, img.load(), ImageDraw.Draw(img)


def house():
    """Cottage over the collision box (290..480 x 650..780). Image 214 x 176, base = y 780."""
    w, h = 214, 176
    img, px, d = canvas(w, h)
    ox = 12                                                       # wall x 12..201 = world 290..479
    wall_top, base = 64, 170                                      # base row = world y 780
    # Walls: warm horizontal planks.
    for y in range(wall_top, base):
        for x in range(ox, ox + 190):
            row = (y - wall_top) % 7
            c = '#e2b27a' if row else '#b98552'
            if row == 1:
                c = '#efc48e'
            if (x - ox) % 47 == 0 and row:
                c = '#c9955f'
            px[x, y] = rgb(c) + (255,)
    for y in range(base - 8, base):                               # stone foundation
        for x in range(ox, ox + 190):
            c = '#a89c8c' if ((x - ox) // 9 + (y - base) // 4) % 2 else '#968a7a'
            if (x - ox) % 9 == 0 or y == base - 8:
                c = '#7d7266'
            px[x, y] = rgb(c) + (255,)
    for y in range(wall_top, base):                               # corner posts
        for x in list(range(ox, ox + 4)) + list(range(ox + 186, ox + 190)):
            px[x, y] = rgb('#8a5c38' if x in (ox, ox + 189) else '#a8744a') + (255,)
    # Roof: terracotta shingles with scalloped rows, overhanging eaves.
    roof_top = 10
    for y in range(roof_top, wall_top + 6):
        inset = max(0, (wall_top - y) // 4) if y < 30 else 0
        for x in range(inset, w - inset):
            row = (y - roof_top) // 6
            scallop = ((x + (row % 2) * 4) % 8)
            c = '#c05a40' if (y - roof_top) % 6 else '#8f3d2c'
            if (y - roof_top) % 6 == 5 and scallop in (0, 7):
                c = '#8f3d2c'
            if (y - roof_top) % 6 == 1:
                c = '#d6704f'
            px[x, y] = rgb(c) + (255,)
    for x in range(0, w):                                         # eave edge and shadow under it
        px[x, wall_top + 6] = rgb('#7a3426') + (255,)
        for k in range(1, 4):
            if ox <= x < ox + 190:
                r, g, b, _ = px[x, wall_top + 6 + k]
                px[x, wall_top + 6 + k] = (int(r * .78), int(g * .74), int(b * .72), 255)
    for x in range(10, w - 10):                                   # ridge cap
        px[x, roof_top] = rgb('#7a3426') + (255,); px[x, roof_top + 1] = rgb('#a84a35') + (255,)
    # Chimney.
    for y in range(0, 26):
        for x in range(30, 44):
            c = '#a0958a' if ((x - 30) // 5 + y // 4) % 2 else '#8c8176'
            if y == 0 or x in (30, 43):
                c = '#6f665d'
            px[x, y] = rgb(c) + (255,)
    # Windows with shutters and flower boxes (world x 311..345 and 426..460).
    for wx in (ox + 21, ox + 136):
        for y in range(wall_top + 24, wall_top + 58):
            for x in range(wx - 6, wx + 40):
                if wx - 6 <= x < wx or wx + 34 <= x < wx + 40:      # shutters
                    c = '#5f8f6a' if (y % 4) else '#4a7556'
                elif wx <= x < wx + 34:
                    c = '#f4ead7' if x in (wx, wx + 33, wx + 16, wx + 17) or y in (wall_top + 24, wall_top + 57, wall_top + 40) else '#a9d6e4'
                    if c == '#a9d6e4' and (x - wx) + (y - wall_top - 24) < 12 and (x - wx) % 5 == 1:
                        c = '#d8f0f6'                                # glint
                px[x, y] = rgb(c) + (255,)
        for y in range(wall_top + 58, wall_top + 64):             # flower box
            for x in range(wx - 2, wx + 36):
                px[x, y] = rgb('#8a5c38' if y > wall_top + 59 else '#a8744a') + (255,)
        for x in range(wx - 1, wx + 35, 3):
            petal = R.choice(['#f4a6b8', '#e07b95', '#fff3a8', '#ffffff'])
            px[x, wall_top + 56] = rgb(petal) + (255,); px[x + 1, wall_top + 57] = rgb('#5f9a4f') + (255,)
            px[x, wall_top + 57] = rgb('#4f8a45') + (255,)
    # Door (world x 361..407, y 738..780) with panels, knob and a lantern.
    dx0 = ox + 71
    for y in range(base - 46, base):
        for x in range(dx0, dx0 + 46):
            c = '#8a5a3a'
            if x in (dx0, dx0 + 45) or y == base - 46:
                c = '#5e3c24'
            elif (dx0 + 6 <= x < dx0 + 20 or dx0 + 26 <= x < dx0 + 40) and (base - 40 <= y < base - 26 or base - 22 <= y < base - 6):
                c = '#7a4e30' if (x in (dx0 + 6, dx0 + 26) or y in (base - 40, base - 22)) else '#9a6a46'
            px[x, y] = rgb(c) + (255,)
    for y in range(base - 52, base - 46):                         # door canopy
        for x in range(dx0 - 4, dx0 + 50):
            px[x, y] = rgb('#a84a35' if y > base - 50 else '#7a3426') + (255,)
    for xy in ((dx0 + 38, base - 24), (dx0 + 38, base - 23)):
        px[xy] = rgb('#e8c55a') + (255,)
    for y in range(base - 44, base - 32):                         # lantern
        for x in range(dx0 + 50, dx0 + 56):
            c = '#ffe9a0' if 1 <= x - dx0 - 50 <= 4 and base - 42 <= y <= base - 34 else '#3b2722'
            px[x, y] = rgb(c) + (255,)
    # Outline.
    out = img.copy()
    opx = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and any(not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] == 0
                                   for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                opx[x, y] = rgb(OUTLINE) + (255,)
    return out


def tree(blossom=False):
    """Round tree; image 72 x 92, trunk base at the bottom centre."""
    w, h = 72, 92
    img, px, d = canvas(w, h)
    leaf = (['#e9a3b8', '#f4bccd', '#fbd6e1', '#d6829c'] if blossom else
            ['#4f9150', '#5fa257', '#7cbc66', '#3f7a45'])
    # Ground shadow.
    for y in range(h - 7, h - 1):
        for x in range(10, w - 10):
            if ((x - w / 2) / 26) ** 2 + ((y - (h - 4)) / 3.5) ** 2 <= 1:
                px[x, y] = (40, 70, 45, 70)
    # Trunk.
    for y in range(h - 30, h - 3):
        for x in range(w // 2 - 6, w // 2 + 6):
            c = '#7a5a3e' if x > w // 2 - 3 else '#5e432d'
            if (y + x) % 7 == 0:
                c = '#4e3826'
            px[x, y] = rgb(c) + (255,)
    for x in (w // 2 - 8, w // 2 - 7, w // 2 + 6, w // 2 + 7):     # roots
        px[x, h - 4] = rgb('#5e432d') + (255,)
    # Canopy: overlapping round clumps, lit from the upper left.
    clumps = [(36, 30, 26), (20, 40, 16), (52, 40, 16), (28, 20, 14), (46, 20, 14), (36, 50, 18)]
    for cx, cy, r in clumps:
        for y in range(cy - r, cy + r):
            for x in range(cx - r, cx + r):
                if 0 <= x < w and 0 <= y < h and (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    lit = (x - cx) + (y - cy) < -r * .5
                    dark = (x - cx) + (y - cy) > r * .6
                    c = leaf[2] if lit else (leaf[3] if dark else leaf[0])
                    px[x, y] = rgb(c) + (255,)
    for _ in range(160):                                          # leaf texture
        x, y = R.randrange(6, w - 6), R.randrange(4, 66)
        if px[x, y][3]:
            px[x, y] = rgb(R.choice(leaf[:3])) + (255,)
    if blossom:
        for _ in range(55):
            x, y = R.randrange(8, w - 8), R.randrange(6, 64)
            if px[x, y][3]:
                px[x, y] = rgb('#ffffff') + (255,)
    else:
        for _ in range(10):                                       # a few apples
            x, y = R.randrange(14, w - 14), R.randrange(14, 58)
            if px[x, y][3]:
                px[x, y] = rgb('#e2574a') + (255,); px[x, y + 1] = rgb('#b8433a') + (255,)
    out = img.copy()
    opx = out.load()
    for y in range(h - 8):
        for x in range(w):
            if px[x, y][3] == 255 and any(not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] < 255
                                          for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                opx[x, y] = rgb('#5a2f3a' if blossom else '#2f4a2c') + (255,)
    return out


def bench():
    """Wooden bench over 124..182 x 460..480; image 62 x 30, base = y 480."""
    w, h = 62, 30
    img, px, d = canvas(w, h)
    for y in range(2, 12):                                        # backrest slats
        for x in range(2, 60):
            c = '#b07a44' if (y - 2) % 4 else '#8a5c30'
            px[x, y] = rgb(c) + (255,)
    for y in range(14, 22):                                       # seat
        for x in range(1, 61):
            c = '#c48a50' if (y - 14) % 3 else '#94643a'
            px[x, y] = rgb(c) + (255,)
    for x0 in (4, 54):                                            # legs
        for y in range(12, 29):
            for x in range(x0, x0 + 4):
                px[x, y] = rgb('#6e4a2a') + (255,)
    out = img.copy(); opx = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and any(not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] == 0
                                   for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                opx[x, y] = rgb(OUTLINE) + (255,)
    return out


def arch():
    """Wedding arch: posts at world x 300..312 and 456..468, beam at y 53..68; image 180 x 106, base = y 152."""
    w, h = 180, 106
    img, px, d = canvas(w, h)
    ox = 6                                                        # world x 294 at image x 0
    for x0 in (300 - 294, 456 - 294):
        for y in range(14, h - 2):
            for x in range(x0, x0 + 12):
                c = '#fbf6ea' if x - x0 < 8 else '#e2d8c2'
                px[x, y] = rgb(c) + (255,)
        for y in range(h - 6, h):                                 # post feet
            for x in range(x0 - 2, x0 + 14):
                px[x, y] = rgb('#d9cdb6') + (255,)
    for y in range(4, 18):                                        # curved top beam
        for x in range(2, w - 2):
            curve = int(((x - w / 2) / (w / 2)) ** 2 * 6)
            if y >= 4 + curve and y < 14 + curve:
                px[x, y] = rgb('#fbf6ea' if y < 10 + curve else '#e2d8c2') + (255,)
    # Vines and roses.
    for _ in range(260):
        x, y = R.randrange(0, w), R.randrange(0, h)
        if px[x, y][3] and R.random() < .5:
            px[x, y] = rgb(R.choice(['#5f9a4f', '#4f8a45', '#79aa62'])) + (255,)
    for _ in range(90):
        x, y = R.randrange(2, w - 2), R.randrange(0, h - 8)
        if px[x, y][3]:
            petal = R.choice(['#f4a6b8', '#e07b95', '#ffffff', '#fbd6e1'])
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                if 0 <= x + dx < w and px[x + dx, y + dy][3]:
                    px[x + dx, y + dy] = rgb(petal if (dx, dy) != (1, 1) else '#c25a78') + (255,)
    out = img.copy(); opx = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and any(not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] == 0
                                   for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                opx[x, y] = rgb('#8a7a66') + (255,)
    return out


def gate(open_):
    """Picket gate between the hedges (world 360..408 x 200..216); image 60 x 30, base = y 216."""
    w, h = 60, 30
    img, px, d = canvas(w, h)
    for x0 in (2, 52):                                            # posts
        for y in range(2, h):
            for x in range(x0, x0 + 6):
                px[x, y] = rgb('#8a5c38' if x == x0 else '#a8744a') + (255,)
        for x in range(x0 - 1, x0 + 7):
            px[x, 1] = rgb('#6e4a2a') + (255,)
    if not open_:
        for x in range(8, 52):                                    # pickets and rails
            if (x - 8) % 6 < 4:
                for y in range(6 - (1 if (x - 8) % 6 in (1, 2) else 0), h - 2):
                    px[x, y] = rgb('#f4ead7' if (x - 8) % 6 < 3 else '#d9cdb6') + (255,)
        for y in (11, 21):
            for x in range(8, 52):
                px[x, y] = rgb('#c9b996') + (255,)
        for x in range(28, 32):                                   # latch
            px[x, 16] = rgb('#3b2722') + (255,)
    else:
        for x0, x1 in ((8, 14), (46, 52)):                        # halves swung open, seen edge-on
            for x in range(x0, x1):
                for y in range(5, h - 2):
                    px[x, y] = rgb('#f4ead7' if (x - x0) % 3 else '#d9cdb6') + (255,)
    out = img.copy(); opx = out.load()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and any(not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] == 0
                                   for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                opx[x, y] = rgb(OUTLINE) + (255,)
    return out


def fountain():
    """Stone fountain over 161..239 x 295..342; 2 frames of 90 x 84, base = y 342."""
    frames = []
    for f in range(2):
        w, h = 90, 84
        img, px, d = canvas(w, h)
        cx, base = 45, 83
        for y in range(base - 46, base):                          # basin rim and water
            for x in range(6, 84):
                ex = ((x - cx) / 39) ** 2 + ((y - (base - 22)) / 22) ** 2
                if ex <= 1:
                    inner = ((x - cx) / 32) ** 2 + ((y - (base - 23)) / 16) ** 2
                    if inner <= 1:
                        c = '#7ec4d6'
                        if (x * 3 + y * 5 + f * 7) % 23 < 2:
                            c = '#bfe8f0'
                        elif (x + y + f * 3) % 17 == 0:
                            c = '#6aaec2'
                    else:
                        c = '#c8c1b4' if (x - cx) + (y - base) < -10 else '#a8a094'
                        if ((x // 6) + (y // 4)) % 2 and inner > 1.3:
                            c = '#b8b0a2'
                    px[x, y] = rgb(c) + (255,)
        for y in range(base - 70, base - 26):                     # pillar
            for x in range(cx - 4, cx + 4):
                px[x, y] = rgb('#d4cdbf' if x < cx else '#b0a898') + (255,)
        for y in range(base - 72, base - 64):                     # top bowl
            for x in range(cx - 12, cx + 12):
                if abs(x - cx) <= 12 - (y - (base - 72)):
                    px[x, y] = rgb('#c8c1b4') + (255,)
        for k in range(12):                                       # water spray, alternating frames
            x = cx - 12 + k * 2 + f
            for y in range(base - 66 + (k % 3), base - 50 + (k % 4) * 3, 2):
                if 0 <= x < w and abs(x - cx) > 6:
                    px[x, y] = rgb('#d8f0f6') + (255,)
        for y in range(base - 80, base - 72):                     # spout jet
            px[cx, y] = rgb('#d8f0f6' if (y + f) % 2 else '#a9dde8') + (255,)
        out = img.copy(); opx = out.load()
        for y in range(h):
            for x in range(w):
                if px[x, y][3] and any(not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] == 0
                                       for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                    opx[x, y] = rgb('#6f665d') + (255,)
        frames.append(out)
    sheet = Image.new('RGBA', (90 * 2, 84))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * 90, 0))
    return sheet


def butterflies():
    """3 colours x 2 frames, 8 x 7 each."""
    sheet = Image.new('RGBA', (8 * 6, 7))
    px = sheet.load()
    colours = [('#fbd6e1', '#e07b95'), ('#fff3a8', '#e8a94e'), ('#d8ecff', '#7aa6e0')]
    for c, (wing, edge) in enumerate(colours):
        for f in range(2):
            ox = (c * 2 + f) * 8
            for y in range(1, 6):
                px[ox + 3, y] = rgb('#3b2722') + (255,); px[ox + 4, y] = rgb('#3b2722') + (255,)
            spread = [(0, 1), (1, 0), (1, 1), (0, 2), (1, 2), (2, 1), (2, 2), (1, 3), (0, 4), (1, 4)] if f == 0 else \
                     [(2, 1), (2, 2), (1, 2), (2, 3), (1, 3)]
            for dx, dy in spread:
                for x in (ox + dx, ox + 7 - dx):
                    px[x, dy + 1] = rgb(wing if dx > 0 or f else edge) + (255,)
    return sheet


def ring():
    """Gold ring with a twinkle; 2 frames of 13 x 13."""
    sheet = Image.new('RGBA', (26, 13))
    px = sheet.load()
    for f in range(2):
        ox = f * 13
        for y in range(13):
            for x in range(13):
                dist = ((x - 6) ** 2 + (y - 7) ** 2) ** .5
                if 2.6 <= dist <= 4.2:
                    px[ox + x, y] = rgb('#f1cf6a' if (x - 6) + (y - 7) < 0 else '#c9a03f') + (255,)
        px[ox + 6, 2] = rgb('#d8f0f6') + (255,)                   # tiny gem
        if f:
            for dx, dy in ((10, 1), (11, 2), (9, 2), (10, 3), (10, 2)):
                px[ox + dx, dy] = rgb('#ffffff') + (255,)
    return sheet


# ------------------------------------------------------------------ bedroom
def bedroom():
    W, H = 360, 400
    img = Image.new('RGBA', (W, H))
    px = img.load()
    for y in range(H):                                            # honey floorboards
        for x in range(W):
            row = y // 12
            seam = (x + row * 37) % 72 == 0
            c = '#cf9c62' if y % 12 else '#a87a48'
            if y % 12 == 1:
                c = '#dcae74'
            if seam:
                c = '#a87a48'
            px[x, y] = rgb(c) + (255,)
    for y in range(0, 44):                                        # wallpaper with little flowers
        for x in range(W):
            c = '#efe1c4' if (x // 6) % 2 else '#e8d8b8'
            if (x % 24 == 12 and y % 14 == 7):
                c = '#e8a9b6'
            px[x, y] = rgb(c) + (255,)
    for y in range(40, 48):                                       # wainscot trim
        for x in range(W):
            px[x, y] = rgb('#8a6440' if y in (40, 47) else '#a8794e') + (255,)
    # Window with curtains (154..206 x 7..36).
    for y in range(7, 37):
        for x in range(154, 207):
            c = '#9fd3e6' if y < 26 else '#b8e2ee'
            if x in (154, 206, 180, 181) or y in (7, 36, 21):
                c = '#f4ead7'
            px[x, y] = rgb(c) + (255,)
    for cx0, cy0 in ((162, 13), (190, 15)):                       # clouds
        for dx in range(-3, 5):
            px[cx0 + dx, cy0] = rgb('#ffffff') + (255,)
        for dx in range(-1, 3):
            px[cx0 + dx, cy0 - 1] = rgb('#ffffff') + (255,)
    for x0 in (146, 207):                                         # curtains
        for y in range(4, 40):
            for x in range(x0, x0 + 8):
                c = '#e89aac' if (x - x0) % 3 else '#c97a8e'
                px[x, y] = rgb(c) + (255,)
    for x in range(140, 222):                                     # curtain rod
        px[x, 4] = rgb('#6e4a2a') + (255,); px[x, 3] = rgb('#8a5c38') + (255,)
    # Picture frames on the wall: a little heart and a landscape.
    for (x0, y0, inner) in ((40, 12, '#f4d6dc'), (290, 10, '#bfe0c8')):
        for y in range(y0, y0 + 20):
            for x in range(x0, x0 + 26):
                c = '#8a5c38' if x in (x0, x0 + 25) or y in (y0, y0 + 19) else inner
                px[x, y] = rgb(c) + (255,)
    for dx, dy in ((10, 7), (11, 6), (12, 7), (13, 6), (14, 7), (10, 8), (11, 9), (12, 10), (13, 9), (14, 8), (11, 7), (12, 8), (13, 7), (12, 9), (11, 8), (13, 8)):
        px[40 + dx, 12 + dy] = rgb('#e07b95') + (255,)
    for x in range(291, 315):
        for y in range(20, 29):
            px[x, y] = rgb('#7cad5a' if y > 22 + (x % 5 == 0) else '#bfe0c8') + (255,)
    # Bed (42..115 x 77..189): wooden frame, pillows, patchwork quilt.
    for y in range(72, 192):
        for x in range(40, 118):
            px[x, y] = rgb('#8a5a3a') + (255,)
    for y in range(66, 80):                                       # headboard
        for x in range(40, 118):
            px[x, y] = rgb('#a8744a' if y > 67 else '#6e4a2a') + (255,)
    for y in range(82, 104):                                      # pillows
        for x in range(46, 112):
            c = '#fbf8f1' if (x - 46) % 33 not in (0, 32) else '#e0d8c9'
            if y in (82, 103):
                c = '#e0d8c9'
            px[x, y] = rgb(c) + (255,)
    quilt = ['#8fc0a0', '#f4d6dc', '#f4ead7', '#e8b4c0', '#a9cbd8', '#f7e3a8']
    for y in range(104, 186):
        for x in range(46, 112):
            cell = ((x - 46) // 11 + (y - 104) // 11 * 2) % len(quilt)
            c = quilt[cell]
            if (x - 46) % 11 == 0 or (y - 104) % 11 == 0:
                c = '#fbf8f1'
            px[x, y] = rgb(c) + (255,)
    for x in range(46, 112):                                      # quilt fold
        px[x, 106] = rgb('#d4cbb6') + (255,)
    # Dresser (228..323 x 52..98) with a lamp, a photo and a plant on top.
    for y in range(58, 100):
        for x in range(226, 325):
            c = '#a8744a'
            if x in (226, 324) or y in (58, 99):
                c = '#6e4a2a'
            elif y in (72, 86):
                c = '#8a5c38'
            px[x, y] = rgb(c) + (255,)
    for y in (64, 78, 92):                                        # knobs
        for x in (262, 288):
            px[x, y] = rgb('#e8c55a') + (255,); px[x + 1, y] = rgb('#e8c55a') + (255,)
    for y in range(44, 58):                                       # lamp
        for x in range(236, 248):
            if y < 52 and abs(x - 242) <= (y - 44) // 2 + 2:
                px[x, y] = rgb('#f7e3a8') + (255,)
            elif y >= 52 and 241 <= x <= 243:
                px[x, y] = rgb('#6e4a2a') + (255,)
    for y in range(48, 58):                                       # photo frame
        for x in range(262, 274):
            px[x, y] = rgb('#8a5c38' if x in (262, 273) or y in (48, 57) else '#f4d6dc') + (255,)
    for y in range(50, 58):                                       # plant
        for x in range(300, 310):
            px[x, y] = rgb('#c26a4a') + (255,)
    for dx, dy in ((0, -2), (-3, -4), (3, -4), (-1, -6), (2, -7), (-4, -2), (4, -2), (0, -5), (1, -3), (-2, -3)):
        px[305 + dx, 50 + dy] = rgb(R.choice(['#5f9a4f', '#4f8a45', '#79aa62'])) + (255,)
    # Woven oval rug.
    for y in range(232, 324):
        for x in range(120, 242):
            e = ((x - 181) / 60) ** 2 + ((y - 278) / 45) ** 2
            if e <= 1:
                ring_ = int(e * 6)
                c = ['#e8d2a8', '#a9cbd8', '#f4ead7', '#e8b4c0', '#f4ead7', '#8fb0c0', '#d9c39a'][ring_]
                px[x, y] = rgb(c) + (255,)
    # Doorway and doormat at the bottom (151..209 x 366..400).
    for y in range(370, 400):
        for x in range(150, 210):
            c = '#6e4a2a' if x in (150, 151, 208, 209) else '#d9bd87'
            px[x, y] = rgb(c) + (255,)
    for y in range(374, 396):
        for x in range(158, 202):
            c = '#b0603f' if (x + y) % 4 else '#9a5034'
            if x in (158, 201) or y in (374, 395):
                c = '#7a3c26'
            px[x, y] = rgb(c) + (255,)
    for x, y in ((170, 384), (175, 384), (180, 384), (185, 384), (190, 384)):
        px[x, y] = rgb('#f4ead7') + (255,)
    # A potted plant and a little bookshelf in the free corners.
    for y in range(330, 352):
        for x in range(320, 336):
            px[x, y] = rgb('#c26a4a' if y > 340 else '#a8553a') + (255,)
    for _ in range(40):
        x, y = R.randrange(316, 340), R.randrange(312, 340)
        if ((x - 328) / 12) ** 2 + ((y - 328) / 14) ** 2 <= 1:
            px[x, y] = rgb(R.choice(['#5f9a4f', '#4f8a45', '#79aa62'])) + (255,)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    garden().save(OUT / 'garden.png', optimize=True)
    bedroom().save(OUT / 'bedroom.png', optimize=True)
    house().save(OUT / 'house.png')
    tree().save(OUT / 'tree.png')
    tree(blossom=True).save(OUT / 'blossom.png')
    bench().save(OUT / 'bench.png')
    arch().save(OUT / 'arch.png')
    gate(False).save(OUT / 'gate-closed.png')
    gate(True).save(OUT / 'gate-open.png')
    fountain().save(OUT / 'fountain.png')
    butterflies().save(OUT / 'butterfly.png')
    ring().save(OUT / 'ring.png')


if __name__ == '__main__':
    main()
