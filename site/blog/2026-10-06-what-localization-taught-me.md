---
slug: what-localization-taught-me
title: What localization taught me about writing source docs
description: Translators can't skim, so every ambiguity in the source becomes a decision. Six habits that remove those decisions, and why they help every reader.
authors: [koray]
tags: [writing, localization, docs-as-code]
---

For two decades I localized other people's software documentation. Translating a sentence means you can't skim past it: every ambiguity in the source becomes a decision, and every target language inherits that decision. The habits I brought back to writing my own docs all do the same thing. They take decisions away from the reader.

{/* truncate */}

## Where translators get stuck

The same few problems turn up in source text from every vendor. Each one has a cheap fix at writing time and an expensive one later.

| Problem in the source | What the translator faces | Fix at writing time |
|---|---|---|
| Two names for one thing: "Settings page" here, "Preferences dialog" there | Are they the same? Every language inherits the guess. | One name per thing, kept in a terms list. |
| A pronoun with no clear antecedent: "it," "this" | Many languages must mark gender or number, so the translator has to choose. | Repeat the noun. |
| The same instruction phrased three ways | Translation memory misses; three translations to pay for and review. | Write recurring instructions identically, or single-source them with an include. |
| An idiom: "out of the box" | No equivalent, and the literal translation is nonsense. | Plain words: "by default." |
| A paraphrased UI label: "use the save option" | The translator can't match it to the localized UI string. | Quote the exact label: `Save`. |
| A sentence assembled from fragments | Word order differs between languages, so the pieces don't fit. | Write complete sentences. |

## Why it isn't about translation

Translators are just the readers who are forced into close reading. Everyone else does the same work less visibly: a non-native speaker reading in their second language, a browser's machine translation, a reader scanning for the one step they need, and now an AI assistant answering questions from your docs. None of them can ask you what "it" refers to.

Clear source text is text that survives close reading. Localization only makes the cost of unclear text visible, because someone sends you a query or an invoice for it.

## Making it mechanical

Some of these habits can be enforced. A prose linter such as Vale can turn the terms list into a rule, so a second name for the same thing fails the check:

```yaml
extends: substitution
message: "Use '%s' instead of '%s'."
level: error
swap:
  Preferences dialog: Settings page
```

:::note[Trade-off]

A linter only catches the variant you already know about. It can't find the ambiguity nobody has noticed yet, such as a pronoun that reads fine to its author. That still takes a close human reader, which is exactly what a translator is.

:::

Which writing habit did you pick up somewhere unexpected?
