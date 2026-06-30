# Review Checklist

Use this checklist as prompts while auditing. Confirm each issue against the document and local style before reporting it.

## Terminology And Casing

- Product names: `vite` as a product name should usually be `Vite`.
- Tool and API names: `jsdoc` -> `JSDoc`, `postcss` -> `PostCSS`, `rollup` -> `Rollup`.
- Web terms: `websocket` or `websockets` -> `WebSocket`, `http` as protocol -> `HTTP`.
- CSS terms: `CSS modules` -> `CSS Modules` when referring to the feature name.
- Keep established local choices, such as `source map` vs `sourcemap`, consistent across nearby docs.

## Chinese And English Spacing

- Add spaces between Chinese prose and English words, product names, or code terms when local style does so:
  `Vite允许` -> `Vite 允许`
  `支持TypeScript` -> `支持 TypeScript`
  `SSR构建` -> `SSR 构建`
- Remove unnecessary spaces after Chinese punctuation:
  `在 CLI 中， `vite dev`` -> `在 CLI 中，`vite dev``
- Use backticks for code identifiers and literal option values:
  `设置为 true 时` -> `设置为 `true` 时`

## Punctuation And Markdown

- Chinese prose should normally end with Chinese punctuation:
  `说明.` -> `说明。`
- Avoid English punctuation in Chinese lists unless it is inside code.
- Do not use Chinese punctuation inside JavaScript or JSON code values:
  `['es'、'umd']` -> `['es', 'umd']`
- Check list indentation, table pipes, fenced code language tags, headings, anchors, and admonition syntax.
- Check links around Chinese text for readable spacing:
  `正如[环境变量]...中` -> `正如 [环境变量]... 中`

## Translation Accuracy

- Compare with source docs when available. Look for missing sentences, stale defaults, and changed conditions.
- Watch for common mistranslations:
  - `overlay`: usually `遮罩层` or `覆盖层`, depending on project style.
  - `transitive dependencies`: `传递性依赖项`.
  - `bundle`: often `打包`, `产物`, or `包`, depending on context.
  - `source map`: avoid mixing `source map`, `sourcemap`, and translated forms without a local convention.
  - `minification`: usually `最小化` or `压缩`, not `混淆` unless obfuscation is meant.
- Prefer natural Chinese over word-for-word translation when meaning stays equivalent.

## Consistency

- Check person and tone, such as `你` vs `您`.
- Check repeated section templates for copy-paste mistakes, such as preview docs saying `开发服务器`.
- Check code comments in docs for product casing and translated terminology too.
- If a term appears inconsistent, inspect surrounding files before choosing the suggested form.
