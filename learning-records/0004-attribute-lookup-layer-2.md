# Attribute lookup for data: layer 2 shown on the same day

Lesson 0003 (2026-10-19, `sessions/2026-10-19-01.md`). **Shown**, not mastery: I can tell a class attribute from an instance attribute and trace a read: the instance first, then its class. I know that assigning to an attribute stores it on the instance and never changes the class. I can see that mutating a class-level list through `self` reaches every instance, and I can decide which data may be shared on the class. All of this is for data attributes. Whether I hold that methods go through the same lookup is unsettled.

**Evidence:**
- P1: predicted `l0003_demo.py`'s shared-list output exactly, with the right reason. The section before P1 said where `commands` is stored, so P1 shows I traced the consequence, not that I found the storage location myself.
- Quiz 5 of 6 on the first pick. Q1–Q4 (read falls through to the class; assignment stores on the instance; `append` mutates the shared list; `+` then `=` stores a new list on the instance) and Q6 (what can safely be shared) were right.
- Q5 missed: picked "methods are always looked up in the class" when an instance attribute named `describe` hid the method. I said I'd misread the f-string's literal `(ios)` as code and missed the assignment. Classified as genuine ambiguity: a reading slip, or a gap in "methods and data share one lookup".
- E1: both class/instance decisions right. The `max_vlan_id` reason gave "the same for all" but not "nothing changes it".
- Exercise (`lessons/code/l0003_switch.py`): fix right the first time; ran; passed checks 1–5.
- Test: failed on the bug before the fix (E2), the watch item from LR-0003. Then two review rounds. The first assert checked the stored list rather than `commands()`. The revision used `in` ("contains") instead of "contains only", so it passed on the original bug; the teacher's run against the bug caught that. The final `==` version fails on the bug and passes on the fix, and I ran it against the bug myself.

**Spaced recall of lesson 0002 (one day later):** R1 (mutate vs rebind) and R3 (attribute name, not parameter name) exact. R2 missed mutation through a parameter: wrote `sw1` unchanged. Corrected after two pointer questions, with a correct reason: `device` refers to the same dict as `sw1`, and the first line mutates it.

**Not yet shown:** that it lasts; that an instance attribute can hide a method (Q5); the optional layer 3 section (`__dict__`, `type(r1).__dict__`), which no question tested.

**Implications:**
- Lesson 0004 (how methods get `self`, route step 4) needs "methods are found by the same lookup as data". Its warm-up must settle Q5 with a fresh case before anything builds on it.
- Retest mutation through a parameter (R2) with a fresh case. LR-0003's "arguments are assignment" didn't come back unaided after one day.
- Tests: running against the bug is now happening. The gap has moved to the condition: does it check exactly what the requirement says ("only", not "contains")? Keep asking me to compare the condition with the requirement's wording, and with my own failure message.
