# Doc Foundry: Video tutorials

Written 2026-10-25. Notes on video tutorials for the site: whether they're worth making, how to
script them, what equipment produces acceptable quality, and where to host them.

## Status

**On hold (2026-10-25).** Revisit after the site has written content. When video work resumes, a
YouTube channel is the leading option for hosting (see [Hosting](#hosting)).

One prototype exists: a 68-second explainer for `Xref` (seven scenes, slides drawn in code,
narrated by a built-in Windows voice). Its build script is in `../tools/video/`. The pipeline
works; the voice doesn't. It sounds robotic, and a robotic voice is the first thing viewers notice
and the first thing they comment on.

The target is longer: about 15 minutes per tutorial. The prototype proves the pipeline, not the
format.

## Format: Screen-led, voice-carried

Viewers forgive plain visuals but not a bad voice, and many dismiss anything that looks
AI-generated. So the format puts the screen first and the voice second, with no face required:

| Element | Choice | Why |
|---|---|---|
| Length | About 15 minutes, one topic per video | Long enough to argue why the topic matters and work through several examples |
| Structure | Chapters of 2–4 minutes: the need, three to five worked examples, a recap | Viewers jump to the example they need; each chapter stands on its own |
| Visuals | Code, terminal and browser scenes, plus a screen recording where the real thing is clearer | Shows the workflow itself, which is what the viewer came for |
| Voice | Recorded human narration (preferred), or a designed synthetic voice | The voice carries the credibility, and over 15 minutes a synthetic voice wears thin |
| Presenter | None, or a small webcam inset later | An AI avatar invites the "it's fake" reaction this format avoids |

## Voice options

| Option | Quality | Cost and effort | Notes |
|---|---|---|---|
| Own narration, recorded per scene | Best, if the room is quiet | A microphone, plus a few minutes per video | Retakes are cheap, because each scene is a separate take |
| Designed synthetic voice (ElevenLabs Voice Design) | Good | Subscription | Describe the voice ("warm, measured British baritone"); the result is a new voice, not a copy of a real person's |
| Open-source TTS run locally (Kokoro, F5-TTS, XTTS) | Fair to good | Free; a GPU helps | Check each model's license for commercial use; the XTTS license is non-commercial |
| Built-in OS voice (Windows SAPI) | Poor | Free | Fine for drafts and timing, never for publishing |

Narration doesn't need radio diction. A clear, unhurried voice reading a tight script beats a
polished voice reading a loose one, and the script is the part that's fully under control.

## Scripting method

Each video is one Markdown file. Level-1 headings are chapters, and level-2 headings are scenes.
Each scene holds the narration and a visual directive; the build reads the file, renders each
scene, and times it to its narration. Text edits re-time the video automatically, and the chapter
headings become the chapter markers.

```markdown
---
title: Cross-references that can't break
voice: recorded        # or: elevenlabs:<voice-id>, sapi:Hazel (drafts only)
---

# Why links break

## problem
visual: code docs/quickstart.mdx | See [Install the CLI](../setup/install-cli.md)
then: command git mv docs/setup/install-cli.md docs/getting-started/
narration: |
  In plain Markdown, a link is a file path. Move or rename the page,
  and every link that points to it breaks. Silently.
```

With recorded narration, the take files follow the section IDs (`problem.wav`), and the build
uses each take's length as the scene's length.

### Workflow

1. **Outline** the chapters: the need, three to five examples, a recap. Then split each chapter
   into scenes of 20–60 seconds.
2. **Script** the narration. At about 150 words per minute, a 15-minute video is about 2,200
   words, the length of a long blog post. The post can share the script.
3. **Read it aloud once** before recording. Anything you stumble over, rewrite.
4. **Record** one take per scene, then build a draft with the synthetic voice to check the
   visuals.
5. **Build** the final video, review it at full speed, then publish it with captions and chapter
   markers.
6. **Cut a trailer** of 60–90 seconds from the same script, for LinkedIn and the top of the post.

### Writing for the ear

Spoken text follows different rules from written text:

| Problem | Fix |
|---|---|
| Acronyms read letter by letter or as a word, unpredictably | Write them as spoken in the narration (`M D X`), and keep the written form in the captions |
| Parentheses and asides lose the listener | Make each aside its own sentence, or cut it |
| Long sentences run out of breath | One idea per sentence; one point per scene |
| Code read aloud is noise | Show the code; say what it does |

## Equipment

### For recording narration

| Item | Recommendation | Why |
|---|---|---|
| Microphone | USB dynamic microphone (Samson Q2U, Shure MV7X or similar) | Dynamic mics pick up less room sound than condensers, which matters in an untreated room |
| Placement | 5–10 cm from the mouth, slightly off-axis, with a foam windscreen or pop filter | Reduces plosives and room echo |
| Room | The smallest, softest room available: curtains, a bed, a closet of clothes | Soft surfaces absorb the echo that marks home recordings |
| Headphones | Closed-back | Monitoring without bleeding into the mic |
| Software | Audacity or Reaper for voice; OBS Studio for screen recording | Free or low-cost, and well documented |

Post-processing runs in the build with ffmpeg: a high-pass filter at about 80 Hz, light noise
reduction and compression, then loudness normalized to about −16 LUFS (`loudnorm`).

### For generating video locally

Slides, screen recordings and ffmpeg assembly run on any recent laptop, including one with
integrated graphics. Local generative AI (voice cloning, avatars, background or face replacement)
doesn't:

| Component | Minimum | Comfortable |
|---|---|---|
| GPU | NVIDIA, 12 GB VRAM (RTX 3060 12 GB) | NVIDIA, 16–24 GB VRAM (RTX 4070 Ti Super, 4090) |
| RAM | 32 GB | 64 GB |
| Storage | 1 TB NVMe SSD | 2 TB NVMe SSD |

Cloud services (ElevenLabs, HeyGen, Synthesia, Descript) avoid the hardware entirely, at a monthly
cost. For screen-led videos with recorded narration, none of this is needed.

## Hosting

Docusaurus serves anything in `site/static/` (a file in `site/static/video/` is at `/video/…`), but
two limits rule that out for long videos. Cloudflare Workers won't serve a static asset larger than
25 MiB, and every committed video stays in the Git history for good.

| Video | Typical size | Where it goes |
|---|---|---|
| Slide-based prototype, about 1 minute | 1–2 MB | `site/static/video/` |
| Trailer, 60–90 seconds, 1080p | 5–20 MB | `site/static/video/` |
| Tutorial, about 15 minutes, 1080p screencast | 100–300 MB | A video host, embedded in the post |

Video host options:

| Host | Strength | Trade-off |
|---|---|---|
| YouTube | Free, and a second place to be found | Ads, and recommended videos from others at the end |
| Cloudflare Stream | Same provider as the site; no ads; adaptive streaming | Billed by minutes stored and delivered |
| Vimeo | Clean player, no ads | Paid plans for the features that matter |

Moving the site to another host doesn't change this. Vercel Pro (checked 2026-10-25) accepts CLI
deployments of up to 1 GB, but its fair use guidelines list media hosting for hot-linking as never
fair use, and its own answer for large files is separate storage (Vercel Blob). The Git history
problem stays on any host. Keeping videos off the site's host also means a future move of the site
doesn't take the videos with it.

Drafts stay in `tools/video/out/`, which Git ignores.

## Disclosure

Platforms such as YouTube ask creators to label realistic synthetic content. If a published video
uses a synthetic voice, say so in the description. Check each platform's current rules before
publishing.

## Open questions

- Is the extra attention worth the production time? A 15-minute tutorial is days of work, not
  hours. Measure it with one or two videos before committing to a series.
- Which host? YouTube brings discovery; Cloudflare Stream keeps viewers on the site.
- Captions: burn them in, or ship a separate track? A separate track is accessible and
  searchable; burned-in captions survive re-uploads to social media.
