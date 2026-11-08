"""Rebuild the review sprite and previews from pinned LPC art layers.

Requires Pillow. Pass a checkout of recipe.json's source commit as argv[1].
Original files are read only; the output sprite composition is CC-BY-SA 4.0.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
import sys

OUT = Path(__file__).resolve().parent
SOURCE = Path(sys.argv[1])
recipe = json.loads((OUT / 'recipe.json').read_text())
sheet = Image.new('RGBA', (576, 256))
for layer in recipe['layers']:
    with Image.open(SOURCE / layer['path']) as source:
        sheet.alpha_composite(source.convert('RGBA').crop(tuple(recipe['source_crop'])))
sheet.save(OUT / 'logan-walk.png')

CREAM = '#f4edda'
GREEN = '#263f32'
PANEL = '#d8dfbf'
def font(size, bold=False):
    path = '/usr/share/fonts/truetype/dejavu/DejaVuSans' + ('-Bold' if bold else '') + '.ttf'
    return ImageFont.truetype(path, size)

def tile(row, col=0):
    return sheet.crop((col * 64, row * 64, (col + 1) * 64, (row + 1) * 64))

board = Image.new('RGBA', (640, 760), CREAM)
d = ImageDraw.Draw(board)
d.text((36, 24), 'CHARACTER REVIEW  /  01', fill=GREEN, font=font(16, True))
d.text((36, 60), 'Logan', fill=GREEN, font=font(42, True))
d.text((36, 119), 'Black suit. White shirt. Ready for the wedding.', fill=GREEN, font=font(19))
for row, (name, x, y) in enumerate([('BACK', 36, 430), ('LEFT', 340, 430), ('FRONT', 36, 166), ('RIGHT', 340, 166)]):
    d.rounded_rectangle((x, y, x + 264, y + 238), radius=10, fill=PANEL)
    board.alpha_composite(tile(row).resize((192, 192), Image.Resampling.NEAREST), (x + 36, y + 6))
    d.text((x + 20, y + 209), name, fill=GREEN, font=font(13, True))
d.text((36, 697), 'Appearance draft — awaiting your review', fill=GREEN, font=font(18))
d.text((36, 729), 'LPC artwork • credits and source layers recorded in the repository', fill='#68745c', font=font(13))
board.convert('RGB').save(OUT / 'logan-review.png')

frames = []
for row, name in [(2, 'FRONT'), (3, 'RIGHT'), (0, 'BACK'), (1, 'LEFT')]:
    for col in range(1, 9):
        frame = Image.new('RGBA', (420, 440), CREAM)
        fd = ImageDraw.Draw(frame)
        fd.text((28, 24), 'LOGAN / WALKING PREVIEW', fill=GREEN, font=font(16, True))
        fd.rounded_rectangle((28, 68, 392, 355), radius=12, fill=PANEL)
        frame.alpha_composite(tile(row, col).resize((256, 256), Image.Resampling.NEAREST), (82, 70))
        fd.text((47, 325), name, fill=GREEN, font=font(13, True))
        fd.text((28, 378), 'Character draft 01', fill=GREEN, font=font(22, True))
        fd.text((28, 414), 'LPC artwork • draft for review', fill='#68745c', font=font(13))
        frames.append(frame.convert('RGB'))
palette = frames[0].quantize(colors=256)
indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
indexed[0].save(OUT / 'logan-walking.gif', save_all=True, append_images=indexed[1:], duration=130, loop=0, disposal=1, optimize=True)
print('Composed 36 frames, review board, and four-direction animation.')
