"""Draft Logan in several pixel-art styles so Lucas can choose one.

    python3 tools/sprites/styles.py

Every style is original hand-placed art in the spirit of a genre, not copied
from any game. Logan wears the look Lucas preferred: white shirt, black bow
tie, black trousers and belt; trimmed warm-brown beard; short ash-brown hair.
The LPC column uses docs/art/logan-lpc-01/logan-walk.png (built separately).
Writes docs/art/style-options-01/logan-styles.png.
"""
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs' / 'art' / 'style-options-01'

BASE = {
    'x': '#2b1d1d', 'y': '#4a3826', 'z': '#a8705a', 'q': '#8d8a82',
    'h': '#5c4834', 'H': '#8a6e50', 'J': '#b0916a', 'L': '#cfb48a',
    'S': '#f5cfa6', 's': '#e0a982', 'r': '#c98a6c',
    'E': '#3d2a1e', 'w': '#ffffff',
    'b': '#8c5a34', 'B': '#6a4024', 'c': '#a8724a',
    'W': '#f7f5ef', 'V': '#d6d1c4', 'X': '#17171c',
    'N': '#2d2e36', 'n': '#1f2026', 'K': '#3a2a20', 'Y': '#c9a24a',
    'O': '#1a1a1e', 'o': '#3a3a44',
}

