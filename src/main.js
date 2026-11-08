import Phaser from 'phaser';
import './style.css';
import { freshProgress, loadProgress, saveProgress, collectRing, gateOpen, objective } from './quest.js';
import { GARDEN, BEDROOM, HEDGES, GATE, NPCS, RINGS, canStand, movePlayer } from './world.js';
import { conversations } from './content.js';

const $ = id => document.getElementById(id);
let storage;
try { storage = window.localStorage; } catch { storage = null; }
let progress = loadProgress(storage);
let scene;
const held = new Set();
const keyboard = new Set();
let dialogue = [];
let afterDialogue = null;
let previousFocus = null;
let restartArmed = false;
const overlays = ['dialogue', 'menu', 'ending'];
// Detailed models shown beside the speaker's name. Sophie and the parents use
// enlarged map sprites until their detailed models are made.
const PORTRAITS = {
  Logan: 'portraits/logan.png', Angie: 'portraits/angie.png', Ryan: 'portraits/ryan.png',
  Sophie: 'portraits/sophie.png', "Logan's Mother": 'portraits/mother.png', "Logan's Father": 'portraits/father.png',
};
// Map sprites: 16 x 24 frames; rows down, right, up, left; columns stand, step A, step B.
const SHEETS = { logan: 'logan', ryan: 'ryan', sophie: 'sophie', parents: 'mother', dad: 'father', angie: 'angie' };
const DIRS = ['down', 'right', 'up', 'left'];
const ZOOM = 1.5;                 // target on-screen scale in CSS pixels
// Render at the screen's real pixel density, and always zoom by a whole number of
// device pixels, so every sprite pixel is an even, crisp square on phones.
const DPR = Math.min(4, window.devicePixelRatio || 1);
const pixelZoom = target => Math.max(1, Math.round(target * DPR));
const blocked = () => overlays.some(id => !$(id).hidden);
function persist() {
  const ok = saveProgress(storage, progress);
  $('save-status').textContent = ok ? 'Progress saves on this device.' : 'Saving is unavailable in this browser. Keep this tab open to continue.';
  $('objective').textContent = objective(progress);
  $('ring-count').textContent = `${progress.rings.length} / 2 ◇`;
}
function showOverlay(id, focusId) {
  held.clear(); keyboard.clear();
  document.querySelectorAll('.pressed').forEach(b => b.classList.remove('pressed'));
  previousFocus = document.activeElement;
  $(id).hidden = false;
  $(focusId).focus();
}
function hideOverlay(id) {
  $(id).hidden = true;
  (previousFocus?.isConnected ? previousFocus : $('action')).focus();
}
function say(lines, done) {
  dialogue = [...lines]; afterDialogue = done;
  showOverlay('dialogue', 'next');
  renderLine();
}
function renderLine() {
  const [speaker, words] = dialogue[0];
  $('speaker').textContent = speaker;
  const portrait = PORTRAITS[speaker];
  $('portrait').hidden = !portrait;
  if (portrait) { $('portrait').src = portrait; $('portrait').alt = speaker; }
  $('words').textContent = words;
  $('next').textContent = dialogue.length > 1 ? 'Next →' : 'Continue →';
}
function nextLine() {
  dialogue.shift();
  if (dialogue.length) return renderLine();
  hideOverlay('dialogue');
  const done = afterDialogue; afterDialogue = null; done?.();
}
$('next').addEventListener('click', nextLine);
$('menu-toggle').addEventListener('click', () => {
  if (blocked()) return;
  restartArmed = false; $('restart').textContent = 'Start over…';
  showOverlay('menu', 'resume');
});
$('resume').addEventListener('click', () => hideOverlay('menu'));
function restart() {
  if (!restartArmed) { restartArmed = true; $('restart').textContent = 'Erase progress and start over'; return; }
  progress = freshProgress(); persist();
  overlays.forEach(id => $(id).hidden = true);
  held.clear(); keyboard.clear(); restartArmed = false;
  scene.scene.restart();
  $('action').focus();
}
$('restart').addEventListener('click', restart);
$('return').addEventListener('click', () => hideOverlay('ending'));
$('replay').addEventListener('click', () => {
  hideOverlay('ending'); restartArmed = false;
  $('restart').textContent = 'Start over…'; showOverlay('menu', 'restart');
});
$('action').addEventListener('click', () => { if (!blocked()) scene?.interact(); });
for (const button of document.querySelectorAll('[data-direction]')) {
  const activePointers = new Set();
  const direction = button.dataset.direction;
  button.addEventListener('pointerdown', event => {
    if (blocked()) return;
    event.preventDefault(); activePointers.add(event.pointerId);
    button.setPointerCapture(event.pointerId); held.add(direction); button.classList.add('pressed');
  });
  const release = event => {
    activePointers.delete(event.pointerId);
    if (!activePointers.size) { held.delete(direction); button.classList.remove('pressed'); }
  };
  for (const type of ['pointerup', 'pointercancel', 'lostpointercapture']) button.addEventListener(type, release);
}
const keyMap = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', w: 'up', a: 'left', s: 'down', d: 'right' };
document.addEventListener('keydown', event => {
  const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
  if (blocked()) {
    if ((key === ' ' || key === 'Enter') && !$('dialogue').hidden) { event.preventDefault(); if (!event.repeat) nextLine(); }
    if (key === 'Escape' && !$('menu').hidden) hideOverlay('menu');
    if (key === 'Tab') {
      const overlay = overlays.map($).find(el => !el.hidden);
      const buttons = [...overlay.querySelectorAll('button')];
      const first = buttons[0], last = buttons.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    return;
  }
  if (keyMap[key]) { event.preventDefault(); keyboard.add(key); }
  else if ((key === ' ' || key === 'Enter') && !event.repeat && (event.target === document.body || event.target === $('action'))) { event.preventDefault(); scene?.interact(); }
});
document.addEventListener('keyup', e => keyboard.delete(e.key.length === 1 ? e.key.toLowerCase() : e.key));
function clearInput() { held.clear(); keyboard.clear(); document.querySelectorAll('.pressed').forEach(b => b.classList.remove('pressed')); }
window.addEventListener('blur', clearInput);
document.addEventListener('visibilitychange', () => { if (document.hidden) { clearInput(); persist(); } });

// Characters use the hand-drawn 16 x 24 sprite sheets in public/sprites; the scenery is still code-drawn.
class Adventure extends Phaser.Scene {
  constructor() { super('adventure'); }
  preload() {
    for (const sheet of new Set(Object.values(SHEETS))) {
      this.load.spritesheet(sheet, `sprites/${sheet}.png`, { frameWidth: 16, frameHeight: 24 });
    }
  }
  create() {
    scene = this;
    this.room = progress.room;
    this.open = gateOpen(progress);
    const roomSize = this.room === 'garden' ? GARDEN : BEDROOM;
    this.cameras.main.setBounds(0, 0, roomSize.width, roomSize.height);
    this.cameras.main.setBackgroundColor(this.room === 'bedroom' ? '#bda27a' : '#97b779');
    const frameRoom = () => this.cameras.main.setZoom(this.room === 'bedroom'
      ? Math.max(pixelZoom(ZOOM), Math.ceil(Math.max(this.scale.width / BEDROOM.width, this.scale.height / BEDROOM.height)))
      : pixelZoom(ZOOM));
    frameRoom();
    this.scale.on('resize', frameRoom);
    this.events.once('shutdown', () => this.scale.off('resize', frameRoom));
    this.backdrop = this.add.graphics();
    if (this.room === 'bedroom') this.drawBedroom(); else this.drawGarden();
    DIRS.forEach((dir, row) => {
      if (!this.anims.exists(`logan-${dir}`)) this.anims.create({ key: `logan-${dir}`, frameRate: 7, repeat: -1,
        frames: [1, 0, 2, 0].map(col => ({ key: 'logan', frame: row * 3 + col })) });
    });
    this.facing = this.room === 'bedroom' ? 0 : 2;
    this.loganSprite = this.add.sprite(0, 1, 'logan', this.facing * 3).setOrigin(0.5, 1);
    this.character = this.add.container(0, 0, [this.add.ellipse(0, 0, 13, 4, 0x263c30, 0.3), this.loganSprite]);
    this.position = this.room === 'bedroom' ? { x: 144, y: 210 } : { x: 384, y: 820 };
    this.character.setPosition(this.position.x, this.position.y);
    this.character.setDepth(this.position.y);
    this.cameras.main.startFollow(this.character, true, 0.15, 0.15);
    this.cameras.main.setRoundPixels(true);
    $('loading')?.remove();
    $('location').textContent = this.room === 'bedroom' ? 'Logan’s bedroom' : 'The wedding garden';
    persist();
    if (this.room === 'bedroom') say([['Logan', "Today's the wedding!"], ['Logan', 'Wait… where are the rings? I had them last night.']], () => {});
  }
  box(x, y, w, h, color) { this.backdrop.fillStyle(color).fillRect(x, y, w, h); }
  label(x, y, text, size = 12) {
    return this.add.text(x, y, text, { fontFamily: 'Georgia', fontSize: `${size}px`, color: '#fff5d9', backgroundColor: '#2d4939', padding: { x: 4, y: 2 } }).setOrigin(0.5).setDepth(3).setResolution(4);
  }
  drawBedroom() {
    this.box(0, 0, 360, 400, 0xbda27a);
    for (let y = 45; y < 400; y += 22) { this.box(0, y, 360, 1, 0xa88b67); for (let x = (y % 44 ? 0 : 38); x < 360; x += 76) this.box(x, y, 1, 22, 0xae926d); }
    this.box(0, 0, 360, 45, 0xded6bc); this.box(0, 42, 360, 6, 0x826c50);
    this.box(42, 77, 73, 112, 0x735b47); this.box(48, 84, 61, 98, 0xe7dfc6);
    this.box(52, 89, 53, 25, 0xf8f1db); this.box(48, 121, 61, 61, 0x6d8d77);
    this.box(48, 122, 61, 5, 0x9aaf87);
    this.box(228, 52, 95, 46, 0x856a4c); this.box(235, 60, 35, 9, 0xb2956c); this.box(279, 60, 35, 9, 0xb2956c);
    this.box(154, 7, 52, 29, 0x765b43); this.box(159, 10, 42, 23, 0xa6c6c5); this.box(179, 10, 3, 23, 0xf7f0d5);
    this.box(125, 235, 112, 85, 0x917b72); this.box(132, 242, 98, 71, 0xac9690);
    this.box(151, 366, 58, 34, 0x6a543f); this.box(155, 370, 50, 30, 0xd7bc87);
    this.label(180, 350, 'Garden ↓', 9);
  }
  tree(x, y) {
    this.box(x - 8, y, 16, 32, 0x826344);
    this.box(x - 29, y - 43, 58, 46, 0x3f6345);
    this.box(x - 22, y - 57, 44, 57, 0x557e50);
    this.box(x - 12, y - 51, 25, 33, 0x69925b);
  }
  drawGarden() {
    this.box(0, 0, 768, 900, 0x97b779);
    // Deterministic ground flecks, with no imported visual assets.
    for (let y = 0; y < 900; y += 24) for (let x = 0; x < 768; x += 24) {
      this.box(x + (y % 17), y + (x % 13), 3, 2, (x + y) % 48 ? 0x88aa70 : 0xa6c389);
    }
    this.box(362, 190, 44, 455, 0xd9bd87);
    this.box(195, 590, 211, 40, 0xd9bd87); this.box(183, 335, 36, 286, 0xd9bd87);
    this.box(384, 380, 204, 38, 0xd9bd87); this.box(570, 286, 36, 132, 0xd9bd87);
    // Front door exit wraps round the house to join the original main path.
    this.box(360, 780, 183, 53, 0xd9bd87); this.box(505, 610, 38, 223, 0xd9bd87); this.box(384, 610, 159, 35, 0xd9bd87);
    this.box(264, 34, 242, 165, 0xd7d3ad);
    this.box(300, 61, 12, 91, 0xf9efcd); this.box(456, 61, 12, 91, 0xf9efcd); this.box(300, 53, 168, 15, 0x537d4d);
    for (let x = 300; x < 470; x += 19) { this.box(x, 50, 8, 8, 0xe5b2ae); this.box(x + 4, 58, 5, 5, 0xf7dbc2); }
    // Hedges close every side of the ceremony space except its gate.
    for (const h of HEDGES) { this.box(h.x, h.y, h.w, h.h, 0x3e6444); this.box(h.x, h.y, h.w, 4, 0x668750); }
    this.gateGraphic = this.add.graphics().setDepth(4); this.drawGate();
    this.box(290, 650, 190, 130, 0xe8cca2); this.box(282, 636, 206, 26, 0x9c604c); this.box(296, 622, 178, 20, 0xb67c5c);
    for (const x of [311, 426]) { this.box(x, 689, 34, 36, 0x785e45); this.box(x + 4, 693, 26, 27, 0xb6d0ce); this.box(x + 16, 693, 3, 27, 0xeed6b0); }
    this.box(361, 738, 46, 42, 0x786047); this.box(396, 758, 3, 4, 0xe7c56e);
    this.box(161, 295, 78, 47, 0x768f84); this.box(167, 300, 66, 35, 0x91c6c8); this.box(190, 280, 17, 41, 0xc6d0b8);
    this.box(194, 278, 9, 8, 0xe1e3c8);
    this.box(124, 460, 58, 7, 0x866b48); this.box(124, 472, 58, 8, 0x9b7d52);
    this.tree(570, 233);
    for (let y = 90; y < 880; y += 115) { this.tree(39, y); this.tree(728, y); }
    for (const [x, y] of [[120, 280], [290, 390], [610, 570], [270, 550], [625, 720], [140, 795]]) {
      for (let n = 0; n < 4; n++) { this.box(x + n * 9, y + (n % 2) * 8, 5, 6, 0xeac4a4); this.box(x + n * 9 + 2, y + 6 + (n % 2) * 8, 2, 6, 0x648555); }
    }
    this.npcSprites = new Map();
    for (const npc of NPCS) {
      const sprite = this.add.sprite(0, 1, SHEETS[npc.id], 0).setOrigin(0.5, 1);
      this.add.container(npc.x, npc.y, [this.add.ellipse(0, 0, 12, 4, 0x263c30, 0.3), sprite]).setDepth(npc.y);   // y-sorted
      this.npcSprites.set(npc.id, sprite);
      this.label(npc.x, npc.y + (npc.id === 'dad' ? 20 : 9), npc.name, 7);
    }
    this.label(384, 868, "Logan's house", 9);
    this.label(384, 39, 'Wedding ceremony', 9);
    this.ringGraphics = new Map();
    for (const ring of RINGS) {
      const g = this.add.graphics().setPosition(ring.x, ring.y).setDepth(4);
      g.lineStyle(3, 0xf1d48a).strokeCircle(0, 0, 5);
      g.fillStyle(0xfff4c7).fillRect(-1, -8, 3, 3);
      g.setVisible(!progress.rings.includes(ring.id)); this.ringGraphics.set(ring.id, g);
    }
  }
  drawGate() {
    const g = this.gateGraphic; g.clear();
    if (this.open) {
      g.fillStyle(0x8e704e).fillRect(355, 200, 5, 19).fillRect(408, 200, 5, 19);
    } else {
      g.fillStyle(0x8e704e).fillRect(GATE.x - 4, GATE.y - 6, 5, 26).fillRect(GATE.x + GATE.w, GATE.y - 6, 5, 26);
      g.fillStyle(0xc4a36e).fillRect(360, 202, 48, 4).fillRect(360, 212, 48, 4);
      for (let x = 363; x < 408; x += 9) g.fillRect(x, 197, 4, 20);
    }
  }
  nearest() {
    const candidates = this.room === 'bedroom' ? [{ id: 'exit', x: 180, y: 375, label: 'Leave room', radius: 38 }] : [
      ...NPCS.filter(n => n.id !== 'angie' || this.open).map(n => ({ ...n, label: 'Talk', radius: 35 })),
      ...RINGS.filter(r => !progress.rings.includes(r.id)).map(r => ({ ...r, label: 'Search', radius: 29 })),
      ...(!this.open ? [{ id: 'gate', x: 384, y: 221, label: 'Check gate', radius: 40 }] : []),
    ];
    return candidates.map(n => ({ ...n, distance: Math.hypot(n.x - this.position.x, n.y - this.position.y) })).filter(n => n.distance <= n.radius).sort((a, b) => a.distance - b.distance)[0];
  }
  interact() {
    const target = this.nearest(); if (!target) return;
    if (target.id === 'exit') {
      progress.room = 'garden'; persist(); clearInput(); this.scene.restart(); return;
    }
    if (target.id === 'gate') return say([['Logan', 'I need to find both rings first!']]);
    if (RINGS.some(r => r.id === target.id)) {
      const wasOpen = gateOpen(progress);
      progress = collectRing(progress, target.id); persist();
      this.ringGraphics.get(target.id)?.setVisible(false);
      this.open = gateOpen(progress); this.drawGate();
      say([['Logan', this.open && !wasOpen ? 'Both rings! Time to get to Angie.' : 'Found one! One more to go.']]);
      return;
    }
    if (target.id === 'angie') {
      if (!gateOpen(progress)) return;
      this.faceLogan(['angie']);
      return say([['Angie', 'You made it!']], () => { progress.completed = true; persist(); showOverlay('ending', 'return'); });
    }
    this.faceLogan(target.id === 'parents' || target.id === 'dad' ? ['parents', 'dad'] : [target.id]);
    const id = target.id === 'dad' ? 'parents' : target.id;
    say(conversations[id], () => { progress.met = [...new Set([...progress.met, id])]; persist(); });
  }
  faceLogan(ids) {
    for (const id of ids) {
      const npc = NPCS.find(n => n.id === id); const sprite = this.npcSprites?.get(id);
      if (!npc || !sprite) continue;
      const dx = this.position.x - npc.x, dy = this.position.y - npc.y;
      sprite.setFrame((Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 1 : 3) : (dy > 0 ? 0 : 2)) * 3);
    }
  }
  update(time, delta) {
    if (!this.character) return;
    const keys = new Set([...held, ...[...keyboard].map(k => keyMap[k])]);
    if (!blocked()) {
      let dx = Number(keys.has('right')) - Number(keys.has('left'));
      let dy = Number(keys.has('down')) - Number(keys.has('up'));
      const length = Math.hypot(dx, dy) || 1;
      const step = 140 * Math.min(delta, 40) / 1000;
      const before = this.position;
      this.position = movePlayer(this.position, dx / length * step, dy / length * step, this.room, this.open);
      const moving = before.x !== this.position.x || before.y !== this.position.y;
      this.character.setPosition(Math.round(this.position.x), Math.round(this.position.y));
      this.character.setDepth(this.position.y);   // in front of whoever stands further up the screen
      if (dx || dy) this.facing = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 1 : 3) : (dy > 0 ? 0 : 2);
      if (moving) this.loganSprite.play(`logan-${DIRS[this.facing]}`, true);
      else { this.loganSprite.stop(); this.loganSprite.setFrame(this.facing * 3); }
    }
    const near = this.nearest();
    $('action').textContent = near?.label ?? 'Explore';
    $('action').disabled = blocked() || !near;
  }
}

const host = $('game');
const deviceSize = () => [Math.max(1, Math.round(host.clientWidth * DPR)), Math.max(1, Math.round(host.clientHeight * DPR))];
const [startW, startH] = deviceSize();
const game = new Phaser.Game({ type: Phaser.AUTO, parent: 'game', backgroundColor: '#97b779', pixelArt: true, roundPixels: true,
  scale: { mode: Phaser.Scale.NONE, width: startW, height: startH, zoom: 1 / DPR }, scene: Adventure, banner: false, audio: { noAudio: true } });
// Keep the canvas matched to its box (rotation, browser bars) at full device resolution.
new ResizeObserver(() => {
  const [w, h] = deviceSize();
  if (w !== game.scale.width || h !== game.scale.height) { game.scale.resize(w, h); game.scale.setZoom(1 / DPR); }
}).observe(host);
