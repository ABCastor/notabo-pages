import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';

const home = await readFile('site/index.html', 'utf8');
const policy = await readFile('site/privacy/index.html', 'utf8');
test('the product page leads to the published privacy route', () => {
  assert.match(home, /<h1>Notabo<\/h1>/);
  assert.match(home, /href="privacy\/"/);
  assert.match(home, /Notabo is in development/);
});
test('the notice describes the current Calendar grant and revocation limits', () => {
  for (const phrase of ['calendars you own', 'read, create, change and delete', 'stored on your own devices', 'when you choose to sync', 'Google also stores your events', 'own 1Password account', 'does not erase copies']) {
    assert.ok(policy.includes(phrase), `Missing disclosure: ${phrase}`);
  }
  assert.match(policy, /href="https:\/\/myaccount.google.com\/permissions"/);
  assert.match(policy, /href="\.\.\/"/);
});
test('pages are readable without script, forms or third-party embeds', () => {
  for (const html of [home, policy]) {
    assert.doesNotMatch(html, /<(script|iframe|form)\b/i);
    assert.match(html, /<html lang="en">/);
    assert.match(html, /name="viewport"/);
    assert.match(html, /class="skip" href="#main"/);
    assert.match(html, /<main id="main"/);
  }
});
test('the build preserves exactly the public site bytes', async () => {
  execFileSync(process.execPath, ['scripts/build.mjs']);
  const entries = (await readdir('site', { recursive: true, withFileTypes: true })).filter(e => e.isFile());
  for (const e of entries) {
    const rel = `${e.parentPath}/${e.name}`.slice('site/'.length);
    assert.deepEqual(await readFile(`dist/${rel}`), await readFile(`site/${rel}`));
  }
  assert.equal(entries.length, 4);
});
