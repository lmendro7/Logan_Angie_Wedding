# Logan & Angie's Wedding Game — Design and Requirements

Last updated: November 8, 2026  
Project owner and design reviewer: Lucas  
Repository: https://github.com/lmendro7/Logan_Angie_Wedding

This document records the agreed design, reference descriptions, implementation plan, and unresolved decisions. Update it as reviews produce new decisions. Proposed details must not silently become approved requirements.

## 1. Purpose and experience

Build a short, personalized wedding gift: a single-player, top-down pixel-art adventure starring Logan. He wakes up in his bedroom already wearing his wedding clothes, realizes he lost the wedding rings last night, and must recover them before reaching Angie at the wedding venue.

Friends and family appear as NPCs. Humor, familiar people, simple clues, and exploration carry the experience.

- Play whenever desired; no scheduled group session.
- Target roughly 5–10 minutes, but allow a shorter game rather than extending development to meet a duration target.
- Keep the world small and navigation simple.
- Prioritize a complete, easy-to-play gift over additional features.
- Pokémon inspires the opening and exploration.
- Stardew Valley inspires the cozy pixel-art aesthetic, not a farming simulation.

## 2. Delivery constraints

- Requested deadline: tomorrow relative to the November 7 planning session (November 8, 2026).
- Exact delivery time and time zone remain unconfirmed.
- Lucas currently has access primarily to his phone.
- Reviews must be practical on a phone: viewable map images, character previews, and a browser playtest link.
- Target mobile browsers on iPhone/iPad and Android; broad device compatibility is a goal to verify, not a guarantee.
- Minimize guest friction and infrastructure costs.
- No paid asset budget has been approved. Use free assets unless Lucas authorizes a purchase.

## 3. Review checkpoints — required

Lucas approved map draft 01 on November 7, 2026, with a closed garden gate required before Angie can be approached. The gate addition is authorized. Final art and character sprites are still subject to their own reviews.

1. **Map layout review — completed:** The reviewed house, paths, NPC positions, fountain, ring locations, tree, and venue arrangement is approved, with the authorized gate addition shown in docs/map-draft-01.svg. Material changes to this arrangement need another review.
2. **Character reviews:** Review characters individually. Names, dialogue, and reference descriptions below are recorded, but final sprites still need visual review. Parents' models are explicitly deferred.
3. **Playable review — in progress:** Lucas tried the first playable version on his phone and reported that the layout and movement seem good. Parent dialogue has been revised per his feedback. Art remains provisional and needs individual character reviews. Further phone checks remain open.
4. **Release review:** Explain important changes and testing results before deployment. Hosting and release details still need to be settled.

Do not build the whole game and only then ask Lucas to review the map. Revisit major design changes with him. Routine implementation choices can proceed within the approved scope.

## 4. Approved core gameplay

- Logan is the player character.
- Movement, brief conversations, environmental clues, and ring collection form the gameplay loop.
- Two rings are found separately.
- Sophie provides a clue toward the first ring.
- Logan's parents provide a clue toward the second ring.
- Both rings must be recovered before Logan can physically approach Angie or trigger the ending.
- A closed garden gate is the only entrance to the ceremony enclosure. Hedges or fences block walking around it.
- The gate opens automatically when both distinct rings are collected. With zero or one ring it stays closed. Early interaction displays: "I need to find both rings first!"
- Gate state is derived from ring progress and restored correctly after a reload. Both ring locations and all clue NPCs remain reachable outside the locked enclosure.
- Angie's interaction also checks for both rings as a second safeguard.
- Lucas has delegated creation of the clue sequence, subject to the agreed map review.
- Ryan's approved exchange must remain intact; any additional clue can be discovered nearby rather than added to that exchange.
- No combat, farming, multiplayer, accounts, or complex inventory is planned for the initial release.

## 5. Map layout — approved with garden gate

One compact garden-like outdoor area connects Logan's house with the wedding venue. A small bedroom/house area supports the opening.

| Place | Agreed purpose |
| --- | --- |
| Logan's house / bedroom | Opening; Ryan nearby |
| Garden bench | Sophie gives the first ring clue |
| Fountain | First ring discovery |
| Parents near the venue | Second ring clue |
| Nearby tree | Second ring discovery beneath the tree |
| Wedding venue and flower arch | Angie waits inside a hedge/fence enclosure; one gate opens automatically after both rings are collected |