STYLES = [
    {
        'key': 'cozy',
        'name': 'A · Cozy farm-life',
        'blurb': ['16 × 32 · dark outline, eye', 'whites, 3–4 tone shading', '(Stardew-like)'],
        'palette': BASE,
        'front': [
            ".....xxxxxx.....",
            "...xxJLLJHHxx...",
            "..xHJLJJHHHHHx..",
            "..xHHJHHHHhHHx..",
            "..xhHHHHHhHHhx..",
            "..xhhSSSSSShhx..",
            "..xhSSSSSSSShx..",
            "..xsShhSShhSsx..",
            "..xsSwESSwESsx..",
            "..xsSEESSEESsx..",
            "..xxcSSrrSScxx..",
            "...xbcSSSScbx...",
            "...xbbBBBBbbx...",
            "....xbbbbbbx....",
            ".....xsSSsx.....",
            ".xVWWWXXXXWWWVx.",
            ".xVWWWWXXWWWWVx.",
            ".xVWxWWVVWWxWVx.",
            ".xVWxWWWVWWxWVx.",
            ".xVWxWWWVWWxWVx.",
            ".xVWxKKKYKKxWVx.",
            ".xsSxNNNNNNxSsx.",
            ".xxxxNNNNNNxxxx.",
            "....xNNNNNNx....",
            "....xNNnnNNx....",
            "....xNNxxNNx....",
            "....xNnxxnNx....",
            "....xNnxxnNx....",
            "....xNnxxnNx....",
            "...xOOoxxoOOx...",
            "...xOOOxxOOOx...",
            "...xxxxxxxxxx...",
        ],
        'side': [
            "....xxxxxx......",
            "...xHJJLLJxx....",
            "..xHHHJJLJJHx...",
            "..xhHHHHJJHHHx..",
            "..xhHHHHHHHHHx..",
            "..xhhHHHHHSSSx..",
            "..xhhhHHSSSSSx..",
            "..xhhhsSSShhSx..",
            "..xhhsrSSSwESx..",
            "..xhhsrSSSEESSx.",
            "...xhcSSSSSSSx..",
            "...xbbcSSSScx...",
            "...xbbbbbBBbx...",
            "....xbbbbbbx....",
            "......xsSsx.....",
            "....xVWWWXXx....",
            "....xVWWWWXx....",
            "....xVWVWWWx....",
            "....xVWVWWWx....",
            "....xVWVWWWx....",
            "....xKKKKKYx....",
            "....xNsSNNNx....",
            "....xNNNNNNx....",
            "....xNNNNNNx....",
            "....xNNNNNNx....",
            ".....xnNNNx.....",
            ".....xnNNNx.....",
            ".....xnNNNx.....",
            "....xOOOOOOx....",
            "....xOOOOOOx....",
            "....xxxxxxxx....",
            "................",
        ],
    },
    {
        'key': 'handheld',
        'name': 'B · Handheld RPG',
        'blurb': ['16 × 24 · big head, short', 'body, bold outline', '(classic monster-catcher era)'],
        'palette': {**BASE, 'x': '#202020'},
        'front': [
            ".....xxxxxx.....",
            "...xxHHJJHHxx...",
            "..xHHJJLJHHHHx..",
            "..xHHHHHHHHHHx..",
            ".xhHHHHHHHHHHhx.",
            ".xhhSSSSSSSShhx.",
            ".xhSSSSSSSSSShx.",
            ".xSSSESSSSESSSx.",
            ".xSSSESSSSESSSx.",
            ".xscSSSSSSSScsx.",
            "..xbbSSBBSSbbx..",
            "...xbbbbbbbbx...",
            "....xxSSSSxx....",
            "..xWWWXXXXWWWx..",
            ".xVWWWWXXWWWWVx.",
            ".xVWxWWWWWWxWVx.",
            ".xVWxWWWWWWxWVx.",
            ".xsSxKKKYKKxSsx.",
            ".xxxxNNNNNNxxxx.",
            "....xNNxxNNx....",
            "....xNnxxnNx....",
            "...xOOOxxOOOx...",
            "...xOOOxxOOOx...",
            "...xxxxxxxxxx...",
        ],
        'side': [
            "....xxxxxx......",
            "...xHHJJHHxx....",
            "..xHHHHJJJHHx...",
            "..xhHHHHHHHHHx..",
            ".xhhHHHHHHHHHx..",
            ".xhhhHHHHSSSSx..",
            ".xhhhsHSSSSSSx..",
            ".xhhhsSSSSSESx..",
            ".xhhhsSSSSSESSx.",
            "..xhcSSSSSSSSx..",
            "..xbbbSSSBBbx...",
            "...xbbbbbbbx....",
            ".....xxSSSx.....",
            "....xWWWWXXx....",
            "....xVWWWWXx....",
            "....xVWVWWWx....",
            "....xVWVWWWx....",
            "....xKsSKKYx....",
            "....xNNNNNNx....",
            ".....xnNNNx.....",
            ".....xnNNNx.....",
            "....xOOOOOOx....",
            "....xOOOOOOx....",
            "....xxxxxxxx....",
        ],
    },
    {
        'key': 'retro',
        'name': 'C · Retro 8-bit',
        'blurb': ['16 × 24 · four flat colours,', 'no shading, no outline', '(early console)'],
        'palette': {'k': '#101010', 'h': '#9c6a3c', 'S': '#fcbc94', 'W': '#fcfcfc'},
        'front': [
            "................",
            "................",
            ".....hhhhhh.....",
            "....hhhhhhhh....",
            "...hhhhhhhhhh...",
            "...hSSSSSSSSh...",
            "...hSkSSSSkSh...",
            "...hSkSSSSkSh...",
            "....SSSSSSSS....",
            "....hSSkkSSh....",
            ".....hhhhhh.....",
            "......SSSS......",
            "...WWWkkkkWWW...",
            "..WWWWWkkWWWWW..",
            "..WW.WWWWWW.WW..",
            "..WW.WWWWWW.WW..",
            "..WW.WWWWWW.WW..",
            "..SS.kkkkkk.SS..",
            ".....kkkkkk.....",
            ".....kk..kk.....",
            ".....kk..kk.....",
            ".....kk..kk.....",
            "....kkk..kkk....",
            "....kkk..kkk....",
        ],
        'side': [
            "................",
            "................",
            ".....hhhhhh.....",
            "....hhhhhhhh....",
            "...hhhhhhhhhh...",
            "...hhhhhSSSSS...",
            "...hhhhSSSSkS...",
            "...hhhSSSSSkSS..",
            "....hhSSSSSSS...",
            "....hhhSSSkkh...",
            ".....hhhhhhh....",
            "......SSSS......",
            ".....WWWWWkk....",
            ".....WWWWWWk....",
            ".....WWWWWW.....",
            ".....WWSSWW.....",
            ".....WWSSWW.....",
            ".....kkSSkk.....",
            ".....kkkkkk.....",
            "......kkkk......",
            "......kkkk......",
            "......kkkk......",
            ".....kkkkkkk....",
            ".....kkkkkkk....",
        ],
    },
    {
        'key': 'hibit',
        'name': 'D · Detailed hi-bit',
        'blurb': ['24 × 40 · tinted outlines,', 'soft 4–5 tone shading,', 'taller proportions (modern indie)'],
        'palette': BASE,
        'front': [
            "........................",
            "..........yyyy..........",
            "........yyJLLJyy........",
            "......yyHJLLJJHHyy......",
            ".....yHHHJJJHHHHHHy.....",
            ".....yHHHHJHHHHhHHy.....",
            ".....yhHHHHHHHHHHhy.....",
            ".....yhhSSSSSSSShhy.....",
            ".....yhSSSSSSSSSShy.....",
            ".....zsShhSSSShhSsz.....",
            ".....zsSwESSSSwESsz.....",
            ".....zsSEESSSSEESsz.....",
            ".....zsSSSSrrSSSSsz.....",
            ".....zcSSSSrSSSSScz.....",
            "......zcbSSSSSSbcz......",
            "......zbbbBBBBbbbz......",
            ".......zbbbbbbbbz.......",
            "........zbbbbbbz........",
            ".........zsSSsz.........",
            "....qWWWWWWXXWWWWWWq....",
            "....qVWWWWXXXXWWWWVq....",
            "....qVWWWWWXXWWWWWVq....",
            "....qVWWqWWWVWWqWWVq....",
            "....qVWWqWWWVWWqWWVq....",
            "....qVWWqWWWVWWqWWVq....",
            "....qVWWqWWWVWWqWWVq....",
            "....qVWWqWWWVWWqWWVq....",
            "....qVVWqKKKYKKqWVVq....",
            "....zsSSxNNNNNNxSSsz....",
            "....zzzzxNNNNNNxzzzz....",
            "........xNNNnNNx........",
            "........xNNnxnNNx.......",
            "........xNNnxnNNx.......",
            "........xNNnxnNNx.......",
            "........xNNnxnNNx.......",
            "........xNNnxnNNx.......",
            ".......xOOOoxoOOOx......",
            ".......xOOOOxOOOOx......",
            ".......xxxxxxxxxxx......",
            "........................",
        ],
        'side': [
            "........................",
            ".........yyyy...........",
            ".......yyJLLJyy.........",
            "......yHHJLLJJHyy.......",
            ".....yHHHHJJJHHHHy......",
            ".....yhHHHHHJJHHHHy.....",
            ".....yhhHHHHHHHHHHy.....",
            ".....yhhhHHHHHSSSSy.....",
            ".....yhhhhHHSSSSSSy.....",
            ".....yhhhhsSSSShhSz.....",
            ".....yhhhzsrSSSSwEz.....",
            ".....yhhhzsrSSSSEESz....",
            "......yhhzsSSSSSSSSSz...",
            "......yhcSSSSSSSSSz.....",
            ".......ycbbSSSSSSz......",
            ".......zbbbbbBBbbz......",
            "........zbbbbbbbz.......",
            ".........zbbbbbz........",
            "..........zsSsz.........",
            ".......qWWWWWWXXq.......",
            ".......qVWWWWWXXXq......",
            ".......qVWWWWWWXq.......",
            ".......qVWqWWqWWq.......",
            ".......qVWqWWqWWq.......",
            ".......qVWqWWqWWq.......",
            ".......qVWqWWqWWq.......",
            ".......qVWqWWqWWq.......",
            ".......qKKqWWqKYq.......",
            ".......xNNzsSzNNx.......",
            ".......xNNNzzNNNx.......",
            ".......xNNNNNNNNx.......",
            "........xnNNNNNx........",
            "........xnNNNNNx........",
            "........xnNNNNNx........",
            "........xnNNNNNx........",
            "........xnNNNNNx........",
            ".......xOOOOOOOOOx......",
            ".......xOOOOOOOOOx......",
            ".......xxxxxxxxxxx......",
            "........................",
        ],
    },
]


