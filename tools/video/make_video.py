"""Build a ~1-minute narrated demo video of the Xref component.

Narration: Windows SAPI (Microsoft Hazel). Frames: Pillow, piped to ffmpeg.
Output: out/xref-demo.mp4 (H.264 + AAC, soft English subtitles). Intermediate files go to build/.
"""
import subprocess, wave, os, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
TMP = HERE / "build"; TMP.mkdir(exist_ok=True)
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
W, H, FPS = 1280, 720, 30
FONTS = Path("C:/Windows/Fonts")
UI = lambda s: ImageFont.truetype(str(FONTS / "segoeui.ttf"), s)
UIB = lambda s: ImageFont.truetype(str(FONTS / "seguisb.ttf"), s)
MONO = lambda s: ImageFont.truetype(str(FONTS / "CascadiaMono.ttf"), s)

BG, PANEL, TEXT, MUTED = "#0F1B2D", "#16263D", "#E6E8EB", "#8A97A8"
ACCENT, GREEN, RED, YELLOW = "#8DB4E2", "#4FDDBF", "#F2666B", "#F2C76B"
KEY, STR, PUNCT = "#8DB4E2", "#B5E08D", "#8A97A8"

# --- scenes: (title, narration, draw function name) ------------------------------
SCENES = [
    ("Cross-references that can't break",
     "In the next minute, you'll see how the x-ref component keeps the links in your M D X "
     "documentation from breaking.", "title"),
    ("The problem: links are file paths",
     "In plain Markdown, a link is a file path. Move or rename the page, and every link "
     "that points to it breaks. Silently.", "problem"),
    ("Step 1: give each page a stable ID",
     "With x-ref, each page gets a stable ID in one registry. The ID never changes, "
     "even when the file moves.", "registry"),
    ("Step 2: link to the ID, not the path",
     "In your M D X, you link to the ID instead of the path. Leave out the link text, "
     "and x-ref fills in the page title for you.", "source"),
    ("Step 3: the build resolves it",
     "When Docusaurus builds the site, each x-ref becomes an ordinary link in the static page. "
     "Readers always see the current title.", "rendered"),
    ("Typos fail the build",
     "Mistype an ID, and the build fails, naming the file and the line. "
     "A broken link never reaches your readers.", "fail"),
    ("Recap",
     "Stable IDs, automatic titles, and checked links. One small component, "
     "reliable cross-references.", "recap"),
]

# --- narration -------------------------------------------------------------------
TTS_PS = r"""
param($txt, $out)
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice('Microsoft Hazel Desktop'); $s.Rate = 1
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(22050, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
$s.SetOutputToWaveFile($out, $fmt)
$s.Speak((Get-Content -Raw $txt)); $s.Dispose()
"""

def narrate(i, text):
    ps, txt, wav = TMP / "tts.ps1", TMP / f"n{i}.txt", TMP / f"n{i}.wav"
    ps.write_text(TTS_PS); txt.write_text(text, encoding="utf-8")
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                    str(ps), str(txt), str(wav)], check=True)
    with wave.open(str(wav)) as w:
        return wav, w.getnframes() / w.getframerate()

LEAD, TAIL = 0.4, 0.7  # silence before and after each scene's narration

# --- drawing helpers ---------------------------------------------------------------
def ease(x): return 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, x)))

def frame_base(title, idx):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.text((60, 34), "Doc Foundry", font=UIB(20), fill=ACCENT)
    d.text((W - 60, 34), f"xref  ·  {idx}/{len(SCENES)}", font=UI(18), fill=MUTED, anchor="ra")
    d.line((60, 72, W - 60, 72), fill="#24364F", width=1)
    if idx > 1:
        d.text((60, 100), title, font=UIB(40), fill=TEXT)
    return im, d

def code_panel(d, x, y, w, lines, shown, size=24, label=None):
    """lines: list of [(text, color)]; shown: chars revealed (typing effect)."""
    lh = int(size * 1.6)
    h = lh * len(lines) + 40 + (30 if label else 0)
    d.rounded_rectangle((x, y, x + w, y + h), 14, fill=PANEL)
    ty = y + 20
    if label:
        d.text((x + 24, ty), label, font=UI(16), fill=MUTED); ty += 30
    left, f = shown, MONO(size)
    for line in lines:
        cx = x + 24
        for seg, col in line:
            if left <= 0: break
            part = seg[:int(left)]; left -= len(seg)
            d.text((cx, ty), part, font=f, fill=col); cx += d.textlength(part, font=f)
        ty += lh
    return y + h

def total_chars(lines): return sum(len(s) for l in lines for s, _ in l)

