#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
const root = path.dirname(fileURLToPath(import.meta.url));
const [projectArg, outputArg] = process.argv.slice(2);
if (!projectArg || !outputArg || process.argv.length !== 4) throw new Error('Usage: node render.mjs <composition-directory> <output.mp4>');
const project = path.resolve(projectArg), output = path.resolve(outputArg);
if (!output.endsWith('.mp4')) throw new Error('Output must end in .mp4');
fs.accessSync(path.join(project, 'index.html'));
const chrome = process.env.CHROME_PATH;
if (!chrome || !path.isAbsolute(chrome)) throw new Error('Set CHROME_PATH to an approved absolute Chromium executable path');
fs.accessSync(chrome, fs.constants.X_OK);
const home = path.join(root, 'runtime/state');
fs.mkdirSync(home, { recursive: true, mode: 0o700 });
fs.mkdirSync(path.dirname(output), { recursive: true });
const env = {
  PATH: '/usr/local/bin:/usr/bin:/bin', HOME: home, LANG: 'C.UTF-8', CI: '1',
  HYPERFRAMES_NO_TELEMETRY: '1', DO_NOT_TRACK: '1',
  HYPERFRAMES_NO_AUTO_INSTALL: '1', HYPERFRAMES_NO_UPDATE_CHECK: '1', HYPERFRAMES_SKIP_SKILLS: '1',
  HYPERFRAMES_BROWSER_PATH: chrome, PRODUCER_HEADLESS_SHELL_PATH: chrome,
  PRODUCER_DISABLE_HEALTH_WORKER: '1', PUPPETEER_SKIP_DOWNLOAD: 'true'
};
function run(command, args) {
  const result = spawnSync(command, args, { cwd: path.join(root, 'runtime'), env, stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}
run(process.execPath, [path.join(root, 'runtime/node_modules/hyperframes/bin/hyperframes.mjs'), 'render', project, '--output', output, '--workers', '1', '--no-browser-gpu', '--no-best-effort']);
const stem = output.slice(0, -4), poster = stem + '.png';
run('/usr/bin/ffmpeg', ['-nostdin', '-y', '-i', output, '-frames:v', '1', poster]);
const esc = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const relative = file => encodeURI(path.relative(path.dirname(output), file).split(path.sep).join('/')).replaceAll('(', '%28').replaceAll(')', '%29');
const source = path.join(project, 'index.html');
fs.writeFileSync(stem + '.html', `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Documentation walkthrough</title><style>body{max-width:80rem;margin:2rem auto;padding:1rem;font:18px/1.6 system-ui}video{width:100%;height:auto}a:focus-visible{outline:3px solid #067}</style><h1>Documentation walkthrough</h1><p>Playback is optional. The linked static explanation contains the complete sequence and evidence.</p><video controls preload="none" playsinline poster="${esc(relative(poster))}"><source src="${esc(relative(output))}" type="video/mp4"><a href="${esc(relative(output))}">Download video</a></video><p><a href="${esc(relative(source))}">Complete static explanation and editable composition</a></p></html>\n`);
fs.writeFileSync(stem + '.md', `[![Walkthrough thumbnail](${relative(poster)})](${relative(stem + '.html')})\n\n[Play video](${relative(stem + '.html')}) · [MP4](${relative(output)}) · [Static explanation / editable source](${relative(source)})\n`);
console.log(output, stem + '.html', poster);
