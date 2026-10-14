# route-compare (practice project)

My class-writing practice ground (see `MISSION.md`). `route_compare_v1.py` is the original script, kept unchanged as the "before" for refactoring. Design status is in `learning-records/0004-route-compare-design-in-progress.md`.

What follows is my original brief for this project (2026-09-26), kept word for word.

---

What I want to build: refactor a script I already wrote — a route comparison tool that takes two pyATS JSON snapshots (before/after, Cisco IOS/IOS-XE/NX-OS) and reports what changed. It's real work: other network engineers who don't script will use it.

Known problems in it:

* `quick_detect_changes()` and `normal_detect_changes()` duplicate ~35 lines of skip logic; they differ only in output detail
* `my_broutes[i].keys() != my_broutes[i].keys()` compares a thing to itself — that check has never fired
* `temp_detected_changes` is only assigned inside an `elif`, so it can raise `NameError` or carry stale data from the previous route
* `routetotals()` omits local/direct/hsrp/glbp from the total
* `args` is a global referenced inside one function but passed as parameters everywhere else

Found later in review (unconfirmed until tested against fixtures):

* `if 1 in temp_detected_changes['next_hop_equal']['next_hops']` reports next-hop changes only when index 1 is among them; a change at index 2 alone is dropped
* The "SKIP UNKNOWN REASON" branch catches every route with an `outgoing_interface` that isn't Null0, which probably includes interface-only statics
* Skip logic checks `connected` and `local` but not `direct` (NX-OS)
* Next hops are compared by list position, so an ECMP reorder looks like a change

Target architecture (from a prior discussion, open to challenge):

* Normalization boundary: one class per vendor producing a common `Route` shape, so Junos support is a new class and zero changes downstream. This is the real motivation — I want to add Junos and couldn't without restructuring.
  *(Later corrected: the axis is input schema, not vendor, and a normalizer may be just a function. See LR-0004.)*
* A `RouteComparison` holding before/after/missing/new — the four values currently threaded through every function
* Reporters (quick/detailed) consuming change objects, so the comparison engine doesn't know about output format
* `routetotals()` should get smaller and stay a function — `collections.Counter`, not a class. Don't let "make it OOP" become the goal.

Constraints: the tool must keep working from files with no device access — that's what makes it usable by others. I have EVE-NG available for generating test fixture pairs.

First exercise: decide the normalized `Route` shape, since everything else depends on it and it's the design decision I'm least equipped to make alone.
