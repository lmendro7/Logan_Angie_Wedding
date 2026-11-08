"""Sophie options: outfits and small design adjustments, for Lucas to pick.

    python3 tools/sprites/sophie_options.py

Lucas (November 8, 2026): Sophie needs a different outfit and a slight
adjustment to her design. Her description: short black hair, pale skin; shy,
funny, sarcastic, very introverted. Outfits are proposals.
Writes docs/art/cast-12/sophie-options.png.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cast12 import DRESS, SOPHIE_DRAFT1 as SOPHIE, TROUSERS, frame        # noqa: E402
from styles import font                                   # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'docs' / 'art' / 'cast-12'
HEAD_F, HEAD_S = SOPHIE['front'][:13], SOPHIE['side'][:13]
BASE_PAL = {k: v for k, v in SOPHIE['palette'].items() if k not in 'Vv'}

OUTFITS = [
    ('1 · Current lavender dress', 'for reference', DRESS,
     {'V': '#9583b0', 'v': '#76679a', 'O': '#1d1d22'}, SOPHIE['front'][13:], SOPHIE['side'][13:]),
    ('2 · Black dress, white collar', 'simple and a little moody', DRESS,
     {'V': '#2f2d38', 'v': '#1f1e26', 'W': '#f4f1ea', 'O': '#1d1d22'},
     ["..xVVWWSSWWVVx..", ".xvVVVWVVWVVVvx.", ".xvVxVVVVVVxVvx.", ".xSSxVVVVVVxSSx.", ".xsSxvvvvvvxSsx."],
     ["....xVVVWWVx....", "....xvVVVWVx....", "....xvSSVVVx....", "....xvSSVVVx....", "....xvssvvvx...."]),
    ('3 · Forest-green dress', 'calm, earthy colour', DRESS,
     {'V': '#4f7a55', 'v': '#3b5e41', 'O': '#2a2622'}, SOPHIE['front'][13:], SOPHIE['side'][13:]),
    ('4 · Cosy sweater + skirt', 'oversized cream sweater, navy skirt', DRESS,
     {'T': '#efe2c6', 't': '#d4c4a0', 'V': '#3f4566', 'v': '#2d3250', 'O': '#1d1d22'},
     ["..xTTTTSSTTTTx..", ".xtTTTTTTTTTTtx.", ".xtTxTTTTTTxTtx.", ".xtTxTTTTTTxTtx.", ".xsSxTTTTTTxSsx."],
     ["....xTTTTTTx....", "....xtTTTTTx....", "....xtTTTTTx....", "....xttTTTTx....", "....xssTTTTx...."]),
    ('5 · Overalls + striped tee', 'playful, casual', TROUSERS,
     {'T': '#f4efe4', 'R': '#c86a6a', 'N': '#5878a8', 'n': '#44608a', 'Y': '#d9c27a', 'O': '#efe9df'},
     ["..xTTTTSSTTTTx..", ".xRTNNNNNNNNTRx.", ".xTRxNYNNYNxRTx.", ".xSSxNNNNNNxSSx.", ".xsSxNNNNNNxSsx."],
     ["....xTTTTTTx....", "....xRNNNNNx....", "....xTSSNNNx....", "....xRSSNNNx....", "....xNssNNNx...."]),
    ('6 · Mustard cardigan + black', 'cardigan over black top and trousers', TROUSERS,
     {'K': '#d9a441', 'k': '#b88630', 'V': '#2a2830', 'N': '#2a2830', 'n': '#1c1b21', 'O': '#1d1d22'},
     ["..xKKKVVVVKKKx..", ".xkKKKVVVVKKKkx.", ".xkKxKVVVVKxKkx.", ".xkKxKVVVVKxKkx.", ".xsSxKVVVVKxSsx."],
     ["....xKKKKVVx....", "....xkKKKVVx....", "....xkkKKVVx....", "....xkkKKVVx....", "....xssKKVVx...."]),
]

# Design adjustments: row index -> replacement (front view, rows 0-12).
HEADS = [
    ('A · Current bob', {}),
    ('B · Side-swept bangs', {4: ".xHHHHHHHHSSHHx.", 5: ".xHHHHSSSSSSHHx."}),
    ('C · Shorter pixie cut', {9: ".xsSSSSSSSSSSsx.", 10: "..xSSSSSmSSSSx..", 11: "...xxSSSSSSxx...", 12: "....xxSSSSxx...."}),
    ('D · Bob + hair clip', {3: ".xHHHHHHHHHYYHx."}),
    ('E · Rosy cheeks', {9: ".xHSrSSSSSSrSHx."}),
]


def main():
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    k = 7
    board = Image.new('RGBA', (1500, 1190), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Sophie — outfit and design options', font=font(40), fill=INK)
    d.text((40, 86), 'Pick one outfit (1–6) and one design tweak (A–E). Front and side at 7×, true size at 2×.',
           font=font(18, False), fill=MUTED)
    for i, (name, blurb, legs, pal, body_f, body_s) in enumerate(OUTFITS):
        p = {**BASE_PAL, **pal}
        f = frame(HEAD_F + body_f + legs['front'][0], p, name)
        s = frame(HEAD_S + body_s + legs['side'][0], p, name)
        x0, y0 = 40 + (i % 3) * 480, 140 + (i // 3) * 330
        d.text((x0, y0), name, font=font(20), fill=INK)
        d.text((x0, y0 + 27), blurb, font=font(14, False), fill=MUTED)
        panel = Image.new('RGBA', (450, 250), '#97b779')
        panel.alpha_composite(f.resize((W := 16 * k, 24 * k), Image.NEAREST), (20, 60))
        panel.alpha_composite(s.resize((W, 24 * k), Image.NEAREST), (160, 60))
        panel.alpha_composite(f.resize((32, 48), Image.NEAREST), (330, 180))
        board.alpha_composite(panel, (x0, y0 + 52))
    y0 = 820
    d.text((40, y0), 'Design tweaks (shown with outfit 2)', font=font(24), fill=INK)
    _, _, legs, pal, body_f, _ = OUTFITS[1]
    for i, (name, rows) in enumerate(HEADS):
        head = [rows.get(n, r) for n, r in enumerate(HEAD_F)]
        f = frame(head + body_f + legs['front'][0], {**BASE_PAL, **pal, 'Y': '#e88aa0', 'r': '#f0b0a8'}, name)
        x0 = 40 + i * 290
        d.text((x0, y0 + 40), name, font=font(18), fill=INK)
        panel = Image.new('RGBA', (270, 270), '#97b779')
        panel.alpha_composite(f.resize((16 * 9, 24 * 9), Image.NEAREST), (20, 30))
        panel.alpha_composite(f.resize((32, 48), Image.NEAREST), (200, 200))
        board.alpha_composite(panel, (x0, y0 + 70))
    board.convert('RGB').save(OUT / 'sophie-options.png', optimize=True)


if __name__ == '__main__':
    main()
