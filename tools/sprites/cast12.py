"""Map sprites for the whole cast in the chosen style (style 12).

    python3 tools/sprites/cast12.py

Lucas, November 8, 2026: full colour, a mix of older Pokémon games and
Stardew; every character the same size (16 x 24); the detailed models appear
as portraits when characters talk. All pixels are original and hand-placed.

Sheet layout (public/sprites/<id>.png): 16 x 24 frames, 3 columns
(stand, step A, step B) x 4 rows (down, right, up, left). Feet touch the
bottom row; anchor at origin (0.5, 1).
Review images go to docs/art/cast-12/.
"""
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / 'public' / 'sprites'
REVIEW = ROOT / 'docs' / 'art' / 'cast-12'
W, H = 16, 24
OUTLINE = '#2b1d1d'
SKIN = {'S': '#f5cfa6', 's': '#e0a982', 'r': '#c98a6c', 'E': '#3d2a1e'}

# ------------------------------------------------------------- legs (rows 18-23)
TROUSERS = {
    'front': [
        [".xxxxNNNNNNxxxx.", "....xNNxxNNx....", "....xNnxxnNx....", "...xOOOxxOOOx...", "...xOOOxxOOOx...", "...xxxxxxxxxx..."],
        [".xxxxNNNNNNxxxx.", "....xNNxxNNx....", "...xOOOxxnNx....", "...xOOOxxOOOx...", "...xxxxxxOOOx...", "........xxxxx..."],
        [".xxxxNNNNNNxxxx.", "....xNNxxNNx....", "....xNnxxOOOx...", "...xOOOxxOOOx...", "...xOOOxxxxxx...", "...xxxxx........"],
    ],
    'side': [
        ["....xNNNNNNx....", ".....xnNNNx.....", ".....xnNNNx.....", "....xOOOOOOx....", "....xOOOOOOx....", "....xxxxxxxx...."],
        ["....xNNNNNNx....", "...xnnxxNNNx....", "..xnnx..xNNNx...", ".xOOOx...xOOOOx.", ".xOOOx...xOOOOx.", ".xxxxx...xxxxxx."],
        ["....xNNNNNNx....", "...xNNxxnnnx....", "..xNNx..xnnnx...", ".xOOOx...xOOOOx.", ".xOOOx...xOOOOx.", ".xxxxx...xxxxxx."],
    ],
}
DRESS = {
    'front': [
        ["..xVVVVVVVVVVx..", ".xvVVVVVVVVVVvx.", ".xxxxxxxxxxxxxx.", "....xSSxxSSx....", "...xOOOxxOOOx...", "...xxxxxxxxxx..."],
        ["..xVVVVVVVVVVx..", ".xvVVVVVVVVVVvx.", ".xxxxxxxxxxxxxx.", "...xOOOxxSSx....", "...xxxxxxOOOx...", "........xxxxx..."],
        ["..xVVVVVVVVVVx..", ".xvVVVVVVVVVVvx.", ".xxxxxxxxxxxxxx.", "....xSSxxOOOx...", "...xOOOxxxxxx...", "...xxxxx........"],
    ],
    'side': [
        ["....xVVVVVVx....", "...xvVVVVVVVx...", "...xxxxxxxxxx...", ".....xSSSx......", "....xOOOOOx.....", "....xxxxxxx....."],
        ["....xVVVVVVx....", "...xvVVVVVVVx...", "...xxxxxxxxxx...", "....xSx.xSx.....", "...xOOx.xOOOx...", "...xxxx.xxxxx..."],
        ["....xVVVVVVx....", "...xvVVVVVVVx...", "...xxxxxxxxxx...", "....xSx.xSx.....", "...xOOx.xOOOx...", "...xxxx.xxxxx..."],
    ],
}
_GOWN_F = ["..xDDDDDDDDDDx..", "..xDDdDDDDdDDx..", ".xDDDdDDDDdDDDx.", ".xDDDDDDDDDDDDx.", "xdDDDDDDDDDDDDdx", "xxxxxxxxxxxxxxxx"]
_GOWN_S = ["....xDDDDDDx....", "...xDDdDDDDx....", "...xDDdDDDDDx...", "..xDDDdDDDDDx...", "..xdDDDDDDDDDx..", "..xxxxxxxxxxxx.."]


