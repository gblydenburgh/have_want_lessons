# Terminology traps I've already been corrected on

These came up in earlier sessions. Watch for them coming back, because each one hides a wrong mental model, not just wrong wording.

- Say "instance of a class", not "instantiated class" or "instanced class". "Instantiate" is the action; the instance is the resulting object.
- `self` is the particular instance running the method. It is not the class, not the initializer, and not "all of the class".
- A class definition is not an instance created from it.
- Instance attributes (`self.have`) are not class attributes defined in the class body.
- A bare name inside a method is a method-local variable, not an instance attribute. It's gone after the call unless the object it refers to is kept somewhere else.
- For an inherited method, the class that *defines* the method is not the instance it *operates on*.
- Method lookup follows the MRO and stops at the first match. It isn't searching "outside the instanced class" or "the parent".
- `super()` continues lookup after the current class in the MRO, on the *same* instance. It doesn't create or refer to a separate parent object.
- Ansible's `merged`/`replaced`/`overridden`/`deleted` are called `state` values by the API, but they're reconciliation policies, not the resulting device state.
- `collections.Counter` is a class (a dict subclass). The point about route-compare was "use an instance of it, don't define a new class".

**Implications:** use these exact distinctions in explanations, and check for them in my answers.
