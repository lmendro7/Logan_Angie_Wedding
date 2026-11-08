"""Sophie options guided by the reference photos Lucas supplied (not stored here).

    python3 tools/sprites/sophie_photo.py

Lucas (November 8, 2026): Sophie's nose needs to be smaller; he attached photos.
The photos show long dark hair with caramel-blonde streaks, dark-framed glasses,
an olive-green top and a small nose. All three options use the skinnier body,
the smaller nose (no nose pixel from the front, no bump in profile) and an olive dress.
Writes docs/art/cast-12/sophie-photo-options.png.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from angie_sophie_options import SLIM_DRESS_F, SLIM_DRESS_S, SLIM_HEAD_F, SLIM_HEAD_S   # noqa: E402
from cast12 import frame                                                              # noqa: E402
from styles import font                                                               # noqa: E402

OUT = Path(__file__).resolve().parents[2] / 'docs' / 'art' / 'cast-12'
PAL = {'S': '#fbe3d3', 's': '#e6bfa6', 'E': '#2a2026', 'm': '#d08f8a',
       'h': '#1a1512', 'H': '#2b2420', 'J': '#b8925e', 'G': '#5c5a62',
       'V': '#6b7044', 'v': '#525634', 'O': '#1d1d22'}

# Short bob, smaller nose: a soft two-pixel mouth replaces the single dark pixel
# that read as a nose; the profile loses its nose bump.
BOB_F = list(SLIM_HEAD_F); BOB_F[10] = "..xHSSSSmmSSHx.."
BOB_S = list(SLIM_HEAD_S); BOB_S[7] = "..xHHHHsSSESx..."; BOB_S[8] = "..xHHHHsSSESx..."; BOB_S[10] = "..xHHHHHSSmSx..."
BOB_BODY_F = ["...xVVVSSVVVx...", "...xvVVVVVVvx...", "..xSxVVVVVVxSx..", "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx.."]
BOB_BODY_S = [".....xVVVVx.....", ".....xvVVVx.....", ".....xvSVVx.....", ".....xvSVVx.....", ".....xvsvvx....."]

LONG_F = [
    ".....xxxxxx.....", "....xHHHHHHx....", "...xHHHhhHHHx...", "..xHHHHSSHHHHx..",
    "..xHHHSSSSHHHx..", "..xHJSSSSSSJHx..", "..xJSSSSSSSSJx..", "..xJSESSSSESJx..",
    "..xJSESSSSESJx..", "..xJSSSSSSSSJx..", "..xJSSSSmmSSJx..", "..xHJxSSSSxJHx..",
    "..xHJxxSSxxJHx..",
    "..xJxVVSSVVxJx..", "..xJxvVVVVvxJx..", "..xHxVVVVVVxHx..", "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx..",
]
LONG_S = [
    "....xxxxxx......", "...xHHHHHHx.....", "..xHHHHHHHHx....", "..xHHHHHHHHHx...",
    "..xHHHHHHHSSx...", "..xHHHHHJSSSx...", "..xHHHHHJSSSx...", "..xHHHHsJSESx...",
    "..xHHHHsJSESx...", "..xHHHHHJSSSx...", "..xHHHHHJSmSx...", "..xHHHHHxSSx....",
    "..xHHHHHxSSx....",
    "..xHHxVVVVx.....", "..xHHxvVVVx.....", "...xHxvSVVx.....", ".....xvSVVx.....", ".....xvsvvx.....",
]
LONG_B = [
    ".....xxxxxx.....", "....xHHHHHHx....", "...xHHHhhHHHx...", "..xHHHHHHHHHHx..",
    "..xHHHHHHHHHHx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..",
    "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..",
    "..xHHHHHHHHHHx..",
    "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xHxHHHHHHxHx..", "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx..",
]
GLASSES_F = {6: "..xJGGGSSGGGJx..", 7: "..xJGESSSSEGJx.."}
GLASSES_S = {6: "..xHHHHHJGGGx...", 7: "..xHHHHsJGESx..."}

OPTIONS = [
    ('1 · Short bob, smaller nose', 'current design, slimmer, nose fixed', BOB_F + BOB_BODY_F, BOB_S + BOB_BODY_S, None),
    ('2 · Long hair with streaks', 'from the photos: long dark hair, caramel streaks', LONG_F, LONG_S, LONG_B),
    ('3 · Long hair + glasses', 'as in the photos', [GLASSES_F.get(n, r) for n, r in enumerate(LONG_F)],
     [GLASSES_S.get(n, r) for n, r in enumerate(LONG_S)], LONG_B),
]


def main():
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    k = 8
    board = Image.new('RGBA', (40 + 3 * 520, 560), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Sophie — smaller nose, guided by the photos', font=font(40), fill=INK)
    d.text((40, 86), 'All skinnier, olive dress (from the photo). Front, side and back at 8×; true size at 2×.',
           font=font(18, False), fill=MUTED)
    for i, (name, blurb, front, side, back) in enumerate(OPTIONS):
        f = frame(front + SLIM_DRESS_F, PAL, name + ' front')
        s = frame(side + SLIM_DRESS_S, PAL, name + ' side')
        views = [f, s] + ([frame(back + SLIM_DRESS_F, PAL, name + ' back')] if back else [])
        x0 = 40 + i * 520
        d.text((x0, 130), name, font=font(21), fill=INK)
        d.text((x0, 160), blurb, font=font(14, False), fill=MUTED)
        panel = Image.new('RGBA', (490, 340), '#97b779')
        for m, v in enumerate(views):
            panel.alpha_composite(v.resize((16 * k, 24 * k), Image.NEAREST), (10 + m * 140, 30))
        panel.alpha_composite(f.resize((32, 48), Image.NEAREST), (440, 280))
        board.alpha_composite(panel, (x0, 190))
    board.convert('RGB').save(OUT / 'sophie-photo-options.png', optimize=True)


if __name__ == '__main__':
    main()
