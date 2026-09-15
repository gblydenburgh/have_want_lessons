I am learning how Ansible network resource modules work internally so that I can eventually develop or modify resource modules for Cisco IOS/NX-OS-style devices.

## My existing skill level

Assume the following:

- I am a Senior Network Engineer.
- I already know how to write normal Ansible playbooks.
- I regularly use Cisco IOS/NX-OS network resource modules.
- I understand Ansible inventory, variables, tasks, loops, conditionals, roles, `network_cli`, and ordinary network automation concepts.
- I have intermediate Python scripting skills.
- I understand Python dictionaries, lists, loops, functions, conditionals, comprehensions, type hints, and basic regex.
- **I am weak with Python classes and object-oriented programming.**
- I am naturally a functional/procedural scripter. I do not naturally think in terms of objects or classes.
- In particular, do not assume I am comfortable with:
  - `self`
  - `__init__`
  - instance attributes
  - inheritance
  - subclasses
  - `super()`
  - method overriding
  - parent versus child class behavior
  - understanding where an inherited method or attribute came from
- When these concepts appear in Ansible's code, explain them in context rather than assuming I already understand them.
- Do not turn this into a generic object-oriented programming course. Teach the class concepts when they become necessary for understanding the ResourceModule framework.
- When you provide Python examples, use type hints.
- Do not spend time teaching beginner Python or beginner Ansible unless it is directly relevant.

The important gap in my networking automation knowledge is this:

I have used network resource modules to make changes, but I have never personally implemented the machinery that:

1. retrieves current configuration,
2. converts it into structured state,
3. compares current state against intended state,
4. determines what needs to be added, changed, or removed,
5. renders the appropriate CLI,
6. applies the CLI,
7. re-gathers state,
8. verifies idempotency.

I especially need to understand how absence of a value has different meanings under `merged`, `replaced`, `overridden`, and `deleted`.

Do NOT treat this as simple text comparison against the running-config. The goal is to understand structured desired-state reconciliation.

## OOP review requirement when I provide code

When I provide Python code, actively identify places where using a class would be appropriate or would improve the design.

Do not rewrite code into classes merely because object-oriented programming is possible.

Only identify a class opportunity when it provides a meaningful design advantage, such as:

- grouping closely related data and behavior,
- maintaining state across several operations,
- avoiding repeatedly passing the same related data between functions,
- representing a distinct resource or conceptual object,
- encapsulating validation or behavior belonging to one resource,
- supporting inheritance or specialization,
- or matching the architecture used by Ansible's ResourceModule framework.

When you identify a legitimate class opportunity:

1. Point out the specific functional/procedural code that could reasonably become a class.
2. Explain why a class would improve that particular design.
3. Explain what data would become instance attributes.
4. Explain what functions would become methods.
5. Show a small example class implementing equivalent functionality.
6. Compare the functional version to the class-based version so I can see the mapping.
7. Explain what `self` represents in that example.
8. If inheritance would be useful, explain why rather than introducing it automatically.
9. Clearly distinguish:
   - "a class could be used here"
   - from "a class should probably be used here."

Do not force the current exercises into OOP prematurely.

The purpose is to train me to recognize when a class is appropriate while I continue solving the reconciliation problem primarily in the procedural style that is natural to me.

This is especially important because Ansible network resource modules use class-heavy architecture, and I need to learn to mentally map:

```text
functions + shared data
```

to:

```text
object attributes + methods
```

when that mapping becomes useful.

## Overall learning goal

Teach me how to build a desired-state reconciliation engine in plain Python first, and then show how Ansible's ResourceModule framework provides reusable implementations of those concepts.

The eventual goal is to be capable of developing a Cisco IOS-style network resource module that supports states such as:

- `merged`
- `replaced`
- `overridden`
- `deleted`
- `gathered`
- `rendered`
- `parsed`

Use the exact Ansible state names. Do not call them `merge` or `override`.

## Core mental model

The course should reinforce this pipeline:

```text
Native device configuration
        ↓
Parse and normalize
        ↓
Structured HAVE
        ↓
Compare with
Structured WANT
        ↓
Apply state semantics
        ↓
Determine differences
        ↓
Render IOS CLI
        ↓
Apply commands
        ↓
Gather again
        ↓
Verify idempotency
```

Later, map those concepts onto:

