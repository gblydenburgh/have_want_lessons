# Progress Evaluation — Pre-Lesson 5 Checkpoint

Date: 2026-09-15

Scope: This evaluation covers work completed through Lessons 1–4, the supplemental parser/normalization exercises, and the retrospective manual tests completed before Lesson 5. It does **not** assume competence in material that has not yet been taught.

## Bottom line

The current evidence supports this assessment:

- **Network automation/domain reasoning:** strong.
- **Desired-state reconciliation concepts:** solid for the simplified resource used so far.
- **Procedural Python:** intermediate and usable.
- **Python software design:** intermediate at best; still somewhat script-oriented.
- **Type-system use:** developing.
- **Testing discipline:** developing; the basic mechanics are understood, but formal test design has not yet been taught.
- **Object-oriented Python:** weak / beginner, as previously stated by the learner; not yet sufficiently exercised to revise that rating.
- **Ansible ResourceModule internals:** beginner-to-developing. Operational familiarity with network resource modules is high, but implementation knowledge is still incomplete because Lessons 5–12 have not happened.
- **Production resource-module development readiness:** not yet demonstrated.

The important distinction is that the learner is no longer merely consuming desired-state abstractions. He can now explain and implement a small reconciliation pipeline in plain Python. That is meaningful progress. It is not yet equivalent to being able to design, implement, and test a production Ansible network resource module independently.

## What is going well

### 1. Reconciliation reasoning is stronger than the starting point

The learner now correctly separates:

```text
raw/native configuration
    -> parse and normalize
    -> structured HAVE
    -> apply state semantics to WANT/HAVE
    -> calculate changes
    -> render CLI
```

This separation matters. Earlier experience was primarily from the consumer side of resource modules. The code now reflects distinct stages rather than treating the problem as a running-config text diff.

The state semantics for the simplified VLAN-name resource are understood well enough to implement independent builders for:

- `merged`,
- `replaced`,
- `overridden`,
- `deleted`.

The learner also understands that ownership changes semantics. In this exercise, the resource owns VLAN `name`, not VLAN existence, so removal means `no name` rather than `no vlan <id>`.

That is one of the more important conceptual gains in the course so far.

### 2. The learner catches bad assumptions instead of accepting them

This has been consistently useful.

A proposed VLAN normalization exercise assumed device data that the selected Cisco configuration source did not actually expose. The learner checked the real behavior and challenged the assumption. The exercise was then discarded.

This is a strong habit for infrastructure automation. Device behavior, collection behavior, and framework behavior should be verified rather than inferred from a convenient teaching example.

The learner has also challenged explanations when wording implied behavior that was not actually established. This reduces the risk of memorizing an incorrect mental model.

### 3. Normalization is understood as a correctness boundary, not formatting cleanup

The learner understood the significance of:

```python
"10" != 10
```

and followed the resulting failure through the comparator.

The intentionally malformed structure:

```python
{"10": {"vlan_id": "10", "name": "USERS"}}
```

was correctly recognized as logically different from an integer-keyed effective state even though both represent the same real VLAN to a human.

The learner also independently noticed that allowing mixed `str` and `int` keys through the state-building path can create an additional Python failure during sorting. That was not merely repeating an explanation; it was an independent observation about program behavior.

This is evidence of useful debugging instincts.

### 4. Exception handling understanding improved materially

The parser exercise exposed several mechanics that were initially not fully understood:

- catching versus propagating an exception,
- capturing an exception object with `as e`,
- comparing `str(e)` rather than comparing an exception object directly to a string,
- using `raise ... from e`,
- distinguishing the outer domain-specific exception from `e.__cause__`.

The learner worked through those mechanics rather than simply copying the final form.

That is preferable to memorizing a `try`/`except` pattern without understanding control flow.

### 5. Test boundaries are starting to make sense

The learner initially asked whether state, change, and renderer tests should all live in the same state-test function. After discussion, the tests were separated by responsibility:

