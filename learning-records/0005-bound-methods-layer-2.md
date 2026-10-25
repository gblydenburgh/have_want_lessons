# Bound methods and reading vs calling: layer 2 shown; methods hidden by instance attributes not yet

Lesson 0004 (2026-10-22 and 2026-10-24, `sessions/2026-10-22-01.md`, `sessions/2026-10-24-01.md`). **Shown**, not mastery: reading a method through an instance gives a bound method, which refers to the function and the instance, and only `()` calls it. I used that to find a real bug: `if switch.needs_change:` reads the bound method, which always counts as true, so a switch with every wanted VLAN still got `end` and `write memory`. **Misconception confirmed:** I don't yet hold that an instance attribute hides a method of the same name. Lesson 0003's Q5 was a concept gap, not a reading slip.

**Evidence:**
- Quiz 4 of 6 first try. Q1: believed `print` runs a method it's given (reading vs calling); corrected on 10-22. Q2: the right reasoning, but given only after the page's feedback.
- E1 (10-24, a later session than the Q1 correction, a different setting, no hint toward the line): correct diagnosis and fix. Precision gaps: no line number; said "evaluates to True" for "evaluates to a bound method, which counts as true". Exercise ran and passed checks 1–4 on my own run.
- E2: the test condition matched the requirement word for word and failed on the bug. The gap from LR-0004 didn't recur.
- R1 (warm-up, probably answered before the Q1 correction): `self.save = True` alongside `def save(self)`. I predicted `print(r1.save)` would print the method's return value and that `r1.save()` would print nothing. Both wrong: the instance attribute is found first (`True`), and calling it raises `TypeError: 'bool' object is not callable`. Fits my 10-22 question "That is a method not an attribute, no?": I treat methods as a separate category from attributes.
- R2: mutation through a parameter, unaided, from memory (it needed prompting on 10-19).

**Picked up along the way (minimum taught, iteration belongs to the parallel course):** list comprehensions. I can trace one on a fresh case (QC2r, exact) once the answer format was clear. But in the same session I said the loop name is local to the comprehension, then reasoned as if it held its last value after the comprehension and across calls (C3). The reference model (the new list refers to the objects, not the name) came together across this session and a ChatGPT session.

**Not yet shown:** an instance attribute hiding a method; that bound methods last (one later-session use only, inside the same lesson); the layer 3 section (functions as descriptors), not tested.

**Implications:**
- Lesson 0005 (inheritance and overriding) is lookup again: a subclass's method hides the parent's. Settle "an instance attribute hides a method" with a fresh case first. Teach it as one lookup for every attribute, methods included, not as a special rule.
- Watch for "method" vs "attribute" as separate categories in my wording.
- Starter code: no untaught constructs (comprehensions included) without explaining them in place.
