# Course State

This file is the **single mutable source of truth** for where the course currently is.

`COURSE_PROMPT_RESTRUCTURED.md` contains standing teaching instructions and the curriculum.
`COURSE_HISTORY.md` contains completed work, decisions, corrections, source checkpoints, and deviations.
`PROGRESS_EVALUATION.md` contains the candid pre-Lesson-5 skill assessment.

Do not duplicate current lesson state elsewhere unless a temporary handoff explicitly points back here.

<!-- STATE:BEGIN -->

## Current checkpoint

**Current lesson:** Lesson 5 — Idempotency

**First action:** Fetch and inspect the current modular exercise code before teaching or reviewing Lesson 5.

**Current working area:**

```text
modular_ex2/
```

The latest repository activity modularized the previous single-file exercise into:

```text
modular_ex2/excercise2.py
modular_ex2/vlan_parser.py
modular_ex2/vlan_states.py
modular_ex2/vlan_diff.py
modular_ex2/vlan_renderer.py
modular_ex2/vlan_tests.py
```

The root-level `excercise2.py` remains the earlier single-file reference implementation. Do not silently delete or rename it.

If the learner says a different file or tree is now active, update this state block first.

**Latest verified repository HEAD at this checkpoint:**

```text
15b635f1e23b92c1d3c454cc98a57afd9ee6d5b3
```

Do not assume that commit remains current after the learner pushes new work. Re-fetch the active files whenever the learner says code was pushed or updated.

## Lesson 5 acceptance condition

Build the complete procedural idempotency cycle:

```text
gather / obtain native state
    -> parse and normalize
    -> structured HAVE
    -> apply state semantics
    -> calculate changes
    -> render commands
    -> apply or simulate apply
    -> gather again
    -> parse and normalize again
    -> calculate changes again
```

The second pass must prove:

```python
commands == []
```

Do not accept "it should be idempotent" as completion. Encode the expectation and run it.

## Lesson 5 teaching correction

From Lesson 5 onward, tests are written **with the behavior being added**, not as retrospective cleanup.

For each new behavior:

```text
predict expected result
    -> implement the smallest behavior
    -> encode the expectation
    -> run it
    -> diagnose any gap
```

Do not defer the test to the end of the lesson.

Lesson 5 must include at least one deliberately broken second-pass case. The instructor may propose the bug or demonstrate it in a scratch snippet, but must not modify the learner's repository code unless explicitly asked. Prefer a normalization/canonicalization or mutation failure that is relevant to real desired-state automation; clearly label synthetic device behavior when used.

## Current skill emphasis

Use `PROGRESS_EVALUATION.md` as the baseline.

Current strengths to exploit:

- strong network/domain reasoning,
- solid simplified desired-state reasoning,
- intermediate procedural Python,
- good debugging skepticism and willingness to inspect mechanics.

Current gaps to train deliberately:

- software decomposition and data modeling,
- testing discipline beyond manual harnesses,
- OOP/classes and inheritance,
- direct ResourceModule/NetworkTemplate/Facts implementation knowledge,
- production collection testing and contribution workflow.

Do not re-teach beginner Python or beginner Ansible.

## Immediate post-Lesson-5 path

After Lesson 5:

1. widen the plain-Python resource beyond one managed scalar attribute,
2. introduce basic pytest and stronger data contracts while keeping tests close to new behavior,
3. complete the focused OOP/inheritance bridge,
4. then map the manual engine onto current Ansible framework source.

The exact curriculum is in `COURSE_PROMPT_RESTRUCTURED.md`.

<!-- STATE:END -->