```text
state tests
    HAVE + WANT -> effective state

change tests
    HAVE + effective state -> change structure

render tests
    change structure -> CLI
```

That is the correct direction.

The final retrospective tests exercise:

- state builders for all four action states,
- change of an existing value,
- addition of a value,
- removal of a value,
- rendering `name VALUE`,
- rendering `no name`,
- parser success and parser validation errors,
- normalization-driven false diff versus normalized no diff.

The test code is still manual and repetitive, but that is intentional at this stage of the course.

## Where the learner is weaker

### 1. The Python is functional, but still visibly script-oriented

The code works, but organization is not yet at the level expected of a mature reusable library.

Examples include:

- substantial reliance on `dict[str, Any]`,
- repeated setup and expected-data structures across manual tests,
- test helpers and test cases living in the same large script as implementation code,
- some inconsistent naming and occasional typographical mistakes,
- no stronger domain types for resource data,
- no explicit abstraction for the resource as an object or component.

None of this is a serious problem for the current teaching exercise. It would become a problem if the same style were carried directly into production module_utils code without refactoring.

### 2. Type hints are being used, but not yet exploited deeply

Adding:

```python
T = TypeVar("T")
```

to the generic result-comparison helper was appropriate and understood after explanation.

However, most resource structures are still typed as:

```python
dict[str, Any]
```

which gives a static type checker little information about required keys, optional keys, or valid value types.

That is acceptable for now, but the learner should not mistake the presence of annotations for strong type modeling.

Later improvements could include `TypedDict`, dataclasses where appropriate, or framework-provided argument/data models. Those should be introduced only when they support the resource-module lessons rather than as unrelated Python cleanup.

### 3. OOP remains a genuine gap

There is not enough evidence to soften the learner's self-assessment that classes are weak.

So far, the course has intentionally avoided forcing the procedural code into classes. That means the learner has not yet demonstrated comfort with:

- instance state,
- `self`,
- constructors,
- inheritance,
- method resolution,
- `super()`,
- inherited versus overridden methods,
- tracing where an attribute is initialized.

This is not a criticism of work that was never assigned. It is simply an unresolved competency gap, and it is directly relevant because Ansible's ResourceModule architecture is class-heavy.

The class bridge after Lesson 5 remains necessary.

### 4. The reconciliation implementation is still deliberately narrow

The current resource manages one property: VLAN `name`.

That simplicity is useful for learning, but it means the learner has not yet had to handle several problems that make real resource modules harder:

- multiple managed properties on the same resource,
- nested data,
- list-valued attributes,
- ordering-sensitive structures,
- multiple CLI forms representing equivalent state,
- more complex removal semantics,
- resource-specific default handling,
- partial versus whole-resource replacement rules,
- parent/child resource relationships.

Success with this VLAN-name exercise should therefore be interpreted as mastery of the basic pattern, not proof that arbitrary network resources will be easy.

### 5. The parser is educational, not production-grade

The current parser's block splitting and regex logic are suitable for the exercise, but they are intentionally simple.

For example, splitting configuration on `!` is not a universal Cisco parser strategy. The parser also assumes a narrow syntax and does not attempt to model all legal VLAN configuration variations.

The learner understands the intended normalization boundary, which is the important lesson. Production parsing robustness still needs to be learned through `NetworkTemplate` and real collection examples.

### 6. Formal testing competence has not been demonstrated yet

The manual PASS/FAIL harness is useful because it exposes the mechanics directly.

It does **not** demonstrate proficiency with:

- pytest fixtures,
- parametrization,
- collection unit-test conventions,
- mock connections,
- command assertions,
- parsed/rendered/gathered state tests,
- idempotency tests in the actual Ansible module architecture,
- regression tests for module bugs.

That remains Lesson 11 material.

A small remaining detail is that the renderer does not yet have a dedicated direct test of:

```python
render_vlan_name_commands({}) == []
```

The comparator's normalized no-diff behavior has been tested. The complete empty-command path will naturally become central in Lesson 5, where idempotency requires the second pass to produce no commands.