def caption(d, text, y, color=TEXT, size=26):
    d.text((60, y), text, font=UI(size), fill=color)

# --- scenes ------------------------------------------------------------------------
def s_title(d, t, T):
    a = ease(t / 1.0)
    d.text((W // 2, 300), "Cross-references", font=UIB(64), fill=TEXT, anchor="mm")
    d.text((W // 2, 380), "that can't break", font=UIB(64), fill=ACCENT, anchor="mm")
    d.text((W // 2, 470), "An Xref component for MDX documentation", font=UI(28), fill=MUTED, anchor="mm")
    d.rectangle((W // 2 - 160 * a, 420, W // 2 + 160 * a, 423), fill=GREEN)

def s_problem(d, t, T):
    line = [[("See ", TEXT), ("[Install the CLI]", ACCENT), ("(../setup/install-cli.md)", STR)]]
    bottom = code_panel(d, 60, 180, W - 120, line, 999, label="docs/quickstart.mdx")
    if t > T * 0.40:
        k = ease((t - T * 0.40) / 0.6)
        code_panel(d, 60, bottom + 30, W - 120,
                   [[("git mv ", MUTED), ("docs/setup/install-cli.md", TEXT),
                     ("  →  ", MUTED), ("docs/getting-started/", YELLOW)]],
                   999 * k, label="Someone reorganizes the docs")
    if t > T * 0.62:
        d.line((84, 241, 84 + 690 * ease((t - T * 0.62) / 0.4), 241), fill=RED, width=3)
        caption(d, "404  —  and nothing warns you", 470, RED, 30)

REG = [[("{", PUNCT)],
       [('  "install-cli"', KEY), (": { ", PUNCT), ('"path"', KEY), (": ", PUNCT),
        ('"/getting-started/install-cli"', STR), (",", PUNCT)],
       [("                 ", PUNCT), ('"title"', KEY), (": ", PUNCT), ('"Installing the CLI"', STR), (" },", PUNCT)],
       [('  "config-ref"', KEY), (":  { ", PUNCT), ('"path"', KEY), (": ", PUNCT),
        ('"/reference/config"', STR), (",", PUNCT)],
       [("                 ", PUNCT), ('"title"', KEY), (": ", PUNCT), ('"Configuration reference"', STR), (" }", PUNCT)],
       [("}", PUNCT)]]

def s_registry(d, t, T):
    n = total_chars(REG) * ease(t / (T * 0.6))
    bottom = code_panel(d, 60, 180, W - 120, REG, n, size=22, label="xrefs.json")
    if t > T * 0.65:
        caption(d, "The ID stays the same.  Only the path changes when a file moves.", bottom + 30, GREEN)

SRC = [[("Before you start, read ", TEXT), ("<Xref ", ACCENT), ("id", KEY), ("=", PUNCT),
        ('"install-cli"', STR), (" />", ACCENT), (".", TEXT)],
       [("All options are in the ", TEXT), ("<Xref ", ACCENT), ("id", KEY), ("=", PUNCT),
        ('"config-ref"', STR), (">", ACCENT), ("configuration reference", TEXT), ("</Xref>", ACCENT), (".", TEXT)]]

def s_source(d, t, T):
    n = total_chars(SRC) * ease(t / (T * 0.55))
    bottom = code_panel(d, 60, 180, W - 120, SRC, n, size=22, label="docs/quickstart.mdx")
    if t > T * 0.6:
        caption(d, "No link text  →  Xref inserts the page title", bottom + 30, GREEN)
        caption(d, "Your own text  →  kept as written", bottom + 75, MUTED)

def s_rendered(d, t, T):
    # mock browser window
    x0, y0, x1, y1 = 60, 180, W - 60, 520
    d.rounded_rectangle((x0, y0, x1, y1), 14, fill="#FFFFFF")
    d.rounded_rectangle((x0, y0, x1, y0 + 44), 14, fill="#E4E7EB")
    d.rectangle((x0, y0 + 30, x1, y0 + 44), fill="#E4E7EB")
    for i, c in enumerate(("#F2666B", "#F2C76B", "#4FDDBF")):
        d.ellipse((x0 + 18 + i * 22, y0 + 15, x0 + 32 + i * 22, y0 + 29), fill=c)
    d.rounded_rectangle((x0 + 100, y0 + 10, x1 - 20, y0 + 34), 8, fill="#FFFFFF")
    d.text((x0 + 114, y0 + 12), "doc-foundry.com/docs/quickstart", font=UI(16), fill="#555")
    d.text((x0 + 40, y0 + 70), "Quickstart", font=UIB(36), fill="#1F3A5F")
    f, link = UI(24), "#2563EB"
    a = ease((t - 0.4) / 0.8)
    def para(y, pre, lt, post):
        cx = x0 + 40
        d.text((cx, y), pre, font=f, fill="#3A3D42"); cx += d.textlength(pre, font=f)
        d.text((cx, y), lt, font=f, fill=link); lw = d.textlength(lt, font=f)
        d.line((cx, y + 32, cx + lw * a, y + 32), fill=link, width=2); cx += lw
        d.text((cx, y), post, font=f, fill="#3A3D42")
    para(y0 + 140, "Before you start, read ", "Installing the CLI", ".")
    para(y0 + 190, "All options are in the ", "configuration reference", ".")
    if t > T * 0.5:
        caption(d, "href = /getting-started/install-cli   ·   title pulled from the registry", 550, GREEN, 24)

ERR = [[("$ ", MUTED), ("npm run build", TEXT)],
       [("", TEXT)],
       [("error ", RED), ('Unknown Xref id "instal-cli"', RED)],
       [("  at docs/quickstart.mdx:12:24", YELLOW)],
       [("  Did you mean ", MUTED), ('"install-cli"', GREEN), ("?", MUTED)],
       [("Build failed.", RED)]]

def s_fail(d, t, T):
    n = 13 if t < 0.8 else 13 + (total_chars(ERR) - 13) * ease((t - 0.8) / 1.2)
    code_panel(d, 60, 180, W - 120, ERR, n, label="Terminal")

def s_recap(d, t, T):
    items = [("Stable IDs", "files can move; links don't care"),
             ("Automatic titles", "link text can't drift from the page"),
             ("Checked links", "a typo stops the build, not the reader")]
    for i, (h, s) in enumerate(items):
        a = ease((t - 0.3 - i * 1.2) / 0.5)
        if a <= 0: continue
        y = 200 + i * 110
        d.text((80, y), "✔", font=ImageFont.truetype(str(FONTS / "seguisym.ttf"), 40), fill=GREEN)
        d.text((140, y), h, font=UIB(36), fill=TEXT)
        d.text((140, y + 50), s, font=UI(24), fill=MUTED)
    if t > T * 0.7:
        d.text((W // 2, 610), "One small component.  Reliable cross-references.",
               font=UIB(28), fill=ACCENT, anchor="mm")

DRAW = {n: globals()[f"s_{n}"] for n in ("title", "problem", "registry", "source", "rendered", "fail", "recap")}

# --- assemble ----------------------------------------------------------------------
def srt_time(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def main():
    durs, wavs = [], []
    for i, (_, text, _) in enumerate(SCENES):
        wav, secs = narrate(i, text); wavs.append(wav); durs.append(LEAD + secs + TAIL)

    # audio track: per scene, LEAD silence + narration + pad to scene length
    with wave.open(str(TMP / "narration.wav"), "wb") as out:
        out.setnchannels(1); out.setsampwidth(2); out.setframerate(22050)
        for wav, dur in zip(wavs, durs):
            with wave.open(str(wav)) as w: data = w.readframes(w.getnframes())
            lead = b"\0\0" * int(LEAD * 22050)
            tail = b"\0\0" * (int(dur * 22050) - len(lead) // 2 - len(data) // 2)
            out.writeframes(lead + data + tail)

    # subtitles
    srt, t0 = [], 0.0
    for i, ((_, text, _), dur) in enumerate(zip(SCENES, durs), 1):
        srt.append(f"{i}\n{srt_time(t0 + LEAD)} --> {srt_time(t0 + dur - 0.3)}\n{text.replace('M D X', 'MDX').replace('x-ref', 'Xref')}\n")
        t0 += dur
    (TMP / "narration.srt").write_text("\n".join(srt), encoding="utf-8")

    out_mp4 = OUT / "xref-demo.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", str(TMP / "narration.wav"), "-i", str(TMP / "narration.srt"),
        "-map", "0:v", "-map", "1:a", "-map", "2:s",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
        "-movflags", "+faststart", "-shortest", str(out_mp4)], stdin=subprocess.PIPE)
    black = Image.new("RGB", (W, H), BG)
    for idx, ((title, _, name), dur) in enumerate(zip(SCENES, durs), 1):
        n = int(round(dur * FPS))
        for k in range(n):
            t = k / FPS
            im, d = frame_base(title, idx); DRAW[name](d, t, dur)
            fade = min(1, t / 0.3, (dur - t) / 0.3)  # fade in/out 0.3 s
            if fade < 1: im = Image.blend(black, im, max(0, fade))
            ff.stdin.write(im.tobytes())
    ff.stdin.close(); ff.wait()
    print(f"{out_mp4}  ({sum(durs):.1f} s)")

if __name__ == "__main__":
    main()
