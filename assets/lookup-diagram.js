// Attribute-lookup diagrams: the objects Python searches for `obj.name`, in
// order (the instance, then its class, later its parent classes), with the
// row where the name is found highlighted and anything after it faded.
//
// <figure class="lookup" data-lookup='{
//   "expr": "sw1.commands",
//   "find": "commands",
//   "chain": [
//     {"title": "sw1", "kind": "instance of ConfigPush",
//      "attrs": [["hostname", "&#39;sw1&#39;"]]},
//     {"title": "ConfigPush", "kind": "class",
//      "attrs": [["commands", "[…]"], ["add", "function"]]}
//   ]
// }'>
//   <figcaption>…</figcaption>
// </figure>
//
// The attribute is single-quoted, so write a ' inside it as &#39;.
// Optional on a box after the first: "link", the text of the step into it
// (default "look in its class"). If no box has the name, the diagram ends
// with Python's AttributeError.

(function () {
  function el(tag, cls, parent, content) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (content !== undefined) node.textContent = content;
    if (parent) parent.appendChild(node);
    return node;
  }

  function code(parent, content) {
    return el("code", "", parent, content);
  }

  function draw(figure) {
    const spec = JSON.parse(figure.dataset.lookup);
    const caption = figure.querySelector("figcaption");
    const wrap = el("div", "lookup-chain");

    const head = el("p", "lookup-head", wrap, "Python reads ");
    code(head, spec.expr || spec.find);

    let foundAt = -1;
    spec.chain.forEach((box, index) => {
      const hasIt = box.attrs.some(([name]) => name === spec.find);
      const reached = foundAt === -1;

      if (index > 0) {
        const step = el("p", "lookup-step" + (reached ? "" : " faded"), wrap);
        el("span", "lookup-arrow", step, "↓ ");
        step.append("no ");
        code(step, spec.find);
        step.append(" on " + spec.chain[index - 1].title + ": "
          + (box.link || "look in its class"));
      }

      const card = el("div", "lookup-box" + (reached ? "" : " faded"), wrap);
      const title = el("p", "lookup-title", card);
      code(title, box.title);
      el("span", "lookup-kind", title, " " + box.kind);

      const rows = el("dl", "lookup-attrs", card);
      for (const [name, value] of box.attrs) {
        const isHit = name === spec.find && reached;
        const dt = el("dt", isHit ? "found" : "", rows);
        code(dt, name);
        const dd = el("dd", isHit ? "found" : "", rows);
        code(dd, value);
        if (isHit) el("span", "lookup-tag", dd, "found here");
        else if (name === spec.find) el("span", "lookup-tag muted", dd, "not reached");
      }
      if (hasIt && reached) foundAt = index;
    });

    if (foundAt === -1) {
      const end = el("p", "lookup-step lookup-error", wrap);
      el("span", "lookup-arrow", end, "↓ ");
      end.append("not found anywhere: ");
      code(end, "AttributeError");
    }

    figure.insertBefore(wrap, caption);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("figure.lookup[data-lookup]").forEach(draw);
  });
})();