def _sway(rows, d):
    """Hem sway for walking in a gown: shift the bottom three rows by d."""
    out = list(rows[:3])
    for r in rows[3:]:
        out.append(('.' + r[:-1]) if d > 0 else (r[1:] + '.'))
    return out


GOWN = {'front': [_GOWN_F, _sway(_GOWN_F, -1), _sway(_GOWN_F, 1)],
        'side': [_GOWN_S, _sway(_GOWN_S, -1), _sway(_GOWN_S, 1)]}

# ------------------------------------------------------------- characters (rows 0-17)
LOGAN = {
    'name': 'Logan', 'legs': TROUSERS,
    'palette': {**SKIN, 'h': '#5c4834', 'H': '#8a6e50', 'J': '#b0916a', 'L': '#cfb48a',
                'b': '#8c5a34', 'B': '#6a4024', 'c': '#a8724a', 'W': '#f7f5ef', 'V': '#d6d1c4',
                'X': '#17171c', 'N': '#2d2e36', 'n': '#1f2026', 'K': '#3a2a20', 'Y': '#c9a24a', 'O': '#1a1a1e'},
    'front': [
        ".....xxxxxx.....", "...xxHHJJHHxx...", "..xHHJJLJHHHHx..", "..xHHHHHHHHHHx..",
        ".xhHHHHHHHHHHhx.", ".xhhSSSSSSSShhx.", ".xhSSSSSSSSSShx.", ".xSSSESSSSESSSx.",
        ".xSSSESSSSESSSx.", ".xscSSSSSSSScsx.", "..xbbSSBBSSbbx..", "...xbbbbbbbbx...",
        "....xxSSSSxx....", "..xWWWXXXXWWWx..", ".xVWWWWXXWWWWVx.", ".xVWxWWWWWWxWVx.",
        ".xVWxWWWWWWxWVx.", ".xsSxKKKYKKxSsx.",
    ],
    'back': [
        ".....xxxxxx.....", "...xxHHHHHHxx...", "..xHHHJJJJHHHx..", "..xHHHHJJHHHHx..",
        ".xhHHHHHHHHHHhx.", ".xhHHHHHHHHHHhx.", ".xhhHHHHHHHHhhx.", ".xshhHHHHHHhhsx.",
        ".xsshhhhhhhhssx.", "..xsbhhhhhhbsx..", "..xxbSSSSSSbxx..", "...xxSSSSSSxx...",
        "....xxSSSSxx....", "..xWWWWWWWWWWx..", ".xVWWWWWWWWWWVx.", ".xVWxWWWWWWxWVx.",
        ".xVWxWWVVWWxWVx.", ".xsSxKKKKKKxSsx.",
    ],
    'side': [
        "....xxxxxx......", "...xHHJJHHxx....", "..xHHHHJJJHHx...", "..xhHHHHHHHHHx..",
        ".xhhHHHHHHHHHx..", ".xhhhHHHHSSSSx..", ".xhhhsHSSSSSSx..", ".xhhhsSSSSSESx..",
        ".xhhhsSSSSSESSx.", "..xhcSSSSSSSSx..", "..xbbbSSSBBbx...", "...xbbbbbbbx....",
        ".....xxSSSx.....", "....xWWWWXXx....", "....xVWWWWXx....", "....xVWVWWWx....",
        "....xVWVWWWx....", "....xKsSKKYx....",
    ],
}
RYAN = {
    'name': 'Ryan', 'legs': TROUSERS,
    'palette': {**SKIN, 'c': '#5b3526', 'C': '#7b4a33', 'P': '#efe5d2', 'L': '#8b90a8',
                'h': '#a8773f', 'H': '#c99a57', 'J': '#e3bd77', 't': '#d6c296', 'T': '#f3e5c2',
                'F': '#e65f55', 'G': '#5a3a2a', 'B': '#6a4128', 'K': '#c9a03f',
                'N': '#323858', 'n': '#232842', 'O': '#77482a'},
    'front': [
        "....xxxxxxxx....", "...xCPPPPPPCx...", "..xCPPLLLLPPCx..", "..xCCCCCCCCCCx..",
        ".xcCCCCCCCCCCcx.", ".xhHJHHJJHHJHhx.", ".xhSSSSSSSSSShx.", ".xSSSESSSSESSSx.",
        ".xSSSESSSSESSSx.", ".xsSSSSSSSSSSsx.", "..xSSSSSSSSSSx..", "...xxSSSSSSxx...",
        "....xxSSSSxx....", "..xTTTTSSTTTTx..", ".xtTTTGTTFTTTtx.", ".xtTxTTFFFTxTtx.",
        ".xSSxTTTFTTxSSx.", ".xsSxBBKKBBxSsx.",
    ],
    'back': [
        "....xxxxxxxx....", "...xCCCCCCCCx...", "..xCCCCCCCCCCx..", "..xCCCCccCCCCx..",
        ".xCCCCchhcCCCCx.", ".xhHHJHHJHHJHhx.", ".xhHHHHHHHHHHhx.", ".xhHHHHHHHHHHhx.",
        ".xshHHHHHHHHhsx.", "..xshhhhhhhhsx..", "..xxSSSSSSSSxx..", "...xxSSSSSSxx...",
        "....xxSSSSxx....", "..xTTTTTTTTTTx..", ".xtTTTTTTTTTTtx.", ".xtTxTTTTTTxTtx.",
        ".xSSxTTTTTTxSSx.", ".xsSxBBBBBBxSsx.",
    ],
    'side': [
        "...xxxxxxx......", "..xCCCCCPPx.....", ".xCCCCCPLLPx....", ".xCCCCCCPPPCx...",
        ".xcCCCCCCCCCCCx.", ".xhhHJHHJHHHx...", ".xhhhHSSSSSSx...", ".xhhhsSSSSESx...",
        ".xhhhsSSSSESSx..", "..xhhSSSSSSSx...", "...xhSSSSSSx....", "....xxSSSSx.....",
        ".....xxSSSx.....", "....xTTTTTFx....", "....xtTTTFGx....", "....xtSSTTGx....",
        "....xtSSTTTx....", "....xBsSBBKx....",
    ],
}
ANGIE = {
    'name': 'Angie', 'legs': GOWN,
    'palette': {**SKIN, 'h': '#5a3a22', 'H': '#7d5332', 'J': '#9c6c43', 'G': '#6b4a3a',
                'm': '#d7766f', 'D': '#fbf7ee', 'd': '#e3dccb', 'w': '#d9cdb4', 'O': '#e9dcc4'},
    'front': [
        ".....xxxxxx.....", "...xxHHJJHHxx...", "..xHHJHHHHJHHx..", ".xHHHHHHHHHHHHx.",
        ".xHHHHSSSSHHHHx.", ".xHHSSSSSSSSHHx.", "xHHSSSSSSSSSSHHx", "xHHSSESSSSESSHHx",
        "xHHSSESSSSESSHHx", "xHHSSSSSSSSSSHHx", "xHHHSSSmmSSSHHHx", "xHHHsSSSSSSsHHHx",
        "xHHhhsSSSSshhHHx", "xHHxSDSSSSDSxHHx", "xHhxSDDDDDDSxhHx", ".xxSxDDDDDDxSxx.",
        "..xSxDDDDDDxSx..", "..xsxwwwwwwxsx..",
    ],
    'back': [
        ".....xxxxxx.....", "...xxHHHHHHxx...", "..xHHJHHHHJHHx..", ".xHHHHHHHHHHHHx.",
        ".xHHJHHHHHHJHHx.", ".xHHHHHHHHHHHHx.", "xHHHHHHHHHHHHHHx", "xHHJHHHHHHHHJHHx",
        "xHHHHHHHHHHHHHHx", "xHHHHHJHHJHHHHHx", "xHHHHHHHHHHHHHHx", "xHhHHHHHHHHHHhHx",
        "xHHhHHHHHHHHhHHx", "xHHHHhHHHHhHHHHx", "xhHxSHHhhHHSxHhx", ".xxSxDDDDDDxSxx.",
        "..xSxDDDDDDxSx..", "..xsxwwwwwwxsx..",
    ],
    'side': [
        "....xxxxxx......", "...xHHHJJHxx....", "..xHHHHHHJHHx...", ".xHHHHHHHHHHHx..",
        ".xHHHHHHHHSSSx..", "xHHHHHHHSSSSSx..", "xHHHHHHHSSSSSx..", "xHHHHHHHSSSESx..",
        "xHHHHHHHSSSESSx.", "xHHHHHHHSSSSSx..", "xHHHHHHHSSSmSx..", "xHHHHHHHxSSSx...",
        "xHHHHHHhxxSSx...", "xHHHHxSSDDDx....", "xhHHHxSDDDDx....", "..xxxDSDDDx.....",
        "....xDSDDDx.....", "....xwswwwx.....",
    ],
}
# Angie wears a short veil (Lucas, November 8, 2026): a veil band on top of her
# head, falling behind her hair. Applied to her current no-glasses model.
_ANGIE_VEIL = {
    'front': {1: "...xxVVVVVVxx...", 2: "..xVHJHHHHJHVx..", 6: "VHHSSSSSSSSSSHHV", 9: "VHHSSSSSSSSSSHHV",
              12: "VHHhhsSSSSshhHHV"},
    'side': {1: "...xVVVVVVxx....", 2: "..VVVHHHHJHHx...", 3: ".VVVHHHHHHHHx...", 5: "VVHHHHHHSSSSSx..",
             8: "VVHHHHHHSSSESSx.", 11: "VvHHHHHHxSSSx...", 13: "VvHHHxSSDDDx....", 14: "vvHHHxSDDDDx...."},
    'back': {1: "...xxVVVVVVxx...", 2: "..xVVVVVVVVVVx..", 3: ".xVVVVVVVVVVVVx.", 4: ".xVVvVVVVVVvVVx.",
             5: ".xVVVVVVVVVVVVx.", 6: "xHVVVVVVVVVVVVHx", 7: "xHVvVVVVVVVVvVHx", 8: "xHVVVVVVVVVVVVHx",
             9: "xHVVVVVVVVVVVVHx", 10: "xHVVvVVVVVVvVVHx", 11: "xHhVVVVVVVVVVhHx", 12: "xHHvVVVVVVVVvHHx",
             13: "xHHHvVVVVVVvHHHx"},
}
for _view, _rows in _ANGIE_VEIL.items():
    for _n, _r in _rows.items():
        ANGIE[_view][_n] = _r
