# Setup quick reference

Start here to find what is available and how to ask for it.

| Guide | What you will find |
| --- | --- |
| [Commands](COMMANDS.md) | Every custom slash command, examples, profile availability, and edit/publication limits |
| [Skills](SKILLS.md) | Every maintained skill, grouped by task, with a purpose and example request |
| [Extensions and integrations](EXTENSIONS.md) | Plugins, browser relay, MCP integrations, and native helpers |
| [Packages](PACKAGES.md) | Source pins, dependencies, configuration ownership, and setup boundaries |
| [Profiles](../profiles/README.md) | Model selection and per-profile resource lists |

## Start a session

From your project directory:

```sh
ohMyPi -model=luna -type=backend
```

Choose `backend`, `frontend`, `ux`, `pm`, or `research`. Model choices are `luna`,
`astra`, `sol`, and `f2p`. Omit options to use the configured defaults.

To inspect the selected catalog without model requests or MCP connections:

```sh
ohMyPi -model=astra -type=research --inspect
```

Read the unavailable-resource lists and warnings. A successful inspection does not
prove authentication or runtime readiness. Restart OMP after resource changes.

## Names mean different things

- **Command:** a named workflow you invoke, such as `/pr-review`.
- **Skill:** task guidance selected from your request. Ask in ordinary language;
  naming the skill makes your intent explicit.
- **Plugin or extension:** adds host capabilities or resources; may execute code.
- **MCP integration:** connects to tools outside the core assistant; needs separate setup.

Profiles expose selected resources; they are not permission sandboxes. Plain
`omp` does not apply the launcher's profile filtering. Availability does not grant
permission to publish, install packages, access production, or spend money.

For setup and migration, read [installation](INSTALL.md).
