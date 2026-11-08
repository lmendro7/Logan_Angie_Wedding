# Character map sprites

`characters.py` holds every character's 16 × 32 map sprite as hand-placed text grids plus a palette. `build.py` renders them:

```sh
python3 tools/sprites/build.py   # requires Pillow
```

Outputs:

- `public/sprites/<id>.png`: runtime sheets, 48 × 128. Rows are down, right, up, left; columns are stand, step A, step B. Feet touch the bottom row.
- `docs/art/sprites-01/`: an 8× sheet and a review board per character (shown beside Ryan), the full lineup and a walking GIF.

Ryan's sheet is approved. The other characters are reviewed one at a time in Ryan's style; each `status` field in `characters.py` records where it stands. All pixels are original; no LPC, Stardew Valley, Pokémon or personal-photo pixels are used.
