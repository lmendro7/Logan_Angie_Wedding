export const GARDEN = { width: 768, height: 900 };
export const BEDROOM = { width: 360, height: 400 };
export const GATE = { x: 360, y: 200, w: 48, h: 16 };
export const HEDGES = [
  { x: 250, y: 20, w: 270, h: 12 },
  { x: 250, y: 20, w: 12, h: 196 },
  { x: 508, y: 20, w: 12, h: 196 },
  { x: 250, y: 200, w: 110, h: 16 },
  { x: 408, y: 200, w: 112, h: 16 },
];
export const OBSTACLES = [
  ...HEDGES,
  { x: 290, y: 650, w: 190, h: 130 }, // House.
  { x: 161, y: 295, w: 78, h: 47 }, // Fountain basin.
  { x: 124, y: 460, w: 58, h: 20 }, // Bench.
  { x: 560, y: 240, w: 20, h: 25 }, // Ring tree trunk.
];
export const NPCS = [
  { id: 'ryan', x: 510, y: 610, name: 'Ryan', color: 0x9a9f9b },
  { id: 'sophie', x: 230, y: 480, name: 'Sophie', color: 0x81719c },
  { id: 'parents', x: 445, y: 365, name: "Logan's Mom", color: 0xbd8796 },
  { id: 'dad', x: 485, y: 365, name: "Logan's Dad", color: 0x7c96aa },
  { id: 'angie', x: 384, y: 115, name: 'Angie', color: 0xfff7dd },
];
export const RINGS = [
  { id: 'fountain', x: 245, y: 350, label: 'Search fountain' },
  { id: 'tree', x: 590, y: 290, label: 'Search tree' },
];
export function overlaps(player, box) {
  return player.x + 8 > box.x && player.x - 8 < box.x + box.w && player.y + 5 > box.y && player.y - 7 < box.y + box.h;
}
export function canStand(player, room, open) {
  const bounds = room === 'bedroom' ? BEDROOM : GARDEN;
  if (player.x < 20 || player.y < 30 || player.x > bounds.width - 20 || player.y > bounds.height - 20) return false;
  const objects = room === 'bedroom' ? [{ x: 42, y: 77, w: 73, h: 112 }, { x: 228, y: 52, w: 95, h: 46 }] : [...OBSTACLES, ...(!open ? [GATE] : [])];
  return !objects.some(box => overlaps(player, box));
}
// Axis-separated movement keeps sliding along obstacles; small steps prevent tunneling.
export function movePlayer(player, dx, dy, room, open) {
  const steps = Math.max(1, Math.ceil(Math.max(Math.abs(dx), Math.abs(dy)) / 3));
  let next = { ...player };
  for (let i = 0; i < steps; i++) {
    const horizontal = { x: next.x + dx / steps, y: next.y };
    if (canStand(horizontal, room, open)) next = horizontal;
    const vertical = { x: next.x, y: next.y + dy / steps };
    if (canStand(vertical, room, open)) next = vertical;
  }
  return next;
}
