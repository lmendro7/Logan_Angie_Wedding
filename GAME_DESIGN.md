# Logan & Angie's Wedding Game — Design and Requirements

Last updated: November 7, 2026  
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

Approval of the garden concept is NOT approval of a finished map.

1. **Map layout review:** Present a visual draft showing the house, paths, NPC positions, fountain, ring locations, tree, and venue. Lucas reviews and approves or requests changes before the playable world and quest placement are built around that layout. A small mockup or blockout may be created for this review.
2. **Character reviews:** Review characters individually. Names, dialogue, and reference descriptions below are recorded, but final sprites still need visual review. Parents' models are explicitly deferred.
3. **Playable review:** Provide a first complete browser preview for Lucas to test on his phone before final polish.
4. **Release review:** Explain important changes and testing results before deployment. Hosting and release details still need to be settled.

Do not build the whole game and only then ask Lucas to review the map. Revisit major design changes with him. Routine implementation choices can proceed within the approved scope.

## 4. Approved core gameplay

- Logan is the player character.
- Movement, brief conversations, environmental clues, and ring collection form the gameplay loop.
- Two rings are found separately.
- Sophie provides a clue toward the first ring.
- Logan's parents provide a clue toward the second ring.
- Both rings must be recovered before the successful ending with Angie.
- Lucas has delegated creation of the clue sequence, subject to the agreed map review.
- Ryan's approved exchange must remain intact; any additional clue can be discovered nearby rather than added to that exchange.
- No combat, farming, multiplayer, accounts, or complex inventory is planned for the initial release.

## 5. Map concept — approved; layout pending

One compact garden-like outdoor area connects Logan's house with the wedding venue. A small bedroom/house area supports the opening.

| Place | Agreed purpose |
| --- | --- |
| Logan's house / bedroom | Opening; Ryan nearby |
| Garden bench | Sophie gives the first ring clue |
| Fountain | First ring discovery |
| Parents near the venue | Second ring clue |
| Nearby tree | Second ring discovery beneath the tree |
| Wedding venue and flower arch | Angie waits; ending after collecting both rings |

Short paths connect these places. Exact dimensions, arrangement, building interiors, collision boundaries, art, clue wording, and precise pickup positions require the map draft and review.

## 6. Characters

### Logan — playable groom

- Appearance reference: the man in the supplied couple photos.
- Short brown hair, trimmed beard, light skin.
- Approved outfit: black suit and white shirt.
- Starts in wedding clothes, including in the bedroom.
- Final sprite needs review.

### Angie — bride

- Appearance reference: the woman in the supplied couple photos.
- Proposed visual interpretation: brown hair, glasses, light skin, white wedding dress.
- Waits at the venue beneath a flower arch.
- Final sprite and dress details need review.
- Approved ending dialogue:

> **Angie:** You made it!

### Ryan — Logan's friend and roommate

- Funny and outgoing.
- Appearance reference: the foreground person in the supplied Ryan photo.
- Reference interpretation: sandy blond hair, light facial stubble, oversized gray hoodie, sunglasses hanging from the neckline.
- Final sprite needs review.
- Approved dialogue, preserving Lucas's wording:

> **Ryan:** You lost the rings?!  
> **Logan:** Yes and I don't remember where  
> **Ryan:** GG

### Sophie — friend of Logan and Angie

- Shy, funny, sarcastic, very introverted.
- Short, black hair, pale skin.
- Gives the clue toward the first ring.
- Dialogue direction supplied by Lucas; location wording remains pending:

> **Logan:** Hey I lost the rings last night and I can't find them can you help me??  
> **Sophie:** Yeah your cooked bud. I think I saw you at [clue location].

The phrase above preserves the user's draft. Grammar/punctuation and the completed clue can be reviewed together; the intended tone is casual and sarcastic.

### Logan's Mom

- Display name must be **Logan's Mom**; actual name is unnecessary.
- White, dirty blonde hair; further model details deferred.
- Approved reaction:

> **Logan's Mom:** Oh No!

### Logan's Dad

- Display name must be **Logan's Dad**; actual name is unnecessary.
- White, dirty blonde hair; further model details deferred.
- Approved reaction:

> **Logan's Dad:** That's not good

The parents then provide the clue toward the second ring. Exact clue and any connecting Logan dialogue remain to be written and reviewed.

## 7. Art and asset approach

- Cozy, top-down pixel art, using a consistent scale and palette.
- Use ready-made tiles, characters, buildings, and interface assets to save time.
- Personalize character appearance where practical.
- Use assets licensed for this use; do not assume Stardew Valley or Pokémon sprites can be copied.
- Record asset sources, licenses, and required attribution.
- Asset pack and exact sprite resolution remain unselected.
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
- Present the visual map draft for Lucas's approval.
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
- Angie cannot trigger the successful ending until both rings are collected.
- After collecting both rings, the player can reach Angie and see "You made it!"
- Device-local progress survives a normal reload where browser storage is available.
- The quest can be completed from a fresh start without getting stuck.
- Lucas has reviewed the map, individual character visuals, and playable preview.
- Production build works and all shipped assets have documented permission/attribution.
- Test iOS Safari and Android Chrome where available; report emulated versus physical-device testing honestly.

## 11. Open decisions

- Exact deadline time and time zone.
- Visual map layout approval.
- Final sprites for every character, including deferred parent models.
- Exact clue wording and any extra dialogue.
- Asset pack, attribution, and any optional spending.
- Hosting provider and deployment configuration.
- Portrait/landscape behavior.
- Optional sound/music, title screen wording, and any extra ending message.

These open items should not expand the small agreed scope. Sound/music and extra ending content are optional unless explicitly chosen.
