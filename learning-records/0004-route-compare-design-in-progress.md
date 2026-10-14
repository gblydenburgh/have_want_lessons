# route-compare: Route shape discussed, not yet written

I started refactoring `route-compare` (`practice/route-compare/`) to practise writing classes. The goal is to add Junos without changing downstream code. **Status: the design was discussed; `Route` and `NextHop` haven't been written yet.** That's the pending exercise.

**Decisions proposed (mine to accept or argue):**
- Design `Route` from the questions downstream code asks: identity, should it be compared, did it change, how to display it. Don't copy the pyATS fields.
- A `Route` is the route *selected for forwarding*. Junos lists inactive candidates; the normalizer picks the active one, so `active` is dropped.
- Prefix is an `ipaddress` network object. VRF belongs to the table, not to `Route`.
- Protocol uses a small, closed, normalized set. Preference and metric get neutral names. None vs 0 must be decided and written down.
- Next hops are a `frozenset` of frozen `NextHop(address | None, interface | None)` dataclasses: ECMP order doesn't matter, and the changes are two set differences.
- Discard routes need a vendor-neutral flag; "Null0" is Cisco vocabulary.
- Keep the raw dict for `--raw` via `field(compare=False, repr=False)`.
- Skip policy belongs to the comparison, not to `Route`. `Route` holds facts and has no methods.
- `routetotals()` stays a function using a `collections.Counter` instance.

**Misconception corrected:** "one class per vendor" was the wrong axis. The axis is *input schema*. Junos via Genie and Junos via `show route | display json` are two schemas, so two normalizers. A normalizer may be just a function. "Vendor bias in pyATS" was also the wrong diagnosis: it's schema heterogeneity, and swapping parsers (NTC templates, a hand-written parser) moves the problem without solving it.

**Open question:** are cross-vendor comparisons (IOS before, Junos after) in scope? That changes the shape most.

**Fixtures available:** an 11-router EVE-NG lab with pyATS working on every device. A `capture.sh` and the null-change pair plan exist in the route-compare work.

**Implications:** a good writing exercise once the OOP bridge reaches design judgment. I write `Route`/`NextHop` with a one-line comment per field saying which question it answers; the teacher reviews.
