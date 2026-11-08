"""Cozy Garden: the game's own character style (16 x 32).

    python3 tools/sprites/cozy.py

Lucas (November 8, 2026) gave full creative freedom to make a Stardew-like
style. Cozy Garden is Stardew's comforting look with a touch of Pokémon:
16 x 32 characters, soft warm-brown outlines (never black), gentle shading lit
from the upper left, round friendly faces with a highlight in each eye, rosy
cheeks, hair with strands and highlights, hands at the sides, and four-direction
walking. Every pixel is original and hand-placed. Approved character features
are kept (Logan's white shirt and bow tie, Angie without glasses and with her
veil, Ryan's cap and flower shirt, Sophie's long streaked hair and olive dress).

Writes public/sprites/<id>.png: 48 x 128, 16 x 32 frames; rows down, right,
up, left; columns stand, step A, step B. Review images go to docs/art/cozy/.
"""
import sys
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from characters import DETAIL_FB_LEGS, SOFT_SIDE_LEGS    # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / 'public' / 'sprites'
REVIEW = ROOT / 'docs' / 'art' / 'cozy'
W, H = 16, 32
OUTLINE = '#3b2722'
SKIN = {'S': '#f7d4b0', 's': '#e6b18c', 'r': '#cf9072', 'p': '#f2aaa2', 'm': '#cf766e',
        'w': '#ffffff', 'E': '#3a2a22'}


def sway(rows, d):
    """Gown hem sway for walking: shift the lower rows by d."""
    return list(rows[:3]) + [('.' + r[:-1]) if d > 0 else (r[1:] + '.') for r in rows[3:]]


# ---------------------------------------------------------------- legs (rows 25-31)
TROUSERS = {'front': DETAIL_FB_LEGS, 'side': SOFT_SIDE_LEGS}
_DRESS_F = [
    [".xxxxxxxxxxxxxx.", "....xSSxxSSx....", "....xSSxxSSx....", "....xSsxxsSx....", "...xOOOxxOOOx...", "...xxxxxxxxxx...", "................"],
    [".xxxxxxxxxxxxxx.", "....xSSxxSSx....", "...xOOOxxSSx....", "...xxxxxxsSx....", "........xOOOx...", "........xxxxx...", "................"],
    [".xxxxxxxxxxxxxx.", "....xSSxxSSx....", "....xSSxxOOOx...", "....xSsxxxxxx...", "...xOOOx........", "...xxxxx........", "................"],
]
_DRESS_S = [
    ["...xxxxxxxxxx...", "......xSSx......", "......xSSx......", "......xsSx......", ".....xOOOOx.....", ".....xxxxxx.....", "................"],
    ["...xxxxxxxxxx...", ".....xSxxSx.....", ".....xSxxSx.....", "....xSx..xSx....", "...xOOx..xOOOx..", "...xxxx..xxxxx..", "................"],
    ["...xxxxxxxxxx...", ".....xSxxSx.....", ".....xSxxSx.....", "....xSx..xSx....", "...xOOx..xOOOx..", "...xxxx..xxxxx..", "................"],
]
DRESS = {'front': _DRESS_F, 'side': _DRESS_S}
_SLIM_F = [
    ["..xxxxxxxxxxxx..", ".....xSxxSx.....", ".....xSxxSx.....", ".....xSxxSx.....", "....xOOxxOOx....", "....xxxxxxxx....", "................"],
    ["..xxxxxxxxxxxx..", ".....xSxxSx.....", "....xOOxxSx.....", "....xxxxxSx.....", "........xOOx....", "........xxxx....", "................"],
    ["..xxxxxxxxxxxx..", ".....xSxxSx.....", ".....xSxxOOx....", ".....xSxxxxx....", "....xOOx........", "....xxxx........", "................"],
]
_SLIM_S = [
    ["....xxxxxxxx....", "......xSSx......", "......xSSx......", "......xSSx......", ".....xOOOOx.....", ".....xxxxxx.....", "................"],
    ["....xxxxxxxx....", ".....xSxxSx.....", ".....xSxxSx.....", "....xSx..xSx....", "...xOOx..xOOOx..", "...xxxx..xxxxx..", "................"],
    ["....xxxxxxxx....", ".....xSxxSx.....", ".....xSxxSx.....", "....xSx..xSx....", "...xOOx..xOOOx..", "...xxxx..xxxxx..", "................"],
]
SLIM = {'front': _SLIM_F, 'side': _SLIM_S}
# Clean vertical folds that continue down from the bodice.
_GOWN_F = ["...xDDdDDdDDx...", "..xDDDdDDdDDDx..", "..xDDDdDDdDDDx..", ".xDdDDdDDdDDdDx.",
           ".xDdDDdDDdDDdDx.", "xDDdDDdDDdDDdDDx", "xxxxxxxxxxxxxxxx"]
