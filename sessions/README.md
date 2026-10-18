# Session records

One file per teaching session, written by whichever teacher ran it, Claude or ChatGPT. Together with `MISSION.md`, `NOTES.md`, `reference/`, `learning-records/`, the lessons and the code history, these files are everything a teacher needs to pick up the course. Nothing course-relevant lives only in a teacher's private memory or chat history. Agreed 2026-10-18 in the parallel course (`/home/gary/Projects/python-design-course`, its `AI_CONVERSATION.md`), which uses the same format.

Learning records stay decision-grade, as before: what has been established, and why it changes what to teach next. Session records are the evidence they cite.

## Start of every session, any teacher

1. Read `MISSION.md`, `NOTES.md` (its rules, then "Next session"), `reference/oop-glossary.html`, the latest two or three files here (their **Assessment** and **Resume here** sections), the learning records they cite, and the parallel course's `learning-records/`.
2. Tell the learner in four lines: what's shown, what's unproven, what's open (errors, unresolved review comments, pending tests), and what you propose next. The learner confirms or corrects. That's the handoff check.
3. Then follow `NOTES.md` ("Ask first, every session").

## End of every session, any teacher

1. Write the session record here, using the template below. Paste the lesson's answer-sheet output into it unchanged.
2. Write or update a learning record only when the evidence clears the bar in `NOTES.md`, and cite the session record's rows.
3. Update `NOTES.md`: observed trends (citing the session file) and the next-session note.
4. Remind the learner to commit.

## File name

`sessions/YYYY-MM-DD-NN.md`, where `NN` counts sessions that day from `01`. A lesson that spans several sessions keeps its lesson ID, and each session gets its own file.

## Template

Leave out any section with nothing to say. A short practice session can be the header, a couple of evidence rows and the resume line. Full detail is for transfer checks, contested grades and significant design decisions.

```md
# Session YYYY-MM-DD-NN · lesson NNNN · teacher: <assistant and model>

Kind: lesson | practice | transfer check
Objective: … · Builds on: LR-NNNN · Route step: N
Files: lessons/… · lessons/code/… @ <commit> · writes LR-NNNN

## Evidence
| # | Asked | Learner's answer | Help given first | Result |
| --- | --- | --- | --- | --- |
| R1 | <the question as asked> | [verbatim, answer-sheet paste] "…" | none | <grade and the specific gap> |

## Code
- Attempt 1: <file> @ <commit>. <ran / passed checks: which ones; what failed>
- Revision: <file> @ <commit>. <result> · Review comments: <resolved / open>

## Decisions made unprompted / after prompting
Unprompted: … After prompting: …

## Teacher corrections
<what the teacher said that was wrong, why, and when it was corrected>

## Assessment
- Shown: … (rows …)
- Ran / passed checks: …
- Not yet shown: …
- Open: …
- Next test: …

## Provenance
<the source of each kind of evidence above, and any gaps>

## Resume here
<where the next session starts; open items>
```

## Provenance labels

Every quoted answer or exchange carries one of these:
- `[verbatim, answer-sheet paste]`: copied unchanged from the lesson's answer sheet.
- `[verbatim, copied from chat]`: copied exactly from the current conversation.
- `[teacher summary]`: the teacher's own account. Never presented as a quote.

Never invent a quotation. If something can't be copied, summarise it and say so. Git doesn't capture any AI conversation automatically, only what's written here. Keep secrets, credentials and sensitive production device output out of these files.

## Evidence labels

Four separate claims. None implies another.
- **Ran:** the learner's code executed and produced output.
- **Passed checks:** the learner's code passed the named tests or check script.
- **Shown:** understanding demonstrated in a session: a correct answer with correct reasoning, after whatever help the record lists.
- **Mastery:** transfer shown, meaning the skill applied without hints to a different problem in a later session (`NOTES.md`, "Mastery means transfer").

A learning record may claim something narrower than mastery, as long as it names the label it's claiming.

## Reviewing a record you didn't write (cold read)

Judge against the **source evidence**, not the first teacher's verdict: the question as asked, the learner's answer, the help that came before it, the tests, the revisions and the course standard. Where your conclusion differs from the record, classify the difference, with a reason:
- **Evidence gap:** the record doesn't hold enough to decide.
- **Teacher assessment error:** the evidence supports a different grade.
- **Reviewer error:** you misread the evidence.
- **Genuine ambiguity:** both readings are defensible.
