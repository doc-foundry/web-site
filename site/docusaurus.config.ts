import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

// The blog is on; docs are still off. The navbar links only to sections that
// have content. The footer carries no links yet.

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

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

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
          // Every post needs a {/* truncate */} marker for its list excerpt (.md is parsed as MDX).
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
      items: [{to: '/blog', label: 'Blog', position: 'left'}],
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