_GOWN_S = ["....xDdDDdDx....", "...xDDdDDdDx....", "...xDDdDDdDDx...", "..xDDDdDDdDDx...",
           "..xDDDdDDdDDDx..", ".xDDDDdDDdDDDx..", ".xxxxxxxxxxxxx.."]
GOWN = {'front': [_GOWN_F, sway(_GOWN_F, -1), sway(_GOWN_F, 1)],
        'side': [_GOWN_S, sway(_GOWN_S, -1), sway(_GOWN_S, 1)]}

# ---------------------------------------------------------------- characters (rows 0-24)
LOGAN = {
    'name': 'Logan', 'legs': TROUSERS,
    'palette': {**SKIN, 'h': '#6a5038', 'H': '#8f6f4f', 'J': '#b08f68', 'L': '#cdb088',
                'b': '#94643c', 'c': '#6f4a2c', 'd': '#b07e52',
                'W': '#fbf9f3', 'V': '#ddd7cb', 'U': '#c6bfb1', 'X': '#232229',
                'K': '#4a3426', 'Y': '#d6b25a', 'N': '#363744', 'n': '#282833', 'O': '#2a2626', 'o': '#4a4444'},
    'front': [
        "................", ".....xxxxxx.....", "....xJLLJHHx....", "...xHJLJJHHHx...",
        "..xHHJJHHHHhHx..", "..xhHHHHHhHHhx..", "..xhhSSSSSShhx..", "..xhSSSSSSSShx..",
        "..xsSwESSwESsx..", "..xsSEESSEESsx..", "..xsSSSrrSSSsx..", "..xcdSSSSSSdcx..",
        "...xbbdSSdbbx...", "....xbbbbbbx....", ".....xsSSsx.....",
        "...xVWWXXWWVx...", "..xVWWXXXXWWVx..", "..xVWWWWWWWWVx..", "..xVWUWWWWUWVx..",
        "..xVWUWWWWUWVx..", "..xVWUWWWWUWVx..", "..xVVUWWWWUVVx..", "..xsSKKYYKKSsx..",
        "..xxxNNNNNNxxx..", "....xNNNNNNx....",
    ],
    'back': [
        "................", ".....xxxxxx.....", "....xHHJJHHx....", "...xHHJLJJHHx...",
        "..xHHHJJHHHhHx..", "..xhHHHHHHHhHx..", "..xhHHHhHHHhhx..", "..xhhHHHHHHhhx..",
        "..xshhhhhhhhsx..", "..xshhhhhhhhsx..", "...xchhhhhhcx...", "...xcSSSSSScx...",
        "....xcSSSScx....", ".....xSSSSx.....", ".....xsSSsx.....",
        "...xVWWWWWWVx...", "..xVWWWWWWWWVx..", "..xVWWWWWWWWVx..", "..xVWUWWWWUWVx..",
        "..xVWUWWWWUWVx..", "..xVWUWVVWUWVx..", "..xVVUWWWWUVVx..", "..xsSKKKKKKSsx..",
        "..xxxNNNNNNxxx..", "....xNNNNNNx....",
    ],
    'side': [
        "................", "....xxxxxx......", "...xHJLLJHxx....", "..xHHJLJJHHHx...",
        "..xhHHJJHHHHHx..", "..xhhHHHHHHHHx..", "..xhhhHHHSSSSx..", "..xhhhsSSSSSSx..",
        "..xhhsrSSSwESx..", "..xhhsrSSSEESSx.", "...xhcSSSSSSSx..", "...xcbbdSSdbx...",
        "....xcbbbbbbx...", ".....xcbbbx.....", "......xsSsx.....",
        "....xVWWWXXx....", "....xVWWWWXx....", "....xVWUWWWx....", "....xVWUWWWx....",
        "....xVWUWWWx....", "....xVWUWWWx....", "....xVVUWWWx....", "....xKsSKKYx....",
        "....xNNNNNNx....", "....xNNNNNNx....",
    ],
}

