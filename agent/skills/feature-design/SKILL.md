---
name: feature-design
description: "Use when planning new features, exploring user intent, gathering requirements, writing user stories, EARS functional requirements, acceptance criteria, and implementation checklists. Brainstorm first, then formalize into a spec before any implementation begins."
license: MIT
metadata:
  domain: workflow
  role: specialist
  scope: design
  output-format: document
  triggers: brainstorming, requirements, feature definition, user stories, EARS, acceptance criteria, planning, specification
---

# Feature Design

Run a structured pre-implementation workshop that turns an idea into a validated feature spec.

## Core Principle

**Flow: brainstorm first → then formalize into specs.**

Do not start implementation until the design/spec has been presented, reviewed, and approved.

## When to Use

- Defining a new feature from scratch
- Clarifying vague ideas or changing behavior
- Writing requirements, user stories, or acceptance criteria
- Producing EARS-style functional requirements
- Creating a concise implementation checklist

## Operating Modes

- **PM hat:** user value, goals, scope, success criteria
- **Dev hat:** feasibility, edge cases, security, performance, error handling

## Required Workflow

1. **Explore context** — inspect relevant files, docs, and recent decisions before asking questions.
2. **Check scope** — if the request spans multiple independent systems, decompose it before going deeper.
3. **Brainstorm** — ask one question at a time to understand purpose, constraints, users, and success criteria.
4. **Use structured choices** — prefer multiple-choice prompts when possible; use open-ended questions only when needed.
5. **Offer visuals when useful** — if a question is inherently visual, offer the browser-based visual companion as its own message.
6. **Compare approaches** — propose 2-3 options with trade-offs and a recommendation.
7. **Present the design** — summarize the intended solution in clear sections and pause for approval after each section when useful.
8. **Formalize the spec** — convert the brainstorm into a written feature spec.
9. **Review the spec** — remove ambiguity, contradictions, placeholders, and gaps.
10. **Get approval** — ask the user to review the written spec before moving on.
11. **Hand off** — once approved, transition into implementation planning.

## Brainstorming Rules

- Ask only **one** question per message.
- Prefer short, answerable questions.
- Focus on: who it is for, why it matters, what constraints exist, and how success is measured.
- If the request is too broad, split it into smaller features and design the first one.
- Stay focused; do not propose unrelated refactors.

## Design Rules

- Break the feature into small, clearly bounded units.
- For each unit, define: what it does, how it is used, and what it depends on.
- Keep the design minimal; avoid extra flexibility that is not needed yet.
- Follow existing project patterns unless there is a clear reason not to.

## Spec Requirements

The final spec should include:

- Overview and user value
- Assumptions and scope
- Functional requirements in **EARS** form
- User stories when helpful
- Non-functional requirements (performance, security, reliability)
- Error handling and edge cases
- Acceptance criteria in testable form
- Implementation checklist

## EARS Guidance

Write requirements as clear, testable statements such as:

- When <trigger>, the system shall <response>.
- Where <condition> is active, the system shall <behavior>.
- The system shall <action> within <measure>.

## Acceptance Criteria Guidance

Use concrete, verifiable scenarios. Favor Given/When/Then language.

## Review Checklist

Before handing off, confirm:

- No TBDs, TODOs, or placeholders remain
- No contradictory requirements
- Scope is still coherent for a single implementation plan
- Ambiguous statements have been made explicit
- Requirements are testable
- Security and error handling are addressed

## Handoff

After the spec is approved, move into implementation planning.
