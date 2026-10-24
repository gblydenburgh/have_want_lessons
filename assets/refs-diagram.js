// Name → object diagrams: names on the left, objects on the right, and an arrow
// from each name to the object it refers to (the style of Ned Batchelder's
// "Facts and Myths about Python names and values").
//
// <figure class="refs" data-refs='{
//   "names":   [{"name": "have", "to": "d1"}, {"name": "want", "to": "d1"}],
//   "objects": [{"id": "d1", "type": "dict", "lines": ["&#39;vlan_id&#39;: 10"]}]
// }'>
//   <figcaption>After line 2</figcaption>
// </figure>
//
// The attribute is single-quoted, so write a ' inside it as &#39;.
//
// Optional on a name: "note" (small text after the box, e.g. "local"),
// "faded": true (a name that no longer exists).
// Optional on an object: "faded": true (an object no name refers to any more);
// "col": 2 (or 3…) to draw it in a further column, for objects that other
// objects refer to; "top": a y position in px within its column, to move it
// clear of arrows that would otherwise cross a box.
//
// Objects that refer to objects: a line can be {"text": "instance", "to": "r1"}
// instead of a string. An arrow runs from that line to the object "r1", which
// should sit in a later column.

(function () {
  const SVG = "http://www.w3.org/2000/svg";
  const CHAR = 7.9;          // approximate width of one 13px monospace character
  const NAME_H = 28;
  const NAME_GAP = 16;
  const LINE_H = 18;
  const OBJ_GAP = 18;
  const ARROW_SPAN = 120;    // horizontal room between names and objects
  const COL_GAP = 90;        // horizontal room between object columns

  function el(tag, attrs, parent) {
    const node = document.createElementNS(SVG, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (parent) parent.appendChild(node);
    return node;
  }

  function text(parent, x, y, content, cls) {
    const node = el("text", { x, y, class: cls || "" }, parent);
    node.textContent = content;
    return node;
  }

  const lineText = (line) => (typeof line === "string" ? line : line.text);
  const lineY = (box, i) => box.y + 24 + (i + 1) * LINE_H - 4;   // text baseline

  function arrow(svg, a) {
    const list = a.target.incoming;
    const i = list.indexOf(a);
    const x2 = a.target.x - 1;
    const y2 = a.target.y + a.target.h / 2 + (i - (list.length - 1) / 2) * 12;
    const g = el("g", { class: "ref-link" + (a.faded ? " faded" : "") }, svg);
    el("line", { x1: a.x1, y1: a.y1, x2: x2 - 7, y2, class: "ref-arrow" }, g);
    const angle = Math.atan2(y2 - a.y1, x2 - a.x1);
    const back = (d, spread) => [
      x2 - d * Math.cos(angle) + spread * Math.sin(angle),
      y2 - d * Math.sin(angle) - spread * Math.cos(angle),
    ];
    const p1 = back(9, 4.5);
    const p2 = back(9, -4.5);
    el("polygon", { points: `${x2},${y2} ${p1.join(",")} ${p2.join(",")}`, class: "ref-head" }, g);
  }

  function draw(figure) {
    let spec;
    try { spec = JSON.parse(figure.dataset.refs); } catch (e) { return; }
    const names = spec.names || [];
    const objects = spec.objects || [];

    const nameW = Math.max(...names.map((n) => n.name.length), 3) * CHAR + 20;
    const noteW = Math.max(0, ...names.map((n) => (n.note ? n.note.length * 6.5 + 8 : 0)));

    // Size each object, then place the columns left to right.
    const widthOf = (obj) =>
      Math.max(...(obj.lines || []).map((l) => lineText(l).length), (obj.type || "").length, 6) * CHAR + 24;
    const cols = [...new Set(objects.map((o) => o.col || 1))].sort((a, b) => a - b);
    const colX = new Map();
    let x = nameW + noteW + ARROW_SPAN;
    for (const c of cols) {
      colX.set(c, x);
      x += Math.max(...objects.filter((o) => (o.col || 1) === c).map(widthOf)) + COL_GAP;
    }

    // Lay out each column's objects top to bottom.
    const colY = new Map(cols.map((c) => [c, 4]));
    const objBox = new Map();
    for (const obj of objects) {
      const c = obj.col || 1;
      const y = typeof obj.top === "number" ? Math.max(obj.top, colY.get(c)) : colY.get(c);
      const height = 24 + (obj.lines || []).length * LINE_H + 8;
      objBox.set(obj.id, { x: colX.get(c), y, w: widthOf(obj), h: height, obj, incoming: [] });
      colY.set(c, y + height + OBJ_GAP);
    }
    const objectsH = Math.max(4, ...colY.values()) - OBJ_GAP;
    const namesH = names.length * NAME_H + (names.length - 1) * NAME_GAP;
    const totalH = Math.max(objectsH, namesH) + 8;
    const totalW = Math.max(...[...objBox.values()].map((b) => b.x + b.w), nameW + noteW + ARROW_SPAN) + 4;

    const describe = (box) => {
      const lines = (box.obj.lines || []).map((l) => {
        const to = typeof l === "string" ? null : objBox.get(l.to);
        return to ? `${l.text} refers to the ${to.obj.type || "object"}` : lineText(l);
      });
      return `${box.obj.type || "an object"} ${lines.join(", ")}`;
    };
    const svg = el("svg", {
      viewBox: `0 0 ${totalW} ${totalH}`,
      width: totalW,
      height: totalH,
      role: "img",
      "aria-label": names.map((n) => {
        const box = objBox.get(n.to);
        return `${n.name} refers to ${box ? describe(box) : "nothing"}`;
      }).join("; "),
    });

    // Names, vertically centred against the objects.
    let ny = 4 + Math.max(0, (objectsH - namesH) / 2);
    const arrows = [];
    for (const n of names) {
      const g = el("g", { class: "ref-name" + (n.faded ? " faded" : "") }, svg);
      el("rect", { x: 1, y: ny, width: nameW, height: NAME_H, rx: 3 }, g);
      text(g, 11, ny + 18.5, n.name);
      if (n.note) text(g, nameW + 6, ny + 18, n.note, "ref-note");
      const target = objBox.get(n.to);
      if (target) {
        const startX = nameW + 1 + (n.note ? noteW : 0);
        const a = { x1: startX, y1: ny + NAME_H / 2, target, faded: n.faded };
        target.incoming.push(a);
        arrows.push(a);
      }
      ny += NAME_H + NAME_GAP;
    }

    // Objects, and arrows from any line that refers to another object.
    for (const box of objBox.values()) {
      const g = el("g", { class: "ref-obj" + (box.obj.faded ? " faded" : "") }, svg);
      el("rect", { x: box.x, y: box.y, width: box.w, height: box.h, rx: 4 }, g);
      text(g, box.x + 10, box.y + 16, box.obj.type || "", "ref-type");
      (box.obj.lines || []).forEach((line, i) => {
        text(g, box.x + 12, lineY(box, i), lineText(line));
        const target = typeof line === "string" ? null : objBox.get(line.to);
        if (target) {
          const a = { x1: box.x + box.w + 1, y1: lineY(box, i) - 4, target, faded: box.obj.faded };
          target.incoming.push(a);
          arrows.push(a);
        }
      });
    }

    // Arrows, spread out where several arrive at one object, in the order they
    // start top to bottom so they don't cross.
    for (const box of objBox.values()) box.incoming.sort((p, q) => p.y1 - q.y1);
    for (const a of arrows) arrow(svg, a);

    figure.insertBefore(svg, figure.firstChild);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("figure.refs[data-refs]").forEach(draw);
  });
})();
