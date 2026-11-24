# Doc Foundry: Downloadable components and Markdown gaps

Written 2026-09-27. Design notes for the MIT-licensed components that go in `../downloads/`.

## Principles

- **Clean, original implementations.** Every component is written from its specification, not ported.
- **MIT-licensed, published early** under the `doc-foundry` GitHub org, one package per component.
- **Build-time over runtime.** Content that exists only after hydration is missing from the static
  HTML and the search index, even when it looks correct in the browser.

## Design direction: Move to a different layer

Build these as **remark plugins that run at build time**, not as runtime React components that
resolve an ID when the page renders:

| Runtime component | Build-time plugin | Why it's better |
|---|---|---|
| `<Xref id="x">text</Xref>` + JSON map | `[text](xref:x)` rewritten in the mdast; registry entries are `{path, title}`; `[](xref:x)` fills in the title | Source stays plain Markdown. An unknown ID fails the build. Link text can't drift from page titles |
| `<Embed id="x" />` resolved at render | `::include{file=… tag=…}` directive spliced into the AST; AsciiDoc-style `tag::x[]` / `end::x[]` regions | Included headings reach the TOC and search index. A runtime component can't do this |
| Term/definition pairs laid out in a `<table>` | Glossary component or definition-list syntax → `<dl>` + CSS grid | Semantic HTML, accessible, and it pairs with first-use tooltips |

Open question for each: ship both a remark plugin and a thin React wrapper, or only the plugin?
Decide per component, and document the trade-offs.

**Decided for `Xref` (2026-10-25): a React component.** Authors write
`<Xref id="install-cli">Installing the CLI</Xref>`, or `<Xref id="install-cli" />` to use the
registry title. The registry, `xrefs.json`, maps each ID to `{path, title}`. The runtime cost
the table above warns about doesn't apply here, because Docusaurus prerenders every page: the link
is in the static HTML and the search index. Two guards keep IDs honest:

- **Typed IDs.** The `id` prop is typed as a key of `xrefs.json`, so the editor flags a typo.
- **Build-time check.** A validation plugin scans the MDX for unknown IDs and fails the build,
  naming the file and the line. The component also throws on an unknown ID, which fails
  prerendering as a backstop.

## Markdown gaps: Candidate components and plugins

Features Markdown (CommonMark/GFM) doesn't provide natively. The table lists the AsciiDoc and DITA features each one mirrors.

| Gap | AsciiDoc | DITA |
|---|---|---|
| Cross-reference by ID, with automatic title | `xref:` | `keyref` |
| Transclusion, with tagged regions | `include::[tag=]` | `conref`, `conkeyref` |
| Variables / attribute substitution | `{attr}` | `keydef` |
| Conditional content (audience, edition, platform) | `ifdef::` | `@audience`, `@props` + DITAVAL |
| Definition lists / glossary, first-use tooltips | `term:: def` | `glossentry` |
| Numbered figures and tables, with cross-references to their numbers | `.Title` + `<<id>>` | `fig`, `xref` |
| Code callouts | `<1>` markers (conums) | None |
| UI markup: keys, menus, buttons | `kbd:[]`, `menu:[]`, `btn:[]` | `uicontrol`, `menucascade` |
| Structured procedures (step, result, example) | None | `task` topic |
| Tables with merged cells and column specs | `cols=`, spans | `tgroup`, `colspec` |
| Edition/version markers | None | `@props`, `@rev` |

**Suggested order:** `xref`, then `include`, then variables, then glossary. The first two are the
foundation that the rest reference.
