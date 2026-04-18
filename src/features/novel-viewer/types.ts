export interface TermNote {
  term: string;
  matched_text?: string;
  reading?: string;
  short_gloss?: string;
  long_note?: string;
}

export interface PreviewParagraph {
  para_id: string;
  para_label: string;
  render_mode: string;
  source_md: string;
  target_md: string;
  notes: string[];
  term_notes: TermNote[];
  search_text: string;
}

export interface PreviewUnit {
  unit_id: string;
  unit_ids: string[];
  speaker: string;
  type: string;
  source_refs: string[];
  paragraphs: PreviewParagraph[];
  titleSource?: string;
  titleTarget?: string;
  titleLabel?: string;
  titleTermNotes?: TermNote[];
}

export interface PreviewGroupPayload {
  group_id: string;
  group_label: string;
  date_label: string;
  source_file: string;
  display_units: PreviewUnit[];
}

export interface PreviewSearchUnit {
  unit_id: string;
  speaker: string;
  type: string;
  source_refs: string[];
  paragraph_count: number;
  search_text: string;
}

export interface PreviewGroupMeta {
  group_id: string;
  group_label: string;
  date_label: string;
  source_file: string;
  group_file: string;
  poem_titles: string[];
  stats: {
    unitCount: number;
    paraCount: number;
    noteCount: number;
  };
  search_units: PreviewSearchUnit[];
}

export interface PreviewIndexPayload {
  work: string;
  edition: string;
  generated_at: string;
  source_files: string[];
  groups: PreviewGroupMeta[];
}

export interface PreparedParagraph extends PreviewParagraph {
  sourceHtml: string;
  targetHtml: string;
}

export interface PreparedUnit extends PreviewUnit {
  paragraphs: PreparedParagraph[];
  titleSourceHtml: string;
  titleTargetHtml: string;
}

export interface PreparedGroup extends PreviewGroupPayload {
  display_units: PreparedUnit[];
  units_by_id: Record<string, PreparedUnit>;
}

export interface SearchEntry {
  groupMeta: PreviewGroupMeta;
  unitMeta: PreviewSearchUnit;
}

export interface SearchResultUnit {
  groupMeta: PreviewGroupMeta;
  unit: PreparedUnit;
}
