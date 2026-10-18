# Names refer to objects: layer 2 shown on the same day

Lesson 0002 (2026-10-17/18). I can use the model "names refer to objects; assignment never copies". I can tell mutating an object from rebinding a name, trace an argument through a call, and tell `==` (equal) from `is` (identical). I found and fixed a HAVE/WANT aliasing bug with a test that fails on the bug.

**Evidence:**
- Quiz: 6 of 6 on the first try. Every option paired an answer with a reason, and I picked the right reason each time. That includes Q1 and Q4, where wrong options had the right output.
- P1 (prediction before running the demo): predicted that HAVE and WANT would print the same and `Needs a change: False`, but wrote `'users'` for both instead of `'staff'`. I said it was a transcription slip, and the teacher accepted that.
- Exercise (`lessons/code/l0002_want.py`): the fix `have.copy()` was correct the first time.
- The test needed four rounds:
  - It checked one key only.
  - Then its condition was inverted (`!=`), so it failed on correct code.
  - Then the expected dict was written twice and the line was 170 characters.
  - Then I didn't know how to wrap the line. Once taught, I wrapped it correctly.
- Asked why parentheses around the message work, then whether they work around any argument. Both are the right follow-up questions.

**Spaced retrieval of lesson 0001** (next day, from memory):
- Methods stored in the class: correct.
- `Device.describe(r1)`: correct.
- `vars()` doesn't hold methods: correct.
- Two slips:
  - Listed r1's attributes as `self.hostname` etc. This is the second time "written vs stored" has come up.
  - Recalled `access_vlan` as `vlan`.

**New knowledge taught along the way (not yet practised):** implicit line joining inside brackets; a parenthesised group vs a tuple (the comma makes the tuple); the `assert (cond, msg)` trap; expression vs statement.

**Not yet shown:** that it lasts. All of the lesson 0002 work was in one session. Also not shown: copies of nested data (`deepcopy` was deferred), and spotting aliasing in real framework code.

**Implications:**
- Open lesson 0003 with spaced retrieval of 0002. Include a mutate-vs-rebind trace, and one question that needs the attribute's name rather than the code that stores it.
- Lesson 0003 is attribute lookup (route step 3). It can now build on "attributes are names that refer to objects".
- Tests: I write tests that pass but don't check what they claim. Keep asking me to run each test against the bug, not just the fix.
