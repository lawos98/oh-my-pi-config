// Local OMP hardening. Linux /proc dirfd traversal prevents parent-symlink races.
import { constants as C, openSync, closeSync, fstatSync, mkdirSync, readFileSync, writeSync, renameSync, unlinkSync, lstatSync, realpathSync } from 'node:fs';
import { resolve, relative, sep, basename, dirname } from 'node:path';
import { randomUUID } from 'node:crypto';
import { lookup } from 'node:dns';
import { isIP } from 'node:net';
import { get } from 'node:https';
import { Readable } from 'node:stream';

export function projectPath(path, root = process.cwd()) {
  const base = realpathSync(root);
  const pathResolved = resolve(path);
  const rel = relative(base, pathResolved);
  if (rel === '..' || rel.startsWith('..' + sep) || resolve(base, rel) !== pathResolved) throw new Error('Path must stay in the selected project');
  return { base, rel };
}

// Open each component relative to an already-open directory, never via an unchecked parent.
export function openDirectory(path, { create = false, root = process.cwd() } = {}) {
  if (process.platform !== 'linux') throw new Error('Hardened Taste file operations require Linux /proc');
  const { base, rel } = projectPath(path, root);
  let fd = openSync(base, C.O_RDONLY | C.O_DIRECTORY | C.O_NOFOLLOW);
  try {
    for (const part of rel.split(sep).filter(Boolean)) {
      const next = `/proc/self/fd/${fd}/${part}`;
      if (create) { try { mkdirSync(next, { mode: 0o700 }); } catch (e) { if (e.code !== 'EEXIST') throw e; } }
      const child = openSync(next, C.O_RDONLY | C.O_DIRECTORY | C.O_NOFOLLOW);
      closeSync(fd); fd = child;
    }
    return fd;
  } catch (e) { closeSync(fd); throw e; }
}
export function safeMkdir(path) { closeSync(openDirectory(path, { create: true })); }
export function openProjectFile(path, root = process.cwd()) {
  const parent = openDirectory(dirname(resolve(path)), { root });
  try {
    const fd = openSync(`/proc/self/fd/${parent}/${basename(path)}`, C.O_RDONLY | C.O_NOFOLLOW | C.O_NONBLOCK);
    if (!fstatSync(fd).isFile()) { closeSync(fd); throw new Error('Only regular files may be read'); }
    return fd;
  } finally { closeSync(parent); }
}
export function safeReadFile(path, options) {
  const fd = openProjectFile(path);
  try { return readFileSync(fd, options); } finally { closeSync(fd); }
}
export function stagedOutput(path) {
  const parent = openDirectory(dirname(resolve(path)), { create: true });
  const target = `/proc/self/fd/${parent}/${basename(path)}`;
  const temp = `/proc/self/fd/${parent}/.taste-${randomUUID()}`;
  let fd;
  try {
    try { if (!lstatSync(target).isFile()) throw new Error('Output must be a regular file, not a symlink'); }
    catch (e) { if (e.code !== 'ENOENT') throw e; }
    fd = openSync(temp, C.O_WRONLY | C.O_CREAT | C.O_EXCL | C.O_NOFOLLOW, 0o600);
  } catch (e) { closeSync(parent); throw e; }
  let closed = false;
  return {
    write(data) { let offset = 0; while (offset < data.length) offset += writeSync(fd, data, offset, data.length - offset); },
    commit() {
      if (closed) throw new Error('Output already closed');
      closeSync(fd); fd = undefined;
      try { renameSync(temp, target); } finally { try { unlinkSync(temp); } catch {} closeSync(parent); closed = true; }
    },
    abort() { if (!closed) { if (fd !== undefined) closeSync(fd); try { unlinkSync(temp); } catch {} closeSync(parent); closed = true; } },
  };
}
export function safeWriteFile(path, data) {
  const output = stagedOutput(path);
  try { output.write(Buffer.isBuffer(data) ? data : Buffer.from(data)); output.commit(); }
  catch (e) { output.abort(); throw e; }
}

// Conservative public IPv4 policy: no local, shared, documentation, benchmark, multicast,
// reserved or IPv6 transition addresses. DNS is resolved inside the socket lookup, not checked
// separately before a second vulnerable resolution. IPv6-only providers fail closed.
export function publicIPv4(address) {
  if (isIP(address) !== 4) return false;
  const [a, b, c] = address.split('.').map(Number);
  return !(a === 0 || a === 10 || a === 127 || a >= 224 ||
    (a === 100 && b >= 64 && b <= 127) || (a === 169 && b === 254) ||
    (a === 172 && b >= 16 && b <= 31) || (a === 192 && (b === 168 || b === 0 || (b === 88 && c === 99))) ||
    (a === 198 && (b === 18 || b === 19 || (b === 51 && c === 100))) ||
    (a === 203 && b === 0 && c === 113));
}
export function assetURL(value) {
  const url = new URL(value);
  if (url.protocol !== 'https:' || url.username || url.password || (url.port && url.port !== '443')) throw new Error('Assets require public HTTPS on port 443 without credentials');
  if (url.hostname.startsWith('[') || (isIP(url.hostname) && !publicIPv4(url.hostname))) throw new Error('Non-public asset address');
  return url;
}
function publicLookup(host, options, callback) {
  lookup(host, { family: 4, all: true }, (error, addresses) => {
    if (error) return callback(error);
    if (!addresses.length || addresses.some(({ address }) => !publicIPv4(address))) return callback(new Error('Non-public asset DNS address'));
    const selected = addresses[0];
    if (options.all) callback(null, [selected]); else callback(null, selected.address, selected.family);
  });
}
export async function boundedBody(response, cap) {
  const reader = response.body.getReader();
  const chunks = []; let bytes = 0;
  try {
    if (Number(response.headers.get('content-length')) > cap) throw new Error(`Response exceeds ${cap} byte limit`);
    for (;;) {
      const { done, value } = await reader.read(); if (done) break;
      bytes += value.length;
      if (bytes > cap) throw new Error(`Response exceeds ${cap} byte limit`);
      chunks.push(value);
    }
    return Buffer.concat(chunks, bytes);
  } finally { await reader.cancel().catch(() => {}); }
}
export async function publicFetch(value, options = {}, redirects = 0) {
  const url = assetURL(value);
  options.signal?.throwIfAborted();
  const response = await new Promise((accept, reject) => {
    const req = get(url, { lookup: publicLookup, family: 4, agent: false, signal: options.signal,
      headers: { ...options.headers, 'Accept-Encoding': 'identity' } }, accept);
    req.on('error', reject);
  });
  const status = response.statusCode;
  if ([301, 302, 303, 307, 308].includes(status)) {
    response.destroy();
    if (redirects >= 5 || !response.headers.location) throw new Error('Asset redirect limit or missing location');
    return publicFetch(new URL(response.headers.location, url), options, redirects + 1);
  }
  if (response.headers['content-encoding'] && response.headers['content-encoding'] !== 'identity') { response.destroy(); throw new Error('Compressed asset responses are not accepted'); }
  const headers = new Headers();
  for (const [key, value] of Object.entries(response.headers)) if (value !== undefined) headers.set(key, Array.isArray(value) ? value.join(', ') : value);
  const result = { status, ok: status >= 200 && status < 300, headers, body: Readable.toWeb(response) };
  return { ...result, json: async () => JSON.parse((await boundedBody(result, 20 * 1048576)).toString('utf8')) };
}
