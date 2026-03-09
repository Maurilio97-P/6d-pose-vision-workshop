"""
generate_aruco_markers.py
--------------------------
Batch-generate ArUco marker PNG files ready to print.

Usage:
    python scripts/generate_aruco_markers.py
    python scripts/generate_aruco_markers.py --ids 0 1 2 3 --size 800
    python scripts/generate_aruco_markers.py --dict DICT_5X5_100 --ids 0-9

Arguments:
    --dict      ArUco dictionary name (default: DICT_4X4_50)
    --ids       Marker IDs to generate. Space-separated list or range (e.g. 0-9)
    --size      Output image size in pixels (default: 600)
    --border    White border padding in pixels (default: 60)
    --out       Output directory (default: assets/aruco_markers)

Output:
    One PNG per marker: <dict>_id<NNN>.png
    Run from repo root. Prints physical size at 300 DPI.

Requirements: opencv-contrib-python
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
