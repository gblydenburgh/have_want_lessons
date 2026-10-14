# Mission: Object-oriented Python, to work inside Ansible resource modules

## Why
I want to learn to design and write object-oriented Python so I can understand, fix and extend Ansible network resource modules, not just use them.

I've only ever used these modules from the outside. My real-world practice was to find a standard block of config, push it, and check by hand afterwards ("spray it and hope for the best"). I've never built anything idempotent myself. The end goal is to fix bugs I hit in the modules, add features, and eventually build my own.

My coding background never needed classes: Perl scripting, then procedural Python, all end-user automation where functions and dicts were enough. The code I want to work in (Ansible collections, and pyATS/Genie too) is built around classes. Until I can design them, I can read that code but can't change it with confidence.

These aren't two separate goals. The resource-module framework is built from classes, so OOP is the gap between where I am and the code I want to work in.

## Success looks like
- **I understand how resource modules work inside:** I can trace a module from input to device and back, and say which class owns each step.
- **Object-oriented design, the judgment part.** I can already read and trace class code. The goal is to *write* it and to decide what deserves to be a class and what should stay a function.
- I can fix a real bug in a resource module, add a feature to one, and eventually build my own, with tests.

## Constraints
- A one-on-one teacher–student exchange, not a lecture.
- I write the code; it gets reviewed.
- Lessons are fresh and network-automation based, not a continuation of old exercises.
- No predefined project. If the teacher judges a project necessary, the teacher designs it.
- I work on a headless Linux host through VS Code Remote-SSH.

## Out of scope
- Lab and infrastructure work (EVE-NG, AWX, k3s, pyATS setup). It's my strong ground and the lab is in good enough shape. The skill I'm building is writing code; if a session drifts into infrastructure, park it.
- OOP for its own sake: don't force code into classes.
- Beginner Python and beginner Ansible.
