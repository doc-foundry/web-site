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

Phase 1 placeholder: docs and blog are disabled, the navbar and footer have no links, and the home
page says "Site under construction" and shows the contact address, contact@doc-foundry.com. Turn docs and blog on only when there is content to link to.

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
