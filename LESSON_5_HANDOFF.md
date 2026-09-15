# Lesson 5 Handoff

Continue the Ansible Resource Module course from the `gblydenburgh/have_want_lessons` GitHub repository.

Read `COURSE_PROMPT.md` first; it is the authoritative current course plan and handoff. Use `COURSE_HISTORY.md` for the execution history and `PROGRESS_EVALUATION.md` for the pre-Lesson 5 skills assessment.

Fetch the current `excercise2.py` from GitHub before teaching or reviewing code.

Lessons 1–4 and the retrospective cleanup are complete. Do not repeat them unless needed to resolve a specific misunderstanding.

Start with **Lesson 5 — Idempotency**.

Use the existing plain-Python pipeline to make the full cycle explicit:

```text
gather
→ parse/normalize
→ compare
→ render
→ apply/simulate apply
→ gather again
→ parse/normalize
→ compare again
```

The second pass must prove:

```python
commands == []
```

Deliberately introduce at least one bug that causes a false second-pass change, let me reason through it, diagnose it through the pipeline, and then fix it.

Do not start the Python classes bridge until Lesson 5 is complete. After Lesson 5, continue with the focused OOP/inheritance bridge before ResourceModule itself.

When I push code, review my submitted procedural code first for correctness, then perform the separate OOP opportunity review. Do not modify my code unless I explicitly ask you to.