ANGIE['palette'].update({'V': '#f6f3ec', 'v': '#ddd8cc'})
# Continuous veil edges: down both sides from the front, behind the head from the side.
for _n in range(6, 15):
    _r = ANGIE['front'][_n]
    ANGIE['front'][_n] = 'V' + _r[1:-1] + 'V'
for _n in range(3, 15):
    _r = ANGIE['side'][_n]
    ANGIE['side'][_n] = ('Vv' if _n > 10 else 'VV') + _r[2:]

SOPHIE_DRAFT1 = {
    'name': 'Sophie', 'legs': DRESS, 'draft': True,
    'palette': {'S': '#fbe3d3', 's': '#e6bfa6', 'E': '#2a2026', 'm': '#9c5f5f',
                'h': '#15161b', 'H': '#25272f', 'J': '#3e4250', 'V': '#9583b0', 'v': '#76679a',
                'O': '#1d1d22'},
    'front': [
        ".....xxxxxx.....", "...xxHHHHHHxx...", "..xHHHJHHHHHHx..", ".xHHHHHHHHHHHHx.",
        ".xHHHHHHHHHHHHx.", ".xHHSSSSSSSSHHx.", ".xHSSSSSSSSSSHx.", ".xHSSESSSSESSHx.",
        ".xHSSESSSSESSHx.", ".xHSSSSSSSSSSHx.", ".xHHSSSSmSSSHHx.", ".xHHHxSSSSxHHHx.",
        "..xxxxSSSSxxxx..", "..xVVVVSSVVVVx..", ".xvVVVVVVVVVVvx.", ".xvVxVVVVVVxVvx.",
        ".xSSxVVVVVVxSSx.", ".xsSxvvvvvvxSsx.",
    ],
    'side': [
        "....xxxxxx......", "...xHHHHHHxx....", "..xHHHJHHHHHx...", ".xHHHHHHHHHHHx..",
        ".xHHHHHHHHHHHx..", ".xHHHHHHHSSSSx..", ".xHHHHHHSSSSSx..", ".xHHHHHsSSSSESx.",
        ".xHHHHHsSSSSESSx", ".xHHHHHHSSSSSx..", ".xHHHHHHSSSmSx..", "..xHHHHHxSSSx...",
        "...xxxxxxSSx....", "....xVVVVVVx....", "....xvVVVVVx....", "....xvSSVVVx....",
        "....xvSSVVVx....", "....xvssvvvx....",
    ],
}
MOTHER = {
    'name': "Logan's Mother", 'legs': DRESS, 'draft': True,
    'palette': {**SKIN, 'm': '#c56f6c', 'h': '#8a6c45', 'H': '#b08e5e', 'J': '#cfae7c',
                'V': '#c48b98', 'v': '#a26f7c', 'O': '#8a6650'},
    'front': [
        ".....xxxxxx.....", "...xxHHJJHHxx...", "..xHHJHHHHHHHx..", ".xHHHHHHHHHHHHx.",
        ".xHHSSSSSSSSHHx.", ".xHSSSSSSSSSSHx.", ".xHSSSSSSSSSSHx.", ".xHSSESSSSESSHx.",
        ".xHSSESSSSESSHx.", ".xHSSSSSSSSSSHx.", ".xHHSSSmmSSSHHx.", ".xHHxSSSSSSxHHx.",
        ".xHHhxSSSSxhHHx.", ".xHxVVSSSSVVxHx.", ".xxVVVVSSVVVVxx.", ".xvVxVVVVVVxVvx.",
        ".xSSxVVVVVVxSSx.", ".xsSxvvvvvvxSsx.",
    ],
    'side': [
        "....xxxxxx......", "...xHHJJHHxx....", "..xHHHHHHJHHx...", ".xHHHHHHHHHHHx..",
        ".xHHHHHHHSSSSx..", ".xHHHHHHSSSSSx..", ".xHHHHHHSSSSSx..", ".xHHHHHsSSSSESx.",
        ".xHHHHHsSSSSESSx", ".xHHHHHHSSSSSx..", ".xHHHHHHSSSmSx..", ".xHHHHHHxSSSx...",
        ".xHHHHHxxSSx....", "....xVVVVVVx....", "....xvVVVVVx....", "....xvSSVVVx....",
        "....xvSSVVVx....", "....xvssvvvx....",
    ],
}
FATHER = {
    'name': "Logan's Father", 'legs': TROUSERS, 'draft': True,
    'palette': {**SKIN, 'h': '#86683f', 'H': '#a98a5b', 'J': '#c3a476',
                'K': '#5e7891', 'k': '#4a6178', 'g': '#7891a8', 'W': '#f6f3ea', 'X': '#2e3a5c',
                'N': '#56708a', 'n': '#435a71', 'O': '#3b2a20'},
    'front': [
        ".....xxxxxx.....", "...xxHHHJJHxx...", "..xHHHHHJJHHHx..", "..xHHHHHHHHHHx..",
        ".xhHHHHHHHHHHhx.", ".xhSSSSSSSSSShx.", ".xSSSSSSSSSSSSx.", ".xSSSESSSSESSSx.",
        ".xSSSESSSSESSSx.", ".xsSSSSssSSSSsx.", "..xSSSSrrSSSSx..", "...xxSSSSSSxx...",
        "....xxSSSSxx....", "..xKKKWWWWKKKx..", ".xgKKKWXXWKKKgx.", ".xgKxKKXXKKxKgx.",
        ".xgKxKKXXKKxKgx.", ".xsSxKKKKKKxSsx.",
    ],
    'side': [
        "....xxxxxx......", "...xHHHJJHxx....", "..xHHHHHJJHHx...", "..xhHHHHHHHHHx..",
        ".xhhHHHHHHHHHx..", ".xhhhHHHHSSSSx..", ".xhhhsHSSSSSSx..", ".xhhhsSSSSSESx..",
        ".xhhhsSSSSSESSx.", "..xhsSSSSSSSSx..", "..xsSSSSSSrSx...", "...xsSSSSSSx....",
        ".....xxSSSx.....", "....xKKKKWXx....", "....xKgKKKXx....", "....xKggKKKx....",
        "....xKggKKKx....", "....xKsSKKKx....",
    ],
}