Short paths connect these places in the approved arrangement shown in docs/map-draft-01.svg. Exact dimensions, building interiors, collision boundaries, art, clue wording, and precise pickup positions remain to be implemented or reviewed as appropriate. The diagram is not final game art.

## 6. Characters

### Logan — playable groom

- Appearance reference: the man in the supplied couple photos.
- Short dirty-blonde hair, matching short beard, light skin. Hair has tapered sides/back, a compact brushed-back top, and soft matte shading.
- Lean, youthful face guided by the reference photos, a gently rounded nose, and a smaller head relative to the body.
- Approved outfit: black suit and white shirt.
- Starts in wedding clothes, including in the bedroom.
- Appearance approved November 7, 2026: see `docs/art/logan-approved-01/README.md`. Animation-ready sprites must still be updated to match this reference before integration.

### Angie — bride

- Appearance reference: the woman in the supplied couple photos.
- Approved appearance: shoulder-length softly wavy brown hair, glasses, light skin, and a white sleeveless wedding dress with broad straps, a square neckline, fitted waist, and flared skirt.
- Slim arms and an elongated oval face with a softly tapering jaw and gently rounded chin, guided by the supplied couple photos.
- **November 8, 2026:** Lucas asked to remove the glasses and give her regular eyes, then to add a short veil. Both the map sprite and the dialogue portrait now show her without glasses and with the veil.
- Waits at the venue beneath a flower arch.
- Appearance approved November 7, 2026: see `docs/art/angie-approved-01/README.md`. Animation-ready sprites still need preparation and verification before integration.
- Approved ending dialogue:

> **Angie:** You made it!

### Ryan — Logan's friend and roommate

- Funny and outgoing.
- Appearance reference: the foreground person in the supplied Ryan photo.
- Approved map-sprite design, November 7, 2026: skinny build; brown/off-white cap worn forward on his head; short sandy blond hair swept beneath the brim; cream short-sleeve button-down with a coral flower; sunglasses at the neckline; navy trousers with a slightly lowered waistband; brown belt and shoes. This replaces the earlier hoodie and waistband-clipped cap directions.
- Approved reference: `docs/art/ryan-approved-01/ryan-review.png`. Exact-resolution runtime sprites, animation, and a separate detailed dialogue portrait still need preparation and review.
- Approved dialogue, preserving Lucas's wording:

> **Ryan:** You lost the rings?!  
> **Logan:** Yes and I don't remember where  
> **Ryan:** GG

### Sophie — friend of Logan and Angie

- Shy, funny, sarcastic, very introverted.
- Short, black hair, pale skin.
- **November 8, 2026:** Lucas asked for a skinnier model and a smaller nose, and supplied reference photos (kept out of the repository). They show long dark hair with caramel-blonde streaks, dark-framed glasses and an olive-green top; options in docs/art/cast-12/sophie-photo-options.png await his pick.
- Gives the clue toward the first ring.
- Dialogue direction supplied by Lucas; location wording remains pending:

> **Logan:** Hey I lost the rings last night and I can't find them can you help me??  
> **Sophie:** Yeah your cooked bud. I think I saw you at [clue location].

The phrase above preserves the user's draft. Grammar/punctuation and the completed clue can be reviewed together; the intended tone is casual and sarcastic.

### Logan's Mother

- Display name must be **Logan's Mother**; actual name is unnecessary.
- White, dirty blonde hair; further model details deferred.
- Approved reaction:

> **Logan's Mother:** You lost them!!

### Logan's Father

- Display name must be **Logan's Father**; actual name is unnecessary.
- White, dirty blonde hair; further model details deferred.
- Approved reaction:

> **Logan's Father:** Thats not good

The parents then provide the clue toward the second ring. Exact clue and any connecting Logan dialogue remain to be written and reviewed.

## 7. Art and asset approach

