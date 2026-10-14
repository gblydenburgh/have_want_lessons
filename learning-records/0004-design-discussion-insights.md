# Insights from a class-design discussion (route-compare, now archived)

In a design discussion about refactoring my old route-compare script (archived in `archive/route-compare/`; not an active project), I was *shown* how to choose a data shape, but I haven't yet *demonstrated* it by writing code.

**Misconception corrected:** I framed the design as "one class per vendor". The real axis is *input schema*: the same vendor can produce two schemas (Junos via Genie vs `display json`), so two normalizers, and a normalizer may just be a function. Likewise, "pyATS vendor bias" was the wrong diagnosis; it's schema heterogeneity, and swapping parsers moves the problem without solving it.

**Exposed to, not yet demonstrated:** designing a record from the questions downstream code asks (not from the fields the source provides); frozen dataclasses and why set members must be hashable (`frozenset`, not `set`, inside a frozen dataclass); `field(compare=False)`; keeping policy (what to skip) out of the data record; "use an instance of `Counter`, don't define a class".

**Implications:** I've seen these ideas in one context. Check them in a fresh one before treating them as known.
