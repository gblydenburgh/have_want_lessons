# OOP: reading is solid; writing and design judgment are untested

After a week of drills (around 2026-09-19 to 26), I can reliably trace class code without notes: class vs instance, what `self` refers to, instance `__dict__` vs class attributes, `__init__` resolution through inheritance, method dispatch (including a parent method calling `self.method()` that resolves to a child override), `type()` vs `isinstance()`, `super()` including chained dispatch, and composition (an object holding another, `self` rebinding across the hop, no inherited methods).

I have **not written** any of it. Assume I can follow class code but can't yet decide what deserves to be a class.

**Evidence:** self-reported at the start of the route-compare conversation (2026-09-26). The drills themselves weren't recorded in this repo, so spot-check one or two tracing questions before building on this.

**Implications:** the curriculum's OOP bridge (Lesson 8) is half done. Skip the reading drills and go straight to writing: first framework-shaped code (subclass a base, override one method, call `super()`, as `ResourceModule` code does), then design judgment (route-compare).
