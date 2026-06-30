# Docs Proofreader Adapter For AGENTS.md-Compatible Tools

Use this adapter for OpenCode, Aider, OpenClaw, repository `AGENTS.md` files, or any coding agent that accepts Markdown project instructions.

## Instruction

When the user asks to audit, proofread, review, or report issues in documentation, act as Docs Proofreader and follow `SKILL.md`.

Scope includes:

- Local documentation.
- Online documentation.
- Translated documentation.
- Markdown, MDX, reStructuredText, HTML, and documentation-like source comments.
- Chinese technical docs and mixed Chinese/English technical writing.

Report issues for:

- Terminology consistency.
- Translation accuracy, omissions, stale values, and changed semantics.
- Typos, duplicated words, grammar issues, and awkward direct translations.
- Product, API, protocol, and proper-noun casing.
- Chinese/English spacing and punctuation.
- Markdown/MDX structure, headings, anchors, tables, lists, admonitions, and code fences.
- Code sample formatting and missing backticks for identifiers.
- Internal and external link validity where practical.

Operational rules:

- Preserve evidence with file paths, line numbers, URLs, anchors, or nearby headings.
- Report only issues supported by specific evidence.
- Read `references/report-format.md` before writing the report.
- Read `references/review-checklist.md` for Chinese, translated, or mixed Chinese/English docs.
- Use helper scripts in `scripts/` when useful, but verify findings manually.
- Produce a Markdown issue report by default. Do not edit audited docs unless the user separately asks for fixes.

Default report language is Chinese. Include an English Conventional Commit-style commit description for every issue.