ANGIE = {
    'name': 'Angie', 'legs': GOWN, 'veil_edges': True,
    'palette': {**SKIN, 'S': '#f7d6b8', 's': '#e8b997', 'p': '#f3aaa4', 'm': '#d2726c', 'E': '#3a2620',
                'h': '#5c3a22', 'H': '#7f5332', 'J': '#a06e44',
                'D': '#fdfaf3', 'd': '#e6dfce', 'q': '#ddd1b8', 'V': '#f8f5ee', 'v': '#e3ddd0', 'O': '#e9dcc4'},
    'front': [
        "................", ".....xxxxxx.....", "....xVVVVVVx....", "...xHHJJJJHHx...",
        "..xHHJHHHHJHHx..", ".xHHHHHHHHHHHHx.", ".xHHhSSSSSShHHx.", ".xHhSSSSSSSShHx.",
        ".xHhSwESSwEShHx.", ".xHhSEESSEEShHx.", ".xHHpSSSSSSpHHx.", ".xHHHSSmmSSHHHx.",
        ".xHJHHSSSSHHJHx.", ".xHHJHxSSxHJHHx.", ".xHhHHxSSxHHhHx.",
        ".xHHxSDSSDSxHHx.", ".xHhxSDDDDSxhHx.", "..xxSxDDDDxSxx..", "...xSxDDDDxSx...",
        "...xSxdDDdxSx...", "...xSxqqqqxSx...", "...xsxDDDDxsx...", "...xsxDdDDxsx...",
        "....xDdDDdDx....", "...xDDdDDdDDx...",
    ],
    'back': [
        "................", ".....xxxxxx.....", "....xVVVVVVx....", "...xVVVVVVVVx...",
        "..xHVVVVVVVVHx..", ".xHHVVvVVvVVHHx.", ".xHHVVVVVVVVHHx.", ".xHhVvVVVVvVhHx.",
        ".xHHVVVVVVVVHHx.", ".xHhVVvVVvVVhHx.", ".xHHVVVVVVVVHHx.", ".xHJVvVVVVvVJHx.",
        ".xHHVVVVVVVVHHx.", ".xHhHVvVVvVHhHx.", ".xHHJVVVVVVJHHx.",
        ".xHHxSVVVVSxHHx.", ".xhHxSDVVDSxHhx.", "..xxSxDvvDxSxx..", "...xSxDDDDxSx...",
        "...xSxdDDdxSx...", "...xSxqqqqxSx...", "...xsxDDDDxsx...", "...xsxDdDDxsx...",
        "....xDdDDdDx....", "...xDDdDDdDDx...",
    ],
    'side': [
        "................", "....xxxxxx......", "...xVVVVVVx.....", "..vxHHJJJHHx....",
        ".vxHHHHHHJHHx...", "vxHHHHHHHSSSSx..", "vxHHHHHHSSSSSx..", "vxHHHHHsSSSSSx..",
        "vxHHHHHsSSwESx..", "vxHHJHHHSSEESSx.", "vxHHHHHHSSpSSx..", "vxHJHHHHSSSmSx..",
        "vxHHHHHHxSSSx...", "vxHHJHHHxSSx....", "vxHhHHHxxSSx....",
        "vxHHHxSSDDx.....", "vxHhHxSDDDx.....", "vxHHxDSDDDx.....", ".vxxxDSDDDx.....",
        ".v..xDSDDDx.....", ".v..xqsqqqx.....", "....xDsDDDx.....", "....xDDDDDx.....",
        "....xDdDDdx.....", "...xDDdDDdDx....",
    ],
}

