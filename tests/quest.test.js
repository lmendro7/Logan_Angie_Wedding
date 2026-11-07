import test from 'node:test';
import assert from 'node:assert/strict';
import { freshProgress, collectRing, gateOpen, loadProgress, saveProgress, normalizeProgress } from '../src/quest.js';
import { canStand, movePlayer, RINGS } from '../src/world.js';

test('gate requires both distinct rings, in either collection order', () => {
  for (const order of [['fountain', 'tree'], ['tree', 'fountain']]) {
    let p = freshProgress();
    assert.equal(gateOpen(p), false);
    p = collectRing(p, order[0]);
    assert.equal(gateOpen(p), false);
    p = collectRing(p, order[0]);
    p = collectRing(p, 'not-a-ring');
    assert.equal(gateOpen(p), false);
    assert.equal(p.rings.length, 1);
    p = collectRing(p, order[1]);
    assert.equal(gateOpen(p), true);
  }
});
test('reload preserves a locked or unlocked gate and rejects malformed progress', () => {
  const memory = new Map();
  const storage = { getItem: k => memory.get(k), setItem: (k, v) => memory.set(k, v) };
  let p = collectRing(freshProgress(), 'tree');
  assert.equal(saveProgress(storage, p), true);
  assert.equal(gateOpen(loadProgress(storage)), false);
  p = collectRing(p, 'fountain');
  saveProgress(storage, p);
  assert.equal(gateOpen(loadProgress(storage)), true);
  assert.deepEqual(normalizeProgress({ version: 1, rings: ['tree', 'tree', 'fake'], completed: true }).rings, ['tree']);
  assert.equal(normalizeProgress({ version: 1, rings: ['tree'], completed: true }).completed, false);
  assert.deepEqual(loadProgress({ getItem: () => '{broken' }), freshProgress());
  assert.equal(saveProgress(null, p), false);
});
test('actual movement blocks gate with zero/one ring and passes with both', () => {
  const start = { x: 384, y: 245 };
  assert.ok(movePlayer(start, 0, -100, 'garden', false).y >= 223);
  assert.ok(movePlayer(start, 0, -100, 'garden', true).y < 200);
  // A long frame still cannot tunnel through a wall.
  assert.ok(movePlayer({ x: 240, y: 130 }, 1000, 0, 'garden', false).x < 250);
});
test('reachable topology: both rings outside the gate, Angie inaccessible until open', () => {
  function reachable(open) {
    const step = 4;
    const queue = [{ x: 384, y: 820 }];
    const seen = new Set(['384,820']);
    for (let i = 0; i < queue.length; i++) {
      const p = queue[i];
      for (const [dx, dy] of [[step, 0], [-step, 0], [0, step], [0, -step]]) {
        const q = { x: p.x + dx, y: p.y + dy }, key = `${q.x},${q.y}`;
        if (!seen.has(key) && canStand(q, 'garden', open)) { seen.add(key); queue.push(q); }
      }
    }
    return target => queue.some(p => Math.hypot(p.x - target.x, p.y - target.y) < 20);
  }
  const closed = reachable(false);
  for (const ring of RINGS) assert.equal(closed(ring), true, ring.id);
  assert.equal(closed({ x: 384, y: 115 }), false);
  assert.equal(reachable(true)({ x: 384, y: 115 }), true);
});
