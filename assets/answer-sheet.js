// Answer sheet: collects every <textarea data-answer="1a" data-label="…"> inside
// <section data-answer-sheet="0001">, keeps a draft in this browser, and copies
// the answers as Markdown to paste into the chat for grading.
//
// The sheet needs:  <button data-sheet-copy>, <button data-sheet-clear>,
//                   <span class="sheet-status">, <pre class="sheet-output" hidden>

(function () {
  function storageGet(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function storageSet(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* drafts are a convenience */ }
  }
  function storageRemove(key) {
    try { window.localStorage.removeItem(key); } catch (e) { /* ignore */ }
  }

  function setUp(sheet) {
    const lessonId = sheet.dataset.answerSheet;
    const title = sheet.dataset.title || "Lesson " + lessonId;
    const fields = Array.from(document.querySelectorAll("textarea[data-answer]"));
    const status = sheet.querySelector(".sheet-status");
    const output = sheet.querySelector(".sheet-output");
    const keyFor = (field) => "answers:" + lessonId + ":" + field.dataset.answer;

    for (const field of fields) {
      const draft = storageGet(keyFor(field));
      if (draft !== null) field.value = draft;
      field.addEventListener("input", () => storageSet(keyFor(field), field.value));
    }

    function asMarkdown() {
      const lines = ["## " + title + ": my answers", ""];
      for (const field of fields) {
        const answer = field.value.trim() || "(no answer)";
        lines.push("**" + field.dataset.label + "**", answer, "");
      }
      return lines.join("\n");
    }

    sheet.querySelector("[data-sheet-copy]").addEventListener("click", async () => {
      const text = asMarkdown();
      output.textContent = text;
      output.hidden = false;
      try {
        await navigator.clipboard.writeText(text);
        status.textContent = "Copied. Paste it into the chat.";
      } catch (e) {
        status.textContent = "Couldn't reach the clipboard. Select the text below and copy it.";
      }
    });

    sheet.querySelector("[data-sheet-clear]").addEventListener("click", () => {
      if (!window.confirm("Clear every answer on this page?")) return;
      for (const field of fields) {
        field.value = "";
        storageRemove(keyFor(field));
      }
      output.hidden = true;
      status.textContent = "Cleared.";
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-answer-sheet]").forEach(setUp);
  });
})();