RYAN = {
    'name': 'Ryan', 'legs': TROUSERS,
    'palette': {**SKIN, 'c': '#5b3526', 'C': '#7b4a33', 'P': '#efe5d2', 'L': '#8b90a8',
                'h': '#a8773f', 'H': '#c99a57', 'J': '#e3bd77', 't': '#d9c69c', 'T': '#f4e7c6',
                'F': '#e65f55', 'G': '#5a3a2a', 'B': '#6a4128', 'K': '#c9a03f',
                'N': '#343a5c', 'n': '#262b47', 'O': '#77482a', 'o': '#96643f'},
    'front': [
        "................", "....xxxxxxxx....", "...xCPPPPPPCx...", "..xCPPLLLLPPCx..",
        "..xCCCCCCCCCCx..", ".xcCCCCCCCCCCcx.", "..xhJHJJHJHJhx..", "..xhSSSSSSSShx..",
        "..xsSwESSwESsx..", "..xsSEESSEESsx..", "..xsSSSrrSSSsx..", "...xSpSSSSpSx...",
        "...xsSSmmSSsx...", "....xxSSSSxx....", ".....xsSSsx.....",
        "...xTTTSSTTTx...", "..xtTTGTTFTTtx..", "..xtTTGTFFFTtx..", "..xSSTTTTFTSSx..",
        "..xSSTTTTTTSSx..", "..xSStTTTTtSSx..", "..xsStTTTTtSsx..", "..xsSBBKKBBSsx..",
        "..xxxNNNNNNxxx..", "....xNNNNNNx....",
    ],
    'back': [
        "................", "....xxxxxxxx....", "...xCCCCCCCCx...", "..xCCCCCCCCCCx..",
        "..xCCCCccCCCCx..", "..xCCCchhcCCCx..", "..xhHJHHJHHJhx..", "..xhHHHHHHHHhx..",
        "..xshHHHHHHhsx..", "..xshhHHHHhhsx..", "...xshhhhhhsx...", "...xSSSSSSSSx...",
        "....xSSSSSSx....", ".....xSSSSx.....", ".....xsSSsx.....",
        "...xTTTTTTTTx...", "..xtTTTTTTTTtx..", "..xtTTTTTTTTtx..", "..xSSTTTTTTSSx..",
        "..xSSTTTTTTSSx..", "..xSStTTTTtSSx..", "..xsStTTTTtSsx..", "..xsSBBBBBBSsx..",
        "..xxxNNNNNNxxx..", "....xNNNNNNx....",
    ],
    'side': [
        "................", "...xxxxxxx......", "..xCCCCCPPx.....", ".xCCCCCPLLPx....",
        ".xCCCCCCPPPCx...", ".xcCCCCCCCCCCCx.", "..xhhJHHJHHHx...", "..xhhhHSSSSSx...",
        "..xhhsrSSwESx...", "..xhhsrSSEESSx..", "...xhSSSSSSSx...", "...xsSSSSmSx....",
        "....xxSSSSx.....", ".....xSSSx......", ".....xsSSx......",
        "....xTTTTTFx....", "....xtTTTFGx....", "....xtSSTTGx....", "....xtSSTTTx....",
        "....xtSSTTTx....", "....xtSSTTTx....", "....xtssTTTx....", "....xBsSBBKx....",
        "....xNNNNNNx....", "....xNNNNNNx....",
    ],
}

