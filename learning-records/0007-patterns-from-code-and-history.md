# Patterns from my code, commits and course history

Read from the `have_want_lessons` repo (97 commits, 2026-09-14 to 09-23; old exercise code now in `archive/web-chat-course/code/`), my 2021 route-compare script, and the course history. These are habits and traits backed by evidence, not one-off events.

## Strengths that show up in the code (build on these)
- **I think in invariants.** In `build_vlan_name_changes`: a `missing = object()` sentinel to tell an absent key from a `None` value, and a final `else: raise RuntimeError(...)` for "can't happen". This will matter for absent-vs-default semantics in resource modules.
- **Mutation awareness.** I use `copy.deepcopy` when building state from HAVE.
- **Contracts at boundaries:** range checks and `raise ... from e` in the parser, names that show origin (`vlan_id_string` → `vlan_id`), sorted output for determinism.
- **I modularize on my own.** I split the 681-line `excercise2.py` into parser/states/diff/renderer/tests modules without being asked.
- **Real growth since 2021.** The 2021 script relied on globals, duplicated logic, positional matching and untyped dicts. The 2026 code has typed signatures, separate stages and explicit invariants. The procedural foundation is solid; the next step up is data modelling, not "learning to code".

## Habits to correct (gently, every time)
- **Print-debugging, with the prints left behind.** Commented-out `print` lines fill `vlan_diff.py`, just as they fill the 2021 script. Five years of the same habit. Show me better tools (pytest output, `-vv`, a debugger, `assert` messages) when they'd actually help.
- **Generic names:** `temp_dict`, `comp_data`, `temp_detected_changes`, `parsed` for something that's indexed, not parsed.
- **Comments that narrate the code** ("Determine if the have vlanid is in effective") instead of explaining intent or the invariant.
- **Small PEP 8 slips:** trailing whitespace, `x=y` without spaces, inconsistent key order (`before`/`after` vs `after`/`before`).
- **I build my own test harness** (`simple_result_compare` with a `TypeVar`). That means I'm ready for pytest and will see why it's better.
- **Typing is broad:** `dict[str, Any]` everywhere, so annotations are present but catch little.

## How I learn (from the history)
- **I check claims against real devices.** Two exercises were dropped after I checked them: the VLAN `state`/`shutdown` normalization (my Cisco output didn't expose it) and the trailing-whitespace HAVE fixture (not justified by device semantics). Ground claims in real output, and expect me to verify.
- **I think by articulating precisely.** I revised the trailing-whitespace test description six times in 30 minutes. Writing it precisely is how I found that the premise was wrong. Have me state expectations in words *before* coding; my challenges come out of that.
- **I find mechanisms on my own:** e.g., noticing that mixed `str`/`int` keys would also break sorting, which no one had pointed out.
- **When teaching frustrates me, I turn the frustration into a rule.** I made 29 commits to `COURSE_PROMPT.md`, about 15 of them during the 5 days of the OOP bridge. The frustrations clustered as:
  - **Missing context:** needing to scroll back, hierarchy not shown, hidden collaborators → keep everything needed in view.
  - **Abstraction before the concrete:** syntax before the real object, vague "this object" → concrete workflow first, then syntax.
  - **Steps too big:** jumping from one method to a full trace → build chains one or two calls at a time.
  - **Unfair assessment:** predictions whose answers were already shown, marked down for parts that weren't asked for → assess fairly and explicitly.

  The friction spikes when the material gets abstract (classes, framework layers). Slow down there, not on the networking or reconciliation logic.

## Working pattern
- Commits suggest sessions late in the evening and into the night, plus weekend mornings, in bursts of many small commits. Keep lessons short enough to finish in one sitting at the end of a workday.
