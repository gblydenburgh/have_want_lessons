# Classes and OOP for Ansible resource modules

My one-on-one course in object-oriented Python, aimed at understanding, fixing and extending Ansible network resource modules. It's taught by an AI teacher (Claude or ChatGPT) from the files in this repository, and runs alongside my Python design course (`/home/gary/Projects/python-design-course`).

## Starting a session

**With Claude:** open a new Claude Code session in this folder in VS Code, then type:

```text
/teach You're my teacher for the course in this repository. Follow sessions/README.md: run the start routine, give me the four-line handoff, then ask whether this is practice or the next lesson.
```

**With ChatGPT:** give it access to this repository on GitHub (branch `teach-workspace`), then paste:

```text
You're my teacher for the course in this repository (branch teach-workspace).
Follow sessions/README.md: run the start routine, give me the four-line handoff,
then ask whether this is practice or the next lesson.
```

**What happens next:**
1. The teacher reads the course files and tells me in four lines what's shown, what's unproven, what's open and what it proposes next. I confirm or correct it.
2. I choose: **practice** on past lessons, or the **next lesson**. There's at least one night between new lessons.
3. The lesson is an HTML file in `lessons/`. I open it with VS Code Live Preview from the Explorer sidebar, work through it, and paste the answer sheet's output into the chat.
4. Exercises go in `lessons/code/`. On a substantive exercise I **commit my first attempt before the review**, then commit the revision.
5. At the end, the teacher writes the session record in `sessions/` and updates the learning records and `NOTES.md`. **I commit and push.**

Always start a fresh session for a new lesson. Long sessions make the teacher less reliable.

## What's where

| File | What it holds |
| --- | --- |
| [MISSION.md](MISSION.md) | Why I'm doing this and what success looks like |
| [NOTES.md](NOTES.md) | How to teach me: the rules, the Route, and the next-session note |
| [sessions/](sessions/README.md) | One record per session, and the routine every teacher follows |
| [learning-records/](learning-records/) | What I've shown, with evidence |
| [lessons/](lessons/) | The lessons, as HTML, and my exercise code in `lessons/code/` |
| [reference/](reference/) | Reference sheets, including the glossary both courses use (`oop-glossary.html`) |
| `assets/` | Shared lesson components: stylesheet, quizzes, answer sheet, diagrams |
| [RESOURCES.md](RESOURCES.md) | Sources the teacher draws on |

## Control words

During a lesson: `HINT` (a small clue), `NUDGE` (the next reasoning step), `ANSWER` (the solution), `NEXT` (move on).
