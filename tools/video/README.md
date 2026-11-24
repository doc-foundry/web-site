# Video builder

Builds the narrated demo videos described in `../../notes/video-tutorials.md`. One Python script
draws every frame, generates the narration, and hands both to ffmpeg. Each scene lasts as long as
its narration, so editing a sentence re-times the video.

## Requirements

- Windows, for the built-in speech voice (Microsoft Hazel) and the fonts in `C:\Windows\Fonts`
- Python 3 with Pillow
- ffmpeg on `PATH`

## Run it

```sh
python make_video.py
```

The video goes to `out/xref-demo.mp4`, and intermediate audio and subtitle files to `build/`.
Both folders are ignored by Git. A full build takes about two minutes.

The built-in voice is for drafts only. For a published video, replace it with recorded or
designed narration, as the notes describe.
