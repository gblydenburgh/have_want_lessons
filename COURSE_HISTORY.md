# Course History and Coverage Audit

This file records what was actually covered during the Ansible Resource Module course, where the course intentionally expanded beyond the original syllabus, and which original-plan items still need to be revisited.

It complements `COURSE_PROMPT.md`:

- `COURSE_PROMPT.md` is the authoritative course plan and current handoff prompt.
- `COURSE_HISTORY.md` records execution history, deviations, supplements, and revisit items.

Do not remove previously covered material from this history simply because a later implementation changes.

## Audit date: 2026-09-14

The chat history through Lesson 4 was reviewed against the original course plan.

## Lesson 1 — Discover differences between WANT and HAVE

### Original-plan material covered

The core Lesson 1 plan was completed.

Covered:

- resource identity using `vlan_id`,
- indexing lists of dictionaries by resource identity,
- dictionary lookup,
- set operations for common / WANT-only / HAVE-only resources,
- same resource / same value,
- same resource / changed value,
- resource only in WANT,
- resource only in HAVE,
- property only in WANT,
- property only in HAVE,
- attribute comparison without yet assigning state semantics.

The user wrote substantial portions of the code instead of receiving the finished solution up front, which matched the original interactive-teaching requirement.

### Supplemental material added during Lesson 1

The course introduced an explicit **observation-before-policy** distinction:

```text
First describe what is different.
Only later decide what that difference means under a state.
```

`diff_vlan_name_states()` was retained as learning/reference scaffolding even after the primary reconciliation pipeline moved beyond it.

This was a useful clarification rather than a change to the Lesson 1 objective.

### Original-plan item to revisit

The global teaching sequence says each lesson should eventually **add tests**.

Lesson 1 did not receive a distinct test exercise at the time. Its logic was manually inspected and exercised, but no isolated test function or formal test cases were added.

Revisit with a very small retrospective test set; do not turn this into the full Lesson 11 testing lesson.

## Lesson 2 — State semantics

### Original-plan material covered

The core Lesson 2 plan was completed in ordinary Python before introducing Ansible framework internals.

Covered:

- `merged`,
- `replaced`,
- `overridden`,
- `deleted`,
- absence under `merged` meaning preserve unmanaged/unspecified existing value,
- absence inside a selected resource under `replaced` meaning managed property removal,
- HAVE-only managed configuration under `overridden`,
- targeted absence under `deleted`.

Implemented state builders:

```python
build_merged_state()
build_replaced_state()
build_overridden_state()
build_deleted_state()
```

The course also verified the effective desired state produced for the representative VLAN data.

### Supplemental material added during Lesson 2

Additional concepts covered beyond the minimal original outline:

- shallow copy versus `copy.deepcopy()`,
- resource ownership boundaries,
- the simplified resource owns VLAN `name` but not VLAN existence,
- therefore removal means `no name`, not `no vlan <id>`,
- `delete_want` is only a separate exercise fixture, not a different Ansible input type,
- deleting a nonexistent target must not manufacture a fake resource,
- the guard:

```python
if vlan_id in deleted:
```

- deterministic ordering of returned dictionaries.

These additions clarified state semantics and should be preserved.

### Original-plan item to revisit

As with Lesson 1, no distinct test exercise was added after the state builders were completed.

Manual output checking occurred, but the teaching-style requirement to add tests was not explicitly completed.

Revisit with a minimal retrospective test matrix covering the expected effective state for each of the four states.

Do not introduce pytest yet unless the course has reached the formal testing lesson.

## Lesson 3 — Render decisions into Cisco IOS commands

### Original-plan material covered

The core Lesson 3 plan was completed.

Covered:

- separation between deciding a change and rendering the CLI,
- hierarchical IOS parent context,
- `vlan <id>` as parent context,
- `name <value>` for add/change,
- `no name` for removal,
- using the same renderer regardless of which state produced the effective desired state.

Implemented:

```python
build_vlan_name_changes()
render_vlan_name_commands()
```

The four state builders were all passed through the same comparison/change and rendering pipeline.

### Supplemental material added during Lesson 3

The lesson first used human-readable descriptive change strings and then intentionally moved to a machine-consumable change representation.

The final representation used `before` / `after` data so the renderer did not need to know about HAVE, WANT, or state semantics.

Additional concepts covered:

- missing dictionary key versus `None`,
- use of `object()` as a unique sentinel,
- why the renderer should only consume changes,
- deterministic command ordering,
- keeping the renderer independent of reconciliation policy.

These were useful expansions and should remain part of the course history.

### Original-plan item to revisit

Again, the lesson did not receive a distinct isolated test exercise after the renderer was completed.

