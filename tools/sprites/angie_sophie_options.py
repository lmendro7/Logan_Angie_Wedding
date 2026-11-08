"""Angie detail options and a skinnier Sophie, for Lucas to pick.

    python3 tools/sprites/angie_sophie_options.py

Lucas (November 8, 2026): Angie without glasses is right, but give her a
little more detail. Sophie's model needs to be skinnier (outfit still open).
Writes docs/art/cast-12/angie-options.png and docs/art/cast-12/sophie-skinny-options.png.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cast12 import ANGIE, SOPHIE, _sway, frame            # noqa: E402
from sophie_options import OUTFITS                        # noqa: E402
from styles import font                                   # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'docs' / 'art' / 'cast-12'

# ------------------------------------------------------------------ Angie
GOWN_DETAIL_F = ["..xDDDqDDqDDDx..", "..xDdDDDDDDdDx..", ".xDdDDdDDdDDdDx.", ".xDdDDdDDdDDdDx.",
                 "xdDdDDdDDdDDdDdx", "xxxxxxxxxxxxxxxx"]
GOWN_DETAIL_S = ["....xDDDDDDx....", "...xDdDDdDDx....", "...xDDdDDdDDx...", "..xDdDDdDDdDx...",
                 "..xdDDdDDdDDDx..", "..xxxxxxxxxxxx.."]
DETAIL = {
    'front': {2: "..xHJJHHHJJHHx..", 3: ".xHHJHHHHHHJHHx.", 4: ".xHhHHSSSSHHhHx.",
              6: "xHhSSSSSSSSSShHx", 7: "xHHSEESSSSEESHHx", 9: "xHhSpSSSSSSpShHx",
              10: "xHHhSSSmmSSShHHx", 11: "xhHHsSSSSSSsHHhx", 13: "xHhxSDSSSSDSxhHx",
              14: "xhHxSDdDDdDSxHhx", 16: "..xSxdDDDDdxSx..", 17: "..xsxwwqqwwxsx.."},
    'side': {2: "..xHJHHHHJHHx...", 4: ".xHhHHJHHHSSSx..", 6: "xHHJHHhHSSSSSx..",
             7: "xHHHHHHHSSEESx..", 9: "xHHHHHHHSpSSSx..", 12: "xhHHHHHhxxSSx..."},
    'back': {2: "..xHJJHHHHJJHx..", 4: ".xHHJHhHHhHJHHx.", 7: "xHHJHhHHHHhHJHHx",
             10: "xHhHHJHHHHJHHhHx", 13: "xHHhHhHHHHhHhHHx"},
}
FLOWER = {
    'front': {2: "..xHJJHHHJFfFx..", 3: ".xHHJHHHHHHFYFx.", 4: ".xHhHHSSSSHHfHx."},
    'side': {2: "..xHJHFfFJHHx...", 3: ".xHHHHFYFHHHHx..", 4: ".xHhHHHfHHSSSx.."},
    'back': {2: "..xFfFHHHHJJHx..", 3: ".xHFYFHHHHHHHHx.", 4: ".xHHfHhHHhHJHHx."},
}
VEIL = {
    'front': {1: "...xxVVVVVVxx...", 2: "..xVHJHHHJJHVx..", 6: "VHhSSSSSSSSSShHV", 9: "VHhSpSSSSSSpShHV",
              12: "VHHhhsSSSSshhHHV"},
    'side': {1: "...xVVVVVVxx....", 2: "..VVVHHHHJHHx...", 3: ".VVVHHHHHHHHx...", 5: "VVHHHHHHSSSSSx..",
             8: "VVHHHHHHSSSESSx.", 11: "VvHHHHHHxSSSx...", 13: "VvHHHxSSDDDx....", 14: "vvHHHxSDDDDx...."},
    'back': {1: "...xxVVVVVVxx...", 2: "..xVVVVVVVVVVx..", 3: ".xVVVVVVVVVVVVx.", 4: ".xVVvVVVVVVvVVx.",
             5: ".xVVVVVVVVVVVVx.", 6: "xHVVVVVVVVVVVVHx", 7: "xHVvVVVVVVVVvVHx", 8: "xHVVVVVVVVVVVVHx",
             9: "xHVVVVVVVVVVVVHx", 10: "xHVVvVVVVVVvVVHx", 11: "xHhVVVVVVVVVVhHx", 12: "xHHvVVVVVVVVvHHx",
             13: "xHHHvVVVVVVvHHHx"},
}
BOUQUET_F = {15: ".xxSxDDDDDDxSxx.", 16: "..xSxdDDDDdxSx..", 17: "..xxSSfFFfSSxx.."}
BOUQUET_F_LEGS = ["..xDGfFYFfGDDx..", "..xDdGGGGGdDDx.."]
BOUQUET_S = {15: "..xxxDSDDDx.....", 16: "....xDSDDGfx....", 17: "....xwsSfFYfx..."}

ANGIE_PAL = {**ANGIE['palette'], 'p': '#f2a7a0', 'q': '#cbb89a', 'F': '#fff6f0', 'f': '#f2b6c0',
             'Y': '#f0cf6a', 'V': '#f6f3ec', 'v': '#ddd8cc', 'G': '#5f8f4f'}

ANGIE_OPTIONS = [
    ('Current (no glasses)', 'for reference', [], False),
    ('A · More detail', 'hair highlights, lashes, blush, sash bow, skirt folds', [DETAIL], False),
    ('B · Detail + hair flower', 'small white-and-pink flower in her hair', [DETAIL, FLOWER], False),
    ('C · Detail + short veil', 'veil comb on top, veil falling behind', [DETAIL, VEIL], False),
    ('D · Detail + bouquet', 'holding a small bouquet', [DETAIL], True),
]


def angie_views(layers, bouquet):
    views = {}
    for view in ('front', 'side', 'back'):
        rows = list(ANGIE[view])
        for layer in layers:
            for n, r in layer.get(view, {}).items():
                rows[n] = r
        detailed = bool(layers)
        legs = (GOWN_DETAIL_F if view != 'side' else GOWN_DETAIL_S) if detailed else \
            (ANGIE['legs']['front'][0] if view != 'side' else ANGIE['legs']['side'][0])
        legs = list(legs)
        if bouquet and view == 'front':
            for n, r in BOUQUET_F.items():
                rows[n] = r
            legs[0:2] = BOUQUET_F_LEGS
        if bouquet and view == 'side':
            for n, r in BOUQUET_S.items():
                rows[n] = r
        views[view] = frame(rows + legs, ANGIE_PAL, f'angie {view}')
    return views


# ------------------------------------------------------------------ Sophie (skinny)
SLIM_HEAD_F = [
    ".....xxxxxx.....", "....xHHHHHHx....", "...xHHJHHHHHx...", "..xHHHHHHHHHHx..",
    "..xHHHHHHHHHHx..", "..xHSSSSSSSSHx..", "..xHSSSSSSSSHx..", "..xHSESSSSESHx..",
    "..xHSESSSSESHx..", "..xHSSSSSSSSHx..", "..xHSSSSmSSSHx..", "..xHHxSSSSxHHx..",
    "...xxxSSSSxxx...",
]
SLIM_HEAD_S = [
    "....xxxxxx......", "...xHHHHHHx.....", "..xHHHJHHHHx....", "..xHHHHHHHHHx...",
    "..xHHHHHHHHHx...", "..xHHHHHHSSSx...", "..xHHHHHSSSSx...", "..xHHHHsSSSESx..",
    "..xHHHHsSSSESSx.", "..xHHHHHSSSSx...", "..xHHHHHSSmSx...", "...xHHHHxSSx....",
    "....xxxxxSSx....",
]
SLIM_DRESS_F = ["...xVVVVVVVVx...", "..xvVVVVVVVVvx..", "..xxxxxxxxxxxx..", ".....xSxxSx.....",
                "....xOOxxOOx....", "....xxxxxxxx...."]
SLIM_DRESS_S = [".....xVVVVx.....", "....xvVVVVVx....", "....xxxxxxxx....", "......xSSx......",
                ".....xOOOOx.....", ".....xxxxxx....."]
SLIM_TROUSERS_F = ["..xxxNNNNNNxxx..", "....xNNxxNNx....", "....xNnxxnNx....", "...xOOOxxOOOx...",
                   "...xOOOxxOOOx...", "...xxxxxxxxxx..."]
SLIM_TROUSERS_S = [".....xNNNNx.....", "......xNNx......", "......xnNx......", ".....xOOOOx.....",
                   ".....xOOOOx.....", ".....xxxxxx....."]
SLIM_BODIES = [   # front rows 13-17, side rows 13-17, trousers?
    (["...xVVVSSVVVx...", "...xvVVVVVVvx...", "..xSxVVVVVVxSx..", "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx.."],
     [".....xVVVVx.....", ".....xvVVVx.....", ".....xvSVVx.....", ".....xvSVVx.....", ".....xvsvvx....."], False),
    (["...xVWWSSWWVx...", "...xvVWVVWVvx...", "..xSxVVVVVVxSx..", "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx.."],
     [".....xVVWVx.....", ".....xvVWVx.....", ".....xvSVVx.....", ".....xvSVVx.....", ".....xvsvvx....."], False),
    (["...xVVVSSVVVx...", "...xvVVVVVVvx...", "..xSxVVVVVVxSx..", "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx.."],
     [".....xVVVVx.....", ".....xvVVVx.....", ".....xvSVVx.....", ".....xvSVVx.....", ".....xvsvvx....."], False),
    (["...xTTTSSTTTx...", "...xtTTTTTTtx...", "..xtxTTTTTTxtx..", "..xtxTTTTTTxtx..", "..xsxTTTTTTxsx.."],
     [".....xTTTTx.....", ".....xtTTTx.....", ".....xtTTTx.....", ".....xttTTx.....", ".....xssTTx....."], False),
    (["...xTTTSSTTTx...", "...xRNNNNNNRx...", "..xTxNYNNYNxTx..", "..xSxNNNNNNxSx..", "..xsxNNNNNNxsx.."],
     [".....xTTTTx.....", ".....xRNNNx.....", ".....xTSNNx.....", ".....xRSNNx.....", ".....xNsNNx....."], True),
    (["...xKKVVVVKKx...", "...xkKVVVVKkx...", "..xkxKVVVVKxkx..", "..xkxKVVVVKxkx..", "..xsxKVVVVKxsx.."],
     [".....xKKVVx.....", ".....xkKVVx.....", ".....xkKVVx.....", ".....xkKVVx.....", ".....xsKVVx....."], True),
]


def sophie_views(i):
    name, blurb, _, pal, _, _ = OUTFITS[i]
    body_f, body_s, trousers = SLIM_BODIES[i]
    p = {**{k: v for k, v in SOPHIE['palette'].items() if k not in 'Vv'}, **pal}
    legs_f = SLIM_TROUSERS_F if trousers else SLIM_DRESS_F
    legs_s = SLIM_TROUSERS_S if trousers else SLIM_DRESS_S
    return (frame(SLIM_HEAD_F + body_f + legs_f, p, f'sophie {i} front'),
            frame(SLIM_HEAD_S + body_s + legs_s, p, f'sophie {i} side'), name, blurb)


def main():
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    # Angie board.
    k = 7
    board = Image.new('RGBA', (40 + 5 * 380, 520), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Angie — detail options (no glasses)', font=font(40), fill=INK)
    d.text((40, 86), 'Front, side and back at 7×; true size at 2× in the corner.', font=font(18, False), fill=MUTED)
    for i, (name, blurb, layers, bouquet) in enumerate(ANGIE_OPTIONS):
        v = angie_views(layers, bouquet)
        x0 = 40 + i * 380
        d.text((x0, 130), name, font=font(19), fill=INK)
        d.text((x0, 157), blurb, font=font(12, False), fill=MUTED)
        panel = Image.new('RGBA', (360, 300), '#97b779')
        for m, view in enumerate(('front', 'side', 'back')):
            panel.alpha_composite(v[view].resize((16 * k, 24 * k), Image.NEAREST), (4 + m * 118, 20))
        panel.alpha_composite(v['front'].resize((32, 48), Image.NEAREST), (318, 240))
        board.alpha_composite(panel, (x0, 185))
    board.convert('RGB').save(OUT / 'angie-options.png', optimize=True)

    # Sophie skinny board, with the current (wider) Sophie for comparison.
    board = Image.new('RGBA', (40 + 3 * 480, 140 + 2 * 330), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Sophie — skinnier, in each outfit', font=font(40), fill=INK)
    d.text((40, 86), 'Slimmer body, arms and legs, slightly slimmer head. Pick an outfit (1–6) and a design tweak '
                     'from the earlier board if wanted.', font=font(18, False), fill=MUTED)
    old = Image.open(Path(__file__).resolve().parents[2] / 'public/sprites/sophie.png').convert('RGBA').crop((0, 0, 16, 24))
    for i in range(6):
        f, s, name, blurb = sophie_views(i)
        x0, y0 = 40 + (i % 3) * 480, 140 + (i // 3) * 330
        d.text((x0, y0), name, font=font(20), fill=INK)
        d.text((x0, y0 + 27), blurb, font=font(14, False), fill=MUTED)
        panel = Image.new('RGBA', (450, 250), '#97b779')
        panel.alpha_composite(f.resize((16 * k, 24 * k), Image.NEAREST), (20, 60))
        panel.alpha_composite(s.resize((16 * k, 24 * k), Image.NEAREST), (150, 60))
        panel.alpha_composite(f.resize((32, 48), Image.NEAREST), (300, 180))
        panel.alpha_composite(old.resize((32, 48), Image.NEAREST), (370, 180))
        ImageDraw.Draw(panel).text((300, 162), 'new    old', font=font(12, False), fill='#1d3324')
        board.alpha_composite(panel, (x0, y0 + 52))
    board.convert('RGB').save(OUT / 'sophie-skinny-options.png', optimize=True)


if __name__ == '__main__':
    main()
