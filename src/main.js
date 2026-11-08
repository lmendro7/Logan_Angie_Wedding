import Phaser from 'phaser';
import './style.css';
import { freshProgress, loadProgress, saveProgress, collectRing, gateOpen, objective } from './quest.js';
import { GARDEN, BEDROOM, NPCS, RINGS, canStand, movePlayer } from './world.js';
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
// Map sprites (Cozy Garden style): 16 x 32 frames; rows down, right, up, left; columns stand, step A, step B.
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

// Characters (public/sprites) and scenery (public/env) are hand-made Cozy Garden pixel art.
class Adventure extends Phaser.Scene {
  constructor() { super('adventure'); }
  preload() {
    for (const name of ['garden', 'bedroom', 'house', 'tree', 'blossom', 'bench', 'arch', 'gate-closed', 'gate-open']) {
      this.load.image(name, `env/${name}.png`);
    }
    this.load.spritesheet('fountain', 'env/fountain.png', { frameWidth: 90, frameHeight: 84 });
    this.load.spritesheet('butterfly', 'env/butterfly.png', { frameWidth: 8, frameHeight: 7 });
    this.load.spritesheet('ring', 'env/ring.png', { frameWidth: 13, frameHeight: 13 });
    for (const sheet of new Set(Object.values(SHEETS))) {
      this.load.spritesheet(sheet, `sprites/${sheet}.png`, { frameWidth: 16, frameHeight: 32 });
    }
  }
  create() {
    scene = this;
    this.room = progress.room;
    this.open = gateOpen(progress);
    const roomSize = this.room === 'garden' ? GARDEN : BEDROOM;
    this.cameras.main.setBounds(0, 0, roomSize.width, roomSize.height);
    this.cameras.main.setBackgroundColor(this.room === 'bedroom' ? '#cf9c62' : '#86b863');
    const frameRoom = () => this.cameras.main.setZoom(this.room === 'bedroom'
      ? Math.max(pixelZoom(ZOOM), Math.ceil(Math.max(this.scale.width / BEDROOM.width, this.scale.height / BEDROOM.height)))
      : pixelZoom(ZOOM));
    frameRoom();
    this.scale.on('resize', frameRoom);
    this.events.once('shutdown', () => this.scale.off('resize', frameRoom));
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
  label(x, y, text, size = 12) {
    return this.add.text(x, y, text, { fontFamily: 'Georgia', fontSize: `${size}px`, color: '#fff5d9', backgroundColor: '#2d4939', padding: { x: 4, y: 2 } }).setOrigin(0.5).setDepth(5000).setResolution(4);
  }
  drawBedroom() {
    this.add.image(0, 0, 'bedroom').setOrigin(0, 0);
    this.label(180, 350, 'Garden ↓', 9);
  }
  // Painted Cozy Garden scenery (tools/env/build_env.py). Tall objects are separate
  // images, depth-sorted by their base so characters walk in front of and behind them.
  // Every position matches the approved layout and the collision boxes in world.js.
  drawGarden() {
    this.add.image(0, 0, 'garden').setOrigin(0, 0);
    const place = (key, left, top, base) => this.add.image(left, top, key).setOrigin(0, 0).setDepth(base);
    place('house', 278, 610, 780);
    place('blossom', 534, 176, 265);                       // the tree with the second ring
    place('bench', 122, 451, 480);
    place('arch', 294, 47, 152);
    for (let y = 90; y < 880; y += 115) for (const x of [39, 728]) place('tree', x - 36, y + 32 - 89, y + 32);
    if (!this.anims.exists('fountain-flow')) {
      this.anims.create({ key: 'fountain-flow', frames: this.anims.generateFrameNumbers('fountain', { start: 0, end: 1 }), frameRate: 3, repeat: -1 });
      this.anims.create({ key: 'ring-twinkle', frames: this.anims.generateFrameNumbers('ring', { start: 0, end: 1 }), frameRate: 2, repeat: -1 });
      for (let c = 0; c < 3; c++) {
        this.anims.create({ key: `butterfly-${c}`, frames: [{ key: 'butterfly', frame: c * 2 }, { key: 'butterfly', frame: c * 2 + 1 }], frameRate: 6, repeat: -1 });
      }
    }
    this.add.sprite(155, 259, 'fountain').setOrigin(0, 0).setDepth(342).play('fountain-flow');
    this.gateImage = this.add.image(352, 187, 'gate-closed').setOrigin(0, 0).setDepth(216);
    this.drawGate();
    // Butterflies drifting over the garden.
    [[120, 230], [640, 420], [300, 520], [560, 760]].forEach(([x, y], i) => {
      const b = this.add.sprite(x, y, 'butterfly').setDepth(4000).play(`butterfly-${i % 3}`);
      this.tweens.add({ targets: b, x: x + 40 + i * 6, y: y - 24, duration: 2600 + i * 400, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
      this.tweens.add({ targets: b, y: `+=${6 + i}`, duration: 700 + i * 90, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
    });
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
      const g = this.add.sprite(ring.x, ring.y, 'ring').setDepth(ring.y).play('ring-twinkle');
      g.setVisible(!progress.rings.includes(ring.id)); this.ringGraphics.set(ring.id, g);
    }
  }
  drawGate() {
    this.gateImage?.setTexture(this.open ? 'gate-open' : 'gate-closed');
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
