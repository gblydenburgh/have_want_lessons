# Classes, instances, attributes, methods and `self`: layer 2 demonstrated

Lesson 0001 (2026-10-17). I can explain and use the basic class model: the class holds the methods once; each instance holds its own data, stored by `__init__`; `r1.describe()` is the same call as `Device.describe(r1)`, with the instance before the dot passed in as `self`.

**Evidence:**
- Quiz: 6 of 6 on the first try.
- Exercise (`lessons/code/l0001_device.py`): added a `username` attribute and an `ssh_target` method, correct on the first attempt. The only review comment was trailing whitespace on a blank line, which I fixed.
- Predicted `vars(r1)` from memory, including the new attribute, and said correctly that `ssh_target` is stored in `Device`.
- Worked out on my own that `a.strip()` is `str.strip(a)`: built-in types are classes, and their methods get `self` the same way.
- Read a bound-method printout correctly once it was explained (`bound method Device.describe of <… object at …>`; the address is the instance's).

**Not yet shown:** that it lasts (all of this was same-day), and the layer 3 mechanism behind binding.

**Implications:** open lesson 0002 with a short spaced review of this one. Next on the route: names refer to objects, bridging from Perl's `@{}`.
