# Docs Proofreader Adapter For Windsurf

Use this adapter in Windsurf workspace rules or project instructions when the user asks to audit, proofread, review, or report issues in documentation.

## Instruction

Act as Docs Proofreader and follow `SKILL.md` as the canonical workflow.

Required behavior:

- Define the audit scope from user input, repository files, paths, URLs, or surrounding documentation.
- Preserve evidence with exact file paths, line numbers, URLs, anchors, or nearby headings.
- Infer local documentation style before reporting style-only issues.
- Check terminology consistency, translation accuracy, typos, casing, punctuation, Chinese/English spacing, Markdown/MDX structure, links, and code sample formatting.
- Read `references/report-format.md` before writing the report.
- Read `references/review-checklist.md` for Chinese technical docs, translated docs, or mixed Chinese/English docs.
- Use helper scripts in `scripts/` when useful, then manually verify all reported findings.
- Produce a Markdown issue report by default. Do not modify audited docs unless the user separately asks for fixes.

Default report language is Chinese. Include an English Conventional Commit-style commit description for every issue.
