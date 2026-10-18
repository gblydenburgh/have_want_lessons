# Ansible Network Resource Modules Resources

## Knowledge

- [Ansible docs: Developing network resource modules](https://docs.ansible.com/ansible/latest/network/dev_guide/developing_resource_modules_network.html)
  The official developer guide: resource model, builder, module structure, testing. Use for: module structure, registration, and testing.
- [Ansible docs: Network resource modules (user guide)](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)
  The user-facing contract for states and results. Use for: what `merged`/`replaced`/`overridden`/`deleted`/`gathered`/`rendered`/`parsed` are promised to do.
- [Source: ansible-collections/ansible.netcommon](https://github.com/ansible-collections/ansible.netcommon)
  Home of `ResourceModule`, `RmEngineBase`, `NetworkTemplate`. Use for: any claim about framework internals. Read the current source; don't rely on memory.
- [Source: ansible-collections/cisco.ios](https://github.com/ansible-collections/cisco.ios)
  Production IOS resource modules, their templates and tests. Use for: real examples of config classes, Facts, rm_templates, and unit tests.
- [Source: ansible-network/cli_rm_builder](https://github.com/ansible-network/cli_rm_builder)
  The scaffolding tool. Use for: what's generated vs what the developer writes.
- [Think Python, 3rd edition (Allen B. Downey, 2023), free online](https://allendowney.github.io/ThinkPython/)
  **Primary source for classes.** Written "for people who have never programmed before". Chapters 14–17 build classes from functions, then methods (ch. 15 moves existing functions into the class), then inheritance. Calls `__init__` "the init method", not constructor. Use for: lesson reading.
- [Think Python, 3rd edition, ch. 9 §9.9–9.11: Objects and values, Aliasing, List arguments](https://allendowney.github.io/ThinkPython/chap09.html#aliasing)
  Beginner explanation of aliasing, `is`, and arguments as aliases, with state diagrams. Says "equivalent" where this course says equal. Use for: lesson 0002 reading. (Checked 2026-10-17.)
- [perlreftut: Mark's very short tutorial about references](https://perldoc.perl.org/perlreftut)
  Perl's own reference tutorial: Make Rule 1 (`\`), Use Rule 1 (`@{$aref}`), and "two references to the same array" when copying a reference. Use for: the Perl-to-Python bridge. (Checked 2026-10-17.)
- [Python for Everybody, ch. 14 Object-oriented programming](https://www.py4e.com/html3/14-objects)
  Beginner-friendly alternative with a glossary. Calls `__init__` a constructor, so terms differ from this course. Use for: a second explanation.
- [Python docs: Classes tutorial](https://docs.python.org/3/tutorial/classes.html)
  The exact rules, but written for people who already program in other languages (compares with C++, uses CS terms). Use for: backing up claims, translated into plain words; not as first reading.
- [Python docs: Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
  **Layer 3 primary source** (route steps 4 and 6): how functions become bound methods, and how `property` works. Written for experienced programmers. Use for: the "Under the hood" sections, translated into plain words. (Not yet checked against the current docs; verify before first use.)
- [Python docs: dataclasses](https://docs.python.org/3/library/dataclasses.html)
  Use for: `frozen=True`, generated `__eq__`/`__hash__`, `field(compare=False)`.
- [Ned Batchelder: Facts and Myths about Python names and values (PyCon 2015 video)](https://youtube.com/watch?v=_AEJHKGk9ns) ([text version](https://nedbatchelder.com/text/names1.html))
  The standard explanation of names, references, aliasing, and mutating vs rebinding. Use for: identity, "assignment never copies", function arguments as assignment. **Primary source for lesson 0002.** (Text checked 2026-10-17.)
- [Corey Schafer: Python OOP Tutorial 1, Classes and Instances (video)](https://www.youtube.com/watch?v=ZDa-Z5JzLYM)
  About 15 minutes: class vs instance, attributes, `__init__` (which he calls the constructor), methods, `self`. Use for: a second explanation of the basics. (Content checked only against summaries, not watched.)
- [Corey Schafer: Python OOP Tutorial 2, Class Variables (video)](https://www.youtube.com/watch?v=BJ-VvGyQxho)
  13 minutes on class vs instance variables, including an instance attribute shadowing a class variable. Use for: where attributes are stored. (Content checked only against a summary, not watched.)
- [pytest documentation](https://docs.pytest.org/en/stable/)
  Use for: assertions, parametrization, fixtures.

## Wisdom (Communities)

Not yet researched. Find well-moderated places where resource-module and collection contributors discuss design and review (e.g. the collections' GitHub issues/discussions, the Ansible community forum's network category) and add them here.

## Gaps

- Pinned so far: `cisco.ios` @ `675a661c` `config/vlans/vlans.py` (the `merged` branch, L111–113) and `ansible.netcommon` @ `a929db70` `utils.py` `dict_merge` (L321–383, returns a new dict, `deepcopy(base)` at L341). Used in lesson 0002.
- No vetted walkthrough yet of a simple, current `cisco.ios` module from argspec to tests. Pick one module and pin its commit SHA when the framework comes up.