Manual verification of rendered commands occurred, but the original teaching sequence included an explicit test step.

Revisit with minimal tests for:

- name change,
- name removal,
- name addition,
- no-op producing no command.

Keep these retrospective tests small; the full current-Ansible testing practices still belong in Lesson 11.

## Lesson 4 — Parsing and normalization

### Original-plan material already covered

Substantial portions of Lesson 4 are complete.

Covered:

- native configuration to structured data,
- block-oriented parsing,
- ignoring unrelated configuration,
- resource identity as the gatekeeper for whether a block belongs to the resource,
- parsing VLAN ID,
- normalization from CLI string to Python integer,
- omission of `name` when the command is absent,
- parsing configured VLAN names,
- distinguishing unrelated configuration from malformed resource-looking configuration.

Implemented:

```python
parse_vlan_config()
```

The current parser normalizes:

```text
"10" -> 10
```

and:

```text
vlan 60
```

into:

```python
{"vlan_id": 60}
```

rather than manufacturing a `name` value.

### Course correction during Lesson 4

An attempted normalization exercise using VLAN `state` / `shutdown` was proposed, but the user's actual Cisco output showed that the chosen configuration source did not expose those values in the assumed way.

That exercise was abandoned rather than being treated as valid device behavior.

The course then stayed grounded in the configuration source:

```text
show running-config all | section ^vlan
```

This is recorded as a course correction, not retained lesson content.

### Supplemental material added during Lesson 4

The parser work expanded into malformed-input validation and exception behavior.

Covered:

- broad regex extraction followed by semantic validation in Python,
- `vlan BAD`,
- `vlan 33BAD`,
- numeric but out-of-range VLAN IDs,
- `try` / `except`,
- the difference between catching and printing versus re-raising,
- exception chaining with `raise ... from e`,
- separating raw `vlan_id_string` from normalized integer `vlan_id`,
- fail-fast parser behavior.

A supplemental manual parser-testing exercise was then added and separately recorded in `COURSE_PROMPT.md`.

### Original-plan material still to revisit before Lesson 4 is complete

The original Lesson 4 plan explicitly says to show how **bad normalization creates false diffs and destroys idempotency**.

This has been explained conceptually but has not yet been demonstrated end-to-end with a deliberate normalization bug.

Before marking Lesson 4 complete, add a small exercise that deliberately leaves equivalent data in different representations, then show that the reconciliation engine incorrectly thinks a change is required.

The exercise should make the failure visible as something like:

```text
same real device state
    -> differently normalized structured values
    -> false difference
    -> unnecessary command
    -> second run still wants to change something
```

Then fix the normalization and show the false change disappear.

### Optional original-plan example not yet used

The original Lesson 4 text also gave this example where appropriate:

```text
GigabitEthernet1/0/1
Gi1/0/1
```

The current VLAN-name resource does not naturally contain interface names, so this example was not used.

It is not considered a mandatory missed requirement because the original prompt says "where appropriate."

A short conceptual normalization side exercise may still be useful, but it should not distort the VLAN-name resource merely to force the example into the code.

## Testing requirement audit

The original teaching style says that, after the implementation is understood, tests should be added.

Actual history:

- Lesson 1: core logic manually exercised; no distinct test exercise.
- Lesson 2: state outputs manually exercised; no distinct test exercise.
- Lesson 3: rendered outputs manually exercised; no distinct test exercise.
- Lesson 4: supplemental manual parser testing is now being added.

This does **not** mean Lessons 1–3 need a full pytest suite now.

Before leaving the plain-Python portion of the course, perform a small retrospective testing pass so the original teaching sequence is honored without stealing Lesson 11's purpose.

## Revisit queue before moving beyond Lesson 4 / into Lesson 5

1. Finish Supplemental Exercise 4.3: isolated parser inputs and manual PASS/FAIL behavior.
2. Demonstrate the original Lesson 4 false-diff/idempotency failure caused by bad normalization.
3. Add a minimal retrospective test for Lesson 1 difference classification/indexing behavior.
4. Add a minimal retrospective test matrix for Lesson 2 state builders.
5. Add minimal Lesson 3 change/render tests.
6. Optionally show the `GigabitEthernet1/0/1` versus `Gi1/0/1` normalization idea as a short side example without changing the current VLAN-name resource.
7. Only then mark Lesson 4 and the retrospective gaps complete and proceed to Lesson 5.

## Lessons not yet audited as completed

Lesson 5 and later lessons have not yet been completed, so nothing in those lessons should be treated as skipped yet.

The focused Python classes bridge is intentionally scheduled after Lessons 1–5 and before direct ResourceModule study. The newer requirement to point out class opportunities during code review is supplemental and does not replace that bridge lesson.