SOPHIE = {
    'name': 'Sophie', 'legs': SLIM,
    'palette': {**SKIN, 'S': '#fbe3d3', 's': '#e9c3ac', 'p': '#f4b4ac', 'm': '#d08f8a', 'E': '#2a2026',
                'h': '#1a1512', 'H': '#2b2420', 'J': '#b8925e',
                'V': '#6b7044', 'v': '#525634', 'O': '#1d1d22'},
    'front': [
        "................", ".....xxxxxx.....", "....xHHHHHHx....", "...xHHHhhHHHx...",
        "..xHHHHSSHHHHx..", "..xHHHSSSSHHHx..", "..xHJSSSSSSJHx..", "..xJSSSSSSSSJx..",
        "..xJSwESSwESJx..", "..xJSEESSEESJx..", "..xJpSSSSSSpJx..", "..xHJSSmmSSJHx..",
        "..xHJxSSSSxJHx..", "..xHJxxSSxxJHx..", "..xJHxxSSxxHJx..",
        "..xJxVVSSVVxJx..", "..xJxvVVVVvxJx..", "..xHxVVVVVVxHx..", "..xSxVVVVVVxSx..",
        "..xSxVVVVVVxSx..", "..xSxvvvvvvxSx..", "..xsxVVVVVVxsx..", "...xVVVVVVVVx...",
        "..xvVVVVVVVVvx..", "..xvVVVVVVVVvx..",
    ],
    'back': [
        "................", ".....xxxxxx.....", "....xHHHHHHx....", "...xHHHhhHHHx...",
        "..xHHHHHHHHHHx..", "..xHHHHHHHHHHx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..",
        "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..",
        "..xHHHHHHHHHHx..", "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..",
        "..xJHHHHHHHHJx..", "..xJHHHHHHHHJx..", "..xHxHHHHHHxHx..", "..xSxVVVVVVxSx..",
        "..xSxVVVVVVxSx..", "..xSxvvvvvvxSx..", "..xsxVVVVVVxsx..", "...xVVVVVVVVx...",
        "..xvVVVVVVVVvx..", "..xvVVVVVVVVvx..",
    ],
    'side': [
        "................", "....xxxxxx......", "...xHHHHHHx.....", "..xHHHHHHHHx....",
        "..xHHHHHHHHHx...", "..xHHHHHHHSSx...", "..xHHHHHJSSSx...", "..xHHHHHJSSSx...",
        "..xHHHHsJSwEx...", "..xHHHHsJSEEx...", "..xHHHHHJSpSx...", "..xHHHHHJSmSx...",
        "..xHHHHHxSSx....", "..xHHHHHxSSx....", "..xHHHHHxSSx....",
        "..xHHxVVVVx.....", "..xHJxvVVVx.....", "..xHHxvSVVx.....", "...xHxvSVVx.....",
        ".....xvSVVx.....", ".....xvsvvx.....", ".....xVsVVx.....", ".....xVVVVx.....",
        "....xvVVVVVx....", "....xvVVVVVx....",
    ],
}

