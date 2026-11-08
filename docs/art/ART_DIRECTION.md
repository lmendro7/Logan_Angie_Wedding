# World sprites and dialogue portraits

Current direction approved November 7, 2026. This document records the requested presentation; the runtime assets and portrait UI remain to be built.

| Asset | Intended presentation | Preparation and review |
| --- | --- | --- |
| World sprite | Very basic, highly pixelated character, readable at the small size used on the map | Original four-direction sprites at a consistent logical resolution, scale, palette, baseline, and frame alignment; review at actual game scale and with crisp nearest-neighbor enlargement |
| Dialogue portrait | Separate, more detailed character image beside the speaking character's name | Adapt retained detailed designs, matching the approved appearance and outfit; review crop and phone readability before integration |

Each of Logan, Angie, Ryan, Sophie, Logan's Mother, and Logan's Father needs both representations. Keep the detailed designs; they are appearance references for portraits. Review boards are not animation-ready sprite sheets or finished portrait crops. Exact sprite dimensions, animation frame counts, and portrait dimensions remain open. A previously suggested 16 by 32 pixels was a proposal, not an approved specification.

## Current references

- Logan: [approved appearance](logan-approved-01/README.md), with youthful slim face, rounded nose, smaller head, soft short dirty-blond hair and beard, black suit, white shirt, and black bow tie. The draft 01 walking animation shows an older appearance.
- Angie: [approved appearance](angie-approved-01/README.md), with slim arms, elongated oval face, softly wavy brown hair, glasses, and a white sleeveless wedding dress.
- Ryan: [approved simple map-sprite design](ryan-approved-01/README.md), with skinny build, brown/off-white cap worn on his head, short swept sandy blond hair, cream flower button-down, sunglasses at neckline, navy trousers, and a slightly lowered waistband. Retain the [earlier detailed studies](ryan-review-01/README.md) for portrait development, updating their cap, hair, and body proportions to match the current approved design.
- Sophie: individual appearance review pending. Short black hair and pale skin; shy, funny, sarcastic, and introverted.
- Parents: individual model details remain deferred. Preserve the display names Logan's Mother and Logan's Father.

## Next work

1. Use Ryan's approved design to prepare an aligned runtime sprite sheet and review it at the game's actual scale. Done as [Ryan runtime sprite 01](ryan-sprite-01/README.md) (16 × 32 frames, proposed), awaiting review. Once approved, use the same frame size, layout, anchor and palette approach for the other characters.
2. Review the remaining characters individually before applying final visuals.
3. Prepare separate portraits, then implement the image beside the speaker's name and check phone readability.

Use Stardew Valley only as a reference for the small world-sprite scale and simplicity. Create original art and preserve the existing attribution chain. Keep the approved map and gameplay. [Character status](CHARACTER_STATUS.md) distinguishes approved appearance decisions from unfinished implementation.
