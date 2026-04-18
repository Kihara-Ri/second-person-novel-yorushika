# 《一人称》项目

这个仓库现在是一个单体的 `Vite + React + TypeScript` 工程，用来查看《一人称》的双语对照页面；文本整理、翻译稿和 JSON 导出仍然保留在仓库内。

## 目录

- `src`
  - React 前端
- `exports`
  - 前端直接读取的 JSON 数据
- `texts`
  - 原稿、整理阅读版、结构索引
- `translations`
  - 双语批次稿
- `docs`
  - 项目需求、解析、术语、规范、注释
- `scripts`
  - 文本整理与 JSON 导出脚本

## 运行

先安装依赖：

```bash
npm install
```

开发预览：

```bash
npm run dev
```

## Node 版本

当前前端基于 Vite 7，要求 Node 不低于 `22.12.0`。仓库已经附带：

- [\.nvmrc](/Users/kiharari/DEV/一人称小说/.nvmrc)
- [\.node-version](/Users/kiharari/DEV/一人称小说/.node-version)
- [with-modern-node.sh](/Users/kiharari/DEV/一人称小说/scripts/with-modern-node.sh)

如果你本机 shell 命中了旧的 `/usr/local/bin/node`，仓库内的 `npm run dev / build / preview` 也会优先尝试以下可用的新版本：

- `~/.nvm/versions/node/v22.22.1/bin/node`
- `/opt/homebrew/bin/node`
- 当前 PATH 中的 `node`

也就是说，即使 `nvm` 没有加载，只要机器上已经装了较新的 Node，这个项目依然可以直接跑起来。

如果你想确认当前 shell 自己正在使用哪一版，再执行：

```bash
node -v
```

你当前机器上可用的新版本应当是 `v22.22.1`。

生产构建：

```bash
npm run build
```

本项目的 Vite `publicDir` 指向 [exports](/Users/kiharari/DEV/一人称小说/exports)，因此前端会直接读取：

- [preview_index.json](/Users/kiharari/DEV/一人称小说/exports/preview_index.json)
- [preview_groups](/Users/kiharari/DEV/一人称小说/exports/preview_groups)

## 数据更新

如果你修改了翻译稿、词注或导出逻辑，重新执行：

```bash
python3 scripts/export_bilingual_parallel.py
```

如果你修改了原稿整理逻辑，重新执行：

```bash
python3 scripts/build_reading_edition.py
```

## 前端入口

- 应用入口： [main.tsx](/Users/kiharari/DEV/一人称小说/src/main.tsx)
- 页面入口： [App.tsx](/Users/kiharari/DEV/一人称小说/src/App.tsx)
- 小说阅读器： [NovelViewerPage.tsx](/Users/kiharari/DEV/一人称小说/src/features/novel-viewer/NovelViewerPage.tsx)
- 样式： [NovelViewerPage.module.css](/Users/kiharari/DEV/一人称小说/src/features/novel-viewer/NovelViewerPage.module.css)

## 当前精简结果

已经移除旧的：

- `preview/`
- `Makefile`
- Go 静态预览服务
- 旧的独立静态打包层
- React 主站集成样板目录

现在仓库里只保留一套正式前端实现。
