# OOP: I can trace short, simple classes; nothing elaborate yet

I can trace **short, primitive classes**: class vs instance, what `self` refers to, instance `__dict__` vs class attributes, `__init__` resolution through inheritance, a parent method calling `self.method()` that resolves to a child override, `type()` vs `isinstance()`, `super()` including chained dispatch, and simple composition.

The limits matter:
- **Only in AI-made exercises.** All my tracing practice was on small, tidy examples written for teaching, in chat.
- **Nothing elaborate.** I haven't traced real-world class code: deeper hierarchies, many methods and attributes, several files, framework code with hidden collaborators (e.g. `ResourceModule` and friends), or code someone wrote without teaching in mind.
- **No writing.** I haven't written classes or decided what deserves to be one.

**Evidence:** self-reported (2026-10-14), correcting an earlier, stronger claim ("can trace reliably, cold") from the route-compare prompt. The drills weren't recorded in the repo.

**Implications:** don't assume my tracing transfers to real code. Spot-check with a short example, then grow the size step by step: more methods, then deeper hierarchies, then real library or framework code with hidden pieces made concrete first. Writing and design judgment start from zero.
