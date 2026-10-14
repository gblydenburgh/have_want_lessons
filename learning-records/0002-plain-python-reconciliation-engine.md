# Built a desired-state reconciliation engine in plain Python (Lessons 1–5)

I built and tested the lower half of a resource module by hand, for a teaching resource (VLAN `name`, identity `vlan_id`): parse/normalize → structured HAVE → state semantics (`merged`/`replaced`/`overridden`/`deleted`) → change calculation → deterministic IOS CLI rendering → simulated apply → gather again → `commands == []` on the second pass. Framework lessons can map onto this engine rather than starting from scratch.

**Evidence:** `modular_ex2/` and `excercise2.py`. Completed 2026-09-19; details in `COURSE_HISTORY.md`. Covered partial apply, a bad-type normalization contract failure, malformed-input validation with exception chaining, and false diffs from bad normalization.

**Insights I own:**
- `HAVE` is *observed* device state and `WANT` is *intended* input. Don't "repair" valid device-derived HAVE just to make idempotency pass. Handle user mistakes on the WANT/validation side. (I challenged a trailing-whitespace normalization exercise on exactly this point, and it was withdrawn.)
- Idempotency is not the same as correctness of intent.
- Normalization is a correctness boundary, not formatting cleanup.
- The teaching resource owns VLAN *name* only, not VLAN existence. Real `cisco.ios.ios_vlans` owns more. Check what a real module owns before comparing semantics.

**Implications:** the engine is narrow (one scalar attribute) and manually tested. Next per the curriculum: widen to a second verified attribute (Lesson 6), then pytest and stronger data contracts (Lesson 7).
