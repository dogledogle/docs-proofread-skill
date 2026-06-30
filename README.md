# Docs Proofreader

Docs Proofreader 是一个可供主流 coding agent 使用的文档审校 skill。

它面向本地文档、在线文档、翻译文档、Markdown/MDX 文件、源码中的文档化注释，以及中英混排的技术文档，目标是产出有证据支撑的 Markdown 问题报告。

## 功能

- 检查术语一致性、翻译准确性、错别字、大小写、标点、中英文空格、Markdown 结构、链接和代码示例格式。
- 在报告中保留证据，包括文件路径、行号、URL、锚点或相邻标题。
- 默认只生成审校报告，不直接修改被审校的原始文档。
- 默认使用中文撰写报告，并为每个问题提供英文 Conventional Commit 风格的修改描述。
- 提供主流 agent 的轻量适配文件，核心审校规则保持在 `SKILL.md` 和 `references/` 中。

## 仓库结构

```text
.
+-- SKILL.md
+-- LICENSE
+-- agents/
|   +-- openai.yaml
|   +-- claude.md
|   +-- gemini.md
|   +-- cursor.mdc
|   +-- windsurf.md
|   +-- copilot-instructions.md
|   +-- cline.md
|   +-- generic.md
+-- references/
|   +-- report-format.md
|   +-- review-checklist.md
+-- scripts/
    +-- check_links.py
    +-- collect_docs.py
    +-- validate_report.py
```

## 工作流程

1. 根据用户请求、本地路径、仓库文件或 URL 明确审校范围。
2. 收集源文本，并保留文件路径、行号、URL 或锚点等证据。
3. 在报告风格类问题前，先推断并遵循项目已有的写作风格。
4. 对每一个拟报告的问题，都回到源文本中核验证据。
5. 按照 `references/report-format.md` 的要求生成 Markdown 报告。

审校中文技术文档、翻译文档或中英混排文档时，还应参考 `references/review-checklist.md`。

## Agent 接入

`SKILL.md` 是本项目的核心指令源。不同 agent 的适配文件都放在 `agents/` 目录中，它们只负责让对应工具知道何时触发和如何引用核心规则。

### Codex / OpenAI

Codex/OpenAI 可直接使用 `SKILL.md` 作为 skill 入口，并读取 `agents/openai.yaml` 中的界面元信息。

### Claude Code

将 `agents/claude.md` 的内容复制到项目的 `CLAUDE.md`，或在现有 `CLAUDE.md` 中引用该文件。

### Gemini CLI

将 `agents/gemini.md` 的内容复制到项目的 `GEMINI.md`，或在 Gemini 项目上下文中引用该文件。

### Cursor

将 `agents/cursor.mdc` 放入目标项目的 `.cursor/rules/` 目录，例如：

```text
.cursor/rules/docs-proofreader.mdc
```

### Windsurf

将 `agents/windsurf.md` 的内容复制到 Windsurf workspace rules 或项目级自定义指令中。

### GitHub Copilot

将 `agents/copilot-instructions.md` 的内容复制到目标项目的 `.github/copilot-instructions.md`。

### Cline / Roo Code

将 `agents/cline.md` 的内容复制到 Cline 或 Roo Code 的 custom instructions / project rules 中。

### OpenCode / Aider / AGENTS.md

将 `agents/generic.md` 的内容复制到目标项目的 `AGENTS.md`，或在该类 agent 的项目级 Markdown 指令中引用它。

## 辅助脚本

`scripts/` 下的脚本用于减少重复性检查工作，但不能替代人工判断。

### 收集文档

收集本地文档文件，或抓取 URL 的文本快照：

```bash
python scripts/collect_docs.py <path-or-url>
```

### 检查链接

从 Markdown 或 HTML 文档中提取并检查链接：

```bash
python scripts/check_links.py <path>
```

### 校验报告

校验生成的审校报告是否符合预期结构：

```bash
python scripts/validate_report.py <report.md>
```

## 元信息与适配文件

核心入口文件是 `SKILL.md`，其中定义了：

- 名称：`docs-proofreader`
- 触发描述
- 审校工作流
- 报告格式要求
- 辅助脚本使用说明

Agent 适配文件位于 `agents/`：

- `openai.yaml`：OpenAI/Codex 界面元信息。
- `claude.md`：Claude Code / `CLAUDE.md` 适配说明。
- `gemini.md`：Gemini CLI / `GEMINI.md` 适配说明。
- `cursor.mdc`：Cursor project rule。
- `windsurf.md`：Windsurf workspace / project rules 适配说明。
- `copilot-instructions.md`：GitHub Copilot repository instructions 适配说明。
- `cline.md`：Cline / Roo Code 适配说明。
- `generic.md`：OpenCode、Aider、`AGENTS.md` 及其他 Markdown 指令型 agent。

## 许可证

本项目使用 MIT License。详情见 `LICENSE`。
