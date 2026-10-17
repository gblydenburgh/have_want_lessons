// Multiple-choice quiz with instant feedback and a first-try score.
//
// <fieldset class="mcq" data-answer="b">
//   <legend>Question text</legend>
//   <label><input type="radio" name="q1" value="a"> option</label> …
//   <div class="feedback" data-for="a">Why a is right or wrong</div> …
// </fieldset>
// <p class="quiz-score" data-quiz-score></p>
//
// Only the first choice on each question counts toward the score; the learner can
// keep trying to read the other explanations.

(function () {
  function setUp() {
    const questions = Array.from(document.querySelectorAll("fieldset.mcq"));
    const scoreLine = document.querySelector("[data-quiz-score]");
    const firstTry = new Map();

    function updateScore() {
      if (!scoreLine) return;
      const answered = firstTry.size;
      const right = Array.from(firstTry.values()).filter(Boolean).length;
      scoreLine.textContent = answered === questions.length
        ? `First-try score: ${right} of ${questions.length}. Tell me this number in the chat.`
        : `Answered ${answered} of ${questions.length}.`;
    }

    questions.forEach((fieldset, index) => {
      fieldset.addEventListener("change", (event) => {
        const choice = event.target.value;
        const correct = choice === fieldset.dataset.answer;
        if (!firstTry.has(index)) firstTry.set(index, correct);

        for (const box of fieldset.querySelectorAll(".feedback")) {
          box.hidden = box.dataset.for !== choice;
        }
        for (const label of fieldset.querySelectorAll("label")) {
          const input = label.querySelector("input");
          label.classList.toggle("chosen-right", input.checked && correct);
          label.classList.toggle("chosen-wrong", input.checked && !correct);
        }
        updateScore();
      });
      for (const box of fieldset.querySelectorAll(".feedback")) box.hidden = true;
    });
    updateScore();
  }

  document.addEventListener("DOMContentLoaded", setUp);
})();
