# Wedding game — next-session handoff

Updated November 7, 2026 after Ryan's map-sprite approval. Read AGENTS.md, GAME_DESIGN.md, docs/SESSION_NOTES.md, and docs/art/ART_DIRECTION.md before continuing.

Lucas approved publishing Ryan's artwork and design notes and gave standing approval for all Git commits and publishing for this project indefinitely. This authorization includes saving the earlier pending art and project handoff work. See AGENTS.md for the project scope.

## Latest user decision — preserve this distinction

Lucas wants Stardew-like character presentation: **very basic, highly pixelated sprites on the map; a separate, more detailed character image beside the speaker's name during dialogue.** Keep the existing detailed designs. They should guide dialogue portraits, not be discarded or repeatedly simplified into large review-board characters. We need a simple in-world version of every character.

The two supplied Stardew screenshots show tiny, readable world characters. They are style/scale references only. Create original artwork. Do not copy the screenshots' map, people, or other game assets into this project. The layout already approved for this game remains binding.

## Repository and exact saved state

- Repository: https://github.com/lmendro7/Logan_Angie_Wedding
- Working art branch: `art/logan-character-review`.
- Draft art PR #3 targets `feat/playable-foundation`: https://github.com/lmendro7/Logan_Angie_Wedding/pull/3
- Playable foundation is in draft PR #2. Main was only the initial README when last inspected; inspect live refs before continuing. Do not assume the game/art work has been merged.
- Approved Logan appearance: `docs/art/logan-approved-01/logan-review.png`, saved in commit `7b67e96`.
- Approved Angie appearance: `docs/art/angie-approved-01/angie-review.png`, saved in commit `8ebc5dd`.
- Angie's saved PNG was verified byte-for-byte against the approved refined image (SHA-256 `f5f591b86af186e633d8b3d3d4e458dd9a8c023b06424c05c41769a426e4bda6`). It includes slimmer arms and a photo-guided face shape.
- Approved Ryan map-sprite design: `docs/art/ryan-approved-01/ryan-review.png`, created in original local commit `1e282a3` and recovered in this publication (with a new GitHub commit ID). The cap is worn on his head, with short swept blond hair beneath it; the waistband is slightly lowered. The exact approved PNG is saved without recompression.
- Earlier Ryan review boards, the superseded hoodie, and Logan draft 02 remain archived. No runtime game code or deployment changes accompany these art saves. Runtime sprite sheets and portrait UI remain unimplemented.
- Lucas explicitly requested saving and committing all pending work after the earlier public push was blocked. The pending two-asset handoff and Ryan boards are included, along with the superseded Ryan hoodie preview and the previously untracked Logan draft 02. Those historical drafts do not replace the approved/current references.

## Character decisions

| Character | Preserve | Next work |
| --- | --- | --- |
| Logan | Approved youthful lean face, rounded nose, smaller head, soft short dirty-blond hair/beard, black suit and white shirt | Simple world sprite; dialogue portrait derived from detailed reference |
| Angie | Approved slim arms, elongated oval face, softly wavy brown hair, glasses, cream/white sleeveless wedding dress | Simple world sprite; dialogue portrait derived from detailed reference |
| Ryan | Approved simple map-sprite design: skinny young adult, short swept sandy blond hair under a worn brown/off-white cap, cream flower short-sleeve button-down, navy trousers with a slightly lowered waistband, sunglasses at neckline | Prepare aligned runtime sprites and a separate detailed portrait matching the approved appearance |
| Sophie | Short black hair, pale skin; shy, funny, sarcastic, introverted | Individual character/portrait and simple sprite review pending |
| Logan's Mother | Display name exactly as written; white, dirty-blond hair | Model details deferred; simple sprite and portrait pending |
| Logan's Father | Display name exactly as written; white, dirty-blond hair | Model details deferred; simple sprite and portrait pending |

Ryan's gray hoodie was replaced at Lucas's request. See `docs/art/ryan-review-01/README.md` for both saved review boards. The detailed outfit board predates the slimming request; preserve the skinny physique from the later direction when adapting it. The older slender pixel board was an exploration before Lucas clarified world-sprite versus portrait separation. Ryan approved 01 is the current approved simple map-sprite design; none of these review boards is an animation-ready sheet.

