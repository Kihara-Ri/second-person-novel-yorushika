# 前端对接导出说明

## 文件

- `双语对照_前端数据.json`
  - 全书双语对照数据
  - 已包含 `group_id / unit_id / para_id / speaker / type / source_md / target_md / term_notes`
- `疑难词注释_前端词库.json`
  - 疑难词独立词库
  - 可单独用于悬浮释义、侧边词条或全文索引
- `疑难词注释_覆盖统计.json`
  - 注释命中统计
  - 可用于前端调试、词条补全和 QA

## 说明

- 补遗部分使用独立通信组 `EX`
- `term_notes` 已按段落自动挂接
- 对人工长注未覆盖、但原稿已用 `{|}` 标出读音的词，会自动生成保底注释
- 当前注释命中基于已整理的作品内高优先级疑难词表
- 如果后续补充新词，只需要更新脚本中的词库并重新导出

## 重新导出

```bash
python3 scripts/export_bilingual_parallel.py
```
