#!/usr/bin/env bun
import { mkdtempSync, realpathSync, rmSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = resolve(dirname(realpathSync(fileURLToPath(import.meta.url))), "..");
const manifestPath = join(root, "profiles/profiles.yml");

function mapping(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be a YAML mapping`);
  }
  return value;
}

function stringList(value, label) {
  if (!Array.isArray(value) || value.some(item => typeof item !== "string" || !item.trim())) {
    throw new Error(`${label} must be an array of nonempty strings`);
  }
  return value;
}

function entry(table, name, label) {
  mapping(table, label);
  if (!Object.hasOwn(table, name)) {
    throw new Error(`Unknown ${label} '${name}'. Available: ${Object.keys(table ?? {}).join(", ")}`);
  }
  return table[name];
}

function combineLists(shared, local, label) {
  return [...new Set([
    ...stringList(shared, `global.${label}`),
    ...stringList(local, `type.${label}`),
  ])];
}

function expandPath(path) {
  return path === "~" ? homedir() : path.startsWith("~/") ? join(homedir(), path.slice(2)) : path;
}

async function main() {
  const manifest = mapping(Bun.YAML.parse(await Bun.file(manifestPath).text()), manifestPath);
  for (const key of ["defaults", "models", "global", "types"]) mapping(manifest[key], key);
  stringList([manifest.defaults.model, manifest.defaults.type], "defaults");
  const args = process.argv.slice(2);
  let model = manifest.defaults.model;
  let type = manifest.defaults.type;
  let cwd = process.cwd();
  let inspect = false;
  const overlays = [];
  const forwarded = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--") {
      forwarded.push(...args.slice(i));
      break;
    }
    if (arg === "--help" || arg === "-h") {
      console.log(`Usage: ohMyPi -model=luna -type=backend [OMP options] [prompt]

Defaults: ${manifest.defaults.model}, ${manifest.defaults.type}. Both -model/--model and -type/--type
accept =value or a separate value. Models: ${Object.keys(manifest.models).join(", ")}.
Types: ${Object.keys(manifest.types).join(", ")}.

  ohMyPi -model=luna -type=backend
  ohMyPi --model luna --type backend --cwd ~/service
  ohMyPi -model=luna -type=backend --inspect

Edit ${manifestPath} for modelRoles and resource selections. Full Markdown
commands live in ${join(root, "agent", "commands")}. Every type inherits global.skills,
global.commands and global.mcpServers, then adds its own explicit lists.
--inspect shows native skill/file-command/MCP discovery without connecting
servers or starting a model session. --cwd and --config are supported.
Use -- before a prompt that looks like a launcher option.

This is a per-launch overlay, not a separate auth profile or security sandbox.
Global rules, auth and connection definitions stay unchanged. Selected model
settings/instructions apply per launch; MCP servers are filtered by exact name.
Built-in commands, extension commands and bundled /init remain. Command and MCP
exclusions are startup snapshots; restart after adding resources or changing projects.
Skills are filtered by resolved name, not source. Other OMP options pass through.
Explicit extension/profile/skill overrides are rejected; use plain omp for those.
Native OMP options: omp --help`);
      return;
    }
    if (arg === "--inspect") {
      inspect = true;
      continue;
    }
    const option = arg.split("=", 1)[0];
    if (["--profile", "--alias", "--skills", "--no-skills", "--provider", "--extension", "-e", "--hook", "--plugin-dir"].includes(option)) {
      throw new Error(`${option} changes profile discovery/model selection; use plain omp instead`);
    }
    if (["-model", "--model", "-type", "--type", "--cwd", "--config"].includes(option)) {
      const value = arg.includes("=") ? arg.slice(arg.indexOf("=") + 1) : args[++i];
      if (!value || value.startsWith("-")) throw new Error(`${option} requires a value`);
      if (option === "-model" || option === "--model") model = value;
      else if (option === "-type" || option === "--type") type = value;
      else if (option === "--cwd") cwd = resolve(expandPath(value));
      else overlays.push(resolve(expandPath(value)));
      continue;
    }
    forwarded.push(arg);
  }
  const agentDir = process.env.PI_CODING_AGENT_DIR;
  if (process.env.OMP_PROFILE || (agentDir && resolve(expandPath(agentDir)) !== join(root, "agent"))) {
    throw new Error("This launcher targets your default OMP setup; unset OMP_PROFILE/PI_CODING_AGENT_DIR or use plain omp");
  }
  const selected = mapping(entry(manifest.types, type, "developer type"), `types.${type}`);
  const skills = combineLists(manifest.global.skills, selected.skills, "skills");
  const commands = combineLists(manifest.global.commands, selected.commands, "commands");
  const mcpServers = combineLists(manifest.global.mcpServers, selected.mcpServers, "mcpServers");
  if (skills.length === 0) throw new Error("Global and type skills cannot both be empty; OMP treats an empty allowlist as all skills");
  const modelProfile = mapping(entry(manifest.models, model, "model alias"), `models.${model}`);
  const modelSettings = mapping(modelProfile.settings ?? {}, `models.${model}.settings`);
  const modelInstructions = modelProfile.instructions ?? "";
  if (typeof modelInstructions !== "string") throw new Error(`models.${model}.instructions must be a string`);
  const modelRoles = mapping(modelProfile.modelRoles, `models.${model}.modelRoles`);
  stringList([modelRoles.default, ...Object.values(modelRoles)], "modelRoles selectors");
  const statusLabel = `${model} - ${type}`;
  const configFiles = overlays;
  const executable = Bun.which("omp");
  if (!executable) throw new Error("omp is not on PATH");
  // Use OMP's own discovery, including project and plugin commands, instead of duplicating it.
  const packageRoot = resolve(dirname(realpathSync(executable)), "..");
  const native = path => import(pathToFileURL(join(packageRoot, "src", path)).href);
  const { Settings } = await native("config/settings.ts");
  const { initializeWithSettings, loadCapability } = await native("discovery/index.ts");
  const { cfgDisabledExtensions, cfgExtensions, cfgSkills } = await native("extensibility/settings.ts");
  const { cfgModelRoles } = await native("config/model-settings.ts");
  const settings = (await Settings.loadReadOnly({ cwd, configFiles })).overlay({ ...modelSettings, modelRoles });
  const temporary = mkdtempSync(join(tmpdir(), "ohMyPi-"));
  const cleanup = () => rmSync(temporary, { recursive: true, force: true });
  let child;
  // Before spawn, signals exit through cleanup; afterward OMP owns interactive Ctrl-C.
  const interrupt = () => { if (!child) process.exit(130); };
  const terminate = () => {
    if (child) child.kill("SIGTERM");
    else process.exit(143);
  };
  process.once("exit", cleanup);
  process.on("SIGINT", interrupt);
  process.on("SIGTERM", terminate);
  try {
    // Use the same status-extension root for inspection and the child process.
    const extensionRoots = {
      explicit: [temporary],
      mode: "merge",
      configured: cfgExtensions.get(settings),
      configuredLevel: settings.extensionsSourceLevel(),
    };
    const disabled = new Set(cfgDisabledExtensions.get(settings));
    let mcpDiscoveryWarnings = [];
    let release = initializeWithSettings(settings);
    try {
      const discovered = await loadCapability("slash-commands", {
        cwd, includeDisabled: true, disabledExtensions: [...disabled], extensionRoots,
      });
      for (const command of discovered.all) {
        if (!commands.includes(command.name)) disabled.add(`slash-command:${command.name}`);
      }
      const discoveredMcp = await loadCapability("mcps", {
        cwd, includeDisabled: true, disabledExtensions: [...disabled], extensionRoots,
      });
      mcpDiscoveryWarnings = discoveredMcp.warnings;
      for (const server of discoveredMcp.all) {
        if (!mcpServers.includes(server.name)) disabled.add(`mcp:${server.name}`);
      }
    } finally {
      release();
    }
    const overlay = {
      ...modelSettings,
      modelRoles,
      skills: { includeSkills: skills },
      disabledExtensions: [...disabled],
    };
    const roles = cfgModelRoles.get(settings);
    if (typeof roles.default !== "string" || !roles.default) throw new Error("Selected model profile has no default model");
    if (inspect) {
      const filtered = settings.overlay({
        "skills.includeSkills": skills,
        disabledExtensions: [...disabled],
      });
      release = initializeWithSettings(filtered);
      try {
        const { loadSkills } = await native("extensibility/skills.ts");
        const { loadSlashCommands } = await native("extensibility/slash-commands.ts");
        const { loadAllMCPConfigs } = await native("mcp/config.ts");
        const { cfgMcpEnableProjectConfig } = await native("mcp/settings.ts");
        const loaded = await loadSkills({
          ...cfgSkills.get(filtered), cwd, disabledExtensions: [...disabled], extensionRoots,
        });
        const fileCommands = await loadSlashCommands({ cwd, extensionRoots });
        const names = loaded.skills.map(skill => skill.name);
        const mcp = await loadAllMCPConfigs(cwd, {
          enableProjectConfig: cfgMcpEnableProjectConfig.get(filtered), extensionRoots,
        });
        const availableMcpServers = Object.keys(mcp.configs).sort();
        console.log(JSON.stringify({
          type, model, modelRoles: roles, cwd, manifest: manifestPath,
          statusLabel,
          modelSettings,
          modelInstructions,
          skillGroups: ["global", type],
          commandGroups: ["global", type],
          skills: names,
          fileCommands: fileCommands.map(command => command.name),
          selectedMcpServers: mcpServers,
          mcpServers: availableMcpServers,
          unavailableMcpServers: mcpServers.filter(name => !availableMcpServers.includes(name)),
          unavailableSkillPatterns: skills.filter(pattern => !names.some(name => new Bun.Glob(pattern).match(name))),
          unavailableCommands: commands.filter(name => !fileCommands.some(command => command.name === name)),
          warnings: [...loaded.warnings, ...mcpDiscoveryWarnings],
        }, null, 2));
      } finally {
        release();
      }
      return;
    }
    const overlayPath = join(temporary, "profile.yml");
    await Bun.write(overlayPath, Bun.YAML.stringify(overlay));
    await Bun.write(join(temporary, "index.js"), `export default function (pi) {
  pi.on("session_start", (_event, ctx) => {
    ctx.ui.setStatus("ohMyPi.profile", ${JSON.stringify(statusLabel)});
  });
  ${modelInstructions ? `pi.on("before_agent_start", event => ({
    systemPrompt: [...event.systemPrompt, ${JSON.stringify(modelInstructions)}],
  }));` : ""}
}
`);
    child = Bun.spawn([
      executable, "--cwd", cwd,
      ...configFiles.flatMap(path => ["--config", path]),
      "--config", overlayPath, "--model", roles.default,
      "--extension", temporary,
      ...forwarded,
    ], { stdin: "inherit", stdout: "inherit", stderr: "inherit" });
    process.exitCode = await child.exited;
  } finally {
    process.off("SIGINT", interrupt);
    process.off("SIGTERM", terminate);
    process.off("exit", cleanup);
    cleanup();
  }
}

try {
  await main();
} catch (error) {
  console.error(`ohMyPi: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
}
