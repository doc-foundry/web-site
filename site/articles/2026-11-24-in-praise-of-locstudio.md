---
slug: in-praise-of-locstudio
title: In praise of LocStudio
description: Quality appears only when the loop closes. What a localization IDE taught me about seeing your own mistakes, and how the same loop works on a docs-as-code site.
authors: [koray]
tags: [localization, tooling, docs-as-code]
---

Take `My Documents`. In a Windows localization project it looks like the easiest string in the
build: two words, one obvious translation. But it's also the name of a folder, and code finds that
folder by name. Most of its instances were internal and had to stay in English. One or two were
shown to the user and had to be translated. Every instance looked identical in a string list.

Translate all of them, and code that looks the folder up by name stops finding it. Translate none,
and a Turkish user meets an English label in the middle of a Turkish desktop. The translation can
be flawless and the product still broken. The only way to tell the instances apart is to see where
each one lives and what happens when it changes.

That's the point of this article: **quality appears only when the loop closes.** The person who
changes a string has to see what the change does. I learned it twice: first with a tool that closed
the loop, then on a docs site.

<!-- truncate -->

## A tool that knew what each string was for

Microsoft localized its products with an in-house tool called LocStudio. I used it, and later its
successor LEAF, on Office, Windows 2000, Internet Explorer and other products. Its core idea fits in
four steps:

1. Put the product's executables and everything they depend on (EXE, DLL, HTML, RTF and INI files)
   in a `Source` folder.
2. Create a LocStudio project that points to them.
3. Let LocStudio parse every resource, keep the hierarchy, and flag each entry with a
   classification label, such as dialog title, button, or message box warning text.
4. Generate the localized product into a `Target` folder, ready to ship.

The result was the whole product, laid out as a translation grid, with each string carrying its
purpose. You could filter by label, batch-edit a class of strings, and, for anything with a GUI,
run the dialog inside LocStudio to see the translated result before a build existed.

The record behind each row shows how seriously it took that purpose. LEAF still ships the LocStudio
object model, and its string record has about 90 string types, from `DialogTitle` and `MenuItem` to
`RegistryValue` and `ShortcutHotKey`. It also stores the control's position, size and font, a
translation lock, and where each translation came from: new, uploaded, copied from a previous
version, pseudo-localized, or machine-translated. A string never traveled without its context.

