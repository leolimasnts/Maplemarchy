"""Generate 4K Maple gradient wallpapers.

Each wallpaper is drawn small (960x540), blurred, upscaled to 3840x2160 and
lightly dithered to avoid banding. Glows are kept dim so Maple's light text
(#cbd5e1) keeps a high contrast ratio anywhere on the image.
"""

import subprocess
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
W, H = 960, 540
GLOW = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

C = {
    "blue": "8fc7ff",
    "lavender": "d2ccff",
    "green": "a4dfae",
    "cyan": "a1e8e5",
    "peach": "f0c0a8",
    "rose": "edabab",
    "yellow": "eecfa0",
    "pink": "e3cbeb",
    "slate": "64748b",
    "slate_dark": "334155",
    "lime": "d5f288",
}

# name: (base top-left, base bottom-right, [(color, x, y, radius, alpha), ...])
WALLS = {
    "slate-glow": ("2a2f3a", "141415", [("blue", 720, 150, 230, 0.13), ("lavender", 225, 425, 200, 0.10)]),
    "lavender-dusk": ("1c1b24", "121214", [("lavender", 480, 80, 300, 0.14), ("pink", 820, 460, 180, 0.08)]),
    "sage-mist": ("161a17", "111112", [("green", 200, 140, 260, 0.11), ("cyan", 780, 420, 200, 0.07)]),
    "peach-ember": ("1a1716", "111112", [("peach", 480, 600, 340, 0.15), ("rose", 120, 520, 180, 0.08)]),
    "rose-night": ("1d1719", "111112", [("rose", 820, 120, 240, 0.12), ("lavender", 160, 470, 220, 0.08)]),
    "cyan-tide": ("141a1b", "111112", [("cyan", 80, 270, 300, 0.12), ("blue", 860, 80, 160, 0.07)]),
    "aurora": ("131618", "0f0f10", [("green", 250, 120, 210, 0.10), ("cyan", 480, 90, 230, 0.10), ("blue", 720, 140, 220, 0.10), ("lavender", 900, 220, 170, 0.07)]),
    "maple-sunset": ("16161a", "1a1514", [("lavender", 480, 160, 320, 0.07), ("rose", 300, 560, 260, 0.11), ("peach", 680, 590, 280, 0.13)]),
    "twilight": ("1b2130", "121214", [("blue", 480, -60, 380, 0.12), ("lavender", 480, 650, 300, 0.07)]),
    "duo": ("151516", "151516", [("cyan", 0, 0, 330, 0.11), ("peach", 960, 540, 330, 0.11)]),
    "prism": ("141415", "141415", [("blue", 0, 0, 260, 0.10), ("lavender", 960, 0, 260, 0.10), ("green", 0, 540, 260, 0.09), ("peach", 960, 540, 260, 0.10)]),
    "midnight": ("1e1e1f", "111112", [("slate", 640, 200, 360, 0.12)]),
    "ink": ("0e0e0f", "0e0e0f", [("blue", 960, 540, 380, 0.08), ("slate_dark", 0, 0, 300, 0.20)]),
    "honey": ("19171a", "111112", [("yellow", 760, 160, 260, 0.11), ("peach", 220, 460, 200, 0.07)]),
    "lagoon": ("12181c", "111112", [("cyan", 300, 420, 260, 0.10), ("green", 700, 460, 220, 0.08), ("blue", 600, 80, 200, 0.07)]),
    "orchid": ("1a171d", "111112", [("pink", 300, 150, 260, 0.11), ("lavender", 760, 430, 240, 0.10)]),
    "horizon": ("111112", "1a1d24", [("blue", 480, 620, 520, 0.12), ("cyan", 480, 640, 260, 0.06)]),
    "spring": ("141615", "111112", [("lime", 780, 120, 220, 0.08), ("green", 300, 400, 260, 0.09)]),
}


def run(*args):
    subprocess.run(["magick", *args], check=True)


def generate(name, base_a, base_b, glows):
    small = OUT / f".{name}-small.png"
    draws = []
    for color, x, y, r, a in glows:
        draws += ["-fill", f"#{C[color]}{min(255, round(a * GLOW * 255)):02x}", "-draw", f"circle {x},{y} {x + r},{y}"]

    run(
        "-size", f"{W}x{H}", f"gradient:#{base_a}-#{base_b}", "-rotate", "0",
        "(", "-size", f"{W}x{H}", "xc:none", *draws, "-blur", "0x90", ")",
        "-composite",
        # soft vignette keeps the edges calm behind bars and corners
        "(", "-size", f"{W}x{H}", "radial-gradient:white-#b8b8b8", ")",
        "-compose", "multiply", "-composite",
        str(small),
    )
    run(
        str(small), "-filter", "Lanczos", "-resize", "3840x2160!",
        "-attenuate", "0.12", "+noise", "Gaussian",
        "-quality", "90", "-sampling-factor", "4:4:4",
        str(OUT / f"maple-{name}.jpg"),
    )
    small.unlink()


for name, (a, b, glows) in WALLS.items():
    generate(name, a, b, glows)
    print(name)
