import { useEffect, useRef, useState } from "react";

import { prepareLoadedGroup } from "./runtime";
import type {
  PreparedGroup,
  PreviewGroupMeta,
  PreviewIndexPayload,
  SearchEntry,
  SearchResultUnit,
} from "./types";

const GLOBAL_SEARCH_BATCH_SIZE = 24;
const SEARCH_DEBOUNCE_MS = 180;

export function useNovelViewer() {
  const dataRoot = import.meta.env.BASE_URL.replace(/\/+$/, "");
  const [dataset, setDataset] = useState<PreviewIndexPayload | null>(null);
  const [activeGroupId, setActiveGroupId] = useState<string | null>(null);
  const [searchInput, setSearchInput] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [activeGroup, setActiveGroup] = useState<PreparedGroup | null>(null);
  const [searchResults, setSearchResults] = useState<SearchResultUnit[]>([]);
  const [renderedCount, setRenderedCount] = useState(GLOBAL_SEARCH_BATCH_SIZE);
  const [status, setStatus] = useState<"idle" | "loading" | "ready" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const groupCacheRef = useRef(new Map<string, PreparedGroup>());

  async function loadGroup(groupMeta: PreviewGroupMeta) {
    const cached = groupCacheRef.current.get(groupMeta.group_id);
    if (cached) return cached;

    const response = await fetch(`${dataRoot}/${groupMeta.group_file}`);
    if (!response.ok) {
      throw new Error(`无法加载 ${groupMeta.group_file}`);
    }

    const prepared = prepareLoadedGroup(await response.json());
    groupCacheRef.current.set(groupMeta.group_id, prepared);
    return prepared;
  }

  useEffect(() => {
    let cancelled = false;

    async function boot() {
      try {
        setStatus("loading");
        setError(null);
        const response = await fetch(`${dataRoot}/preview_index.json`);
        if (!response.ok) {
          throw new Error("无法读取 preview_index.json");
        }
        const payload = (await response.json()) as PreviewIndexPayload;
        if (cancelled) return;
        setDataset(payload);
        setActiveGroupId(payload.groups[0]?.group_id ?? null);
        setStatus("ready");
      } catch (err) {
        if (cancelled) return;
        setError(String(err));
        setStatus("error");
      }
    }

    void boot();
    return () => {
      cancelled = true;
    };
  }, [dataRoot]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setSearchQuery(searchInput.trim().toLowerCase());
    }, SEARCH_DEBOUNCE_MS);
    return () => {
      window.clearTimeout(timer);
    };
  }, [searchInput]);

  useEffect(() => {
    if (!dataset || searchQuery) return;
    const groupMeta = dataset.groups.find((group) => group.group_id === activeGroupId);
    if (!groupMeta) return;
    const selectedGroupMeta = groupMeta;

    let cancelled = false;
    async function syncActiveGroup() {
      try {
        setStatus("loading");
        setError(null);
        const group = await loadGroup(selectedGroupMeta);
        if (cancelled) return;
        setActiveGroup(group);
        setStatus("ready");
      } catch (err) {
        if (cancelled) return;
        setError(String(err));
        setStatus("error");
      }
    }

    void syncActiveGroup();
    return () => {
      cancelled = true;
    };
  }, [activeGroupId, dataset, searchQuery]);

  const searchMatches: SearchEntry[] =
    dataset && searchQuery
      ? dataset.groups.flatMap((groupMeta) =>
          groupMeta.search_units
            .filter((unitMeta) => unitMeta.search_text.includes(searchQuery))
            .map((unitMeta) => ({ groupMeta, unitMeta })),
        )
      : [];

  useEffect(() => {
    setRenderedCount(GLOBAL_SEARCH_BATCH_SIZE);
  }, [searchQuery]);

  useEffect(() => {
    if (!dataset || !searchQuery) {
      setSearchResults([]);
      return;
    }
    const currentDataset = dataset;

    let cancelled = false;
    async function syncSearchResults() {
      try {
        setStatus("loading");
        setError(null);
        const visibleEntries = searchMatches.slice(0, renderedCount);
        const groupIds = [...new Set(visibleEntries.map((entry) => entry.groupMeta.group_id))];
        const groupMap = new Map<string, PreparedGroup>();

        for (const groupId of groupIds) {
          const groupMeta = currentDataset.groups.find((group) => group.group_id === groupId);
          if (!groupMeta) continue;
          groupMap.set(groupId, await loadGroup(groupMeta));
        }

        if (cancelled) return;

        setSearchResults(
          visibleEntries.flatMap((entry) => {
            const group = groupMap.get(entry.groupMeta.group_id);
            const unit = group?.units_by_id[entry.unitMeta.unit_id];
            return unit ? [{ groupMeta: entry.groupMeta, unit }] : [];
          }),
        );
        setStatus("ready");
      } catch (err) {
        if (cancelled) return;
        setError(String(err));
        setStatus("error");
      }
    }

    void syncSearchResults();
    return () => {
      cancelled = true;
    };
  }, [dataset, renderedCount, searchMatches, searchQuery]);

  function selectGroup(groupId: string) {
    setActiveGroupId(groupId);
    setSearchInput("");
    setSearchQuery("");
    setSearchResults([]);
    setActiveGroup(null);
    setStatus("loading");
  }

  function updateSearch(value: string) {
    setSearchInput(value);
  }

  function loadMore() {
    setRenderedCount((count) => count + GLOBAL_SEARCH_BATCH_SIZE);
  }

  return {
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
  };
}
