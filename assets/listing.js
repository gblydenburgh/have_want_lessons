// Numbered code listings that stay in view.
//
// <pre class="listing" id="code">…</pre>  gets one numbered span per line.
// <div class="listing-again" data-listing="code"></div>  gets a collapsible
// copy of that listing, so a question can repeat the code on narrow screens
// (on wide screens CSS hides it, because the listing pane stays visible).

(function () {
  function numberLines(pre) {
    const lines = pre.textContent.replace(/\n$/, "").split("\n");
    pre.textContent = "";
    for (const line of lines) {
      const span = document.createElement("span");
      span.className = "ln";
      span.textContent = line === "" ? " " : line;
      pre.appendChild(span);
    }
  }

  function repeatListings() {
    for (const slot of document.querySelectorAll(".listing-again[data-listing]")) {
      const source = document.getElementById(slot.dataset.listing);
      if (!source) continue;
      const details = document.createElement("details");
      const summary = document.createElement("summary");
      summary.textContent = "Show the code again";
      details.appendChild(summary);
      details.appendChild(source.cloneNode(true)).removeAttribute("id");
      slot.appendChild(details);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("pre.listing").forEach(numberLines);
    repeatListings();
  });
})();
