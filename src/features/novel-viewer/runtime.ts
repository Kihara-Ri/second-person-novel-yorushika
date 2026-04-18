import styles from "./NovelViewerPage.module.css";
import type { PreparedGroup, PreparedParagraph, PreviewGroupPayload, TermNote } from "./types";

const PLACEHOLDER_NOTE_MARKERS = [
  "当前尚未补入详细人工词条",
  "前端至少应显示注音",
  "后续优先补写的疑难词候选",
];

export function escapeHtml(text: string) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

export function hasDetailedNote(note: TermNote) {
  const longNote = note.long_note || "";
  return !PLACEHOLDER_NOTE_MARKERS.some((marker) => longNote.includes(marker));
}

function shouldAnnotateTerm(note: TermNote) {
  return Boolean(note.reading || hasDetailedNote(note));
}

function buildNoteMarkup(labelHtml: string, note: TermNote) {
  return `
    <span
      class="${styles.termHit} ${styles.hasNote}"
      data-note-term="${escapeHtml(note.term)}"
      data-note-reading="${escapeHtml(note.reading ?? "")}"
      data-note-short-gloss="${escapeHtml(note.short_gloss ?? "")}"
      data-note-long-note="${escapeHtml(note.long_note ?? "")}"
    >
      ${labelHtml}
    </span>
  `;
}

function annotatePlainText(text: string, termNotes: TermNote[]) {
  const annotatableNotes = termNotes.filter(shouldAnnotateTerm);
  if (!annotatableNotes.length) return escapeHtml(text);

  const hits: Array<{ start: number; end: number; note: TermNote }> = [];
  for (const note of annotatableNotes) {
    const needle = note.matched_text || note.term;
    if (!needle) continue;

    let fromIndex = 0;
    while (fromIndex < text.length) {
      const index = text.indexOf(needle, fromIndex);
      if (index === -1) break;
      hits.push({
        start: index,
        end: index + needle.length,
        note,
      });
      fromIndex = index + needle.length;
    }
  }

  hits.sort((a, b) => {
    if (a.start !== b.start) return a.start - b.start;
    return b.end - a.end;
  });

  const filtered = [];
  let cursor = -1;
  for (const hit of hits) {
    if (hit.start < cursor) continue;
    filtered.push(hit);
    cursor = hit.end;
  }

  if (!filtered.length) return escapeHtml(text);

  let html = "";
  let position = 0;
  for (const hit of filtered) {
    html += escapeHtml(text.slice(position, hit.start));
    const matchedText = text.slice(hit.start, hit.end);
    const ruby = hit.note.reading
      ? `<ruby><span>${escapeHtml(matchedText)}</span><rt>${escapeHtml(hit.note.reading)}</rt></ruby>`
      : escapeHtml(matchedText);
    html += hasDetailedNote(hit.note)
      ? buildNoteMarkup(ruby, hit.note)
      : `<span class="${styles.termReading}">${ruby}</span>`;
    position = hit.end;
  }
  html += escapeHtml(text.slice(position));
  return html;
}

export function renderInline(text: string, termNotes: TermNote[]) {
  let html = "";
  let lastIndex = 0;

  text.replace(/\{([^|}]+)\|([^}]+)\}/g, (match, term, reading, offset) => {
    html += annotatePlainText(text.slice(lastIndex, offset), termNotes);
    const hit = termNotes.find((note) => note.matched_text === term || note.term === term);
    const ruby = `<ruby><span>${escapeHtml(term)}</span><rt>${escapeHtml(reading)}</rt></ruby>`;
    html += hit && hasDetailedNote(hit) ? buildNoteMarkup(ruby, hit) : `<span class="${styles.termReading}">${ruby}</span>`;
    lastIndex = offset + match.length;
    return match;
  });

  html += annotatePlainText(text.slice(lastIndex), termNotes);
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/~~([^~]+)~~/g, "<del>$1</del>");
  return html;
}

function splitInlineTeacherNotes(text: string, noteStart: number) {
  const notes: Array<{ id: number; text: string }> = [];
  let current = noteStart;
  const cleaned = text.replace(/\{([^{}]+)\}\^\[([^\]]+)\]/g, (_match, body, note) => {
    current += 1;
    notes.push({ id: current, text: note.trim() });
    return `${body}@@TEACHER_NOTE_${current}@@`;
  });
  return { cleaned, notes, nextIndex: current };
}

function injectTeacherNoteAnchors(html: string) {
  return html.replaceAll(
    /@@TEACHER_NOTE_(\d+)@@/g,
    (_match, id) => `<sup class="${styles.teacherNoteAnchor}">※${id}</sup>`,
  );
}

