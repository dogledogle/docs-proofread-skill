# Docs Proofreader Skill

这是一个只面向 Codex 的文档审校 skill。它把文档问题转化为有证据、可定位、可执行的 Markdown 报告，适用于本地文档、在线文档、翻译文档、Markdown/MDX、源码中的文档注释，以及中英混排技术内容。

## 使用方式

将整个 skill 目录放入 Codex 的 skills 目录，例如：

```text
%CODEX_HOME%/skills/docs-proofreader-skill/
```

未设置 `CODEX_HOME` 时，Windows 通常使用 `%USERPROFILE%/.codex/skills/docs-proofreader-skill/`。

在 Codex 中使用 `$docs-proofreader-skill`，或直接提出文档审校请求。skill 默认只审校、不修改原文档；如需修复，应在审校报告完成后明确提出。

## 能力范围

- 检查术语、产品/API/协议名称大小写和跨文件一致性。
- 检查翻译遗漏、误译、过时默认值、条件变化和生硬直译。
- 检查错别字、重复词、语法、中文英文空格、标点和括号。
- 检查 Markdown/MDX 结构、代码示例、链接、锚点和基础渲染问题。
- 为每个问题保留文件路径、行号、URL、锚点或相邻标题等证据。

## 工作流

1. 明确用户指定的路径、URL、语言对和审校边界。
2. 收集源文本并保留稳定位置；在线内容优先使用规范来源，仓库中有源文件时优先使用源文件。
3. 先观察项目既有术语和写作风格，再判断问题。
4. 逐项回到源文本核验，避免把推测或个人偏好写成问题。
5. 按 `references/report-format.md` 生成中文报告；审校中文、翻译或中英混排内容时参考 `references/review-checklist.md`。
6. 生成报告文件后运行校验脚本，并在结果中说明网络或渲染检查的限制。

## 目录结构

```text
.
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- report-format.md
|   `-- review-checklist.md
`-- scripts/
    |-- check_links.py
    |-- collect_docs.py
    `-- validate_report.py
```

## 辅助脚本

```bash
python scripts/collect_docs.py <path-or-url>
python scripts/check_links.py <path> [--check-http]
python scripts/validate_report.py <report.md>
```

脚本用于收集证据和减少重复工作，不能替代 Codex 对上下文、项目风格和问题影响的判断。