Existing four-view boards are appearance references, not finished portrait crops, rigs, or animation-ready sheets. The old Logan draft 01 animation shows an outdated appearance and must not be passed off as matching the approved design.

## Recovery publication

This update publishes the recovered approved Ryan image, retained studies, current handoff, reconstructed notes in `docs/SESSION_NOTES.md`, and explicit directions in `docs/art/ART_DIRECTION.md` on `art/logan-character-review`. The branch is the complete continuation point for this scope. Main still contains the initial README; PRs #1–#3 remain unmerged. Original unpublished local commit hashes are provenance, not a claim that those hashes exist on GitHub.

## Current state — November 8, 2026 (latest)

- **Style chosen:** map sprites in full-colour style 12 (older Pokémon meets Stardew), all characters 16 × 24, detailed models as dialogue portraits. Implemented in the game on branch `claude/awesome-darwin-eto2cf`: `public/sprites/*.png` (built by `tools/sprites/cast12.py`), `public/portraits/*.png` (`tools/sprites/portraits.py`), walking animation, characters facing Logan when he talks, y-sorting, camera zoom 1.5×. See `docs/art/cast-12/README.md`.
- **Needs review:** all six sprites in this style; Sophie and the parents are first drafts with stand-in portraits.
- **Next:** take Lucas's feedback per character; make detailed portrait models for Sophie and the parents; scenery art is still placeholder.
- Older explorations (16×32 sprites, style boards, LPC rebuilds, board extractions) are history in `docs/art/`.

## Earlier update — November 8, 2026

Ryan's runtime map sprite sheet is drafted at `docs/art/ryan-sprite-01/` (16 × 32 px frames; rows down/right/up/left; columns stand/step A/step B; rebuilt by `build_sprite.py`). It was checked at game scale in a temporary local build and is **awaiting Lucas's review**. It is not integrated into the game yet. Once it is approved, integrate it, then repeat the format for Logan, Angie, Sophie and the parents.

## Immediate next session

1. Read the repo's current requirements and inspect branch/PR state; preserve any newer work.
2. Continue from the approved Ryan simple map-sprite design. Exact logical resolution remains a proposal; the board is not a native-pixel export. Prepare and verify a runtime sheet at game scale before integration.
3. Review each remaining character individually before integration. Maintain the portrait/sprite distinction and consistent scale/palette. Sophie's individual design is pending; parent details remain deferred.
4. Prepare separate portrait assets and simple four-direction sprites as needed; later integrate portrait beside speaker name in the dialogue UI and check phone readability. Do not deploy or change the map as part of the art review.

Ryan's cap-on and lowered-waistband revision was approved with "Perfect please save him to the repo". The following publishing approval is recorded in AGENTS.md. Keep artwork approval separate from whether animation/runtime integration is complete.

## Gameplay and review constraints

- Short single-player wedding gift, Phaser browser game, phone-friendly controls, device-local progress, no backend/accounts.
- Logan starts dressed for the wedding in his bedroom and must find two separate rings.
- Approved map: house/Ryan, Sophie at bench, fountain ring, parents, tree ring, gated ceremony venue with Angie.
- Angie cannot be physically approached until both distinct rings are gathered. Gate/enclosure and interaction checks enforce this. Keep approved layout and movement.
- Ryan exchange: Ryan: "You lost the rings?!" / Logan: "Yes and I don't remember where" / Ryan: "GG".
- Logan's Mother: "You lost them!!". Logan's Father: "Thats not good".
- Angie ending: "You made it!".
- Review art individually. Parent model details remain deferred. Keep the deadline context and open release questions in GAME_DESIGN.md rather than inventing them.
- Personal photos stay out of the public repository. Retain existing art licenses/credits for derived assets.
- Previous playable validation was reported before this session; it is not fresh validation of unimplemented art/portrait changes. No runtime tests were required for this documentation/art-reference handoff.

## Optional reference recovery if scratch paths are unavailable

Persistent reference images are in Lucas's ChatGPT files: `IMG_7047.jpeg`, `IMG_7048.jpeg`, and `IMG_7039.jpeg` are Ryan photos; `IMG_7049.jpeg` and `IMG_7050.jpeg` are the Stardew screenshots supplied with the latest direction. Resolve exact files there if needed; do not rely on transient local paths or upload personal photos to this public repo.
