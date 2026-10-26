import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync(new URL('../motion-state.js', import.meta.url), 'utf8');
function setup(reduced) {
  const classes = new Set(), events = [], mediaListeners = {};
  const button = {
    hidden: true, attrs: {}, listeners: {},
    setAttribute(name, value) { this.attrs[name] = value; },
    addEventListener(name, listener) { this.listeners[name] = listener; }
  };
  const document = {
    body: { classList: { toggle(name, enabled) { enabled ? classes.add(name) : classes.delete(name); } } },
    querySelectorAll() { return [button]; },
    dispatchEvent(event) { events.push(event); }
  };
  const window = {};
  vm.runInNewContext(source, {
    window, document,
    matchMedia: () => ({ matches: reduced, addEventListener: (name, fn) => { mediaListeners[name] = fn; } }),
    CustomEvent: class { constructor(type, options) { this.type = type; this.detail = options.detail; } }
  });
  return { window, button, classes, events, mediaListeners };
}

test('reduced motion starts paused and exposes an accessible play control', () => {
  const state = setup(true);
  assert.equal(state.window.SnowMotion.paused, true);
  assert.equal(state.button.hidden, false);
  assert.equal(state.button.attrs['aria-label'], '動きを再生');
  assert.equal(state.classes.has('all-motion-paused'), true);
});

test('button updates one shared state and notifies decorative consumers', () => {
  const state = setup(false);
  state.button.listeners.click();
  assert.equal(state.window.SnowMotion.paused, true);
  assert.equal(state.button.attrs['aria-pressed'], 'true');
  assert.equal(state.events.at(-1).type, 'snow-motion-change');
  assert.equal(state.events.at(-1).detail.paused, true);
  state.button.listeners.click();
  assert.equal(state.window.SnowMotion.paused, false);
  assert.equal(state.classes.has('all-motion-paused'), false);
});

test('OS preference changes update the same state after page load', () => {
  const state = setup(false);
  state.mediaListeners.change({ matches: true });
  assert.equal(state.button.attrs['aria-label'], '動きを再生');
  assert.equal(state.window.SnowMotion.paused, true);
});


test('closing an overlay restores motion without changing the visitor preference', () => {
  const state = setup(false);
  state.window.SnowMotion.setSuspended('menu', true);
  assert.equal(state.window.SnowMotion.paused, true);
  assert.equal(state.events.at(-1).detail.paused, true);
  assert.equal(state.button.attrs['aria-pressed'], 'false');
  state.window.SnowMotion.setSuspended('menu', false);
  assert.equal(state.window.SnowMotion.paused, false);
  state.window.SnowMotion.setPaused(true);
  state.window.SnowMotion.setSuspended('menu', true);
  state.window.SnowMotion.setSuspended('menu', false);
  assert.equal(state.window.SnowMotion.paused, true);
  assert.equal(state.button.attrs['aria-pressed'], 'true');
});

test('independent occlusion reasons cannot prematurely resume motion', () => {
  const state = setup(false);
  state.window.SnowMotion.setSuspended('menu', true);
  state.window.SnowMotion.setSuspended('people', true);
  state.window.SnowMotion.setSuspended('menu', false);
  assert.equal(state.window.SnowMotion.paused, true);
  state.window.SnowMotion.setSuspended('people', false);
  assert.equal(state.window.SnowMotion.paused, false);
});
