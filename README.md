# Logan & Angie Wedding Game

A repository for planning and developing an interactive wedding game.

## Continue from the recovered art and notes

Read [SESSION_HANDOFF.md](SESSION_HANDOFF.md), [session notes](docs/SESSION_NOTES.md), [world-sprite and portrait directions](docs/art/ART_DIRECTION.md), and [character status](docs/art/CHARACTER_STATUS.md). Logan and Angie have approved appearance boards; Ryan has an approved hat-on, lowered-waistband map-sprite design. These references still need runtime sprite and dialogue portrait adaptation.

## Status

The first playable foundation implements the approved garden layout, bedroom opening, touch/keyboard movement, character dialogue, two separate ring discoveries, device-local progress, and a ceremony gate that opens only after both rings are collected.

**This is a review build.** Characters use hand-drawn 16 × 24 sprites in the chosen style (older Pokémon meets Stardew) with detailed portraits in conversations; see [docs/art/cast-12](docs/art/cast-12/README.md). Scenery is still original code-drawn placeholder art. Remaining individual character reviews, runtime sprite preparation, dialogue portraits, and environment asset selection are still ahead. The clue endings, opening lines, title, and extra ending-screen wording are provisional. No reference photos are shipped.

## Run locally

Requires Node.js 22.12+ (tested with Node 24).

```sh
npm ci
npm run dev
```

```sh
npm test
npm run build
```

The build produces a static `dist/` directory with the engine bundled locally; it does not require an external CDN, backend, database, or API keys at runtime. The hosting manifest configures the private review deployment. Public guest hosting/sharing is a later release decision.

## Controls

- Hold directional buttons on touch screens, or use arrows / WASD on a keyboard.
- Walk near a person or clue and tap the action button, or press Space / Enter.
- The menu allows resuming or starting over with a second confirmation tap.
- Progress saves in this browser on this device. Reloading retains rings and conversations, but returns Logan to the room entrance rather than saving precise coordinates. Browser privacy settings or cleared storage may prevent persistence; the menu reports save availability.

## Source guide

- `GAME_DESIGN.md`: agreed requirements and review checkpoints.
- `docs/MAP_REVIEW.md`: approved map layout and gate design.
- `src/main.js`: Phaser presentation, movement inputs, conversations, and overlays.
- `src/world.js`: shared geometry and collision/movement functions.
- `src/quest.js`: ring identity, save validation, gate condition, and objective text.
- `src/content.js`: editable dialogue, including approved wording and provisional clue endings.
- `tests/quest.test.js`: quest, save recovery, collision, and reachability checks.
- `tests/sprites.test.js`: every character has a correctly sized sprite sheet and portrait.
- `tools/sprites/`: scripts that build the sprites (`cast12.py`) and portraits (`portraits.py`).
- `public/LICENSES.txt`: runtime dependency license notices.

## Validation and remaining reviews

Automated tests check duplicate/unknown rings, either collection order, malformed/unavailable storage, save/reload gate states, collision tunneling, and map reachability with the gate locked and unlocked. Production build passes.

A Chromium browser playthrough in a 390 × 844 CSS-pixel iframe verified the bedroom exit, all NPC dialogue, both ring pickups, one-ring gate blocking and its message, unlocked approach, and ending. This is a portrait layout check, not physical iOS/Android or touch-device certification. Lucas tried the first playable version on his phone and reported that the layout and movement seem good. Further device checks and individual character-art reviews remain open.

No paid assets, analytics, third-party accounts, combat, or multiplayer have been added. The current route is intentionally very short; do not add filler to reach a duration target.
