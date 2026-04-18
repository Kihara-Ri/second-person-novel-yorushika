from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "texts/source/一人称小说.md"
TARGET = ROOT / "texts/editions/一人称小说_整理阅读版.md"
INDEX_TARGET = ROOT / "texts/indexes/一人称小说_结构索引.md"

MANUAL_OVERRIDES = {
    "1-7": ("老师", "回信"),
    "3-8": ("老师", "回信"),
    "7-7": ("老师", "回信"),
    "9-2": ("我", "来信"),
    "10-1": ("未判定", "异文"),
    "11-1.a": ("我", "来信"),
    "11-1.b": ("老师", "回信"),
    "13-6.a": ("老师", "回信"),
    "13-6.b": ("我", "来信"),
    "13-8": ("老师", "回信"),
    "16-6": ("老师", "回信"),
    "19-8": ("老师", "回信"),
    "19-9": ("老师", "回信"),
    "21-2": ("老师", "回信"),
    "21-1.2": ("老师", "回信"),
    "21-1.4": ("老师", "回信"),
    "23-4": ("我", "附诗"),
    "31-1": ("老师", "回信"),
}

SEPARATOR_SPLIT_IDS = {"3-7", "5-2", "5-3", "14-2", "14-5", "15-3", "16-1", "16-5", "21-1", "21-4", "22-2"}


@dataclass
class Subsection:
    raw_id: str
    content: list[str]
    speaker: str = "未判定"
    kind: str = "文本"
    continued: bool = False
    merged_ids: list[str] = field(default_factory=list)


@dataclass
class Section:
    raw_number: str
    raw_date: str
    subsections: list[Subsection] = field(default_factory=list)


def parse_sections(lines: list[str]) -> tuple[str, list[Section]]:
    title = "# 一人称"
    sections: list[Section] = []
    current_section: Section | None = None
    current_sub: Subsection | None = None

    for line in lines:
        if line.startswith("# "):
            title = line.rstrip()
            continue
        match_h2 = re.match(r"^##\s+(\S+)(?:\s+(.+))?$", line)
        if match_h2:
            if current_sub is not None and current_section is not None:
                current_section.subsections.append(current_sub)
                current_sub = None
            if current_section is not None:
                sections.append(current_section)
            current_section = Section(
                raw_number=match_h2.group(1),
                raw_date=(match_h2.group(2) or "").strip(),
            )
            continue
        match_h3 = re.match(r"^###\s+(.+)$", line)
        if match_h3:
            if current_sub is not None and current_section is not None:
                current_section.subsections.append(current_sub)
            current_sub = Subsection(raw_id=match_h3.group(1).strip(), content=[])
            continue
        if current_sub is not None:
            current_sub.content.append(line.rstrip("\n"))

    if current_sub is not None and current_section is not None:
        current_section.subsections.append(current_sub)
    if current_section is not None:
        sections.append(current_section)

    return title, sections


