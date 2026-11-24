# doc-foundry/web-site

Source for doc-foundry.com. **This repository is public.** Everything committed here is published:
no personal circumstances, no private paths, no references to any employer or client work.
Private planning lives outside the repo.

## Layout

npm workspace rooted here:

- `site/`: Docusaurus 3 (classic preset, TypeScript), package `@doc-foundry/site`.
- `downloads/*`: one independent package per component, each with its own `package.json`,
  `LICENSE` (MIT) and README. The site consumes them as workspace dependencies, exactly as an
  outside user would. A download must never import from `site/`.
- `notes/`: design notes (public).

Run npm commands from the root (`npm start`, `npm run build`, `npm run typecheck`). There is a
single `node_modules/`, at the root.

## Status

The blog is live (`site/blog/`, first post merged in #6), and the navbar links to it. Docs are
still disabled, and the footer has no links. The home page still says "Site under construction"
and shows the contact address, contact@doc-foundry.com. Turn docs on only when there is content
to link to.

## Content program

Content comes first: articles, tutorials, solutions and downloads. Polish (dates, layout details)
comes second.

- **Blog posts:** short, practical, first-person.
- **Pattern articles:** one documentation pattern per post, compared across Docusaurus, Mintlify,
  Hugo, MkDocs and Antora with a matrix (native / plugin / custom / not feasible), plus the
  trade-offs of each route. Each pattern gets an MIT package in `downloads/`.
- **Tutorials and series:** multi-part, built from a worked example.

Editorial rules:
- Every solution has trade-offs. Cover them in admonitions and let the reader decide; no
  single-verdict posts.
- Every post ships with a runnable artifact: a package, a CI rule, or lab code.
- Describe patterns and generic failure modes only; name no client or employer.

The private plan (backlog, sources, idea queue) lives outside the repo and is loaded through the
gitignored `CLAUDE.local.md`.

## Blog

- Posts are `site/blog/YYYY-MM-DD-slug.md`, with `authors: [koray]` and tags from `tags.yml`
  (inline authors and tags fail the build).
- **`.md` is CommonMark, `.mdx` is MDX** (`markdown.format: 'detect'`). Write posts as `.md`
  with the excerpt marker `<!-- truncate -->`; use `.mdx` (marker `{/* truncate */}`) only when a
  post needs JSX or imported components. Every post needs a marker, or the build fails.
  Admonitions (`:::note`) work in both.
- **Scheduling:** the blog plugin doesn't hide future-dated posts; a post dated tomorrow is live
  as soon as it merges. Merge an unpublished post with `draft: true` (excluded from production
  builds, shown by `npm start`), then remove the flag in a one-line PR on its publication day.
  Set the filename date to that day too.
- **Vale blog profile** (`[site/blog/*.{md,mdx}]` in `.vale.ini`): `Microsoft.FirstPerson`, `We`
  and `QuestionMarks` off, with the reason for each. Change the profile, not individual posts.
  CI fails on warnings and errors; suggestions (such as Passive) stay advisory.

## CI and deploy

- `.github/workflows/ci.yml`:
  - `build` job: `npm ci`, typecheck, build (`onBrokenLinks: 'throw'`), then lychee over the
    Markdown and the built HTML.
  - `vale` job: Vale on `*.md` with the Microsoft style and the `DocFoundry` vocabulary.
- **Cloudflare Workers** (Worker name `web-site`, custom domains `doc-foundry.com` and `www`,
  zone setting Always Use HTTPS on) deploys from the repo root. The config is in `wrangler.jsonc` (assets from
  `site/build`), and the build command is `npm run build`. Keep `"previews": {}`, or PR preview
  builds fail. The Node version comes from `.node-version`.
- Builds authenticate with a user API token (My Profile → API Tokens). Deleting a Worker doesn't
  delete the token; deleting the token breaks builds.
- The user connects Git in the Cloudflare dashboard and merges PRs. Claude can't see Cloudflare
  build logs, so ask for them.

## Adding MDX to Vale

Vale checks `*.md` only. Before `.mdx` posts exist, add an `[*.mdx]` section to `.vale.ini`, and
install `mdx2vast` in CI.
