# Lesson 5 Handoff

Continue the Ansible Resource Module course from the `gblydenburgh/have_want_lessons` GitHub repository.

Read `COURSE_PROMPT.md` first; it remains the authoritative course plan. Use `COURSE_HISTORY.md` for execution history and `PROGRESS_EVALUATION.md` for the pre-Lesson 5 skills assessment.

## Working code for Lesson 5

Use the root file:

```text
excercise2.py
```

Fetch the current root `excercise2.py` from GitHub before teaching or reviewing code.

Ignore `modular_ex2/` for the course. That directory was an independent experiment to see what a responsibility-based file split would look like. It is not the Lesson 5 implementation and should not change the teaching sequence.

Keep the Lesson 5 implementation in the single root `excercise2.py` file. The single-file layout is intentional at this stage so the complete reconciliation pipeline remains visible and easy to trace while idempotency is being learned.

The one intentional supporting file for Lesson 5 is:

```text
lesson5_inputs.py
```

That file contains **data fixtures only** for controlled idempotency/failure scenarios. It is not a modularization of the implementation. Do not move parser, state, diff, renderer, or orchestration logic out of `excercise2.py` during Lesson 5.

Do **not** introduce modularization, classes, pytest, or Ansible framework abstractions during Lesson 5 unless they are required to explain a specific problem.

Lessons 1–4 and the retrospective cleanup are complete. Do not repeat them unless needed to resolve a specific misunderstanding.

## Lesson 5 — Idempotency

Teach idempotency as the reason the reconciliation pipeline must be correct, not merely as another Ansible feature.

Tie it explicitly to the operational habit I am trying to move beyond:

```text
configure
→ inspect afterward
→ decide whether it looks right
```

versus the desired automation model:

```text
observe current state
→ calculate only the required changes
→ apply them
→ observe current state again
→ prove that no work remains
```

Use the existing plain-Python pipeline to make the full cycle explicit:

```text
gather
→ parse/normalize
→ apply state semantics
→ compare
→ render
→ apply/simulate apply
→ gather again
→ parse/normalize again
→ apply the same state semantics
→ compare again
→ render again
```

The acceptance condition on the second pass is:

```python
commands == []
```

Do not merely state that the process is idempotent. Make the code prove it.

## Teaching workflow for Lesson 5

Do not repeat the earlier pattern of writing several pieces of behavior and adding tests afterward.

For each new behavior:

1. State the expected result.
2. Ask me to predict what should happen where useful.
3. Have me implement the smallest required change.
4. Encode the expectation immediately using the existing simple/manual test approach.
5. Run or inspect the result.
6. Explain any discrepancy before continuing.

Default interaction pattern:

```text
predict
→ implement
→ test
→ explain
```

If my prediction and reasoning are correct, confirm that briefly and continue. Do not add unnecessary explanatory turns merely to follow a rigid lesson script.

Keep tests simple for now. Lesson 5 is about the habit of proving behavior as it is built, not about learning pytest syntax. Formal pytest and Ansible collection testing remain later topics.

Optional learner signals if I use them:

```text
HINT    = give a small hint only
NUDGE   = give a stronger directional hint without solving it
ANSWER  = show/explain the answer
NEXT    = move on because I understand the current point
```

## Controlled idempotency failures

First prove the normal path is idempotent. Do not begin with a broken case.

After a clean second pass has demonstrated:

```python
commands == []
```

use `lesson5_inputs.py` to introduce controlled failures through **input/observed state**, while leaving the working reconciliation implementation unchanged initially.

The file currently provides these scenario categories:

1. **Converged control state** — the second observation reflects the complete intended merged state and should produce no commands.
2. **Partial apply** — one intended change is absent from the second observation. A second-pass command is legitimate because the device is not yet converged.
3. **Stale second gather** — the second observation still looks like the original pre-change state. The learner should diagnose the gather/observation boundary rather than blaming the comparator.
4. **Normalization-contract violation** — the logical state is converged, but one internal resource identity uses a string where the normalized contract requires an integer. This should produce a false diff and must be traced back to the normalization boundary.

These are synthetic teaching inputs. Do not present them as claims about actual Cisco canonicalization behavior unless that behavior has been verified separately from current device/documentation/source evidence.

Prefer these data-driven failures before deliberately corrupting implementation code.

The learner should diagnose each failure through the pipeline rather than jumping directly to the fixture or bad value:

```text
input/device state
→ parse/normalize
→ effective desired state
→ comparison
→ rendered commands
→ simulated applied state
→ re-gathered state
→ second comparison
```

The key distinction to teach is:

```text
non-empty second pass because real work remains
versus
non-empty second pass because equivalent state was represented incorrectly
```

An implementation bug may be introduced later only if it teaches a different failure mode, such as accidental mutation of HAVE. Do not modify `excercise2.py` directly unless I explicitly ask you to.

## Code review protocol

When I push code:

1. Fetch the latest root `excercise2.py` from GitHub.
2. Review my submitted procedural code first on its own terms for correctness, reconciliation behavior, Python behavior, naming/signatures, typing, and readability.
3. Only after that, perform the separate OOP opportunity review.
4. If no meaningful class opportunity exists, say so explicitly.
5. Do not modify my working code unless I explicitly ask you to.

A design that is valid but different from the instructor's stylistic preference should not be rewritten merely to match the instructor's preferred style. Adapt to my design unless it is incorrect, misleading, or creates a concrete maintainability problem.

## What does not belong in Lesson 5

Do not move ahead into:

- modularizing the program into multiple implementation files,
- `TypedDict` or broader data-model refactoring,
- pytest,
- classes or inheritance,
- `ResourceModule`,
- `NetworkTemplate`,
- argspec,
- formal Ansible collection testing.

Those are later concerns.

## After Lesson 5

Once the single-file reconciliation engine has proven idempotency end-to-end, the next architectural step should be to revisit the now-understood responsibilities and refactor them by responsibility where useful, for example parsing, state transformation/reconciliation, rendering, fixtures/tests, and orchestration.

That refactor should be taught as procedural software decomposition first: separation of concerns, cohesion, coupling, module boundaries, imports, and dependency direction.

Only after those responsibilities are understood as modules should the focused Python OOP/inheritance bridge begin. Then continue into `ResourceModule` and the Ansible framework.
