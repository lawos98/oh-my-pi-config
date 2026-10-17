# OMP skill mechanics

## Invocation

Choose one invocation mode deliberately.

### Model-invoked

Use a precise `description` and omit `disable-model-invocation` when OMP must discover the skill automatically or another workflow depends on it. The description is always-loaded context, so include only distinct trigger branches.

### User-invoked

Set `disable-model-invocation: true` when the capability should run only after the user explicitly selects it. The description is then a concise human-facing summary. Prefer this for expensive surveys, broad audits, and workflows with material side effects.

A model-invoked skill remains directly invocable by the user.

## Supporting files

Keep the main `SKILL.md` on the common path. Move branch-specific templates, examples, and detailed reference into sibling files, and link them from the exact branch that needs them.

## Provenance

For externally adapted skills:

- pin an immutable upstream revision;
- preserve the upstream license and attribution;
- add `provenance.json` beside the skill;
- describe behavior-changing adaptations;
- never depend on a floating installer or mutable branch at runtime.

## OMP compatibility

Use OMP tool and agent names. OMP global rules remain authoritative over imported instructions, including Git approval, execution limits, delegation, and verification. Remove instructions that assume another host's skill loader, hooks, plugin lifecycle, or command syntax.