Joel Spolsky once defended Hungarian notation, the original kind that encodes what a variable
means rather than its data type, with one line: [it "makes wrong code look
wrong."](https://www.joelonsoftware.com/2005/05/11/making-wrong-code-look-wrong/) That's the first
job of any IDE, the same way it's the first job of a failing test. LocStudio did it for strings: a
translation that didn't fit, clashed, or broke something looked wrong while you were still working
on it.

That's what made the loop short. The bugs that survive a string review came back to the same
person, either in the tool or in regression testing:

| Bug | How the loop caught it |
|---|---|
| A translated string that code depends on (a folder name, a string a dialog needs to launch) | The hierarchy and the labels showed where each instance lived; a test run showed what broke |
| Static text that doesn't fit its control | Caught at compile time; resized with LocStudio's own tools before the build |
| Text truncated at runtime, such as a path inserted into a warning message | Found in regression testing; resized during bug fixing |
| Formatting broken by Turkish characters | A test run before the build shipped |
| A crash in a localized build | DEBUG builds wrote trace logs; a spy tool (WinSpy, in my case) showed the resource behind a control; LocStudio's filters led to the string |

Keyboard shortcuts show how tight the constraints got. An access key like the `K` in `&Kaydet`
(Save) has to obey three rules at once:

- No two strings in the same menu bar or dialog can share a key.
- Some elements appear only in certain states, so the elements that stay put must keep the same
  key in every instance of that menu or dialog. LocStudio let you apply the same keys to the same
  elements everywhere.
- Keys the operating system already assigns can't move. In Turkish Windows, Save is Ctrl+K, and that
  stays.

Stack those up in a crowded dialog, and sometimes the only letters left are Turkish ones: `ç`, `ş`,
`ö`, `ü`. The worst of them was the dotless `ı`. Its capital is `I`, the same letter English uses as
the capital of the dotted `i`. Turkish gives its dotted `i` a capital of its own, `İ`. Any code that
compared letters without knowing the language mixed the two up, and we got a steady stream of bugs
from it, in shortcuts and in path names alike.

Word order was the other fight. When a field or a checkbox sits in the middle of an English
sentence, the dialog freezes English word order, and Turkish wants the verb at the end. (I called
this the Yoda problem in *AI-driven localization*.) LocStudio was where we jumped through the
hoops: warped sentences that still fit around the controls, and a good deal of resizing and
aligning. Inside a single string, format specifiers helped. Microsoft had wisely added numbered
inserts such as `%1!s!`, so a translation could put a value wherever Turkish wanted it. Across
separate strings, nothing helped, so we swapped text between rows to match Turkish word order.

Each swap had a side effect. Word counts were English-based, so rows with the same English text
counted as the same string, while their Turkish versions now differed, at least slightly. On a
project of a few million words, that adds up to a visible amount. We never made an issue of it.
The point is that nobody on the English side had thought to ask.

The loop thinned where the parser's knowledge ended. In a C++ resource file, the parser handled
access keys itself, so `&Kaydet` was enough. Embedded HTML had no such help, and we underlined the
letter by hand: `<u>K</u>aydet`. Links brought more. A localized URL had to exist before it could
go in, and Microsoft Türkiye had to decide on it, create it, and hand it over. When a link called a
script that shipped in the resource bundle, as it often did, the script's internal strings landed
in the same LocStudio project, next to the UI text. We edited those with one goal: the fewest
runtime bugs.

DLLs were the trickiest of all. They load at runtime, and they built more strings on the fly than
anything else in the product. A typical one:

> Your `<component>` component, which you added from `<source>` to do `<task>`, seems to be
> missing from `<location>`.

The project held only the frame. Every slot was filled at runtime from somewhere else: a user ID,
a component name, a path, or settings chosen in another dialog. Turkish attaches suffixes to
whatever fills a slot, so translating that sentence meant knowing what would land in each one. We
ran tests to trigger the message, then traced each value back to the resource that produced it.
For that, spy tools were the only option.

On some products, regression ran for months before the scheduled release, while each update added
new features or modified existing ones. Nobody stays on top of that by reading strings. The tool made it possible.

I did a few jobs in Catalyst, a well-developed commercial localization IDE, and it was fine. But no
tool I've used came near LocStudio's elegance, because LocStudio never separated the string from
the thing the string was part of.

That's an opinion, and it comes from one side of the work. LocStudio rewarded the people doing
localization engineering. Teammates who mostly localized Help in HTML files never complained about
Helium, Microsoft's Help localization tool, and they were very reluctant to work in LocStudio. At a
large vendor, where half a dozen engineers handle the build side, the translator at the far end has
little to form an opinion about. I loved it for one reason: it gave me an IDE where I could see
what I was doing. Without that, localization feels like flying on autopilot at night.

Then the work moved. Microsoft handed localization engineering to the large multi-language vendors,
and translation and bug fixing ended up in different teams. The split had good reasons: it was
cheaper, and the vendors could fund engineering teams. But the translator no longer saw who fixed a
bug, or whether the fix was right. The tool still worked. The loop didn't.

LEAF, LocStudio's successor, later moved the parsed resources to a cloud service. You check out a bundle
by name, mark it done, and it's gone unless someone routes it back to you. More secure, certainly.
It's also one more step out of the loop.

**The tool didn't make translators better. It let them see their mistakes.**

## Closing the loop on a docs site

My last role was sole technical writer for a security data-processing platform: 550 published pages
on Docusaurus. I owned the information architecture, every pull request merge, and the GitHub
Actions pipeline that deployed the site. That sounds like a heavy load, and it was. It was also the
first job since LocStudio where I could see every step from source to result.

The localization lessons carried over almost one to one:

| Localization | Docs-as-code |
|---|---|
| Content vs identifiers (`My Documents`) | Prose vs xref IDs, heading anchors and file paths the build depends on |
| Flagging each resource by type | Front matter and registries that say what each page and link is |
| Running the dialog inside the tool | Preview builds of every change |
| Spy tools (WinSpy, Spy++) | Browser developer tools |
| Months of regression before release | Pre-release drift audits against the source |

The last row did the most work. I kept a map from chapters and sections to the server and client
code they described, with 475 entries by the time I left. Before each release, I audited it to catch
pages that had drifted from the code. A page can read perfectly and still describe a feature that
changed last sprint. The map made that page look wrong, the same way LocStudio made a clipped
button look wrong.

The principle behind all of it: I can guarantee valid output only when I can attend every step of
the cycle. That means the whole corpus, the automation runs, and the updates that follow each fix.
A workflow that hides one of those steps from the writer breaks the loop, however efficient it
looks.

This has a limit, and it's a real one. One person closing the loop is a single point of failure, and
it doesn't scale to a team of ten by willpower. What scales is what LocStudio did: tooling that puts
the result in front of whoever made the change. The vendors' split wasn't wrong because it divided
the work. It was wrong because it divided the feedback.

**Quality isn't a review step. It's a loop, and someone has to stand inside it.**

One thing to try today: pick the last page you changed. Find out who saw it rendered, in every
version and locale it ships in. If the answer is nobody, you've found your broken loop.

*P.S. Microsoft, LEAF still ships the LocStudio engine. Open-source it, and I'll write the Markdown
parser myself.*

## Sources

- [Making Wrong Code Look Wrong](https://www.joelonsoftware.com/2005/05/11/making-wrong-code-look-wrong/), Joel Spolsky, Joel on Software, May 2005: the original, meaning-based Hungarian notation.
