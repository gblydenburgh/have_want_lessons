# Starting profile: self-taught, classes from zero

I'm a self-taught network engineer with no formal programming education: 30 years in IT since 1996, after a few years as a car mechanic, learning on the job plus a few one-week courses (one in Perl). My scripting has been data gathering and reports, in Perl and then procedural Python with dicts and functions.

**Evidence:** my own account (2026-10-17), and the first attempt at classes. Lessons built on assumed vocabulary (namespace, MRO, identity) and on the Python tutorial's programmer-oriented sections left me unable to tell what answers were wanted.

**What I can build on:** dicts, functions, f-strings and everyday procedural Python; strong networking and Ansible usage; a habit of checking what actually happens rather than trusting labels.

**Starting point for classes:** zero. Lesson 0001 maps classes onto dict-and-functions code. Two things clicked on 2026-10-17 and I restated them correctly: the instance holds its own data while the methods are stored once in the class, and `r1.describe()` is the same call as `Device.describe(r1)`.

**Gap carried over from Perl: references.** I used `@{}` and `->` to dereference without understanding why. I've never had a working mental model of references. Python uses references everywhere (every name, attribute and list/dict entry refers to an object) and follows them automatically, so the model is invisible but still decides behaviour: after `b = a`, both names refer to one object.

**Implications:** teach "names refer to objects" as its own lesson, bridging from Perl's `@{}`, before any lesson on shared or changed data (aliasing, identity with `is`, copies, mutating HAVE). Primary source: Ned Batchelder, "Facts and Myths about Python names and values".

**Other implications:** define every term, including general programming ones. Separate where code is written from where its results are stored. Check claims in the REPL with me. Choose beginner-oriented primary sources.