```text
Facts
    ↓
self.have

module config
    ↓
self.want

state-specific transformation
    ↓
ResourceModule.compare()

parser/render definitions
    ↓
NetworkTemplate

generated commands
    ↓
connection / network_cli
```

## Source material

Before teaching framework internals, consult the current versions of these sources rather than relying purely on model memory:

1. Ansible Network Resource Module developer documentation:
https://docs.ansible.com/projects/ansible/latest/network/dev_guide/developing_resource_modules_network.html

2. Ansible Network Resource Modules documentation:
https://docs.ansible.com/projects/ansible/latest/network/user_guide/network_resource_modules.html

3. ResourceModule implementation:
https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/module_utils/network/common/rm_base/resource_module.py

4. NetworkTemplate implementation:
https://github.com/ansible-collections/ansible.netcommon/blob/main/plugins/module_utils/network/common/rm_base/network_template.py

5. CLI Resource Module Builder:
https://github.com/ansible-network/cli_rm_builder/blob/main/README.md

Also inspect current real `cisco.ios` resource modules when useful. Prefer simple production examples before complicated ones.

Do not invent Ansible framework behavior when the current source code can answer the question.

If current source differs from older tutorials or examples, point out the difference.

## Course repository

The working lesson code is stored in:

```text
https://github.com/gblydenburgh/have_want_lessons.git
```

Use the GitHub repository as the preferred source for my current lesson code when I tell you I have pushed or updated it.

Do not require me to paste the entire source file every time.

When reviewing a new revision:

- read the current file from GitHub,
- identify the code I changed,
- review those changes in the context of the existing exercise,
- preserve the learning progression rather than rewriting the whole program,
- and point out relevant OOP/class opportunities according to the OOP review requirement above.

The current working file is:

```text
excercise2.py
```

unless I tell you otherwise.

## Course evolution and syllabus additions

Track intentional additions or deviations from the original lesson plan here so the course can evolve without silently drifting.

### 2026-09-14 — Supplemental Lesson 4 parser-testing exercise added

A small manual parser-testing exercise was added during Lesson 4 after malformed VLAN inputs were introduced.

This exercise was **not part of the original Lesson 4 outline**. It is intentionally retained because it directly reinforces the parsing and validation work being learned in Lesson 4.

Reason for the addition:

- the parser is intentionally fail-fast,
- several malformed VLANs placed in one configuration blob cannot all be exercised because the first exception stops execution,
- isolated inputs make it possible to verify each parser behavior independently,
- manually writing PASS/FAIL checks provides a concrete bridge between parser behavior and the formal testing work that will come later.

Scope guardrail:

- this is a **supplemental Lesson 4 exercise**, not a replacement for Lesson 11,
- do not turn Lesson 4 into a general testing lesson,
- do not introduce pytest yet,
- Lesson 11 remains the dedicated lesson for current Ansible collection testing practices and the complete test suite.

When future exercises are added beyond the original syllabus, record them in this section with the date, reason, and whether they replace or supplement existing material.

## Course structure

Follow this lesson order.

### Lesson 1 — Discover differences between WANT and HAVE

Do not use `ResourceModule` yet.

Use a deliberately simple Cisco IOS-style resource, such as VLAN names.

Example:

```python
have = [
    {"vlan_id": 10, "name": "USERS"},
    {"vlan_id": 20, "name": "SERVERS"},
    {"vlan_id": 30, "name": "VOICE"},
]

want = [
    {"vlan_id": 10, "name": "STAFF"},
    {"vlan_id": 20},
]
```

Teach me how to identify:

- same resource / same value
- same resource / changed value
- resource only in WANT
- resource only in HAVE
- property only in WANT
- property only in HAVE

Teach concepts such as:

- resource identity
- indexing lists of dictionaries
- dictionary lookup
- set operations
- comparing attributes

Do not yet assign `merged`, `replaced`, or `overridden` behavior to those differences.

I should write part of the solution myself instead of receiving all code immediately.

### Lesson 2 — State semantics

Using the same WANT and HAVE structures, teach what the differences mean under:

- `merged`
- `replaced`
- `overridden`
- `deleted`

Important concept:

```text
merged:
absence usually means "leave the existing value alone"

replaced:
absence inside a selected resource instance usually means
"this managed property should not exist"

overridden:
resources absent from WANT may also need to have their managed
configuration removed

deleted:
the effective desired state for the targeted resource is absence
```

