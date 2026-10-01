"""Generate Doc Foundry logo SVGs: a gear with a pen-nib cut-out, plus an outlined wordmark.

Needs fonttools and Montserrat.ttf (the Google Fonts variable font, ofl/montserrat) beside this
script. Writes to ./out; copy logo*.svg and mark.svg to site/static/img.
"""
import math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

NAVY, CHARCOAL = "#1F3A5F", "#3A3D42"
NAVY_DARK, TEXT_DARK = "#8DB4E2", "#E6E8EB"


def gear(cx=50, cy=50, teeth=8, R=48, r=40):
    pts, step = [], 2 * math.pi / teeth
    for i in range(teeth):
        a = i * step - math.pi / 2
        # root -> flank up -> tip -> flank down (tip narrower than base)
        for ang, rad in ((a - 0.30 * step, r), (a - 0.17 * step, R),
                         (a + 0.17 * step, R), (a + 0.30 * step, r)):
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


# Nib cut-out (upright, tip down), its slit and breather hole re-filled via even-odd.
NIB = ("M37 22 L63 22 L64.5 38 C69 48 66 60 50 84 "
       "C34 60 31 48 35.5 38 Z")
SLIT = "M48.9 58 L51.1 58 L51.1 78 L48.9 78 Z"
HOLE = "M50 46.5 a4.5 4.5 0 1 0 0.001 0 Z"
COLLAR = "M35.5 31 L64.5 31 L64.7 34 L35.3 34 Z"  # band across the nib shoulder
MARK = " ".join((gear(), NIB, SLIT, HOLE, COLLAR))


def wordmark(text, weight, cap_height, tracking=0.06):
    font = instantiateVariableFont(TTFont("Montserrat.ttf"), {"wght": weight})
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    s = cap_height / font["OS/2"].sCapHeight
    pen, x = SVGPathPen(gs), 0.0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, cap_height)))
        x += gs[g].width * s + (tracking * cap_height if ch != " " else 0)
    return pen.getCommands(), x - tracking * cap_height


def mark_svg(color, bg=None, scale=1.0):
    rect = f'<rect width="100" height="100" fill="{bg}"/>' if bg else ""
    t = f' transform="translate(50 50) scale({scale}) translate(-50 -50)"' if scale != 1 else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{rect}'
            f'<path fill="{color}" fill-rule="evenodd"{t} d="{MARK}"/></svg>')


def lockup_svg(mark_color, text_color):
    cap = 40
    d, w = wordmark("DOC FOUNDRY", 700, cap)
    gap, ty = 22, 50 - cap / 2
    W = 100 + gap + w
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} 100">'
            f'<path fill="{mark_color}" fill-rule="evenodd" d="{MARK}"/>'
            f'<path fill="{text_color}" transform="translate({100 + gap} {ty:.2f})" d="{d}"/>'
            f'</svg>')


if __name__ == "__main__":
    files = {
        "out/logo.svg": lockup_svg(NAVY, CHARCOAL),
        "out/logo-dark.svg": lockup_svg(NAVY_DARK, TEXT_DARK),
        "out/mark.svg": mark_svg(NAVY),
        "out/mark-dark.svg": mark_svg(NAVY_DARK),
        "out/avatar.svg": mark_svg("#FFFFFF", NAVY, scale=0.66),
    }
    import os
    os.makedirs("out", exist_ok=True)
    for p, s in files.items():
        open(p, "w", encoding="utf-8").write(s)
        print(p, len(s))
