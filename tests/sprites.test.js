import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { NPCS } from '../src/world.js';

// PNG width/height live in the IHDR chunk at bytes 16-23.
const size = path => {
  const b = readFileSync(new URL(`../public/${path}`, import.meta.url));
  assert.equal(b.toString('ascii', 1, 4), 'PNG', path);
  return [b.readUInt32BE(16), b.readUInt32BE(20)];
};
const SHEETS = { logan: 'logan', ryan: 'ryan', sophie: 'sophie', parents: 'mother', dad: 'father', angie: 'angie' };

test('every character has a 16 x 32 sprite sheet: 3 frames x 4 directions', () => {
  for (const id of ['logan', ...NPCS.map(n => n.id)]) {
    assert.ok(SHEETS[id], `no sheet mapped for ${id}`);
    assert.deepEqual(size(`sprites/${SHEETS[id]}.png`), [48, 128], id);
  }
});

test('every speaker has a 96 x 96 dialogue portrait', () => {
  for (const id of ['logan', 'angie', 'ryan', 'sophie', 'mother', 'father']) {
    assert.deepEqual(size(`portraits/${id}.png`), [96, 96], id);
  }
});
