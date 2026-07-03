#!/usr/bin/env python3
"""Write the BLOCKS logo splash to /dev/fb0 and cache as raw bytes.

Two modes:
  default       — write to /dev/fb0 and save cache (no VT switch; X11 activates tty7 itself)
  --precompute  — render and save cache only (no fb0 write)

The raw cache is consumed by bs-pre-stop.py (ExecStop) and bs-splash-holder.py
(tty8 boot splash); the PNG by feh in ExecStopPost.
"""

import argparse
import os
import struct
import tempfile
from pathlib import Path
from typing import Any

_SPLASH_LOG = Path(tempfile.gettempdir()) / "bs-splash.log"

_CACHE_PATH = Path("/home/blocks/.cache/blockscreen/splash.raw")

_LOGO_SEARCH = [
    Path(__file__).parent.parent
    / "BlocksScreen/lib/ui/resources/media/logoblocks400x300.png",
    Path(__file__).parent.parent / "BlocksScreen/lib/ui/resources/media/logoblocks.png",
    Path(__file__).parent.parent
    / "BlocksScreen/lib/ui/resources/media/graphics/logo_blocks.png",
]


def _log(msg: str) -> None:
    try:
        with _SPLASH_LOG.open("a") as f:
            f.write(f"{msg}\n")
    except Exception:  # nosec B110
        pass


def _fb_info() -> tuple[int, int, int, int] | None:
    base = "/sys/class/graphics/fb0"
    try:
        with open(f"{base}/virtual_size") as f:
            w, h = (int(x) for x in f.read().strip().split(","))
        with open(f"{base}/bits_per_pixel") as f:
            bpp = int(f.read().strip())
        try:
            with open(f"{base}/stride") as f:
                stride = int(f.read().strip())
        except OSError:
            stride = w * (bpp // 8)
        return w, h, bpp, stride
    except OSError as e:
        _log(f"Failed to read framebuffer info: {e}")
        return None


def _load_logo(Image):
    for path in _LOGO_SEARCH:
        if path.exists():
            try:
                img = Image.open(path).convert("RGBA")
                return img
            except Exception:  # nosec B112
                continue
    return None


def _render(w: int, h: int, Image, ImageDraw, ImageFont) -> Any:
    bg = Image.new("RGB", (w, h), (20, 20, 20))
    draw = ImageDraw.Draw(bg)
    logo = _load_logo(Image)
    if logo is not None:
        lw, lh = logo.size
        max_w, max_h = min(w // 2, 600), min(h // 2, 400)
        scale = min(max_w / lw, max_h / lh, 1.0)
        if scale < 1.0:
            lw, lh = int(lw * scale), int(lh * scale)
            logo = logo.resize((lw, lh), Image.LANCZOS)
        x, logo_y = (w - lw) // 2, (h - lh) // 2
        bg.paste(logo, (x, logo_y), logo)
        text_y = logo_y + lh + 24
    else:
        # Fallback: no logo — draw a placeholder card
        card_w, card_h = 500, 160
        cx, cy = (w - card_w) // 2, (h - card_h) // 2
        draw.rectangle(
            [(cx, cy), (cx + card_w, cy + card_h)],
            fill=(30, 30, 30),
            outline=(60, 60, 60),
            width=2,
        )
        text_y = cy + card_h + 24
    font = None
    for _fp in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ):
        try:
            font = ImageFont.truetype(_fp, 19)
            break
        except (OSError, AttributeError):
            pass
    if font is None:
        font = ImageFont.load_default()
    text = "Starting ..."
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
    except AttributeError:
        text_w = int(draw.textlength(text, font=font))
    draw.text(((w - text_w) // 2, text_y), text, fill=(180, 180, 180), font=font)
    return bg


def _encode(img, bpp: int, w: int, h: int, stride: int, Image) -> bytes | None:
    try:
        if bpp == 32:
            r, g, b = img.split()
            bgra = Image.merge("RGBA", (b, g, r, Image.new("L", (w, h), 255)))
            raw = bgra.tobytes()
            if stride == w * 4:
                return raw
            rows = [bytearray(stride) for _ in range(h)]
            for y, row in enumerate(rows):
                row[: w * 4] = raw[y * w * 4 : (y + 1) * w * 4]
            return b"".join(bytes(row) for row in rows)
        pixels = img.tobytes()
        arr = bytearray(h * stride)
        for y in range(h):
            for x in range(w):
                off = (y * w + x) * 3
                struct.pack_into(
                    "<H",
                    arr,
                    y * stride + x * 2,
                    ((pixels[off] >> 3) << 11)
                    | ((pixels[off + 1] >> 2) << 5)
                    | (pixels[off + 2] >> 3),
                )
        return bytes(arr)
    except Exception as e:
        _log(f"Encode error: {e}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--precompute",
        action="store_true",
        help="Save cache only; skip fb0 write and tty setup",
    )
    args = parser.parse_args()

    if not args.precompute and not os.path.exists("/dev/fb0"):
        _log("No /dev/fb0")
        return

    fb_info = _fb_info()
    if fb_info is None:
        return
    w, h, bpp, stride = fb_info

    if bpp not in (16, 32):
        _log(f"Unsupported bpp: {bpp}")
        return

    try:
        from PIL import Image, ImageDraw, ImageFont  # noqa: PLC0415
    except ImportError:
        _log("PIL not available")
        return

    try:
        img = _render(w, h, Image, ImageDraw, ImageFont)
    except Exception as e:
        _log(f"Render error: {e}")
        return

    # Save PNG for X11 root-window splash (feh --bg-fill in ExecStopPost)
    try:
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(_CACHE_PATH.parent / "splash.png"))
    except Exception as e:
        _log(f"PNG save failed: {e}")

    fb_data = _encode(img, bpp, w, h, stride, Image)
    if fb_data is None:
        return

    # Save raw cache so bs-pre-stop.py / bs-splash-holder.py can write fb0 directly
    try:
        _CACHE_PATH.write_bytes(fb_data)
    except OSError as e:
        _log(f"Cache write failed: {e}")

    if args.precompute:
        return

    # Write logo to fb0 so fbcon on tty7 shows it immediately when X11 activates tty7.
    # We do NOT switch VTs or set KD_GRAPHICS here — X11 does VT_ACTIVATE(7) itself
    # at startup (that init step is not affected by -novtswitch), which keeps tty8
    # active with the splash visible until X11 is truly ready to take over the display.
    try:
        with open("/dev/fb0", "wb") as fb:
            fb.write(fb_data)
    except PermissionError:
        _log("Permission denied on /dev/fb0 — check 'video' group membership")
    except OSError as e:
        _log(f"fb0 write error: {e}")


if __name__ == "__main__":
    main()
