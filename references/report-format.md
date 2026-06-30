# Report Format

Use this format for the final Markdown report unless the user provides a stricter template.

## Top Matter

Start with:

```markdown
# <scope> 文档审校问题汇总

审校范围：`<glob-or-path-or-url>`

参考原文：<https://example.com/source> <!-- omit when not applicable -->

说明：以下仅汇总建议修改项，未直接修改原文档。每条均包含位置、问题描述、修改建议和英文 commit 描述。
```

Rules:

- Use a concise H1 that names the audited area.
- Keep `审校范围：` explicit. Use paths, globs, URLs, or a short phrase if the scope spans several inputs.
- Include `参考原文：` only when there is a source document, upstream docs, or canonical URL.
- If the user asks for a saved artifact, write the report to a `.md` file with a descriptive name.

## File Sections

Group issues by file or page:

```markdown
## config/index.md

### 1. `config/index.md:19`

- 问题描述：句末缺少中文句号。
- 修改建议：将「（相对于 `cwd` 路径进行解析）」改为「（相对于 `cwd` 路径进行解析）。」
- English commit description: `docs(config): add missing punctuation to --config description`
```

Rules:

- Use one `## <file-or-page>` section per file or page.
- Number issues globally across the full report. Do not restart numbering in each file.
- Use `### <number>. \`path:line\`` for each issue.
- For multiple locations, separate locations with `、`, for example:
  `### 4. \`config/index.md:35\`、\`config/index.md:44\``
- For ranges, use `path:start-end`, for example:
  `### 21. \`config/shared-options.md:272-274\``
- If exact line numbers are unavailable for online HTML docs, use the nearest heading or anchor:
  `### 3. \`https://example.com/docs#install\``
  Then mention in the problem description that source line numbers were unavailable.

## Required Fields

Each issue must contain:

- `问题描述`: what is wrong and why it matters.
- `修改建议`: the exact replacement or a concrete rewrite direction.
- `English commit description`: a Conventional Commit-style English description in backticks.

Do not include Chinese commit descriptions by default. Add them only if the user asks or if exact compatibility with a provided sample requires them.

## Commit Description Style

Use:

```markdown
`docs(<scope>): <imperative summary>`
```

Examples:

- `docs(config): normalize JSDoc capitalization`
- `docs(guide): fix spacing around TypeScript`
- `docs(api): update stale option default`

Keep the English description concise, specific, and focused on the documentation change.