- **Latest direction, November 7, 2026:** Each character needs two separate visual assets: a very basic, highly pixelated in-world sprite and a more detailed dialogue portrait displayed beside their name when they speak. The supplied Stardew Valley screenshots guide the small in-world scale and simplicity.
- Keep the existing detailed character designs as appearance/portrait references. Adapt them into dialogue portraits rather than using enlarged review-board figures as map sprites. Retain Ryan's skinny build and latest flower-shirt/cap outfit in both representations.
- Create the simple in-world version for Logan, Angie, Ryan, Sophie, Logan's Mother, and Logan's Father. Review a sample at actual game scale before making the full set. Exact sprite dimensions/frame counts and portrait crops remain implementation proposals to review.
- This direction and Ryan's map-sprite design are approved; the other simple character sprites and dialogue portrait presentation still need visual review. No new sprite or dialogue-portrait UI has been integrated yet.
- Cozy, top-down pixel art, using a consistent scale and palette.
- Use ready-made tiles, characters, buildings, and interface assets to save time.
- Personalize character appearance where practical.
- Use assets licensed for this use; do not assume Stardew Valley or Pokémon sprites can be copied.
- Record asset sources, licenses, and required attribution.
- **Chosen November 8, 2026:** map sprites in full-colour style 12, "a mix of older Pokémon games and Stardew": every character 16 × 24 pixels, the same size, with four-direction walking. The detailed models appear as portraits beside the speaker's name in conversations. All six characters are in the game in this style ([docs/art/cast-12](docs/art/cast-12/README.md)); Sophie's and the parents' sprites are first drafts awaiting review, and their portraits are stand-ins until detailed models exist.
- Scenery is still code-drawn placeholder art; environment assets remain unselected.
- Reference photos guide appearance; uploading them to the public repository or including them in the shipped game has not been requested.

## 8. Agreed technical direction

| Component | Direction |
| --- | --- |
| Game framework | Phaser, lightweight 2D browser game |
| Access | Browser link, no installation or guest accounts |
| Mobile input | On-screen directional controls and one interact button |
| Progress | Device-local save so switching apps does not unnecessarily restart progress |
| Hosting | Static website; provider not yet selected |
| Backend | No server or database required for the agreed game |
| Source control | Feature branches and pull requests in this repository |
| Code organization | Straightforward, maintainable code with dialogue and quest content easy to edit |

A QR code is a potential convenience after a stable URL exists, not a finalized requirement. Browser storage behavior and supported screen orientations need testing.

## 9. Milestones and order

### Milestone 0 — reviewable design

- Keep this document current.
- Choose reusable art candidates.
- Map draft reviewed and approved; incorporate the authorized ceremony gate.
- Review character sprite previews individually.
- Confirm exact delivery time.

### Milestone 1 — playable foundation

After map layout approval, implement the small world, collision, movement, touch controls, and dialogue. Use approved characters or clearly marked provisional sprites while their visual reviews continue.

### Milestone 2 — complete adventure

Implement opening, clue sequence, two separate ring pickups, progress indicators/save, and the ending. Keep approved dialogue intact. Provide a browser preview for Lucas's phone review.

### Milestone 3 — polish and release

Incorporate review feedback, finish character details, check mobile usability, record asset attribution, and prepare hosting plus a shareable URL. Explain validation results and remaining limitations before deployment.

## 10. Acceptance checks

- A guest can open the game on a supported mobile browser and start without an account.
- Text and touch controls are readable and usable on a small phone screen.
- Movement and interaction work without accidental page scrolling or stuck input.
- Logan starts in his bedroom in black-and-white wedding clothes.
- NPCs use the correct display names and approved dialogue.
- Both ring locations can be reached; clues accurately describe the final approved map.
- Each ring can only be collected once.
- With zero rings, either single ring, or a repeated pickup of one ring, the gate stays closed and Angie cannot be approached or trigger the ending.
- With both distinct rings, the gate opens automatically and the ending becomes reachable.
- The locked enclosure cannot be bypassed on either side, and neither ring is placed inside it.
- Reloading with one ring keeps the gate closed; reloading with both keeps it open.
- After collecting both rings, the player can reach Angie and see "You made it!"
- Device-local progress survives a normal reload where browser storage is available.
- The quest can be completed from a fresh start without getting stuck.
- Lucas has reviewed the map, individual character visuals, and playable preview.
- Production build works and all shipped assets have documented permission/attribution.
- Test iOS Safari and Android Chrome where available; report emulated versus physical-device testing honestly.

## 11. Open decisions

- Exact deadline time and time zone.
- Final sprites for every character, including deferred parent models.
- Exact clue wording and any extra dialogue.
- Asset pack, attribution, and any optional spending.
- Hosting provider and deployment configuration.
- Portrait/landscape behavior.
- Optional sound/music, title screen wording, and any extra ending message.

These open items should not expand the small agreed scope. Sound/music and extra ending content are optional unless explicitly chosen.