def derive_back(c, long_hair=False):
    """Back view for drafts: face becomes hair; chest details become plain cloth."""
    face = set('SsErmGcbB')
    out = []
    for y, row in enumerate(c['front']):
        if y <= 10 or (long_hair and y <= 12):
            row = ''.join('H' if ch in face else ch for ch in row)
        elif y <= 12:
            row = ''.join('S' if ch in 'bBc' else ch for ch in row)
        elif y <= 14:
            row = ''.join(c.get('back_cloth', {}).get(ch, ch) for ch in row)
        out.append(row)
    return out


SOPHIE_DRAFT1['back_cloth'] = {'S': 'V'}
MOTHER['back_cloth'] = {'S': 'V'}
FATHER['back_cloth'] = {'W': 'K', 'X': 'K'}
SOPHIE_DRAFT1['back'] = derive_back(SOPHIE_DRAFT1)
MOTHER['back'] = derive_back(MOTHER, long_hair=True)
FATHER['back'] = derive_back(FATHER)
for y in range(15, 17):                                   # Father: plain jacket back, no tie
    FATHER['back'][y] = FATHER['back'][y].replace('X', 'K')


# Sophie, chosen by Lucas (November 8, 2026): option 2 from sophie-photo-options,
# guided by his reference photos: long dark hair with caramel streaks framing her
# face, skinnier body, small nose (no nose pixel; flush profile), olive dress.
SLIM_DRESS = {
    'front': [
        ["...xVVVVVVVVx...", "..xvVVVVVVVVvx..", "..xxxxxxxxxxxx..", ".....xSxxSx.....", "....xOOxxOOx....", "....xxxxxxxx...."],
        ["...xVVVVVVVVx...", "..xvVVVVVVVVvx..", "..xxxxxxxxxxxx..", "....xOOxxSx.....", "....xxxxxOOx....", "........xxxx...."],
        ["...xVVVVVVVVx...", "..xvVVVVVVVVvx..", "..xxxxxxxxxxxx..", ".....xSxxOOx....", "....xOOxxxxx....", "....xxxx........"],
    ],
    'side': [
        [".....xVVVVx.....", "....xvVVVVVx....", "....xxxxxxxx....", "......xSSx......", ".....xOOOOx.....", ".....xxxxxx....."],
        [".....xVVVVx.....", "....xvVVVVVx....", "....xxxxxxxx....", ".....xSxxSx.....", "....xOOxxOOOx...", "....xxxxxxxxx..."],
        [".....xVVVVx.....", "....xvVVVVVx....", "....xxxxxxxx....", ".....xSxxSx.....", "....xOOxxOOOx...", "....xxxxxxxxx..."],
    ],
}
SOPHIE = {
    'name': 'Sophie', 'legs': SLIM_DRESS,
    'palette': {'S': '#fbe3d3', 's': '#e6bfa6', 'E': '#2a2026', 'm': '#d08f8a',
                'h': '#1a1512', 'H': '#2b2420', 'J': '#b8925e',
                'V': '#6b7044', 'v': '#525634', 'O': '#1d1d22'},
    'front': [
        ".....xxxxxx.....", "....xHHHHHHx....", "...xHHHhhHHHx...", "..xHHHHSSHHHHx..",
        "..xHHHSSSSHHHx..", "..xHJSSSSSSJHx..", "..xJSSSSSSSSJx..", "..xJSESSSSESJx..",
        "..xJSESSSSESJx..", "..xJSSSSSSSSJx..", "..xJSSSSmmSSJx..", "..xHJxSSSSxJHx..",
        "..xHJxxSSxxJHx..", "..xJxVVSSVVxJx..", "..xJxvVVVVvxJx..", "..xHxVVVVVVxHx..",
        "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx..",
    ],
    'side': [
        "....xxxxxx......", "...xHHHHHHx.....", "..xHHHHHHHHx....", "..xHHHHHHHHHx...",
        "..xHHHHHHHSSx...", "..xHHHHHJSSSx...", "..xHHHHHJSSSx...", "..xHHHHsJSESx...",
        "..xHHHHsJSESx...", "..xHHHHHJSSSx...", "..xHHHHHJSmSx...", "..xHHHHHxSSx....",
        "..xHHHHHxSSx....", "..xHHxVVVVx.....", "..xHHxvVVVx.....", "...xHxvSVVx.....",
        ".....xvSVVx.....", ".....xvsvvx.....",
    ],
    'back': [
        ".....xxxxxx.....", "....xHHHHHHx....", "...xHHHhhHHHx...", "..xHHHHHHHHHHx..",
        "..xHHHHHHHHHHx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..",
        "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..",
        "..xHHHHHHHHHHx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xHxHHHHHHxHx..",
        "..xSxVVVVVVxSx..", "..xsxvvvvvvxsx..",
    ],
}

