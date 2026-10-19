#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
const root = path.dirname(fileURLToPath(import.meta.url));
const [type, sourceArg, outputArg] = process.argv.slice(2);
if (!type || !sourceArg || !outputArg || process.argv.length !== 5) throw new Error('Usage: node generate.mjs <type> <source.json> <output.html>');
const source = path.resolve(sourceArg), output = path.resolve(outputArg);
if (!output.endsWith('.html')) throw new Error('Output must end in .html');
const spec = JSON.parse(fs.readFileSync(source, 'utf8'));
if (!['none', 'trace'].includes(spec.meta?.animation)) throw new Error('Set meta.animation explicitly: none by default; trace only when requested.');
const executablePath = process.env.CHROME_PATH;
if (!executablePath || !path.isAbsolute(executablePath)) throw new Error('Set CHROME_PATH to an approved absolute Chromium executable path');
fs.accessSync(executablePath, fs.constants.X_OK);
const result = spawnSync(process.execPath, [path.join(root, 'bin/archify.mjs'), 'render', type, source, output], { stdio: 'inherit', env: { ...process.env, ARCHIFY_UPDATE_CHECK_DISABLED: '1' } });
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status ?? 1);
const require = createRequire(path.join(root, '../hyperframes/runtime/package.json'));
const { default: puppeteer } = await import(pathToFileURL(require.resolve('puppeteer-core')).href);
const browser = await puppeteer.launch({ executablePath, headless: true });
const png = output.slice(0, -5) + '.png';
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 1200, deviceScaleFactor: 1 });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.setRequestInterception(true);
  page.on('request', request => /^(file:|data:|blob:)/.test(request.url()) ? request.continue() : request.abort());
  await page.goto(pathToFileURL(output).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const diagram = await page.$('.diagram-container');
  if (!diagram) throw new Error('Rendered Archify diagram container is missing');
  await diagram.screenshot({ path: png });
} finally { await browser.close(); }
const link = file => encodeURI(path.relative(path.dirname(output), file).split(path.sep).join('/')).replaceAll('(', '%28').replaceAll(')', '%29');
const markdown = `[![Diagram preview](${link(png)})](${link(output)})\n\n[Interactive diagram](${link(output)}) · [Editable source](${link(source)})\n`;
fs.writeFileSync(output.slice(0, -5) + '.md', markdown);
console.log(output, png);