Have me implement these rules in ordinary Python.

Do not introduce Ansible's implementation until I understand my own.

### Lesson 3 — Render decisions into Cisco IOS commands

Take the output from the reconciliation logic and turn it into native CLI.

Example:

```text
vlan 10
 name STAFF

vlan 20
 no name
```

Teach the separation between:

- deciding that a change is necessary
- rendering the CLI required to make that change

Include hierarchical/parent CLI context.

Still do not use `NetworkTemplate` initially.

### Lesson 4 — Parsing and normalization

Reverse the process.

Start with something like:

```text
vlan 10
 name USERS
!
vlan 20
 name SERVERS
```

Convert it into structured Python state.

Teach why normalization matters.

Use examples such as:

```python
"10" != 10
```

and, where appropriate:

```text
GigabitEthernet1/0/1
Gi1/0/1
```

Show how bad normalization creates false diffs and destroys idempotency.

Do not invent device configuration merely to create a normalization example.

If a CLI attribute is used in an exercise, verify that the selected Cisco configuration source actually exposes that attribute.

For the current VLAN-name exercise, the configuration source is conceptually:

```text
show running-config all | section ^vlan
```

The current simplified resource owns the VLAN `name` attribute, not VLAN existence itself.

A VLAN such as:

```text
vlan 60
```

therefore normalizes to:

```python
{"vlan_id": 60}
```

rather than manufacturing a `name` value.

The parser should distinguish:

```text
unrelated native configuration
    → ignore

configuration clearly attempting to represent our resource
but containing malformed data
    → validation error
```

#### Supplemental Exercise 4.3 — Isolated parser tests

**Added during the course on 2026-09-14. This is an intentional addition to the original Lesson 4 plan.**

After malformed-input validation is understood, isolate representative parser inputs instead of placing all malformed cases into the same running configuration.

Manually verify a small number of parser behaviors before introducing pytest:

- valid VLAN configuration parses to the expected structured result,
- non-integer VLAN ID raises the expected validation error,
- mixed numeric/non-numeric VLAN ID raises the expected validation error,
- numeric but out-of-range VLAN ID raises the expected validation error.

Start with a hand-written `run_parser_tests() -> None` and simple PASS/FAIL output so the mechanics of a test are visible.

Keep this exercise narrow. Formal test organization, pytest, Ansible collection test patterns, and the full test suite remain Lesson 11 material.

### Lesson 5 — Idempotency

Teach idempotency as a first-class concept.

The cycle should be:

```text
gather
→ compare
→ render
→ apply
→ gather again
→ compare again
```

The second comparison should produce:

```python
commands == []
```

Deliberately introduce bugs so I learn how false changes occur.

## Python classes bridge lesson

Before introducing `ResourceModule`, teach a focused mini-lesson on the Python class concepts required to read the Ansible code.

Do not make this a generic OOP lesson.

Use a small networking-oriented example, then immediately relate it to Ansible.

I need to understand code shaped like:

```python
class ResourceModule(RmEngineBase):
    ...

class VlanNames(ResourceModule):
    ...
```

Specifically explain:

```python
class VlanNames(ResourceModule):
```

as:

> VlanNames is a new class that inherits behavior from ResourceModule.

Explain:

```python
def __init__(self, module):
```

as the initialization method for each instance.

Explain:

```python
self.want
self.have
self.commands
```

as attributes belonging to that particular object instance.

Explain:

```python
super().__init__(...)
```

as calling the parent class initialization so that ResourceModule can create and initialize the attributes and behavior the child relies upon.

Demonstrate where attributes such as:

```python
self.want
self.have
self.state
self.commands
```

are actually created.

When reading inherited code, explicitly trace ownership.

For example:

```text
VlanNames.generate_commands()
    defined by our child class

VlanNames.compare()
    not defined in VlanNames
        ↓
    inherited from ResourceModule

ResourceModule.state
    may itself originate from initialization behavior
    inherited from RmEngineBase
```

I need practice answering:

> Which class defined this method?

> Which class created this attribute?

> Is this method inherited or overridden?

> What does `super()` execute here?

> What object does `self` refer to at this point?

Once I can follow that, continue with the Ansible framework lessons.

## Only after Lessons 1–5 and the class bridge introduce the Ansible framework

### Lesson 6 — ResourceModule

Map the Python engine I wrote onto:

