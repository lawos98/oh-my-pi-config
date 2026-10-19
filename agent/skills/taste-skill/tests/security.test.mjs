import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, symlinkSync, renameSync, linkSync, existsSync, closeSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import https from 'node:https';
import dns from 'node:dns';
import { syncBuiltinESMExports } from 'node:module';
import { PassThrough } from 'node:stream';
import { EventEmitter } from 'node:events';
import { openProjectFile, safeWriteFile, stagedOutput, boundedBody, assetURL, publicIPv4, publicFetch } from '../scripts/lib/security.mjs';

// No browser, internet, packages or credentials. Run with Node's built-in test runner.
test('file boundaries refuse links and survive parent/leaf replacement races', () => {
  const oldCwd = process.cwd();
  const root = mkdtempSync(join(tmpdir(), 'taste-security-'));
  const project = join(root, 'project'); const outside = join(root, 'outside');
  mkdirSync(project); mkdirSync(outside); process.chdir(project);
  try {
    writeFileSync(join(outside, 'secret'), 'secret');
    symlinkSync(outside, 'escape');
    symlinkSync(join(outside, 'secret'), 'leaf');
    assert.throws(() => openProjectFile('escape/secret'));
    assert.throws(() => openProjectFile('leaf'));
    assert.throws(() => openProjectFile(join(outside, 'secret')));
    assert.throws(() => safeWriteFile('escape/new', 'bad'));
    assert.throws(() => safeWriteFile('leaf', 'bad'));
    assert.throws(() => safeWriteFile('../outside/new', 'bad'));
    safeWriteFile('assets/ok', 'first');
    const fd = openProjectFile('assets/ok');
    try { assert.equal(readFileSync(fd, 'utf8'), 'first'); } finally { closeSync(fd); }
    const staged = stagedOutput('assets/race');
    staged.write(Buffer.from('safe'));
    renameSync('assets', 'original-assets'); symlinkSync(outside, 'assets');
    staged.commit();
    assert.equal(readFileSync('original-assets/race', 'utf8'), 'safe');
    assert.equal(existsSync(join(outside, 'race')), false);
    const leafRace = stagedOutput('original-assets/replaced');
    symlinkSync(join(outside, 'secret'), 'original-assets/replaced');
    leafRace.write(Buffer.from('replacement')); leafRace.commit();
    assert.equal(readFileSync('original-assets/replaced', 'utf8'), 'replacement');
    assert.equal(readFileSync(join(outside, 'secret'), 'utf8'), 'secret');
    linkSync(join(outside, 'secret'), 'original-assets/hardlink');
    safeWriteFile('original-assets/hardlink', 'independent');
    assert.equal(readFileSync(join(outside, 'secret'), 'utf8'), 'secret');
    const aborted = stagedOutput('original-assets/race');
    aborted.write(Buffer.from('partial')); aborted.abort();
    assert.equal(readFileSync('original-assets/race', 'utf8'), 'safe');
  } finally { process.chdir(oldCwd); rmSync(root, { recursive: true, force: true }); }
});

test('stream limits reject announced and chunked oversized responses and cancel', async () => {
  let cancelled = false;
  const response = (chunks, length) => ({ headers: new Headers(length ? { 'content-length': String(length) } : {}), body: new ReadableStream({
    pull(controller) { if (chunks.length) controller.enqueue(Buffer.from(chunks.shift())); else controller.close(); },
    cancel() { cancelled = true; },
  }) });
  assert.equal((await boundedBody(response(['ab', 'cd']), 4)).toString(), 'abcd');
  await assert.rejects(boundedBody(response(['ab', 'cde', 'more']), 4), /limit/);
  assert.equal(cancelled, true);
  cancelled = false;
  await assert.rejects(boundedBody(response(['a'], 10), 4), /limit/);
  assert.equal(cancelled, true);
});

test('URL policy rejects private, encoded IP, credentials, scheme and port escapes', async () => {
  for (const ip of ['0.0.0.0', '10.0.0.1', '127.0.0.1', '169.254.169.254', '100.64.0.1', '172.31.0.1', '192.168.1.1', '192.0.0.9', '198.18.0.1', '198.51.100.1', '203.0.113.1', '224.0.0.1', '255.255.255.255', '::1', '::ffff:127.0.0.1']) assert.equal(publicIPv4(ip), false, ip);
  assert.equal(publicIPv4('8.8.8.8'), true);
  for (const url of ['http://example.org/a', 'file:///etc/passwd', 'https://127.1/a', 'https://2130706433/a', 'https://0x7f000001/a', 'https://[::1]/a', 'https://user:pass@example.org/a', 'https://example.org:8443/a']) {
    assert.throws(() => assetURL(url));
    await assert.rejects(publicFetch(url));
  }
  assert.equal(assetURL('https://example.org/a').protocol, 'https:');
});

test('redirects reapply URL policy, cap hops, and use connection-time DNS lookup', async (t) => {
  let calls = 0; let location = 'https://127.0.0.1/secret';
  let connectionLookup;
  t.mock.method(https, 'get', (url, options, callback) => {
    calls++;
    assert.equal(options.agent, false);
    assert.equal(options.family, 4);
    assert.equal(typeof options.lookup, 'function');
    connectionLookup = options.lookup;
    const res = new PassThrough(); res.statusCode = 302; res.headers = { location };
    queueMicrotask(() => callback(res));
    return new EventEmitter();
  });
  syncBuiltinESMExports();
  try {
    await assert.rejects(publicFetch('https://example.org/start'), /Non-public/);
    assert.equal(calls, 1, 'private redirect never reaches transport');
    t.mock.method(dns, 'lookup', (host, options, callback) => callback(null, [
      { address: '8.8.8.8', family: 4 }, { address: '127.0.0.1', family: 4 },
    ]));
    syncBuiltinESMExports();
    await assert.rejects(new Promise((resolve, reject) => connectionLookup('untrusted.example', {}, (error, address) => error ? reject(error) : resolve(address))), /Non-public asset DNS/);
    location = 'http://example.org/downgrade'; calls = 0;
    await assert.rejects(publicFetch('https://example.org/start'), /HTTPS/);
    assert.equal(calls, 1);
    location = '/again'; calls = 0;
    await assert.rejects(publicFetch('https://example.org/start'), /redirect limit/);
    assert.equal(calls, 6);
  } finally { t.mock.restoreAll(); syncBuiltinESMExports(); }
});
