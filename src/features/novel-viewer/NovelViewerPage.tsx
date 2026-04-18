import { useEffect, useRef, useState } from "react";

import styles from "./NovelViewerPage.module.css";
import coverArt from "../ヨルシカ-yorushika-二人称-Cover-Art.webp";

import { highlightRenderedHtml, renderInline } from "./runtime";
import type { PreparedParagraph, PreparedUnit, PreviewGroupMeta } from "./types";
import { useNovelViewer } from "./useNovelViewer";

function ParagraphBlock({ paragraph, query }: { paragraph: PreparedParagraph; query: string }) {
  return (
    <section className={styles.paragraphBlock}>
      <div className={styles.parallelText}>
        <section className={`${styles.textSection} ${styles.sourceSection}`}>
          <div
            className={styles.textBody}
            dangerouslySetInnerHTML={{ __html: highlightRenderedHtml(paragraph.sourceHtml, query) }}
          />
        </section>
        <section className={`${styles.textSection} ${styles.targetSection}`}>
          <div
            className={styles.textBody}
            dangerouslySetInnerHTML={{ __html: highlightRenderedHtml(paragraph.targetHtml, query) }}
          />
        </section>
      </div>
    </section>
  );
}

function UnitCard({
  unit,
  query,
  groupLabel,
  dateLabel,
}: {
  unit: PreparedUnit;
  query: string;
  groupLabel?: string;
  dateLabel?: string;
}) {
  const titleText = groupLabel ? `${groupLabel}｜${unit.speaker}` : unit.speaker;
  const refsText = groupLabel
    ? `${dateLabel}｜原文编号：${unit.source_refs.join(", ") || "无"}`
    : `原文编号：${unit.source_refs.join(", ") || "无"}`;

  return (
    <article className={styles.unitCard}>
      <header className={styles.unitHead}>
        <div className={styles.unitTitleRow}>
          <h3 className={styles.unitTitle}>{titleText}</h3>
          <span className={styles.unitBadge}>{unit.type}</span>
        </div>
        <p className={styles.unitRefs}>{refsText}</p>
        {unit.titleSourceHtml ? (
          <p
            className={styles.unitPoemTitle}
            dangerouslySetInnerHTML={{ __html: highlightRenderedHtml(unit.titleSourceHtml, query) }}
          />
        ) : null}
        {unit.titleTargetHtml ? (
          <p
            className={styles.unitPoemSubtitle}
            dangerouslySetInnerHTML={{ __html: highlightRenderedHtml(unit.titleTargetHtml, query) }}
          />
        ) : null}
      </header>

      <div className={styles.unitColumnsHead}>
        <span>原文</span>
        <span>译文</span>
      </div>

      <div className={styles.paragraphList}>
        {unit.paragraphs.map((paragraph) => (
          <ParagraphBlock key={paragraph.para_id} paragraph={paragraph} query={query} />
        ))}
      </div>
    </article>
  );
}

function GroupNav({
  groups,
  activeGroupId,
  searchQuery,
  onSelectGroup,
}: {
  groups: PreviewGroupMeta[];
  activeGroupId: string | null;
  searchQuery: string;
  onSelectGroup: (groupId: string) => void;
}) {
  return (
    <nav className={styles.groupNav}>
      {groups.map((group) => {
        const isActive = group.group_id === activeGroupId && !searchQuery;
        return (
          <button
            key={group.group_id}
            className={`${styles.navButton} ${isActive ? styles.navButtonActive : ""}`}
            onClick={() => onSelectGroup(group.group_id)}
            type="button"
          >
            {group.group_label}
            <small>{group.date_label}</small>
            {group.poem_titles.length ? (
              <small
                className={styles.navPoems}
                dangerouslySetInnerHTML={{
                  __html: group.poem_titles.map((title) => renderInline(title, [])).join("・"),
                }}
              />
            ) : null}
          </button>
        );
      })}
    </nav>
  );
}

