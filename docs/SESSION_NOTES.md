# Recovered wedding-game session notes

Updated November 7, 2026 from saved project files, Git history, and available conversation evidence. This is a reconstructed decision log, not a verbatim chat export. Later explicit decisions supersede earlier proposals.

| Stage | Decisions and saved result |
| --- | --- |
| Planning and map | Short single-player phone-friendly wedding game. Logan starts dressed for the wedding in his bedroom, gathers two distinct rings through exploration and NPC clues, then reaches Angie. Approved map: house/Ryan, Sophie at bench, fountain ring, parents, tree ring, gated ceremony venue. Angie must remain physically inaccessible until both rings are collected. |
| Playable review | Phaser/Vite source, touch and keyboard controls, conversations, two ring pickups, browser-local progress, ceremony gate, and ending saved on the playable branch. Lucas reported that the layout and movement seemed good on his phone. Runtime art remains provisional. |
| Logan | Refined to a youthful lean face, rounded nose, smaller head, short dirty-blond hair/beard, and softer hair shading. Approved appearance saved in original commit `7b67e96`. Older walking frames do not match this final appearance. |
| Angie | Refined slimmer arms and face closer to the supplied reference. Approved appearance saved in original commit `8ebc5dd`. Runtime sprites and portrait adaptation remain pending. |
| Ryan outfit | Gray hoodie superseded by a flower short-sleeve button-down and nice trousers, initially with cap clipped at the waistband. Lucas requested a skinny physique and more basic pixel styling. Earlier studies are retained as historical references. |
| Presentation decision | Every character needs a very basic, highly pixelated world sprite and a separate, more detailed dialogue image beside the speaker's name. Preserve existing detailed designs for portraits. No exact logical sprite resolution has been approved. |
| Ryan approval | Cap moved onto his head, hair matched to the cap reference, then waistband lowered slightly. Lucas approved with “Perfect please save him to the repo”. Approved image: `art/ryan-approved-01/ryan-review.png`. Original local commit: `1e282a3`; the current GitHub import has its own commit ID. |
| Interruptions and publishing | Earlier sessions saved work locally but did not advance the remote beyond `8ebc5dd`. A failed stream is not evidence of a successful push. Lucas explicitly requested publication of Ryan's new artwork, the latest handoff/notes, and the world-sprite/dialogue-portrait direction in this session. |

## Earlier dialogue decisions — Ryan superseded November 8

| Speaker | Text |
| --- | --- |
| Ryan | You lost the rings?! |
| Logan to Ryan | Yes and I don't remember where |
| Ryan | GG |
| Logan's Mother | You lost them!! |
| Logan's Father | Thats not good |
| Angie | You made it! |

The added fountain/edge clue and Father's tree clue in `src/content.js` are provisional playtest content. Final title, opening prose, extra ending wording, sound/music, final hosting, and exact deadline time remain open as recorded in [GAME_DESIGN.md](../GAME_DESIGN.md).

## Continuation

Read [SESSION_HANDOFF.md](../SESSION_HANDOFF.md), [art directions](art/ART_DIRECTION.md), and [character status](art/CHARACTER_STATUS.md). Continue from Ryan's approved map-sprite design, then individual character reviews and separate portrait preparation. Do not restart approved appearances or treat historical studies as final runtime assets.

This recovery changes documentation and art references only. Runtime sheets, walking animations matching the latest designs, and dialogue portrait UI remain unfinished. Existing gameplay validation is historical; no new runtime or physical-device verification is claimed by this save.

## November 8 — opening and Ryan revision

Lucas requested that Logan notice the missing rings when trying to leave for the venue and Angie. The bedroom opening now expresses anticipation; the doorway interaction reveals the missing rings, then sends Logan outside to speak to Ryan. The initial objective and hidden bedroom ring counter follow that timing. Garden saves resume after discovery.

Ryan's old shocked reaction and ‘GG’ are replaced by a short sympathetic exchange: Logan says he cannot find the rings; Ryan says ‘Oh no. I'm sorry, man. We'll figure it out.’ and points him to Sophie at the bench, explaining she was the last person Logan was with the night before. Exact implemented wording is in `src/content.js`. Other characters' dialogue and the two-ring gate are unchanged.
