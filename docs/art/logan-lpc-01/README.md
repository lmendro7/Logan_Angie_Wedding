# Logan — original-style walking sprite 01

**Awaiting Lucas's review. Not yet in the game.**

![Review board](logan-lpc-review.png)

![Walking preview](logan-walking.gif)

This rebuilds Logan in the style of his [approved board](../logan-approved-01/README.md), which started from the LPC layers in [draft 01](../logan-draft-01/README.md). The approved board itself is a single still image with no walking frames, so the game needs a rebuilt sheet.

## What changed from draft 01

- The buzzcut is replaced by the LPC "cowlick" hair: short sides with a lifted, textured top.
- The trimmed beard is replaced by the fuller "medium" beard.
- Colours follow reference photos Lucas supplied on November 8, 2026: light ash-brown hair, lighter on top, and a warmer ginger-brown beard. The photos are not stored in the repository and no photo pixels are used.
- The darkest stock skin shadow, which read as bright red, is softened to a warm brown.
- Same black suit, white shirt, bow tie (mostly hidden by the beard) and black shoes.

![Close-up](logan-closeup.png)

Other haircut and beard combinations in the same colours, for comparison:

![Hair and beard options](logan-hair-beard-options.png)

## Sheet

- `logan-walk.png`: 576 × 256 px, 64 × 64 frames, 9 columns. Rows are up, left, down, right. Column 0 is standing; columns 1–8 are the walk cycle.
- The figure is about 46 px tall, larger than the 16 × 32 sprites. Using this style means the other characters need the same style and size, and the garden scale may need adjusting.

## Rebuild

Needs a checkout of the LPC generator at the commit pinned in `recipe.json` (Pillow required):

```sh
python3 tools/sprites/lpc_logan.py /path/to/Universal-LPC-Spritesheet-Character-Generator
```

## Licence and credits

The composition is distributed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). `recipe.json` lists every layer with its artists, licence and source links. The hair is CC0 (bluecarrot16 and ElizaWy); the other layers keep the CC-BY-SA 3.0 or OGA-BY 3.0 choices recorded in draft 01. Changes: layer composition, hair and beard swaps, hair, beard and skin-shadow recolouring, nearest-neighbour preview enlargement. These credits must appear in the game's credits before this sprite ships. No personal photo pixels are used.
