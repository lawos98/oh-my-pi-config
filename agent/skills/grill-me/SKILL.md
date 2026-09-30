---
name: grill-me
description: Interview me about one decision at a time, using beginner-friendly explanations, clear options, a recommendation, and simple comparisons.
disable-model-invocation: true
license: MIT
metadata:
  source: https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grilling
  source_commit: c55ee46073ed923f86ce59a5eb3b6d895095d1b7
  adaptation: OMP one-question mode
---

# Grill Me

Help the user make a plan or decision through a calm, step-by-step interview. Assume no prior knowledge of the subject.

## 1. Learn the facts first

Inspect the repository, configuration, documentation, or other available evidence before asking a question. Do not ask the user for facts the tools can find.

Ask only about intent, priorities, preferences, risk, scope, and trade-offs.

## 2. Map the decisions

Build a private decision tree. Pick the earliest unanswered decision whose prerequisites are already settled. Questions that depend on its answer wait for later turns.

Do not show the whole tree unless the user asks for it.

## 3. Explain it for a complete beginner

Before asking the question, give the user enough context to choose without searching elsewhere. Explain:

- what the decision means;
- why it matters;
- what will change after the choice;
- a concrete example when it helps.

Use common words and short sentences. Put one idea in each sentence. Define every necessary technical term or acronym immediately.

Speak to the user as a capable person who is new to the subject. Be simple without being childish, insulting, sarcastic, or patronizing. Never imply that the answer should be obvious.

## 4. Ask exactly one question

Use the `ask` tool with exactly one question and `multi: false`.

Provide two to five real options. Each option must have:

- a short label;
- a simple explanation of what it means;
- its main benefit;
- its main downside;
- when it is the better choice;
- the practical result of choosing it.

Keep sentences short. Explain technical words when they are necessary. Do not create fake choices when only one answer is valid; explain the constraint instead.

## 5. Recommend one option

Mark exactly one option as recommended.

Before asking, explain the recommendation in simple language:

- why it fits the known goal;
- what the user gains by choosing it;
- what the user gives up by choosing it;
- why it is better than the main alternative in this situation;
- when the alternative would be better instead.

Example:

> I recommend **A** because it is simpler and easier to change. It is better than **B** when speed and low maintenance matter most. Choose **B** instead if you need its extra control now.

Be direct, but keep the choice with the user.

## 6. Continue one answer at a time

Wait for the answer. Use it to update the decision tree, then ask the next single question. Do not batch independent questions into one turn.

If the user gives a custom answer, restate it briefly and use it as the settled decision. If the answer exposes a missing fact, research that fact before asking the next question.

## 7. Finish clearly

Stop when no material decision remains silently assumed. Summarize:

- the decisions made;
- the main reasons;
- important non-goals or rejected options;
- anything still uncertain.

Ask the user to confirm the shared understanding. Do not create files, change code, or execute the plan until the user confirms or explicitly asks you to proceed.
