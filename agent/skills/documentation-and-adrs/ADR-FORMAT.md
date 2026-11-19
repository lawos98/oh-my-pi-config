# ADR format

Match the repository's existing ADR convention. Use this fallback only when no convention exists.

Store decisions under `docs/decisions/` with sequential names such as `0001-use-postgresql.md`.

```md
# {Short decision title}

## Status

Proposed

## Context

{The constraint or problem that required a decision.}

## Decision

{What was chosen and why.}

## Alternatives considered

{Only credible alternatives whose rejection may matter later.}

## Consequences

{Only non-obvious costs, constraints, or follow-up effects.}
```

Keep the record proportional to the decision. A short decision may need only a title and one paragraph covering context, choice, and reason. Add sections only when they preserve information a future engineer could not reconstruct cheaply.

Use `Accepted` only after actual approval. Follow the repository's lifecycle; distinguish proposed, accepted, rejected, deprecated, and superseded records. If the decision is already settled, record that accurately rather than staging an artificial approval round. Optional confirmation criteria explain how implementation/compliance will be established; optional revisit conditions name assumptions whose change warrants reconsideration. Neither requires a file-by-file plan.

When a decision changes, preserve history and add or follow the repository's supersession convention rather than rewriting the old rationale as though it never existed.