## Learning behavior

The learner's strongest learning behavior is skepticism combined with willingness to inspect mechanics.

Useful examples so far:

- questioning state semantics instead of accepting labels,
- checking real Cisco output against proposed examples,
- noticing the mixed-key sorting problem,
- asking what `TypeVar` actually accomplishes rather than accepting the annotation decoratively,
- examining exception chaining rather than treating the error message as magic,
- asking whether normalization belongs in the parser or indexer.

This is more valuable than fast completion of exercises.

The main behavioral weakness is that code is sometimes pushed with small naming/typing/formatting defects that would be easy to catch with a quick local review. The `run_render_rest()` typo is a representative example. It did not break execution because the call used the same typo, but it shows that correctness checks are currently more focused on logic than polish.

For production contribution work, the learner will need to add a final pass specifically for naming, interfaces, typing, and test completeness rather than stopping once behavior is correct.

## Current competency by area

| Area | Current assessment | Basis |
| --- | --- | --- |
| Network engineering context | Strong | Existing professional experience and accurate device-behavior challenges |
| Ansible playbook/resource-module usage | Strong user-level | Existing operational experience |
| Desired-state reasoning | Solid | Correct HAVE/WANT/state transformations and ownership reasoning |
| Procedural Python | Intermediate | Functions, dictionaries, loops, exceptions, regex, copying, comparison logic |
| Debugging Python behavior | Intermediate to strong | Independent observations and exception/normalization tracing |
| Type hints | Developing | Uses annotations and understands basic `TypeVar`; models remain broad |
| Software design/modularity | Developing | Pipeline separation is good; overall script organization remains basic |
| Testing | Developing | Manual isolated tests understood; formal framework testing not yet covered |
| OOP/classes | Beginner / weak | Explicit known gap; bridge lesson not yet completed |
| ResourceModule internals | Beginner to developing | Mental model forming; direct framework implementation lessons not yet done |
| NetworkTemplate/Facts/argspec | Not yet demonstrated | Scheduled for later lessons |
| Production module authoring | Not yet demonstrated | Too much of the framework/testing path remains |

## Progress against the actual course goal

The course goal is not merely to write a VLAN script. It is to understand enough of the machinery to develop or modify an Ansible network resource module.

At this checkpoint, the learner has built the conceptual lower half manually:

```text
parse/normalize
    -> structured HAVE
    -> state semantics
    -> comparison
    -> change representation
    -> CLI rendering
```

The missing major pieces are:

```text
full idempotency cycle
    -> OOP/inheritance bridge
    -> ResourceModule
    -> NetworkTemplate
    -> Facts
    -> argspec/registration/builder files
    -> complete module assembly
    -> formal tests
    -> realistic feature work
```

So the learner is approximately at the point where the manual mechanics are becoming credible, but the Ansible framework mapping has barely started.

## Recommendation for the next phase

Do not accelerate because Lessons 1–4 went reasonably well.

Lesson 5 should force the entire pipeline to prove idempotency rather than merely discussing it. The key acceptance condition should remain:

```python
commands == []
```

on the second pass.

After that, the class bridge should be taken seriously. The temptation will be to recognize the functional equivalents and assume the class architecture is understood. That should not be accepted without exercises that require tracing `self`, inherited methods, constructor chains, and ownership of attributes.

Only after that should `ResourceModule` internals be treated as the same concepts in framework form.

## Overall assessment

Progress is good and technically meaningful, but still early relative to the final objective.

The strongest evidence is that the learner can now reason about a small desired-state reconciliation engine rather than merely use one. The weakest area remains class-based Python, followed by lack of experience with the actual ResourceModule/NetworkTemplate/Facts implementation and formal tests.

There is no basis yet for saying the learner can independently author a production Ansible network resource module. There **is** a reasonable basis for saying the learner has built the prerequisite reconciliation model needed to make the upcoming framework code understandable rather than opaque.
