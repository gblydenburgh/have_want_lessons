# Mission: Ansible network resource modules, from the inside

## Why
I use Cisco IOS/NX-OS resource modules every day. I want to be able to diagnose, modify and eventually write one myself, for example fixing a real defect like the `cisco.nxos.nxos_snmp_server` SNMPv3 idempotency/state problem, instead of filing a bug and waiting.

## Success looks like
- I can trace a resource module end to end: argspec → `self.want`, Facts/template → `self.have`, state handling, `compare()`, NetworkTemplate rendering, `run_commands()`, and say which class owns each step.
- I can write the class code a module needs: subclass `ResourceModule`, override the right methods, use `super()`, and know what `self` holds at each point.
- I can design the data model, state semantics (`merged`, `replaced`, `overridden`, `deleted`, `gathered`, `rendered`, `parsed`) and parser/render templates for a real IOS/NX-OS feature.
- I can test it the way the collection does: unit tests with mocked connections, every state, and an idempotency round trip.
- I can decide what deserves to be a class in my own tools, and say plainly when a function or dict is fine.

## Constraints
- I write the code. The teacher explains, sets exercises and reviews; it does not write my solutions.
- I work on a headless Linux host through VS Code Remote-SSH.
- Lessons are built on network examples I already understand, never generic OOP toys.

## Out of scope
- Lab and infrastructure troubleshooting (EVE-NG, AWX, SSH, device configs). If a session drifts there, park it and come back to the lesson.
- A general OOP or application-development course. Teach class concepts when the framework or my tools need them.
- Beginner Python and beginner Ansible.

## Practice project
`route-compare` (see `practice/route-compare/`) is my practice ground for *writing* classes and making design calls. It serves the mission and doesn't replace it: work on it only when it trains a skill on the path above, and only with fixtures I already have.