MOTHER = {
    'name': "Logan's Mother", 'legs': DRESS, 'draft': True,
    'palette': {**SKIN, 'm': '#c56f6c', 'h': '#8a6c45', 'H': '#b08e5e', 'J': '#cfae7c',
                'V': '#c48b98', 'v': '#a26f7c', 'O': '#8a6650'},
    'front': [
        "................", ".....xxxxxx.....", "....xHHJJHHx....", "...xHJJHHHHHx...",
        "..xHHHHHHHHHHx..", "..xHHHSSSSHHHx..", "..xHHSSSSSSHHx..", "..xHSSSSSSSSHx..",
        "..xHSwESSwESHx..", "..xHSEESSEESHx..", "..xHpSSSSSSpHx..", "..xHHSSmmSSHHx..",
        "..xHHhSSSShHHx..", "..xhHxxSSxxHhx..", "...xxxsSSsxxx...",
        "...xVVVSSVVVx...", "..xvVVVVVVVVvx..", "..xvVVVVVVVVvx..", "..xSSVVVVVVSSx..",
        "..xSSVVVVVVSSx..", "..xSSvvvvvvSSx..", "..xsSVVVVVVSsx..", "..xxvVVVVVVvxx..",
        "..xvVVVVVVVVvx..", ".xvVVVVVVVVVVvx.",
    ],
    'back': [
        "................", ".....xxxxxx.....", "....xHHHHHHx....", "...xHHJHHJHHx...",
        "..xHHHHHHHHHHx..", "..xHHHJHHJHHHx..", "..xHHHHHHHHHHx..", "..xHJHHHHHHJHx..",
        "..xHHHHHHHHHHx..", "..xHHHHHHHHHHx..", "..xhHHJHHJHHhx..", "..xhHHHHHHHHhx..",
        "..xhhHHHHHHhhx..", "..xhhhhhhhhhhx..", "...xxxsSSsxxx...",
        "...xVVVVVVVVx...", "..xvVVVVVVVVvx..", "..xvVVVVVVVVvx..", "..xSSVVVVVVSSx..",
        "..xSSVVVVVVSSx..", "..xSSvvvvvvSSx..", "..xsSVVVVVVSsx..", "..xxvVVVVVVvxx..",
        "..xvVVVVVVVVvx..", ".xvVVVVVVVVVVvx.",
    ],
    'side': [
        "................", "....xxxxxx......", "...xHHJJHHx.....", "..xHHHHHHJHx....",
        "..xHHHHHHHHHx...", "..xHHHHHHHSSx...", "..xHHHHHHSSSSx..", "..xHHHHHsSSSSx..",
        "..xHHHHHsSSwEx..", "..xHHHHHHSSEESx.", "..xHHHHHHSSpSx..", "..xHHHHHHSSmSx..",
        "..xhHHHHxSSSx...", "..xxhhhxxSSx....", ".......xsSSx....",
        "....xVVVVVVx....", "....xvVVVVVx....", "....xvVVVVVx....", "....xvSSVVVx....",
        "....xvSSVVVx....", "....xvssvvvx....", "....xvSSVVVx....", "....xvVVVVVx....",
        "...xvVVVVVVVx...", "...xvVVVVVVVx...",
    ],
}

