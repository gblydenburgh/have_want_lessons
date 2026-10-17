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
- [Python docs: Classes tutorial](https://docs.python.org/3/tutorial/classes.html)
  The primary source on Python's class model. Use for: scopes, `self`, inheritance, method resolution.
- [Python docs: dataclasses](https://docs.python.org/3/library/dataclasses.html)
  Use for: `frozen=True`, generated `__eq__`/`__hash__`, `field(compare=False)`.
- [Ned Batchelder: Facts and Myths about Python names and values (PyCon 2015 video)](https://youtube.com/watch?v=_AEJHKGk9ns) ([text version](https://nedbatchelder.com/text/names1.html))
  The standard explanation of names, references, aliasing, and mutating vs rebinding. Use for: identity, "assignment never copies", function arguments as assignment.
- [Corey Schafer: Python OOP Tutorial 1, Classes and Instances (video)](https://www.youtube.com/watch?v=ZDa-Z5JzLYM)
  About 15 minutes: class vs instance, attributes, `__init__` (which he calls the constructor), methods, `self`. Use for: a second explanation of the basics. (Content checked only against summaries, not watched.)
- [Corey Schafer: Python OOP Tutorial 2, Class Variables (video)](https://www.youtube.com/watch?v=BJ-VvGyQxho)
  13 minutes on class vs instance variables, including an instance attribute shadowing a class variable. Use for: where attributes are stored. (Content checked only against a summary, not watched.)
- [pytest documentation](https://docs.pytest.org/en/stable/)
  Use for: assertions, parametrization, fixtures.

## Wisdom (Communities)

Not yet researched. Find well-moderated places where resource-module and collection contributors discuss design and review (e.g. the collections' GitHub issues/discussions, the Ansible community forum's network category) and add them here.

## Gaps

- No vetted walkthrough yet of a simple, current `cisco.ios` module from argspec to tests. Pick one module and pin its commit SHA when the framework comes up.
