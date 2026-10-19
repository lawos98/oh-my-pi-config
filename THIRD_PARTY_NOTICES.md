# Third-party notices

This repository contains adapted guidance from several external projects. It does not apply one license to the complete repository.

Keep the source references and license notices in each skill. This repository is public. The unresolved provenance concerns below predate this update; they are not a claim of redistribution clearance.

## Ponytail

The public snapshot no longer vendors standalone Ponytail skills. The pinned `@dietrichgebert/ponytail@4.9.0` package supplies its skills, commands, and extension at installation time.

Source: <https://github.com/DietrichGebert/ponytail>

Copyright (c) 2026 DietrichGebert.

License: MIT.

The package version and dependency integrity are recorded in `plugins/package.json` and `plugins/bun.lock`. Preserve the package's own license notices if you redistribute its code.

## React performance

File: `agent/skills/react-best-practices/performance-workflow.md`

Source: <https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/react-best-practices/SKILL.md>

The pinned source repository README labels the project as MIT. The pinned tree does not contain a root `LICENSE` or `NOTICE` file. Verify the license text before public redistribution.

This file is a narrow adaptation of Vercel's React best-practice guidance.

## Simple English

File: `agent/skills/simple-english/SKILL.md`

Source: <https://github.com/AminBlg/SimpleEnglish/tree/8e8a008a13e4b478f9ccc20ca16e79aef66c0739>

Copyright (c) 2026 AminBlg.

License: MIT. The skill contains the source attribution and MIT permission notice.

## Infrastructure review

File: `agent/skills/infrastructure-review/SKILL.md`

Adapted sources:

- Srobroek OMP infrastructure rules: <https://github.com/srobroek/omp-plugins/tree/8427f2098ec7b8d62245f16f4c9d7bdc22d05d75/infrastructure> — Apache-2.0.
- HashiCorp agent skills: <https://github.com/hashicorp/agent-skills/tree/326846817128fd1d052d25fbfded490ce2c5886e> — MPL-2.0.
- FluxCD agent skills: <https://github.com/fluxcd/agent-skills/tree/e7e95ef1648a72f5276db6f98b799c5974ea846f> — Apache-2.0.
- Kubernetes documentation: <https://kubernetes.io/docs/>.
- HashiCorp Terraform documentation: <https://developer.hashicorp.com/terraform/docs>.

MPL-2.0 can impose file-level source and notice duties. Review those duties before public redistribution.

## Observability engineering

File: `agent/skills/observability-engineering/SKILL.md`

Adapted sources:

- Grafana agent skills: <https://github.com/grafana/skills/tree/51d33e71e191b409bbd25fc7be2684c610d18166> — Apache-2.0.
- OpenTelemetry documentation: <https://opentelemetry.io/docs/>.
- Prometheus documentation: <https://prometheus.io/docs/>.

## External supply-chain review

File: `agent/skills/external-supply-chain-review/SKILL.md`

Adapted sources:

- NVIDIA SkillSpector: <https://github.com/NVIDIA/SkillSpector/tree/1b875933a666b627c3ed1b695f066a21a6773dc4> — Apache-2.0.
- Trail of Bits skills: <https://github.com/trailofbits/skills/tree/d1f1575cff97816e5cc08af66cd2506099c681d3> — CC BY-SA 4.0.
- Vibe Skills: <https://github.com/foryourhealth111-pixel/Vibe-Skills/tree/eace1927e5cd7aed57501f81b5ef57ed3ea7008d> — Apache-2.0.
- Testzugang OMP plugins: <https://github.com/testzugang/omp-plugins/tree/417b40455f93da9c5c88dff36ba40cc4bb120a51> — MIT.

The Trail of Bits source uses CC BY-SA 4.0. Public adaptations can require attribution, a modification notice, and ShareAlike terms.

## Simplify

File: `agent/skills/simplify/SKILL.md`

Source named by the local skill: <https://github.com/addyosmani/ai-coding-workflow>

Copyright 2025 Addy Osmani.

License: MIT.

The local skill points to the floating `main` branch. It does not record an immutable source revision.

## Remaining skills

Several existing skills were created or merged locally and do not contain complete provenance metadata. Their inclusion in a setup snapshot does not establish a blanket license grant or resolve missing upstream notices. Preserve all available source metadata and verify applicable rights before redistributing those files further.

## OMP 18.4.4 skill refresh

The following skills retain their source revisions and redistribution notices in their own directories. Their licenses apply separately, not to this whole repository:

| Skill | Source | License |
|---|---|---|
| `i-have-adhd` | ayghri/i-have-adhd, `723af7d9afaf43eb871dbcce6129e2bf80de90d5` | MIT |
| `stop-slop` | hardikpandya/stop-slop, `8da1f030185bdfe8471220585162991eaeb970e9` | MIT |
| `session-handoff`, `lesson-learned` | softaworks/agent-toolkit, `3027f20f3181758385a1bb8c022d4041dfb4de84` | MIT |
| `deprecation-and-migration` | addyosmani/agent-skills, `1401c8b8030e023baeebb31781a6653fe8e93026` | MIT |
| `spec-to-code-compliance` | trailofbits/skills, `d1f1575cff97816e5cc08af66cd2506099c681d3` | CC BY-SA 4.0 |
| `skill-creator` | anthropics/skills, `9d630808e4add0a7146de4af9384155d5dee350a` | Apache-2.0 |