FATHER = {
    'name': "Logan's Father", 'legs': TROUSERS, 'draft': True,
    'palette': {**SKIN, 'h': '#86683f', 'H': '#a98a5b', 'J': '#c3a476',
                'K': '#5e7891', 'k': '#4a6178', 'g': '#7891a8', 'W': '#f6f3ea', 'X': '#2e3a5c',
                'N': '#56708a', 'n': '#435a71', 'O': '#4a3426', 'o': '#6a4e3a'},
    'front': [
        "................", ".....xxxxxx.....", "....xHHHJJHx....", "...xHHHHHJJHx...",
        "..xHHHHHHHHHHx..", "..xhHHHHHHHHhx..", "..xhSSSSSSSShx..", "..xSSSSSSSSSSx..",
        "..xsSwESSwESsx..", "..xsSEESSEESsx..", "..xsSSSrrSSSsx..", "..xsSSSSSSSSsx..",
        "...xSSSmmSSSx...", "....xsSSSSsx....", ".....xsSSsx.....",
        "...xKKWXXWKKx...", "..xkKKWXXWKKkx..", "..xkKKKXXKKKkx..", "..xkKgKXXKgKkx..",
        "..xkKgKKKKgKkx..", "..xkKgKKKKgKkx..", "..xkkgKKKKgkkx..", "..xsSKKKKKKSsx..",
        "..xxxNNNNNNxxx..", "....xNNNNNNx....",
    ],
    'back': [
        "................", ".....xxxxxx.....", "....xHHHHHHx....", "...xHHHJHHHHx...",
        "..xHHHHHHHHHHx..", "..xhHHHHHHHHhx..", "..xhHHHHHHHHhx..", "..xhhHHHHHHhhx..",
        "..xshhhhhhhhsx..", "..xshhhhhhhhsx..", "...xshhhhhhsx...", "...xSSSSSSSSx...",
        "....xSSSSSSx....", ".....xSSSSx.....", ".....xsSSsx.....",
        "...xKKKKKKKKx...", "..xkKKKKKKKKkx..", "..xkKKKKKKKKkx..", "..xkKgKKKKgKkx..",
        "..xkKgKKKKgKkx..", "..xkKgKkkKgKkx..", "..xkkgKkkKgkkx..", "..xsSKKKKKKSsx..",
        "..xxxNNNNNNxxx..", "....xNNNNNNx....",
    ],
    'side': [
        "................", "....xxxxxx......", "...xHHHJJHxx....", "..xHHHHHJJHHx...",
        "..xhHHHHHHHHHx..", "..xhhHHHHHHHHx..", "..xhhhHHHSSSSx..", "..xhhhsSSSSSSx..",
        "..xhhsrSSSwESx..", "..xhhsrSSSEESSx.", "...xhsSSSSSSSx..", "...xsSSSSSmSx...",
        "....xsSSSSSx....", ".....xsSSSx.....", "......xsSsx.....",
        "....xKKKKWXx....", "....xKgKKKXx....", "....xKgKKKKx....", "....xKgKKKKx....",
        "....xKgKKKKx....", "....xKgKKKKx....", "....xkgKKKKx....", "....xKsSKKKx....",
        "....xNNNNNNx....", "....xNNNNNNx....",
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
                img.putpixel((x, y), ImageColor.getrgb(OUTLINE if ch == 'x' else pal[ch]) + (255,))
    return img


def frames_for(cid):
    c = CAST[cid]
    out = []
    for view, legs_key in (('front', 'front'), ('side', 'side'), ('back', 'front'), ('side', 'side')):
        top = list(c[view])
        assert len(top) == 25, (cid, view, len(top))
        if c.get('veil_edges') and view == 'front':          # veil falling behind, both sides
            top = [('v' + r[1:-1] + 'v') if 4 <= n <= 20 and r[0] == '.' and r[-1] == '.' else r
                   for n, r in enumerate(top)]
        out.append([frame(top + legs, c['palette'], f'{cid} {view}') for legs in c['legs'][legs_key]])
    out[3] = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in out[3]]
    return out


def main():
    from styles import font
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

    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    k = 6
    cw = 4 * (W * k + 12) + 40
    board = Image.new('RGBA', (max(1150, 40 + 2 * cw), 140 + 3 * (H * k + 140)), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Cozy Garden — the cast', font=font(40), fill=INK)
    d.text((40, 86), 'Our own style: Stardew\'s comfort with a touch of Pokémon. 16 × 32; front, right, back, left at 6×; '
                     'walk frames at 2× below.', font=font(17, False), fill=MUTED)
    for i, cid in enumerate(CAST):
        c, rows = CAST[cid], all_rows[cid]
        x0, y0 = 40 + (i % 2) * cw, 140 + (i // 2) * (H * k + 140)
        d.text((x0, y0), c['name'] + ('  ·  draft' if c.get('draft') else ''), font=font(22), fill=INK)
        panel = Image.new('RGBA', (cw - 30, H * k + 20), '#97b779')
        for r in range(4):
            panel.alpha_composite(rows[r][0].resize((W * k, H * k), Image.NEAREST), (8 + r * (W * k + 12), 10))
        board.alpha_composite(panel, (x0, y0 + 34))
        for r in range(4):
            for col in range(3):
                board.alpha_composite(rows[r][col].resize((W * 2, H * 2), Image.NEAREST),
                                      (x0 + r * (W * k + 12) + col * 34, y0 + 34 + H * k + 26))
    board.convert('RGB').save(REVIEW / 'cast.png', optimize=True)
    frames = []
    for col in (1, 0, 2, 0):
        fr = Image.new('RGBA', (len(CAST) * 2 * (W * 4 + 8) + 8, H * 4 + 16), '#97b779')
        for n, cid in enumerate(CAST):
            for m, r in enumerate((0, 1)):
                fr.alpha_composite(all_rows[cid][r][col].resize((W * 4, H * 4), Image.NEAREST),
                                   (8 + (2 * n + m) * (W * 4 + 8), 8))
        frames.append(fr.convert('RGB'))
    frames[0].save(REVIEW / 'cast-walking.gif', save_all=True, append_images=frames[1:], duration=170, loop=0)


if __name__ == '__main__':
    main()
