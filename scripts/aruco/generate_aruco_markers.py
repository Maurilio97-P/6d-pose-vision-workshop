"""
generate_aruco_markers.py
--------------------------
Batch-generate ArUco marker PNG files ready to print.

Before you run — set up your environment:
    If you haven't already, create and activate a virtual environment:

    # 1. Create the venv (only once, from the repo root):
    python -m venv venv

    # 2. Activate it (every time you open a new terminal):
    #    Windows:
    venv\Scripts\activate
    #    macOS / Linux:
    source venv/bin/activate

    # 3. Install dependencies (only once, after activating):
    pip install -r requirements.txt

    You should see (venv) at the start of your terminal prompt.
    If you don't, the venv is not active and the script will fail with
    "ModuleNotFoundError: No module named 'cv2'".

Usage:
    python scripts/aruco/generate_aruco_markers.py
    python scripts/aruco/generate_aruco_markers.py --ids 0 1 2 3 --size 800
    python scripts/aruco/generate_aruco_markers.py --dict DICT_5X5_100 --ids 0-9

Arguments:
    --dict      ArUco dictionary name (default: DICT_4X4_50).
                Choose from: DICT_4X4_50, DICT_4X4_100, DICT_4X4_250,
                DICT_5X5_50, DICT_5X5_100, DICT_5X5_250, DICT_6X6_250, DICT_7X7_1000.
                Use the same dictionary when generating and detecting.
    --ids       Marker IDs to generate. Space-separated integers or a dash range.
                Examples: --ids 0 1 2 3   or   --ids 0-9   (default: 0-9)
    --size      Marker image size in pixels, not counting the border (default: 600)
    --border    White border padding added around the marker in pixels (default: 60).
                A white border is required for reliable detection.
    --out       Output directory (default: assets/aruco_markers).
                Created automatically if it does not exist.

How it works, step by step:
    1. Parses the requested IDs (space-separated integers or a dash range like 0-9).
    2. Looks up the OpenCV ArUco dictionary constant for the chosen --dict name.
    3. For each requested ID, calls cv2.aruco.generateImageMarker (or the legacy
       drawMarker on older OpenCV) to render the black-and-white pattern.
    4. Adds a white border of --border pixels on all four sides.
    5. Saves the result as a PNG file named <dict>_id<NNN>.png in the output folder.
    6. Prints a physical size estimate at 300 DPI so you know how large the marker
       will be when you print it.

After running:
    - Open assets/aruco_markers/ (or your --out directory) to find the PNG files.
    - Print them on plain matte paper at 100% scale (do not let the printer rescale).
    - Measure the printed marker with a ruler and record the size — you will need
      this measurement as --marker-length when running the pose estimation scripts.
    - Mount markers flat on a rigid surface for best detection results.
"""

import cv2
import numpy as np
import os
import argparse

# ── Dictionary name → cv2 constant ──────────────────────────────────────────
DICT_MAP = {
    "DICT_4X4_50":   cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100":  cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250":  cv2.aruco.DICT_4X4_250,
    "DICT_5X5_50":   cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100":  cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250":  cv2.aruco.DICT_5X5_250,
    "DICT_6X6_250":  cv2.aruco.DICT_6X6_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
}
# ────────────────────────────────────────────────────────────────────────────


def parse_args():
    p = argparse.ArgumentParser(description="Batch-generate ArUco marker PNGs.")
    p.add_argument("--dict",   default="DICT_4X4_50",
                   choices=list(DICT_MAP.keys()), help="ArUco dictionary")
    p.add_argument("--ids",    nargs="+", default=["0-9"],
                   help="Marker IDs. Space-separated or range e.g. '0 1 2' or '0-9'")
    p.add_argument("--size",   type=int, default=600, help="Image size in pixels")
    p.add_argument("--border", type=int, default=60,  help="White border padding (px)")
    p.add_argument("--out",    default="assets/aruco_markers", help="Output directory")
    return p.parse_args()


def parse_ids(id_args):
    """Parse '0 1 2' or '0-9' into a list of ints."""
    ids = []
    for token in id_args:
        if "-" in token and not token.startswith("-"):
            lo, hi = token.split("-")
            ids.extend(range(int(lo), int(hi) + 1))
        else:
            ids.append(int(token))
    return sorted(set(ids))


def get_aruco_dict(dict_id):
    try:
        return cv2.aruco.getPredefinedDictionary(dict_id)
    except AttributeError:
        return cv2.aruco.Dictionary_get(dict_id)


def generate_marker(aruco_dict, marker_id, size_px):
    try:
        return cv2.aruco.generateImageMarker(aruco_dict, marker_id, size_px)
    except AttributeError:
        buf = np.zeros((size_px, size_px, 1), dtype="uint8")
        cv2.aruco.drawMarker(aruco_dict, marker_id, size_px, buf, 1)
        return buf.squeeze()


def add_white_border(img, border_px):
    h, w = img.shape[:2]
    canvas = np.ones((h + 2 * border_px, w + 2 * border_px), dtype=np.uint8) * 255
    canvas[border_px:border_px + h, border_px:border_px + w] = img
    return canvas


def main():
    args = parse_args()
    ids = parse_ids(args.ids)

    os.makedirs(args.out, exist_ok=True)

    dict_id = DICT_MAP[args.dict]
    aruco_dict = get_aruco_dict(dict_id)

    cm_per_px = 2.54 / 300  # at 300 DPI
    total_px = args.size + 2 * args.border
    print_cm = total_px * cm_per_px

    print(f"Dictionary : {args.dict}")
    print(f"IDs        : {ids}")
    print(f"Size       : {args.size}px marker + {args.border}px border = {total_px}px total")
    print(f"Print size : {print_cm:.1f} cm × {print_cm:.1f} cm at 300 DPI")
    print(f"Output dir : {args.out}/")
    print()

    for mid in ids:
        img = generate_marker(aruco_dict, mid, args.size)
        if args.border > 0:
            img = add_white_border(img, args.border)

        dict_short = args.dict.lower().replace("dict_", "")
        filename = f"{dict_short}_id{mid:03d}.png"
        path = os.path.join(args.out, filename)
        cv2.imwrite(path, img)
        print(f"  Saved: {path}")

    print(f"\nDone — {len(ids)} markers saved to '{args.out}/'")
    print("Tip: Use matte paper, print B&W, mount flat on rigid surface.")


if __name__ == "__main__":
    main()
