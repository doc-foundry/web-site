import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

// Sections: Solutions (docs plugin, off until its first page), Downloads (custom page, added
// with the first package), Articles (second blog instance) and Blog. The navbar links only to
// sections that have content. The footer carries no links yet.

const config: Config = {
  title: 'Doc Foundry',
  tagline: 'Documentation engineering, in practice',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://doc-foundry.com',
  baseUrl: '/',

  onBrokenLinks: 'throw',

  // .md files are CommonMark, so HTML comments such as <!-- truncate --> work. Use .mdx for any
  // page that needs JSX or imported components.
  markdown: {
    format: 'detect',
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [
    [
      '@docusaurus/plugin-content-blog',
      {
        // Long, evergreen articles. Short posts go to the blog.
        id: 'articles',
        path: 'articles',
        routeBasePath: 'articles',
        blogTitle: 'Articles',
        blogDescription: 'Long-form articles on documentation engineering.',
        // Shared with the blog, so one author and tag list serves both.
        authorsMapPath: '../blog/authors.yml',
        tags: '../blog/tags.yml',
        showReadingTime: true,
        blogSidebarTitle: 'All articles',
        blogSidebarCount: 'ALL',
        feedOptions: {
          type: ['rss', 'atom'],
          xslt: true,
        },
        onUntruncatedBlogPosts: 'throw',
        onInlineAuthors: 'throw',
        onInlineTags: 'throw',
      },
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: false,
        blog: {
          showReadingTime: true,
          blogSidebarTitle: 'All posts',
          blogSidebarCount: 'ALL',
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Every post needs a truncate marker for its list excerpt: <!-- truncate --> in .md,
          // {/* truncate */} in .mdx.
          onUntruncatedBlogPosts: 'throw',
          onInlineAuthors: 'throw',
          onInlineTags: 'throw',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      // The logo is a lockup that already carries the wordmark, so no title.
      logo: {
        alt: 'Doc Foundry',
        src: 'img/logo.svg',
        srcDark: 'img/logo-dark.svg',
      },
      // Final order: Solutions, Downloads, Articles, Blog.
      items: [
        {to: '/articles', label: 'Articles', position: 'left'},
        {to: '/blog', label: 'Blog', position: 'left'},
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Doc Foundry`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
