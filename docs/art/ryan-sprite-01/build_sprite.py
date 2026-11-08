"""Build Ryan's runtime map sprite sheet and review previews.

Every pixel is hand-placed below (original art, guided by the approved design
board docs/art/ryan-approved-01/ryan-review.png). Requires Pillow.

    python3 build_sprite.py          # writes outputs next to this script

Sheet layout: 16x32 px frames; rows = down, right, up, left;
columns = stand, step A, step B. Feet touch the bottom row (origin 0.5, 1).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 16, 32

PAL = {
    '.': None,
    'c': '#5b3526',  # cap dark edge
    'C': '#7b4a33',  # cap brown
    'P': '#efe5d2',  # cap front panel (off-white)
    'L': '#8b90a8',  # cap logo
    'h': '#a8773f',  # hair shadow
    'H': '#c99a57',  # sandy blond
    'J': '#e3bd77',  # hair highlight
    's': '#d8a47e',  # skin shade
    'S': '#f1c9a0',  # skin
    'E': '#3a2820',  # eyes
    't': '#d6c296',  # shirt shade
    'T': '#f3e5c2',  # cream shirt
    'F': '#e65f55',  # coral flower
    'G': '#5a3a2a',  # sunglasses
    'B': '#6a4128',  # belt
    'K': '#c9a03f',  # buckle
    'n': '#232842',  # trouser shade
    'N': '#323858',  # navy trousers
    'O': '#77482a',  # shoes
    'o': '#4e2f1c',  # soles
}

FRONT_TOP = [
    ".....cCCCCc.....",
    "...cCPPPPPPCc...",
    "...CPPLLLLPPC...",
    "...CPPPPPPPPC...",
    "..cCCCCCCCCCCc..",
    "..hHJHHJJHHJHh..",
    "..hHSSSSSSSSHh..",
    "..hHSESSSSESHh..",
    "..hHSESSSSESHh..",
    "...sSSSSSSSSs...",
    "....SSSSSSSS....",
    ".....sSSSSs.....",
    "......SSSS......",
    "...TTTTSSTTTT...",
    "...tTTTGTFTTt...",
    "...tTTTTFFFTt...",
    "....StTGTFTS....",
    "....StTTTTTS....",
    "....StTTTTTS....",
    "....StTTTTTS....",
    "....StTTTTTS....",
    "....stTTTTTs....",
    ".....BBKKBB.....",
    ".....NNNNNN.....",
    ".....NNNNNN.....",
]
BACK_TOP = [
    ".....cCCCCc.....",
    "...cCCCCCCCCc...",
    "...CCCCCCCCCC...",
    "...CCCCCCCCCC...",
    "...cCCchhcCCc...",
    "..hHHJJHHJJHHh..",
    "..hHHHHHHHHHHh..",
    "..hHHHHHHHHHHh..",
    "...hHHHHHHHHh...",
    "...shHHHHHHhs...",
    "....hHHHHHHh....",
    ".....sSSSSs.....",
    "......SSSS......",
    "...TTTTTTTTTT...",
    "...tTTTTTTTTt...",
    "...tTTTTTTTTt...",
    "....STTTTTtS....",
    "....STTTTTtS....",
    "....STTTTTtS....",
    "....STTTTTtS....",
    "....STTTTTtS....",
    "....sTTTTTts....",
    ".....BBBBBB.....",
    ".....NNNNNN.....",
    ".....NNNNNN.....",
]
# Front/back legs (rows 25-31): stand, step A (left foot lifted), step B.
FB_LEGS = [
    [".....NN..NN.....", ".....NN..NN.....", ".....Nn..nN.....", ".....Nn..nN.....",
     ".....Nn..nN.....", "....OOO..OOO....", "....ooo..ooo...."],
    [".....NN..NN.....", ".....Nn..NN.....", ".....Nn..nN.....", "....OOO..nN.....",
     "....ooo..nN.....", ".........OOO....", ".........ooo...."],
    [".....NN..NN.....", ".....NN..nN.....", ".....Nn..nN.....", ".....Nn..OOO....",
     ".....Nn..ooo....", "....OOO.........", "....ooo........."],
]
SIDE_TOP = [
    "....cCCCCc......",
    "...cCCCCPPPc....",
    "...CCCCPPLLPc...",
    "...CCCCCPPPPC...",
    "...cCCCCCCCCCCc.",
    "...hHHJHHJHHh...",
    "...hHHHHSSSSS...",
    "...hHHsSSSSES...",
    "...hHHsSSSSESS..",
    "....hHSSSSSSS...",
    ".....hSSSSSS....",
    "......sSSSs.....",
    ".......SSS......",
    "......TttTT.....",
    "......tttTTF....",
    "......tttTFG....",
    "......tSSTTG....",
    "......tSSTT.....",
    "......tSSTT.....",
    "......tSSTT.....",
    "......tSSTT.....",
    "......tssTT.....",
    "......BBBBK.....",
    "......NNNNN.....",
    "......NNNNN.....",
]
SIDE_LEGS = [
    ["......nNNN......", "......nNNN......", "......nNNN......", "......nNNN......",
     "......nNNN......", "......OOOOO.....", "......ooooo....."],
    [".....nnNNN......", ".....nn.NN......", "....nn...NN.....", "....nn...NN.....",
     "...nn.....NN....", "..OOO.....OOOO..", "..ooo.....oooo.."],
    [".....NNnnn......", ".....NN.nn......", "....NN...nn.....", "....NN...nn.....",
     "...NN.....nn....", "..OOO.....OOOO..", "..ooo.....oooo.."],
]


def frame(rows):
    assert len(rows) == H, len(rows)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == W, (y, row)
        for x, ch in enumerate(row):
            if PAL[ch]:
                img.putpixel((x, y), Image.new('RGB', (1, 1), PAL[ch]).getpixel((0, 0)) + (255,))
    return img


def build_frames():
    down = [frame(FRONT_TOP + legs) for legs in FB_LEGS]
    up = [frame(BACK_TOP + legs) for legs in FB_LEGS]
    right = [frame(SIDE_TOP + legs) for legs in SIDE_LEGS]
    left = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in right]
    return [down, right, up, left]


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
    rows = build_frames()
    sheet = Image.new('RGBA', (W * 3, H * 4), (0, 0, 0, 0))
    for r, frames in enumerate(rows):
        for c, f in enumerate(frames):
            sheet.paste(f, (c * W, r * H))
    sheet.save(OUT / 'ryan-sheet.png')
    scaled(sheet, 8).save(OUT / 'ryan-sheet-x8.png')

    # Walking GIF: four directions side by side, cycle stand-A-stand-B.
    k, pad = 6, 12
    gif = []
    for i in [1, 0, 2, 0]:
        canvas = Image.new('RGBA', (4 * (W * k + pad) + pad, H * k + 2 * pad), '#97b779')
        d = ImageDraw.Draw(canvas, 'RGBA')
        for r, frames in enumerate(rows):
            x0 = pad + r * (W * k + pad)
            shadow(d, x0 + W * k // 2, pad + H * k, k)
            canvas.alpha_composite(scaled(frames[i], k), (x0, pad))
        gif.append(canvas.convert('RGB'))
    gif[0].save(OUT / 'ryan-walking.gif', save_all=True, append_images=gif[1:], duration=170, loop=0)

    # Review board.
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    k = 8
    board = Image.new('RGBA', (1150, 1240), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((60, 50), 'Ryan — runtime map sprite 01', font=font(46), fill=INK)
    d.text((60, 112), '16 × 32 px frames · 4 directions × 3 frames · shown 8× below', font=font(22), fill=MUTED)
    labels = ['FRONT', 'RIGHT', 'BACK', 'LEFT']
    for r, frames in enumerate(rows):
        x0 = 60 + r * 270
        d.text((x0 + 64 - d.textlength(labels[r], font=font(22)) / 2, 172), labels[r], font=font(22), fill=INK)
        board.alpha_composite(scaled(frames[0], k), (x0, 210))
    d.text((60, 500), 'Walk frames (stand · step A · step B)', font=font(26), fill=INK)
    for r, frames in enumerate(rows):
        for c, f in enumerate(frames):
            board.alpha_composite(scaled(f, 4), (60 + r * 270 + c * 72, 545))
    # Actual game scale: garden at camera zoom 1 means 1 sprite px = 1 CSS px.
    d.text((60, 715), 'Actual game scale on a phone (1×), and 2× / 3×', font=font(26), fill=INK)
    for j, s in enumerate([1, 2, 3]):
        gx, gy, gw, gh = 60 + j * 345, 760, 320, 170
        d.rectangle([gx, gy, gx + gw, gy + gh], fill='#97b779')
        d.rectangle([gx + gw // 2 - 22 * s // 2, gy, gx + gw // 2 + 22 * s // 2, gy + gh], fill='#d9bd87')
        for r, frames in enumerate(rows):
            cx = gx + 40 + r * 80
            base = gy + gh // 2 + 16 * s
            shadow(d, cx, base, s)
            board.alpha_composite(scaled(frames[0], s), (cx - 8 * s, base - 32 * s))
        d.text((gx, gy + gh + 10), f'{s}×' + ('  (current garden zoom)' if s == 1 else ''), font=font(20), fill=MUTED)
    d.text((60, 990), 'Palette', font=font(26), fill=INK)
    for i, (ch, col) in enumerate((k_, v) for k_, v in PAL.items() if v):
        d.rectangle([60 + i * 52, 1035, 100 + i * 52, 1075], fill=col, outline='#00000022')
    d.text((60, 1120), 'Original hand-placed pixels based on the approved Ryan design board.', font=font(22), fill=MUTED)
    d.text((60, 1155), 'Map sprite only — the detailed dialogue portrait is a separate asset.', font=font(22), fill=MUTED)
    board.convert('RGB').save(OUT / 'ryan-sprite-review.png')


if __name__ == '__main__':
    main()