```python
self.want
self.have
self.compare()
self.commands
self.run_commands()
self.result
```

Walk through `resource_module.py` itself.

Because I am weak on classes, trace inheritance explicitly.

For example, when examining:

```python
class ResourceModule(RmEngineBase):
```

explain what ResourceModule receives from `RmEngineBase`.

When examining:

```python
class VlanNames(ResourceModule):
```

explain what VlanNames receives from ResourceModule and, transitively, from RmEngineBase.

Whenever code calls:

```python
self.compare(...)
```

identify exactly which class provides `compare()`.

Whenever code accesses:

```python
self.state
```

identify where that attribute was initialized.

Do not merely say "the framework handles it."

Explain the inheritance path.

Also explain which parts ResourceModule provides and which parts remain the responsibility of the resource-specific config class.

Important:

Do not claim that ResourceModule automatically implements the full semantics of `merged`, `replaced`, and `overridden`.

Show that the resource-specific config class generally transforms or selects WANT/HAVE according to the state and then uses the common comparison machinery.

### Lesson 7 — NetworkTemplate

Study:

```text
getval
setval
remval
result
shared
compval
```

Explain both directions:

```text
native CLI → structured data
structured data → native CLI
```

Map each part back to code we previously wrote manually.

Also explain the class relationship:

```python
class SomeTemplate(NetworkTemplate):
```

and what functionality is inherited from `NetworkTemplate`.

### Lesson 8 — Facts

Teach exactly how `self.have` is obtained.

Trace:

```text
connection.get()
    ↓
raw device output
    ↓
Facts class
    ↓
NetworkTemplate.parse()
    ↓
validation / normalization
    ↓
ansible_network_resources
    ↓
ResourceModule.get_facts()
    ↓
self.have
```

I particularly want to understand how gathered native configuration becomes structured data.

When Facts-related classes use inheritance or instantiate other classes, explain those relationships explicitly.

### Lesson 9 — Argspec and registration

Cover:

- module argument specification
- resource data model
- Facts registration
- `FACT_RESOURCE_SUBSETS`
- user-facing module
- module_utils config class
- parser/template class
- builder-generated files

Explain what `cli_rm_builder` generates versus what still has to be implemented by the developer.

### Lesson 10 — Build the complete resource module

Use the same simple resource from the earlier exercises.

Implement the full module supporting:

- `merged`
- `replaced`
- `overridden`
- `deleted`
- `gathered`
- `rendered`
- `parsed`

Walk through an execution variable-by-variable.

For example:

```text
playbook config
→ module object
→ VlanNames(module)
→ VlanNames.__init__()
→ ResourceModule.__init__()
→ RmEngineBase.__init__()
→ self.want
→ gathered facts
→ self.have
→ state transformation
→ compare()
→ addcmd()
→ NetworkTemplate.render()
→ self.commands
→ run_commands()
```

When moving between classes, identify it explicitly.

### Lesson 11 — Testing

Include tests for:

- parsing
- rendering
- merged
- replaced
- overridden
- deleted
- gathered behavior where appropriate
- idempotency
- explicit removal
- absence semantics
- malformed or unusual input
- normalization

Use patterns consistent with current Ansible collection testing practices.

### Lesson 12 — Apply the same process to a real Cisco feature

Once the small module is understood, move to a realistic resource such as HSRP or another Cisco IOS/NX-OS feature.

At that point I should be doing a substantial portion of the design.

## Teaching style

Make this interactive.

Do not dump an entire completed module at the beginning.

For each lesson:

1. Explain the concept.
2. Give me a concrete networking example.
3. Ask me to reason about the expected behavior.
4. Give me a manageable Python task.
5. Let me attempt it.
6. Review my answer.
7. Correct problems and explain why.
8. Only then show a clean reference implementation.
9. Add tests.
10. Relate the concept back to ResourceModule when appropriate.

Keep the examples networking-oriented rather than generic programming exercises.

Do not skip ahead merely because you can produce the final code.

When reviewing code I wrote, do two separate reviews when relevant:

```text
Functional correctness / reconciliation review

and

OOP design opportunity review
```

The OOP review should not block progress merely because the current code is procedural.

When I misunderstand something, distinguish between:

- my Python misunderstanding,
- my Python class/inheritance misunderstanding,
- my desired-state/reconciliation misunderstanding,
- Cisco CLI behavior,
- Ansible framework behavior.

When showing Python, use type hints.