export function renderMarkdown(md: string, termNotes: TermNote[]) {
  const normalizedMd = md.replace(/<br\s*\/?>/gi, "\n");
  const teacherNotes: Array<{ id: number; text: string }> = [];
  let noteIndex = 0;
  const blocks = normalizedMd.split(/\n{2,}/).filter(Boolean);
  const html = blocks
    .map((block) => {
      const lines = block.split("\n");
      const mainLines: string[] = [];
      const appendLines: string[] = [];

      for (const line of lines) {
        const result = splitInlineTeacherNotes(line, noteIndex);
        noteIndex = result.nextIndex;
        const { cleaned, notes } = result;
        teacherNotes.push(...notes);
        if (cleaned.trim().startsWith(">")) {
          appendLines.push(cleaned.replace(/^\s*>\s?/, ""));
        } else {
          mainLines.push(cleaned);
        }
      }

      const parts: string[] = [];
      if (mainLines.length) {
        const renderedLines = mainLines.map((line) =>
          injectTeacherNoteAnchors(renderInline(line, termNotes)),
        );
        parts.push(`<p>${renderedLines.join("<br>")}</p>`);
      }

      if (appendLines.length) {
        const appendHtml = appendLines
          .map(
            (line) =>
              `<p class="${styles.paperAdditionLine}">${injectTeacherNoteAnchors(renderInline(line, termNotes))}</p>`,
          )
          .join("");
        parts.push(`<aside class="${styles.paperAdditions}">${appendHtml}</aside>`);
      }

      return parts.join("");
    })
    .join("");

  if (!teacherNotes.length) return html;

  const notesHtml = teacherNotes
    .map(
      (note) =>
        `<p class="${styles.letterNote}"><span class="${styles.teacherNoteLabel}">※${note.id}</span>${renderInline(note.text, termNotes)}</p>`,
    )
    .join("");
  return `${html}<aside class="${styles.sectionNotes}">${notesHtml}</aside>`;
}

function preprocessParagraph(paragraph: {
  para_id: string;
  para_label: string;
  render_mode: string;
  source_md: string;
  target_md: string;
  notes: string[];
  term_notes: TermNote[];
  search_text: string;
}): PreparedParagraph {
  return {
    ...paragraph,
    sourceHtml: renderMarkdown(paragraph.source_md, paragraph.term_notes),
    targetHtml: renderMarkdown(paragraph.target_md, paragraph.term_notes),
  };
}

export function prepareLoadedGroup(group: PreviewGroupPayload): PreparedGroup {
  const displayUnits = group.display_units.map((unit) => ({
    ...unit,
    paragraphs: unit.paragraphs.map(preprocessParagraph),
    titleSourceHtml: unit.titleSource ? renderInline(unit.titleSource, unit.titleTermNotes ?? []) : "",
    titleTargetHtml:
      unit.titleTarget && unit.titleTarget !== unit.titleSource
        ? renderInline(unit.titleTarget, unit.titleTermNotes ?? [])
        : "",
  }));

  return {
    ...group,
    display_units: displayUnits,
    units_by_id: Object.fromEntries(displayUnits.map((unit) => [unit.unit_id, unit])),
  };
}

function highlightTextNode(node: Text, query: string) {
  const text = node.nodeValue ?? "";
  const lowerText = text.toLowerCase();
  const lowerQuery = query.toLowerCase();
  let fromIndex = 0;
  let matchIndex = lowerText.indexOf(lowerQuery, fromIndex);

  if (matchIndex === -1 || !node.parentNode) return;

  const fragment = document.createDocumentFragment();
  while (matchIndex !== -1) {
    if (matchIndex > fromIndex) {
      fragment.appendChild(document.createTextNode(text.slice(fromIndex, matchIndex)));
    }

    const mark = document.createElement("mark");
    mark.className = styles.searchHit;
    mark.textContent = text.slice(matchIndex, matchIndex + query.length);
    fragment.appendChild(mark);

    fromIndex = matchIndex + query.length;
    matchIndex = lowerText.indexOf(lowerQuery, fromIndex);
  }

  if (fromIndex < text.length) {
    fragment.appendChild(document.createTextNode(text.slice(fromIndex)));
  }

  node.parentNode.replaceChild(fragment, node);
}

function applySearchHighlight(root: ParentNode, query: string) {
  if (!query) return;

  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.nodeValue || !node.nodeValue.trim()) {
        return NodeFilter.FILTER_REJECT;
      }

      const parent = node.parentElement;
      if (!parent) {
        return NodeFilter.FILTER_REJECT;
      }

      if (
        parent.closest(
          `rt, .${styles.letterNote}`,
        )
      ) {
        return NodeFilter.FILTER_REJECT;
      }

      return node.nodeValue.toLowerCase().includes(query.toLowerCase())
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_REJECT;
    },
  });

  const nodes: Text[] = [];
  while (walker.nextNode()) {
    nodes.push(walker.currentNode as Text);
  }
  nodes.forEach((textNode) => highlightTextNode(textNode, query));
}

export function highlightRenderedHtml(html: string, query: string) {
  if (!query || typeof document === "undefined") return html;
  const template = document.createElement("template");
  template.innerHTML = html;
  applySearchHighlight(template.content, query);
  return template.innerHTML;
}