export function NovelViewerPage() {
  const viewerRef = useRef<HTMLDivElement | null>(null);
  const [tooltip, setTooltip] = useState<null | {
    x: number;
    y: number;
    term: string;
    reading: string;
    shortGloss: string;
    longNote: string;
  }>(null);
  const {
    dataset,
    activeGroupId,
    activeGroup,
    searchInput,
    searchQuery,
    searchMatches,
    searchResults,
    renderedCount,
    status,
    error,
    selectGroup,
    updateSearch,
    loadMore,
  } = useNovelViewer();

  const activeMeta = dataset?.groups.find((group) => group.group_id === activeGroupId) ?? null;

  useEffect(() => {
    const root = viewerRef.current;
    if (!root) return;
    const host = root;

    const triggerSelector = `.${styles.termHit}.${styles.hasNote}`;
    let activeTrigger: HTMLElement | null = null;

    function setTooltipFromTrigger(trigger: HTMLElement, event: MouseEvent) {
      if (activeTrigger !== trigger) {
        activeTrigger = trigger;
      }
      setTooltip({
        x: event.clientX,
        y: event.clientY,
        term: trigger.dataset.noteTerm ?? "",
        reading: trigger.dataset.noteReading ?? "",
        shortGloss: trigger.dataset.noteShortGloss ?? "",
        longNote: trigger.dataset.noteLongNote ?? "",
      });
    }

    function clearTooltip() {
      if (!activeTrigger) return;
      activeTrigger = null;
      setTooltip(null);
    }

    function handleMouseMove(event: MouseEvent) {
      const pointed = document.elementFromPoint(event.clientX, event.clientY);
      const trigger = pointed instanceof Element ? pointed.closest(triggerSelector) : null;
      if (trigger instanceof HTMLElement) {
        setTooltipFromTrigger(trigger, event);
        return;
      }
      clearTooltip();
    }

    function handleScroll() {
      clearTooltip();
    }

    function handleMouseLeaveWindow() {
      clearTooltip();
    }

    host.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("scroll", handleScroll, true);
    window.addEventListener("blur", handleMouseLeaveWindow);
    document.addEventListener("mouseleave", handleMouseLeaveWindow);

    return () => {
      host.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("scroll", handleScroll, true);
      window.removeEventListener("blur", handleMouseLeaveWindow);
      document.removeEventListener("mouseleave", handleMouseLeaveWindow);
    };
  }, [activeGroupId, searchQuery, searchResults.length]);

  return (
    <div className={styles.viewerShell} ref={viewerRef}>
      <aside className={styles.sidebar}>
        <div className={styles.sidebarHead}>
          <p className={styles.eyebrow}>Kihara Archive</p>
          <div className={styles.sidebarTitleRow}>
            <div className={styles.sidebarTitleBox}>
              <h1>二人称</h1>
              <p className={styles.sidebarCopy}>ヨルシカ</p>
            </div>
            <a
              className={styles.coverLink}
              href="https://yorushika.com/"
              target="_blank"
              rel="noreferrer"
              aria-label="打开ヨルシカ官方网站"
            >
              <img className={styles.coverArt} src={coverArt} alt="二人称专辑封面" />
            </a>
          </div>
        </div>

        <div className={styles.toolbar}>
          <label className={styles.searchWrap}>
            <span>搜索</span>
            <input
              type="search"
              placeholder="搜索原文、译文或词条"
              value={searchInput}
              onChange={(event) => updateSearch(event.target.value)}
            />
          </label>
        </div>

        <div className={styles.navScroll}>
          {dataset ? (
            <GroupNav
              groups={dataset.groups}
              activeGroupId={activeGroupId}
              searchQuery={searchQuery}
              onSelectGroup={selectGroup}
            />
          ) : null}
        </div>
      </aside>

      <main className={styles.content}>
        <header className={styles.contentHead}>
          <div className={styles.contentTitleWrap}>
            {searchQuery ? (
              <h2>全局搜索</h2>
            ) : (
              <h2>{activeMeta ? activeMeta.group_label : "加载中…"}</h2>
            )}
          </div>
          <div className={styles.contentMeta}>
            {searchQuery ? `关键词：${searchQuery}` : activeMeta ? activeMeta.date_label : ""}
          </div>
        </header>

        <section className={styles.contentBody}>
          {status === "error" ? <div className={styles.emptyState}>加载失败。{error}</div> : null}

          {status === "loading" && !searchQuery && !activeGroup ? (
            <div className={styles.emptyState}>正在加载这一组通信…</div>
          ) : null}

          {status === "loading" && searchQuery && !searchResults.length ? (
            <div className={styles.emptyState}>正在载入搜索结果…</div>
          ) : null}

          {searchQuery && status !== "error" ? (
            <>
              {!searchMatches.length ? <div className={styles.emptyState}>全书范围内没有匹配内容。</div> : null}

              {searchResults.map(({ groupMeta, unit }) => (
                <UnitCard
                  key={`${groupMeta.group_id}-${unit.unit_id}`}
                  unit={unit}
                  query={searchQuery}
                  groupLabel={groupMeta.group_label}
                  dateLabel={groupMeta.date_label}
                />
              ))}

              {renderedCount < searchMatches.length ? (
                <div className={styles.loadMoreWrap}>
                  <button className={styles.loadMoreButton} onClick={loadMore} type="button">
                    继续加载 {Math.min(24, searchMatches.length - renderedCount)} 个结果
                  </button>
                </div>
              ) : null}
            </>
          ) : null}

          {!searchQuery && activeGroup ? (
            <>
              {activeGroup.display_units.length ? (
                activeGroup.display_units.map((unit) => (
                  <UnitCard key={unit.unit_id} unit={unit} query="" />
                ))
              ) : (
                <div className={styles.emptyState}>当前分组没有可显示内容。</div>
              )}
            </>
          ) : null}
        </section>
      </main>

      {tooltip ? (
        <div
          className={styles.floatingTooltip}
          style={{
            left: Math.min(tooltip.x + 16, window.innerWidth - 360),
            top: Math.max(tooltip.y + 16, 12),
          }}
        >
          <span className={styles.floatingTooltipTitle}>
            {tooltip.term}
            {tooltip.reading ? `（${tooltip.reading}）` : ""}
          </span>
          {tooltip.shortGloss ? (
            <span className={styles.floatingTooltipLine}>{tooltip.shortGloss}</span>
          ) : null}
          {tooltip.longNote ? (
            <span className={styles.floatingTooltipLine}>{tooltip.longNote}</span>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
