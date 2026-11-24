# Doc Foundry house style

The reviewer checks changed lines against these rules. Vale already covers spelling, terminology,
and the Microsoft style mechanics, so don't repeat what a linter catches; judge what a linter can't.

## Rules

1. **Front-load.** Context first, then the objects involved, then how it works. The reader learns
   *why* before *what*, and *what* before *how*. Flag a paragraph that names a mechanism before the
   reader knows the problem it solves.
2. **Concise, with a one-line rationale.** Cut sentences that carry no information: warm-ups,
   restatements, blanket hedges ("this may help in some cases"). Keep the reason, though; a bare
   instruction reads as telegraphic.
3. **Tables at three or more rows.** A comparison or mapping with three or more items belongs in a
   table, by default a two-column problem → fix table. Under three items, use a lead sentence and
   bullets.
4. **Monospace for code only.** Code, file names, paths, commands, config keys, component names,
   and literal UI strings go in monospace. Product names (Docusaurus, Vale, GitHub Actions) stay
   plain. Bold is rare: a key term or a warning.
5. **Subtitles name the content.** Two or three short subtitles per article, such as "Where it
   breaks" or "Registry vs redirects". Never generic labels like "Introduction" or "Overview".
   Headings use sentence case.
6. **Keep the spice.** Vivid, opinionated phrasing that carries a true point stays. Don't flag it
   or sand it down into neutral catalog prose.
7. **Open an article with an incident, not a thesis.** A short concrete scene with real numbers,
   then the principle.
8. **Be specific.** A named role, a real figure, or a literal title beats a category. When the
   reader must say something, script it word for word.
9. **End a section on its sharpest line,** not on a summary of what it just said.
10. **Name the limits once.** One precise hedge where the answer truly varies, instead of softening
    every sentence.
11. **Close an article with one small action** the reader can do in minutes, not a recap.

## Where each rule applies

| File | Rules |
|---|---|
| Blog posts (`site/blog/`) | 1–11 |
| Docs, READMEs, notes | 1–6, 8, 10 |

## Spelling and punctuation

- American spelling: *localization*, *organize*, *color*.
- Commas and periods go inside quotation marks.
- Serial comma: "fast, tireless, and literal."

## Project vocabulary

| Use | Not |
|---|---|
| `Xref` component, registry `xrefs.json` | `Topic`, `topics.json`, `Ref` |
| `include` directive (`::include{file=… tag=…}`) | `Include` as a runtime component |
