# Tracing check: dispatch is solid, attribute storage and identity are not

Lesson 0001 measured LR-0003's self-reported tracing on a fresh three-class hierarchy (`IpInterfaceBrief`, `IosIpInterfaceBrief`, `NxosIpInterfaceBrief`). The result splits cleanly.

**Evidence:** my lesson 0001 answers, graded 2026-10-15.

**Demonstrated:**
- Method lookup to an override: `NxosIpInterfaceBrief.is_data_row` runs first when `gather` (defined on the base) calls `self.is_data_row(line)`.
- `super()` continues to the base method on the *same* instance: `self` is `nx` throughout.
- I traced the NX-OS `parse_row` override correctly through to values (`protocol-down/...` becomes `"down"`).
- A method-local name (`fields`) doesn't become an attribute (right result, loose terms).

**Not demonstrated, and contradicts LR-0003:**
- **Where an attribute is stored vs where it's found.** I said `"command" in nx.__dict__` and `"network_os" in nx.__dict__` are both `True` ("they are both attributes of the nx object"), in the same answer set where I correctly said lookup finds them on the classes. I took "reachable through `nx`" to mean "stored on `nx`". I also explained `nx.interfaces == {}` by "gather wasn't called" without naming `__init__` as the code that creates it.
- **Object identity.** I justified `result is nx.interfaces` being `True` with "a dictionary is successfully returned". I didn't reason about `is` at all.
- **Attribute name vs value:** I wrote `result` as `"interfaces": {...}`, putting the attribute's name inside the value.
- **Return values back up a call chain.** In Q2 c I took the `True` that `super()` returned to line 34 as the value that reaches `gather`'s line 13, and didn't carry on to line 35, where the override returns `False`. I had every piece (I used line 35's banner test myself to explain why `parse_row` isn't called) but didn't assemble them. Remedy: write out the call stack while tracing (method, defining class, `self`, arguments, then return value and the line it goes back to).

**Answer discipline:** I left out asked-for parts (the values in Q1 a/b, the defining class in Q3 d), listed `parse_row` as running in Q2 a while saying in Q2 c that it isn't called, and gave thin reasoning traces. Small slips again (`IPInterfaveBrief`, `field` for `fields`, stray commas in dicts).

**Implications:** dispatch and `super()` are good enough to build on. Before writing classes, close two gaps with a fresh case: where an attribute is stored vs where it's found (instance `__dict__` vs class body, and what `__init__` creates), and identity vs a fresh copy. The identity gap connects to the mutation awareness noted in LR-0007.
