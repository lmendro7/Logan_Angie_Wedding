export const SAVE_KEY = 'logan-angie-wedding:v1';
export const RING_IDS = ['fountain', 'tree'];
export const freshProgress = () => ({ version: 1, rings: [], met: [], room: 'bedroom', completed: false });

export function normalizeProgress(raw) {
  if (!raw || raw.version !== 1) return freshProgress();
  const rings = RING_IDS.filter(id => Array.isArray(raw.rings) && raw.rings.includes(id));
  return { version: 1, rings, met: ['ryan', 'sophie', 'parents'].filter(id => Array.isArray(raw.met) && raw.met.includes(id)), room: raw.room === 'garden' ? 'garden' : 'bedroom', completed: rings.length === 2 && raw.completed === true };
}
export const gateOpen = progress => RING_IDS.every(id => progress.rings.includes(id));
export function collectRing(progress, id) {
  return normalizeProgress({ ...progress, rings: [...progress.rings, id] });
}
export function loadProgress(storage) {
  try { return normalizeProgress(JSON.parse(storage.getItem(SAVE_KEY))); }
  catch { return freshProgress(); }
}
export function saveProgress(storage, progress) {
  try { storage.setItem(SAVE_KEY, JSON.stringify(normalizeProgress(progress))); return true; }
  catch { return false; }
}
export function objective(progress) {
  if (progress.completed) return 'You made it. Enjoy your day together.';
  if (gateOpen(progress)) return 'Both rings found! Head to Angie.';
  if (!progress.met.includes('ryan')) return 'See if Ryan knows what happened.';
  if (!progress.rings.includes('fountain')) return progress.met.includes('sophie') ? 'Search around the fountain.' : 'Find Sophie by the garden bench.';
  return progress.met.includes('parents') ? 'Search beneath the tree near the venue.' : 'Talk to Mother and Father near the venue.';
}