These are modified OMP adaptations; their provenance files describe the modifications. `spec-to-code-compliance` retains Trail of Bits attribution, its license URL, and ShareAlike terms. `skill-creator` retains its supporting scripts, references, `LICENSE.txt`, and `NOTICE.txt`; its execution remains subject to OMP approval policy.


## Documentation and ADRs

File: `agent/skills/documentation-and-adrs/SKILL.md`

Source: <https://github.com/addyosmani/agent-skills/blob/0d52faf08da5a706616e7b1ae05226940c387ad1/skills/documentation-and-adrs/SKILL.md>

Copyright (c) 2025 Addy Osmani.

License: MIT. The permission notice below applies to this file.

## Humanizer

File: `agent/skills/humanizer/SKILL.md`

Source: <https://github.com/blader/humanizer/tree/e2e92e7b4b8229253ed5c8e81dc65463fdeddda5>

Copyright (c) 2025 Siqi Chen.

License: MIT. The permission notice below applies to this file.

This documentation-only adaptation preserves technical facts and requires explicit invocation. It excludes upstream CLI and plugin files.

## MIT permission notice for the additions above

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Complete portable skill assets

This refresh includes the installed generic skill references, templates, images, licenses, and provenance that the earlier file allowlist omitted. It does not import new upstream implementations or claim that an MIT label by itself establishes authorship.

- `writing-for-agents` retains Matt Pocock's MIT license and source revision `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`, plus the additional Softaworks attribution recorded in its provenance.
- React, Supabase, and shadcn support files retain their embedded authorship and source links. Their existing provenance limitations are not resolved by this snapshot.
- The public export omits organization-specific skills and runtime state. Home-relative paths replace workstation paths; Chromium adapters require an explicitly selected `CHROME_PATH`. Historical acceptance evidence in provenance is not verification of this export.

## Plugin and extension manifests

`plugins/package.json`, `plugins/bun.lock`, and `plugins/omp-plugins.lock.json` record the existing installation's package versions, dependency integrity, and enabled state. Plugin runtime code, `node_modules`, marketplace caches, and generated machine-specific registries are not redistributed here. Installations remain subject to each package's own license and lifecycle behavior.

Use the plugin guide for installation and source-pin details. A marketplace fallback version `0.0.0` is not a substitute for an immutable source pin.

## Portable refresh: 2026-10-19

The following additions preserve licenses and source metadata in their skill directories. These are recorded upstream terms, not a blanket clearance for all assets or downstream uses.

| Component | Source revision | Recorded license |
| --- | --- | --- |
| Archify | [tt-a1i/archify](https://github.com/tt-a1i/archify/tree/68be1e0971208ef0b1550ec3b29f3d4d177f3cd6) | MIT; separate font and brand-mark terms |
| HyperFrames adapter and lock | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes/tree/7735338b49ed6e11c227b0710da3bd35c3366b9c) | Apache-2.0; runtime packages not bundled |
| Taste | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill/tree/f624f37a8c650b9cc550253104925efe4c8de246) | MIT; photo/font rights separate |
| Impeccable | [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/c74755d920985f7a92cef691ca970ba95f90126e) | Apache-2.0 |
| Arena | [Jakeschincariol/arena-skill](https://github.com/Jakeschincariol/arena-skill/tree/df07b8e518e10cdecd8cd7712d9958b6f396250e) | MIT |
| Gradle, Jackson and Spring proxy specialists | [yalishevant/kotlin-backend-agent-skills](https://github.com/yalishevant/kotlin-backend-agent-skills/tree/fd0ed521d22efd28221d532c9abab97af0b9bf0e) | MIT, copyright 2026 Anton Yalyshev |
| Penpot UI/UX | [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/d6131471b85fbb4799e64175ebc42c9309ecc28a) | MIT |
| UI UX Pro Max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/09170eec67eefd46a7ae85de61b40c194020f997) | MIT |

Ktor implementation and runtime troubleshooting are locally authored guidance based on linked official documentation; their provenance states that upstream text and code were not vendored. `service-documentation` is also locally authored. It records Zensical 0.0.71 at commit `786383193ba87e7091456e3e30926375b1510127`, under MIT. Only configuration, instructions and dependency locks are included, not Zensical or its dependency binaries.

### Separate asset terms and unresolved issues

- Archify's [third-party notices](agent/skills/archify/THIRD_PARTY_NOTICES.md) and font license are retained. Brand vectors include attribution, ShareAlike, non-commercial and trademark restrictions. In particular, the recorded Vue artwork terms are CC BY-NC-SA 4.0. Do not infer commercial redistribution rights from Archify's MIT license.
- Taste's photo and font URLs do not transfer asset rights. Review the provider's terms before downloading or publishing assets.
- HyperFrames' lock includes packages with LGPL and other licenses. Dependencies and native binaries are not redistributed here; installation and any later redistribution require their own review.
- React's existing missing-license-text concern remains unresolved. Supabase, shadcn and locally merged skills with incomplete provenance also remain unresolved; preserving files does not establish redistribution clearance.
- `grill-me`, `prototype` and `improve-codebase-architecture` record MIT upstream provenance but do not carry standalone license files in the installed source. Review and preserve the applicable upstream copyright and permission text before further redistribution.
- Existing MPL-2.0 and CC BY-SA obligations noted above still apply. This export does not resolve missing source notices or certify compliance.

Public portability modifications replace personal paths, require explicit browser selection, remove unavailable company-skill references and omit a project-specific Penpot reference. Generated renders, dependencies, runtime state and private acceptance reports are excluded. Upstream originals and available licenses remain alongside adaptations.
