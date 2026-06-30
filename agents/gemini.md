# Docs Proofreader Adapter For Gemini CLI

Use this adapter in Gemini CLI project instructions, for example by copying it into `GEMINI.md` or referencing this file from the project's Gemini context.

## Instruction

When the user asks for documentation proofreading, documentation audit, translation review, Markdown/MDX review, link checking, terminology review, or mixed Chinese/English technical writing review, use the Docs Proofreader workflow from `SKILL.md`.

Required behavior:

- Establish the audit scope from the user request, local files, repository paths, URLs, or surrounding documentation.
- Gather source evidence and keep exact file paths, line numbers, URLs, anchors, or headings.
- Check terminology, translation accuracy, typos, grammar, casing, punctuation, Chinese/English spacing, Markdown structure, links, and code sample formatting.
- Do not report speculative style preferences unless the local style rule is visible or the user requested stylistic polishing.
- Produce a Markdown report. Do not directly modify audited documentation unless separately requested.

Before finalizing the report:

- Use `references/report-format.md` as the report template.
- Use `references/review-checklist.md` for Chinese, translated, or mixed Chinese/English docs.
- Optionally run `scripts/validate_report.py <report.md>` when a report file is produced.

Default report language is Chinese. Each issue must include an English Conventional Commit-style commit description.