def render(rows, palette, label):
    w = len(rows[0])
    img = Image.new('RGBA', (w, len(rows)), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == w, (label, y, row, len(row))
        for x, ch in enumerate(row):
            if ch != '.':
                img.putpixel((x, y), ImageColor.getrgb(palette[ch]) + (255,))
    return img


def font(size, bold=True):
    name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/' + name, size)
    except OSError:
        return ImageFont.load_default()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    columns = []
    for st in STYLES:
        columns.append((st['name'], st['blurb'],
                        render(st['front'], st['palette'], st['key'] + ' front'),
                        render(st['side'], st['palette'], st['key'] + ' side'), 0))
    lpc = ROOT / 'docs/art/logan-lpc-01/logan-walk.png'
    if lpc.exists():
        sheet = Image.open(lpc).convert('RGBA')
        front = sheet.crop((0, 128, 64, 192)).crop((12, 8, 52, 64))
        side = sheet.crop((0, 192, 64, 256)).crop((12, 8, 52, 64))
        columns.append(('E · Original (LPC)', ['64 × 64 frames · finer detail,', 'realistic proportions', '(the original model)'],
                        front, side, 2))

    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    colw = 300
    board = Image.new('RGBA', (60 + colw * len(columns), 1060), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Logan — art style drafts', font=font(40), fill=INK)
    d.text((40, 84), 'Same outfit in each style. Top: enlarged so each fills about the same height. '
                     'Bottom: true size side by side at 3×.', font=font(18, False), fill=MUTED)
    target = 380
    for i, (name, blurb, front, side, feet_pad) in enumerate(columns):
        x0 = 40 + i * colw
        d.text((x0, 130), name, font=font(22), fill=INK)
        for j, line in enumerate(blurb):
            d.text((x0, 162 + j * 22), line, font=font(15, False), fill=MUTED)
        k = max(1, min(target // front.height, ((colw - 20) // 2 - 8) // front.width))
        panel = Image.new('RGBA', (colw - 20, target + 40), '#97b779')
        for m, img in enumerate((front, side)):
            big = img.resize((img.width * k, img.height * k), Image.NEAREST)
            px = m * (colw - 20) // 2 + ((colw - 20) // 2 - big.width) // 2
            panel.alpha_composite(big, (max(0, px), panel.height - big.height - 10))
        board.alpha_composite(panel, (x0, 240))
        d.text((x0, 240 + target + 48), f'front · right   ({k}×)', font=font(14, False), fill=MUTED)
    # True-size lineup.
    gy = 760
    d.text((40, gy), 'True size at 3× (how they compare on the same map)', font=font(22), fill=INK)
    strip = Image.new('RGBA', (board.width - 80, 220), '#97b779')
    for i, (name, _, front, _, feet_pad) in enumerate(columns):
        big = front.resize((front.width * 3, front.height * 3), Image.NEAREST)
        cx = 40 + i * colw + 110
        base = 190
        sd = ImageDraw.Draw(strip, 'RGBA')
        sd.ellipse([cx - 40 + 20, base - 6, cx + 40 - 20 + 20, base + 6], fill=(38, 60, 48, 70))
        strip.alpha_composite(big, (cx - big.width // 2 + 20, base - big.height + feet_pad * 3))
    board.alpha_composite(strip, (40, gy + 40))
    board.convert('RGB').save(OUT / 'logan-styles.png', optimize=True)




# ------------------------------------------------- style A eye variants (review)
# Each variant replaces face rows 6-9 of style A's front and side views.
EYE_VARIANTS = [
    ('1 · Current: white + dark', {}, {}),
    ('2 · Simple dark eyes', {
        8: "..xsSESSSSESsx..", 9: "..xsSESSSSESsx.."}, {
        8: "..xhhsrSSSSESx..", 9: "..xhhsrSSSSESSx."}),
    ('3 · Brown iris + shine', {
        8: "..xsSwiSSwiSsx..", 9: "..xsSiESSiESsx.."}, {
        8: "..xhhsrSSSwiSx..", 9: "..xhhsrSSSiESSx."}),
    ('4 · Blue-grey iris + shine', {
        8: "..xsSwuSSwuSsx..", 9: "..xsSuESSuESsx.."}, {
        8: "..xhhsrSSSwuSx..", 9: "..xhhsrSSSuESSx."}),
    ('5 · Big friendly eyes', {
        6: "..xhShhSShhShx..", 7: "..xsSwESSwESsx..", 8: "..xsSEESSEESsx..", 9: "..xsSEESSEESsx.."}, {
        7: "..xhhhsSSSwESx..", 8: "..xhhsrSSSEESx..", 9: "..xhhsrSSSEESSx."}),
    ('6 · Happy closed (^ ^)', {
        8: "..xsSESSSSESsx..", 9: "..xsESESSESEsx.."}, {
        8: "..xhhsrSSSSESx..", 9: "..xhhsrSSSESESx."}),
]


def eye_board():
    a = STYLES[0]
    pal = {**a['palette'], 'i': '#6b4a32', 'u': '#5f7d94'}
    BG, INK, MUTED = '#f7efe9', '#14634a', '#5d6b64'
    colw, k = 290, 8
    board = Image.new('RGBA', (40 + colw * len(EYE_VARIANTS), 860), BG)
    d = ImageDraw.Draw(board, 'RGBA')
    d.text((40, 30), 'Logan — style A eye options', font=font(40), fill=INK)
    d.text((40, 84), 'Front and right at 8×; bottom row at 3× true size. Everything else is unchanged.',
           font=font(18, False), fill=MUTED)
    strip = Image.new('RGBA', (board.width - 80, 150), '#97b779')
    for i, (label, front_rows, side_rows) in enumerate(EYE_VARIANTS):
        front = [front_rows.get(n, r) for n, r in enumerate(a['front'])]
        side = [side_rows.get(n, r) for n, r in enumerate(a['side'])]
        f, s = render(front, pal, label + ' front'), render(side, pal, label + ' side')
        x0 = 40 + i * colw
        d.text((x0, 130), label, font=font(18), fill=INK)
        panel = Image.new('RGBA', (colw - 20, 300), '#97b779')
        panel.alpha_composite(f.resize((16 * k, 32 * k), Image.NEAREST), (2, 22))
        panel.alpha_composite(s.resize((16 * k, 32 * k), Image.NEAREST), (138, 22))
        board.alpha_composite(panel, (x0, 165))
        head = f.crop((0, 0, 16, 16)).resize((16 * 10, 16 * 10), Image.NEAREST)
        board.alpha_composite(head, (x0 + 50, 490))
        strip.alpha_composite(f.resize((48, 96), Image.NEAREST), (i * colw + 110, 30))
    d.text((40, 650), 'True size at 3×', font=font(16, False), fill=MUTED)
    d.text((40, 470), 'Face close-up (10×)', font=font(16, False), fill=MUTED)
    board.alpha_composite(strip, (40, 670))
    board.convert('RGB').save(OUT / 'logan-A-eyes.png', optimize=True)


if __name__ == '__main__':
    main()
    eye_board()