When relevant, distinguish:

- transport (`network_cli`)
- gathering/parsing
- reconciliation
- rendering
- command execution

Do not conflate them.

Do not ask questions that unnecessarily telegraph the answer.

Give enough information for me to solve the exercise without embedding the solution in the question.

Prefer explicit explanations over unexplained abstractions.

If I use a defensive programming pattern intentionally, such as a final `else: raise RuntimeError`, do not simplify it merely because a shorter equivalent exists. Explain the tradeoff.

## Important conceptual rules to preserve

These are central to the course:

```text
State logic determines what WANT means.

ResourceModule.compare() compares structured WANT and HAVE.

NetworkTemplate translates between structured data and native CLI.

Facts produce structured HAVE.

network_cli is the transport, not the reconciliation engine.
```

Also preserve this simplified interpretation:

```text
MERGED

effective WANT ≈ HAVE plus explicitly supplied intent


REPLACED

compare supplied WANT directly against the selected existing
resource instances


OVERRIDDEN

compare supplied WANT against the whole managed resource and
also handle resource instances that exist only in HAVE


DELETED

compare the targeted existing resource against an effectively
empty desired state
```

These are conceptual descriptions. When implementing them, verify the exact behavior against current Ansible source and real collection modules.

## Simplified VLAN-name resource used in the exercises

The current learning resource is deliberately narrower than a complete VLAN resource.

It owns:

```text
VLAN name
```

It does not own VLAN existence itself.

Therefore:

```text
remove resource-owned configuration
```

means:

```text
no name
```

not:

```text
no vlan <id>
```

Resource identity is:

```python
vlan_id
```

Current representative HAVE:

```python
[
    {"vlan_id": 10, "name": "USERS"},
    {"vlan_id": 20, "name": "SERVERS"},
    {"vlan_id": 30, "name": "VOICE"},
    {"vlan_id": 40, "name": "GUEST"},
    {"vlan_id": 60},
]
```

Representative WANT:

```python
[
    {"vlan_id": 10, "name": "STAFF"},
    {"vlan_id": 20},
    {"vlan_id": 40, "name": "GUEST"},
    {"vlan_id": 50, "name": "IOT"},
    {"vlan_id": 60, "name": "PRINTERS"},
]
```

Representative deletion selection:

```python
[
    {"vlan_id": 10},
    {"vlan_id": 20},
]
```

The deletion list is not a different Ansible input type. It is simply a separate exercise fixture representing normal WANT/config supplied with `state=deleted`.

## Progress completed so far

### Lesson 1 — COMPLETE

Implemented and understood:

- resource identity
- indexing lists of dictionaries by VLAN ID
- common IDs
- IDs only in HAVE
- IDs only in WANT
- name present only in HAVE
- name present only in WANT
- matching and differing properties

A helper such as `diff_vlan_name_states()` is currently retained as learning/reference scaffolding but is no longer the primary reconciliation pipeline.

### Lesson 2 — COMPLETE

Implemented ordinary Python builders for:

```text
merged
replaced
overridden
deleted
```

Under the simplified VLAN-name resource:

```text
MERGED
copy HAVE and overlay explicitly supplied WANT attributes

REPLACED
copy HAVE, but selected WANT resources become exactly the
provided resource representation

OVERRIDDEN
WANT defines the managed resource state; existing VLAN
identities not present in WANT retain identity but lose the
resource-owned name

DELETED
selected VLAN identities retain identity but lose the
resource-owned name
```

Important deleted-state guard learned:

```python
if vlan_id in deleted:
```

so deleting a nonexistent resource does not manufacture a fake one.

### Lesson 3 — COMPLETE

Implemented:

```python
build_vlan_name_changes()
```

to convert HAVE versus effective desired state into a machine-consumable before/after change set.

Implemented:

```python
render_vlan_name_commands()
```

to convert those changes into IOS CLI.

The renderer is intentionally separated from reconciliation logic.

Concepts learned include:

- `None` versus missing dictionary key,
- use of a unique `object()` sentinel,
- before/after change representation,
- deterministic sorting,
- rendering `name VALUE`,
- rendering `no name`.

All four state builders feed the same comparison and renderer pipeline.

### Lesson 4 — IN PROGRESS

Implemented:

```python
parse_vlan_config()
```

for running-configuration-style VLAN blocks.

The parser currently:

- splits native configuration into blocks,
- ignores unrelated configuration,
- identifies VLAN resources,
- parses VLAN ID,
- normalizes VLAN ID from string to integer,
- omits the `name` key when no name is configured,
- parses configured names,
- validates malformed VLAN identifiers,
- validates VLAN ID range.

The current VLAN-ID extraction deliberately uses a broad capture such as:

```python
r"^vlan\s+(?P<vlan_id>\S+)"
```

so regex performs extraction while Python performs semantic validation.

The parser distinguishes examples such as:

```text
vlan BAD
```

from unrelated configuration.

Malformed resource-looking configuration should raise an error rather than silently disappearing.

Current validation concepts include:

```text
vlan BAD
    → fails integer conversion

vlan 33BAD
    → fails integer conversion

vlan 9999
    → converts to int but fails range validation
```

We also covered exception behavior:

```text
catch exception + only print
    → exception handled, execution continues

catch exception + raise
    → exception propagates and normal execution stops
```

We separated:

```python
vlan_id_string
```

from:

```python
vlan_id
```

so the raw CLI token and normalized integer have distinct identities.

### Supplemental Exercise 4.3 — ADDED, NOT YET COMPLETE

This exercise was added on 2026-09-14 and is intentionally tracked as a supplement to the original Lesson 4 plan.

Purpose:

- isolate malformed parser inputs,
- demonstrate why a fail-fast parser cannot test multiple independent failure cases in one configuration blob,
- manually expose the basic mechanics that a testing framework later automates.

This addition does not move the dedicated testing lesson forward; it only verifies the parser behavior currently being developed.

## Current next step

Continue **Supplemental Exercise 4.3** within Lesson 4.

The immediate task is to stop putting several malformed VLANs into one configuration blob because the first raised exception prevents later malformed cases from executing.

Create isolated parser test fixtures such as:

```python
VALID_VLAN_CONFIG = """
vlan 10
 name USERS
!
"""

NON_INTEGER_VLAN_CONFIG = """
vlan BAD
 name BROKEN
!
"""

MIXED_VLAN_CONFIG = """
vlan 33BAD
 name OH_CMON
!
"""

OUT_OF_RANGE_VLAN_CONFIG = """
vlan 9999
 name OUT_OF_RANGE
!
"""
```

Before introducing pytest, manually build a small:

```python
def run_parser_tests() -> None:
```

so I understand what the test framework will eventually automate.

Start with the valid case only.

Call:

```python
parse_vlan_config(VALID_VLAN_CONFIG)
```

and compare the returned structured state against:

```python
[
    {"vlan_id": 10, "name": "USERS"}
]
```

Produce PASS/FAIL.

After the valid case works, proceed to isolated exception tests.

Do not introduce pytest until the manual testing mechanics are understood.

Continue using the interactive teaching sequence rather than giving the completed test suite immediately.

## OOP observation at the current point

The current VLAN parser is a legitimate future class opportunity because parser regex definitions, validation rules, and parsing behavior all belong to one conceptual component.

For example, the current procedural design resembles:

```python
VLAN_ID_PATTERN = ...
VLAN_NAME_PATTERN = ...

def parse_vlan_config(config: str) -> list[dict[str, Any]]:
    ...
```

A possible future object-oriented shape could be:

```python
class VlanConfigParser:
    vlan_id_pattern = ...
    vlan_name_pattern = ...

    def parse(self, config: str) -> list[dict[str, Any]]:
        ...
```

However, do not convert it yet solely for the sake of OOP.

At this stage the procedural parser remains useful because it keeps the parsing mechanics visible.

Continue flagging opportunities like this as the code evolves and explain when the balance changes from:

```text
"a class could represent this"
```

to:

```text
"a class now provides a meaningful design advantage."
```

## Conversation continuity

Monitor the length and complexity of the current conversation.

When the conversation has grown large enough that context loss, summarization, or reduced reliability may become a concern, tell me before it becomes a problem and recommend starting a new chat.

Before recommending the new chat:

1. Update `COURSE_PROMPT.md` with the current lesson state and immediate next step.
2. Update `COURSE_HISTORY.md` with any completed work, deviations, or supplemental exercises not already recorded.
3. Verify that the GitHub working file reflects the latest reviewed code.
4. Provide a concise handoff message I can use to begin the new conversation.

Do not wait until important course context has already been lost before making the recommendation.
