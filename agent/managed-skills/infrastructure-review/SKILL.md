---
name: infrastructure-review
description: "Use when reviewing or changing Dockerfiles, Terraform or OpenTofu, Kubernetes or Helm, CI/CD workflows, deployment configuration, infrastructure policy, or observability infrastructure."
---

# Infrastructure Review

Review infrastructure as executable production behavior. Reuse the repository's deployment model and existing tooling. Do not introduce a second platform convention.

## Discover before changing

- Identify the owning deployable, environments, state backend, deployment controller, secret source, and existing validation commands.
- Read the relevant Docker, Terraform or OpenTofu, Kubernetes or Helm, CI/CD, policy, and environment files together. Trace generated files to their source.
- Determine whether a file is source, generated output, live state, or an exported plan. Never edit state or generated output as source.
- Preserve existing environment names, resource identities, public endpoints, persisted state, and rollout compatibility unless the request explicitly changes them.

## Safety boundary

- Treat plans, state, kubeconfigs, credentials, rendered secrets, logs, and exported diagnostics as sensitive.
- Never deploy, apply, destroy, import, mutate state, rotate credentials, or target a live
  cluster without explicit user scope and approval.
- Before every apply or state mutation, explicitly verify the selected environment, workspace,
  backend, account, region, and plan target. Require approval after the plan and replacement or
  deletion risks are available for review; an earlier request to “fix production now” does not
  approve an unseen plan.
- If target verification or post-plan approval is missing, stop after read-only inspection and
  the saved plan. Do not present an apply command as the next executable step.
- Do not install CLIs, providers, modules, actions, charts, policies, or scanners automatically. Use repository-pinned tooling.

## Terraform and OpenTofu

- Never hand-edit `*.tfstate*`. Use state subcommands only for a proven state operation, after a recoverable backup and an inspected plan.
- Pin provider and module versions according to repository policy. Commit the dependency lock file when the repository owns it.
- Keep provider configuration, variables, outputs, data sources, resources, and modules explicit. Avoid hidden cross-workspace coupling and remote-state dependencies when a normal interface exists.
- Review lifecycle rules, replacement risk, moved/import blocks, sensitive outputs, backend security, drift, and rollback before changing resources.
- `sensitive` redacts display but does not remove a value from state. Use ephemeral or write-only capabilities only when the repository's Terraform and provider versions support them.
- Run the repository's formatting and validation commands. Produce a plan only for a clearly identified non-production target unless the user explicitly authorizes otherwise.

## Kubernetes and Helm

- Distinguish startup, readiness, and liveness. Startup protects slow initialization; readiness controls traffic; liveness is only for conditions a restart can repair.
- Review requests and limits, termination grace, disruption budgets, rollout strategy, service accounts, RBAC, network policy, workload identity, and secret references where relevant.
- Do not place plaintext secrets in manifests, values files, command arguments, annotations, ConfigMaps, or rendered output.
- Preserve selectors, immutable fields, ownership labels, and API compatibility. For controllers, keep desired state in `spec`, observed state in `status`, and never mutate user-owned intent silently.
- Render and validate charts or overlays with the repository's pinned commands before proposing an apply.

## Docker and build images

- Minimize build context and use `.dockerignore`. Keep credentials out of `ARG`, `ENV`, layers, caches, and copied files; use the existing secret-mount mechanism.
- Prefer pinned, maintained base images and multi-stage builds when they reduce the shipped surface. Do not add stages or images without a concrete benefit.
- Run as a non-root user unless the workload proves a narrow privilege requirement. Review capabilities, mounts, ports, health checks, signal handling, and writable paths.
- Do not confuse a small image with a secure image. Verify provenance, update policy, and runtime permissions.

## CI/CD and supply chain

- Minimize workflow permissions. Prefer short-lived OIDC credentials over stored cloud keys when the platform supports them.
- Pin third-party actions and reusable workflows to immutable revisions. Review what secrets, source, caches, artifacts, and tokens each step can access or transmit.
- Separate untrusted pull-request code from privileged jobs. Never expose protected secrets to fork-controlled execution.
- Review cache poisoning, artifact retention, environment approvals, concurrency, cancellation, and deployment rollback where relevant.

## Verification

- Use the narrowest repository-native checks: formatter, validate, render, policy check, static schema check, or read-only plan.
- Report the exact target and command, whether it contacted a remote service, and whether it could read sensitive state.
- A successful syntax check does not prove a safe rollout. Verify replacement, state, compatibility, and failure behavior relevant to the change.

## Sources

Passive guidance adapted from reviewed snapshots:

- `srobroek/omp-plugins@8427f2098ec7b8d62245f16f4c9d7bdc22d05d75` (`infrastructure`, Apache-2.0)
- `hashicorp/agent-skills@326846817128fd1d052d25fbfded490ce2c5886e` (Terraform skills, MPL-2.0)
- `fluxcd/agent-skills@e7e95ef1648a72f5276db6f98b799c5974ea846f` (GitOps audit references, Apache-2.0)
- Kubernetes documentation for startup, readiness, and liveness probes
- HashiCorp documentation for dependency locks and sensitive state
