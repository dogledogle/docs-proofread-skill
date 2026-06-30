---
name: docs-proofreader
description: Agent-neutral documentation audit and proofreading workflow for Codex, Claude Code, Cursor, Gemini CLI, OpenCode, Aider, and other coding agents. Use when asked to review, proofread, audit, or report issues in online docs, local docs, translated docs, Markdown/MDX/source documentation, and documentation-like code comments involving terminology consistency, translation accuracy, typos, casing, Chinese/English punctuation and spacing, proper noun formatting, links, Markdown/MDX formatting, code examples, or basic documentation structure. Produce a Markdown issue report with file/line locations and English commit descriptions.
---

# Docs Proofreader

## Agent Compatibility

Use this folder as an agent-neutral instruction pack. `SKILL.md` is the canonical workflow for agents that understand Codex/OpenAI-style skills. For other agents, load or copy the matching adapter from `agents/`:

- `agents/openai.yaml`: OpenAI/Codex UI metadata.
- `agents/claude.md`: Claude Code or Claude project instructions.
- `agents/gemini.md`: Gemini CLI project instructions.
- `agents/cursor.mdc`: Cursor project rule.
- `agents/windsurf.md`: Windsurf workspace or project instructions.
- `agents/copilot-instructions.md`: GitHub Copilot repository instructions.
- `agents/cline.md`: Cline and Roo Code custom instructions.
- `agents/generic.md`: OpenCode, Aider, AGENTS.md-compatible tools, or any agent that accepts plain Markdown instructions.

Adapters must stay thin. Keep the audit rules, report shape, and helper script behavior in this file and `references/`, then make each adapter point back to those canonical files.

## Workflow

1. Define the audit scope from the user request, referenced files, repository paths, URLs, or surrounding docs. If scope is ambiguous after inspection, ask for the missing boundary before auditing.
2. Gather source text with evidence:
   - For local docs, inspect the relevant files and preserve exact file paths and line numbers.
   - For online docs, fetch or browse the canonical pages and preserve source URLs. If source files are available in a repository, prefer them for line numbers.
   - For translation audits, compare the target document against the original source when available and report omissions, mistranslations, stale values, and changed semantics.
3. Infer local style before reporting style issues. Check nearby docs, project terminology, product names, and existing wording conventions.
4. Report only issues supported by specific evidence. Avoid speculative preferences unless the project style rule is visible or the user requested stylistic polishing.
5. Produce a Markdown report file. Do not directly modify audited documentation unless the user separately asks for fixes.

## What To Check

Cover these categories at minimum:

- Terminology consistency across files and sections.
- Translation accuracy, missing source content, stale defaults, and mistranslated technical terms.
- Typos, duplicated words, grammar problems, and awkward direct translations.
- Product, API, protocol, and proper-noun casing.
- Chinese/English spacing, punctuation, parentheses, quotes, and list punctuation.
- Markdown/MDX structure, headings, anchors, tables, lists, admonitions, and code fences.
- Code sample formatting, invalid punctuation in code literals, and missing backticks for identifiers.
- Internal and external link validity, including relative links and anchors where practical.
- Basic rendered structure issues such as broken indentation, malformed lists, or confusing headings.

## Report Format

Read `references/report-format.md` before writing the final report. Match its structure unless the user provides a stricter template.

Read `references/review-checklist.md` when auditing Chinese technical docs, translated docs, or mixed Chinese/English documentation.

Default report language is Chinese. Include an English commit description for every issue. Do not include Chinese commit descriptions unless the user asks for them or explicitly requests exact compatibility with a sample that includes them.

## Helper Scripts

Use scripts when they reduce repetitive work:

- `scripts/collect_docs.py`: collect local documentation files or fetch URL text snapshots.
- `scripts/check_links.py`: extract and check Markdown/HTML links from files or directories.
- `scripts/validate_report.py`: validate that a generated Markdown report follows the required shape.

These scripts are helpers, not substitutes for judgment. Always verify reported issues against the source text before including them.