CAST = {'logan': LOGAN, 'angie': ANGIE, 'ryan': RYAN, 'sophie': SOPHIE, 'mother': MOTHER, 'father': FATHER}


def frame(rows, pal, who):
    assert len(rows) == H, (who, len(rows))
    img = Image.new('RGBA', (W, H))
    for y, row in enumerate(rows):
        assert len(row) == W, (who, y, row, len(row))
        for x, ch in enumerate(row):
            if ch != '.':
                colour = OUTLINE if ch == 'x' else pal[ch]
                img.putpixel((x, y), ImageColor.getrgb(colour) + (255,))
    return img


def frames_for(cid):
    c = CAST[cid]
    rows = []
    for view, legs_key in (('front', 'front'), ('side', 'side'), ('back', 'front'), ('side', 'side')):
        top = c[view]
        assert len(top) == 18, (cid, view, len(top))
        rows.append([frame(top + legs, c['palette'], f'{cid} {view}') for legs in c['legs'][legs_key]])
    rows[3] = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in rows[3]]
    return rows                                            # down, right, up, left


def main():
    RUNTIME.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    all_rows = {}
    for cid in CAST:
        rows = frames_for(cid)
        all_rows[cid] = rows
        sheet = Image.new('RGBA', (W * 3, H * 4))
        for r, frs in enumerate(rows):
            for col, f in enumerate(frs):
                sheet.paste(f, (col * W, r * H))
        sheet.save(RUNTIME / f'{cid}.png')

    from styles import font                                # local import keeps runtime build light
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    k = 7
    cw = 4 * (W * k + 14) + 30
    board = Image.new('RGBA', (40 + 2 * cw, 140 + 3 * (H * k + 150)), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'The cast — map sprites (style 12)', font=font(40), fill=INK)
    d.text((40, 86), 'All 16 × 24. Front, right, back, left at 7×; walk frames and true size (2×) below each.',
           font=font(18, False), fill=MUTED)
    for i, cid in enumerate(CAST):
        c, rows = CAST[cid], all_rows[cid]
        x0, y0 = 40 + (i % 2) * cw, 140 + (i // 2) * (H * k + 150)
        d.text((x0, y0), c['name'] + ('  ·  draft for review' if c.get('draft') else ''), font=font(22), fill=INK)
        for r in range(4):
            board.alpha_composite(rows[r][0].resize((W * k, H * k), Image.NEAREST), (x0 + r * (W * k + 14), y0 + 34))
        yy = y0 + 34 + H * k + 10
        for r in range(4):
            for col in range(3):
                board.alpha_composite(rows[r][col].resize((W * 2, H * 2), Image.NEAREST),
                                      (x0 + r * (W * k + 14) + col * 36, yy))
    board.convert('RGB').save(REVIEW / 'cast-sprites.png', optimize=True)

    # Walking GIF of the whole cast.
    frames = []
    for col in (1, 0, 2, 0):
        fr = Image.new('RGBA', (len(CAST) * 2 * (W * 5 + 10) + 10, H * 5 + 20), '#97b779')
        for n, cid in enumerate(CAST):
            for m, r in enumerate((0, 1)):
                fr.alpha_composite(all_rows[cid][r][col].resize((W * 5, H * 5), Image.NEAREST),
                                   (10 + (2 * n + m) * (W * 5 + 10), 10))
        frames.append(fr.convert('RGB'))
    frames[0].save(REVIEW / 'cast-walking.gif', save_all=True, append_images=frames[1:], duration=170, loop=0)


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
