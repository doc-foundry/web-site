# doc-foundry.com

Source for [doc-foundry.com](https://doc-foundry.com): documentation engineering, in practice.

## Layout

| Path | What it holds |
|---|---|
| `site/` | The Docusaurus site |
| `downloads/` | Independent, MIT-licensed components and plugins, one package per folder |
| `notes/` | Design notes and plans |

The repository is an npm workspace. Run every command from the root:

```sh
npm install
npm start          # development server
npm run build      # production build into site/build
npm run typecheck
```

## Checks

Every pull request runs the TypeScript check, the production build (which fails on broken internal
links), [lychee](https://github.com/lycheeverse/lychee) for external links, and
[Vale](https://vale.sh) for prose style.