def strip_edge_blanks(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def split_subsection(sub: Subsection) -> list[Subsection]:
    if sub.raw_id in SEPARATOR_SPLIT_IDS:
        chunks: list[list[str]] = []
        current: list[str] = []
        for line in sub.content:
            if line.strip() == "---":
                chunk = strip_edge_blanks(current)
                if chunk:
                    chunks.append(chunk)
                current = []
                continue
            current.append(line)
        chunk = strip_edge_blanks(current)
        if chunk:
            chunks.append(chunk)
        if len(chunks) > 1:
            return [
                Subsection(raw_id=f"{sub.raw_id}.{i + 1}", content=chunk)
                for i, chunk in enumerate(chunks)
            ]

    if sub.raw_id == "11-1":
        try:
            idx = next(i for i, line in enumerate(sub.content) if line.strip() == "敬具")
        except StopIteration:
            idx = -1
        if idx >= 0:
            first = strip_edge_blanks(sub.content[: idx + 1])
            second = strip_edge_blanks(sub.content[idx + 1 :])
            if first and second:
                return [
                    Subsection(raw_id="11-1.a", content=first),
                    Subsection(raw_id="11-1.b", content=second),
                ]

    if sub.raw_id == "13-6":
        for i, line in enumerate(sub.content):
            if line.strip() == "6/30":
                first = strip_edge_blanks(sub.content[:i])
                second = strip_edge_blanks(sub.content[i:])
                if first and second:
                    return [
                        Subsection(raw_id="13-6.a", content=first),
                        Subsection(raw_id="13-6.b", content=second),
                    ]
                break

    return [sub]


def significant_lines(content: list[str]) -> list[str]:
    return [line.strip() for line in content if line.strip()]


def count_token(text: str, token: str) -> int:
    return text.count(token)


def is_date_line(line: str) -> bool:
    return bool(re.fullmatch(r"\d{1,2}[/-]\d{1,2}(?:\s+\d+)?", line))


def looks_like_poem(sig: list[str]) -> bool:
    if not sig:
        return False
    candidate = sig[:6]
    punctuation_hits = sum(1 for line in candidate if re.search(r"[。！？]", line))
    title_like = False
    first = sig[0]
    if first.startswith("**") and first.endswith("**"):
        title_like = True
    elif (
        len(first) <= 16
        and not re.search(r"[。！？]", first)
        and len(sig) >= 3
        and not re.search(r"[。！？]", sig[1])
    ):
        title_like = True
    line_shortness = sum(1 for line in candidate if len(line) <= 24)
    return title_like or (punctuation_hits <= 1 and line_shortness >= 4)


def infer_metadata(section_number: str, sub: Subsection) -> None:
    sig = significant_lines(sub.content)
    text = "\n".join(sig)
    first = sig[0] if sig else ""
    second = sig[1] if len(sig) > 1 else ""

    if section_number == "29":
        sub.speaker = "老师"
        if first == "P.S.":
            sub.kind = "补遗追伸"
        else:
            sub.kind = "补遗回信"
        return

    if sub.raw_id in MANUAL_OVERRIDES:
        sub.speaker, sub.kind = MANUAL_OVERRIDES[sub.raw_id]
        return

    if "---" in sub.content:
        sub.speaker = "我 / 老师"
        sub.kind = "混合文本"
        return

    if first == "P.S.":
        sub.speaker = "老师"
        sub.kind = "追伸"
        return

    if is_date_line(first) and second == "拝啓":
        sub.speaker = "我"
        sub.kind = "来信"
        return

    if is_date_line(first) and (count_token(text, "僕") > 0 or count_token(text, "先生") > 0):
        sub.speaker = "我"
        sub.kind = "来信"
        return

    if first.startswith(("私は", "それは、私", "私にとって", "原稿用紙について", "ちなみに", "離思を調べてくれたんだね")):
        sub.speaker = "老师"
        sub.kind = "回信"
        return

    if first == "拝啓" and count_token(text, "君") > 0 and count_token(text, "先生") == 0 and count_token(text, "僕") == 0:
        sub.speaker = "老师"
        sub.kind = "回信"
        return

    if first == "拝啓":
        sub.speaker = "我"
        sub.kind = "来信"
        return

    if looks_like_poem(sig):
        sub.speaker = "我"
        sub.kind = "附诗"
        return

    if first.startswith(("先生", "母さん", "僕")):
        sub.speaker = "我"
        sub.kind = "来信"
        return

    if "敬具" in text and count_token(text, "私") == 0:
        sub.speaker = "我"
        sub.kind = "来信"
        return

    if count_token(text, "僕") > count_token(text, "私"):
        sub.speaker = "我"
        sub.kind = "来信"
        return

    if count_token(text, "先生") >= 2 and count_token(text, "君") == 0:
        sub.speaker = "我"
        sub.kind = "来信"
        return

    if count_token(text, "君") >= 1 or "手紙をありがとう" in text or "詩を読みました" in text:
        sub.speaker = "老师"
        sub.kind = "回信"
        return

    if any(marker in text for marker in ["お母さん", "彼", "許します"]):
        sub.speaker = "老师"
        sub.kind = "回信"
        return

    sub.speaker = "未判定"
    sub.kind = "文本"


def merge_key(raw_id: str) -> str:
    if " " in raw_id:
        return raw_id.split()[0]
    if "-" in raw_id:
        return raw_id.split("-")[0]
    return raw_id


def should_merge(section_number: str, previous: Subsection, current: Subsection) -> bool:
    if previous.speaker != current.speaker or previous.kind != current.kind:
        return False
    if section_number == "29":
        return merge_key(previous.raw_id) == merge_key(current.raw_id)
    current_sig = significant_lines(current.content)
    if not current_sig:
        return True
    first = current_sig[0]
    if current.kind == "附诗":
        if first.startswith("**") and first.endswith("**"):
            return False
        if len(first) <= 16 and not re.search(r"[。！？]", first):
            return False
        return True
    if current.kind in {"来信", "回信", "补遗回信"}:
        if first in {"拝啓", "P.S."}:
            return False
        if is_date_line(first):
            return False
        if first.startswith("手紙をありがとう") or first.startswith("詩を読みました"):
            return False
        return True
    return False


def merge_subsections(section_number: str, subsections: list[Subsection]) -> list[Subsection]:
    merged: list[Subsection] = []
    for sub in subsections:
        sub.merged_ids = [sub.raw_id]
        if merged and should_merge(section_number, merged[-1], sub):
            merged[-1].content.extend(["", *sub.content])
            merged[-1].merged_ids.append(sub.raw_id)
            merged[-1].continued = True
            continue
        merged.append(sub)
    return merged


def section_label(section: Section) -> str:
    if section.raw_number == "29":
        return "## 补遗｜被截留或延后送达的回信"
    number = int(section.raw_number)
    date = f"｜{section.raw_date}" if section.raw_date else ""
    return f"## 第{number:02d}组通信{date}"


def unit_title(index: int, sub: Subsection) -> str:
    return f"### 单元 {index:02d}｜{sub.speaker}{sub.kind}"


def clean_source_title(title: str) -> str:
    if title.startswith("# "):
        return title[2:].strip()
    return title.strip()


def emit(title: str, sections: list[Section]) -> str:
    out: list[str] = []
    out.append(f"# {clean_source_title(title)}｜整理阅读版")
    out.append("")
    out.append("> [整理说明] 本文件为阅读用整理稿。原稿保留在 `texts/source/一人称小说.md`。")
    out.append("> [整理说明] 本稿优先优化阅读顺序与结构辨识，不改写正文，不删除删改痕迹与校注。")
    out.append("> [整理说明] `## 29` 被明确标注为补遗区；连续的来信、附诗、回信会在同组内合并为可读单元。")
    out.append("")
    for section in sections:
        out.append(section_label(section))
        out.append("")
        if section.raw_number == "29":
            out.append("> [整理说明] 本组为后置补遗，内容对应此前未被及时读到的老师回信。")
            out.append("")
        merged = merge_subsections(section.raw_number, section.subsections)
        for idx, sub in enumerate(merged, start=1):
            out.append(unit_title(idx, sub))
            out.append("")
            out.append(f"> [整理标注] 原编号：{', '.join(sub.merged_ids)}")
            out.append(f"> [整理标注] 推定说话人：{sub.speaker}")
            out.append(f"> [整理标注] 推定文本类型：{sub.kind}")
            if sub.continued:
                out.append("> [整理标注] 本单元由连续分页或续写片段合并而成。")
            out.append("")
            out.extend(sub.content)
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def emit_index(title: str, sections: list[Section]) -> str:
    out: list[str] = []
    out.append(f"# {clean_source_title(title)}｜结构索引")
    out.append("")
    out.append("> [索引说明] 本文件根据整理规则自动生成，用于梳理通信组、说话人、文本类型与原编号对应关系。")
    out.append("> [索引说明] `第29组` 在原稿中为 `## 29`，此处按“补遗”处理。")
    out.append("")
    out.append("| 组别 | 日期 | 单元 | 说话人 | 类型 | 原编号 | 备注 |")
    out.append("| --- | --- | --- | --- | --- | --- | --- |")
    for section in sections:
        merged = merge_subsections(section.raw_number, section.subsections)
        section_name = "补遗" if section.raw_number == "29" else f"第{int(section.raw_number):02d}组"
        section_date = section.raw_date or "-"
        if section.raw_number == "29":
            section_date = "补遗"
        for idx, sub in enumerate(merged, start=1):
            notes: list[str] = []
            if sub.continued:
                notes.append("连续分页/续写")
            if sub.kind == "异文":
                notes.append("需保留特殊状态")
            out.append(
                f"| {section_name} | {section_date} | {idx:02d} | {sub.speaker} | {sub.kind} | {', '.join(sub.merged_ids)} | {'；'.join(notes) or '-'} |"
            )
    out.append("")
    return "\n".join(out)


def main() -> None:
    title, sections = parse_sections(SOURCE.read_text(encoding="utf-8").splitlines())
    for section in sections:
        expanded: list[Subsection] = []
        for sub in section.subsections:
            expanded.extend(split_subsection(sub))
        section.subsections = expanded
        for sub in section.subsections:
            infer_metadata(section.raw_number, sub)
    TARGET.write_text(emit(title, sections), encoding="utf-8")
    INDEX_TARGET.write_text(emit_index(title, sections), encoding="utf-8")


if __name__ == "__main__":
    main()
