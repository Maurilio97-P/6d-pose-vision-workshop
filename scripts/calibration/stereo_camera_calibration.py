"""
stereo_camera_calibration.py
-----------------------------
Full stereo camera calibration pipeline (one-time setup).
Reads matching chessboard image pairs from two folders (left/ and right/),
calibrates each camera individually, runs stereoCalibrate, rectifies,
builds undistort+rectify maps, and saves everything to stereo_maps.npz.

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
    python scripts/calibration/stereo_camera_calibration.py --left-dir left/ --right-dir right/
    python scripts/calibration/stereo_camera_calibration.py --left-dir images/L --right-dir images/R --cols 9 --rows 6

Image requirements:
    - Capture pairs simultaneously: left camera saves calib_00.jpg AND right camera
      saves calib_00.jpg at the same moment, with identical filenames in each folder.
    - Minimum 8–10 image pairs at varied chessboard angles and distances.
    - The chessboard must be fully visible in BOTH cameras in every single pair.
    - At least 4 valid pairs are required; aim for 15–20 for a good calibration.

Arguments:
    --left-dir    Folder containing left camera images (default: stereo_left)
    --right-dir   Folder containing right camera images (default: stereo_right)
    --cols        Number of inner corner columns on the chessboard (default: 9)
    --rows        Number of inner corner rows on the chessboard (default: 6)
    --square      Physical side length of one square in METERS (default: 0.025 = 2.5 cm)
    --out         Output .npz file path (default: assets/calibration/stereo_maps.npz)
    --alpha       Rectification crop setting: 0 = crop to valid pixels only (default),
                  1 = keep full field of view (leaves black borders after rectification)

How it works, step by step:
    1. Scans both folders and matches image pairs by filename (falls back to
       positional matching if filenames differ).
    2. For each pair, runs findChessboardCorners on both images.
       Pairs where the board is not found in either camera are skipped.
    3. Calibrates each camera individually with calibrateCamera to get K and dist.
       Prints RMS reprojection error — a value below 1.0 px is excellent.
    4. Runs stereoCalibrate (fixing intrinsics) to compute the rotation R and
       translation T between the two cameras. Prints stereo RMS and baseline distance.
    5. Runs stereoRectify to compute rectification transforms R1, R2, P1, P2, Q.
    6. Builds per-pixel remap tables (map1_L, map2_L, map1_R, map2_R) with
       initUndistortRectifyMap for fast per-frame remapping at runtime.
    7. Saves everything to the output .npz file.

Output file (stereo_maps.npz) contains:
    map1_L, map2_L, map1_R, map2_R  — remap maps for left/right cameras
    Q                                — 4×4 disparity-to-depth matrix
    K_L, dist_L, K_R, dist_R        — intrinsics
    R, T, R1, R2, P1, P2            — stereo geometry
    baseline_m                       — camera separation in meters
    rms_stereo                       — reprojection error at calibration time

After running:
    The .npz file is saved to --out (default: assets/calibration/stereo_maps.npz).
    Use it with scripts/stereo/stereo_depth_live.py to run real-time depth estimation.

    Load in your own depth app:
        data = np.load("stereo_maps.npz")
        left_rect  = cv2.remap(left_raw,  data["map1_L"], data["map2_L"], cv2.INTER_LINEAR)
        right_rect = cv2.remap(right_raw, data["map1_R"], data["map2_R"], cv2.INTER_LINEAR)
        Q          = data["Q"]  # disparity-to-depth matrix
"""

import cv2
import numpy as np
import os
import glob
import argparse


def parse_args():
    p = argparse.ArgumentParser(description="Stereo camera calibration.")
    p.add_argument("--left-dir",  default="stereo_left",  help="Left image folder")
    p.add_argument("--right-dir", default="stereo_right", help="Right image folder")
    p.add_argument("--cols",   type=int,   default=9,     help="Inner corner columns")
    p.add_argument("--rows",   type=int,   default=6,     help="Inner corner rows")
    p.add_argument("--square", type=float, default=0.025, help="Square side in meters")
    p.add_argument("--out",    default="assets/calibration/stereo_maps.npz")
    p.add_argument("--alpha",  type=float, default=0.0,
                   help="Rectification alpha (0=crop valid, 1=full FOV)")
    return p.parse_args()


def find_image_pairs(left_dir, right_dir):
    """Match images by filename across left and right folders."""
    exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    def collect(d):
        files = []
        for ext in exts:
            files.extend(glob.glob(os.path.join(d, ext)))
        return sorted(files)

    left_files  = collect(left_dir)
    right_files = collect(right_dir)

    # Match by basename
    left_map  = {os.path.basename(f): f for f in left_files}
    right_map = {os.path.basename(f): f for f in right_files}
    shared = sorted(set(left_map) & set(right_map))

    if not shared:
        # Fall back to positional matching
        n = min(len(left_files), len(right_files))
        return list(zip(left_files[:n], right_files[:n]))

    return [(left_map[name], right_map[name]) for name in shared]


def detect_corners(img, board_size, criteria):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)
    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    return ret, corners, gray


def main():
    args = parse_args()
    board_size = (args.cols, args.rows)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # 3D object points
    objp = np.zeros((args.cols * args.rows, 3), np.float32)
    objp[:, :2] = np.mgrid[0:args.cols, 0:args.rows].T.reshape(-1, 2)
    objp *= args.square

    print(f"Board      : {args.cols}×{args.rows} inner corners, {args.square*100:.1f}cm squares")
    print(f"Left dir   : {args.left_dir}")
    print(f"Right dir  : {args.right_dir}")

    # ── Find image pairs ──────────────────────────────────────────────────────
    pairs = find_image_pairs(args.left_dir, args.right_dir)
    if not pairs:
        print(f"ERROR: No matching image pairs found in '{args.left_dir}' and '{args.right_dir}'")
        return
    print(f"Found      : {len(pairs)} image pairs")

    # ── Detect corners ────────────────────────────────────────────────────────
    all_objpts, imgpts_L, imgpts_R = [], [], []
    img_size = None

    for i, (path_L, path_R) in enumerate(pairs):
        img_L = cv2.imread(path_L)
        img_R = cv2.imread(path_R)
        if img_L is None or img_R is None:
            print(f"  Skipped pair {i}: could not read images")
            continue

        if img_size is None:
            img_size = (img_L.shape[1], img_L.shape[0])  # (W, H)

        ret_L, c_L, gray_L = detect_corners(img_L, board_size, criteria)
        ret_R, c_R, gray_R = detect_corners(img_R, board_size, criteria)

        if ret_L and ret_R:
            all_objpts.append(objp)
            imgpts_L.append(c_L)
            imgpts_R.append(c_R)
            print(f"  Pair {i:02d}: ✓  ({os.path.basename(path_L)})")
        else:
            status = f"{'✗L' if not ret_L else '  '}{'✗R' if not ret_R else '  '}"
            print(f"  Pair {i:02d}: {status} corners not found — skipped")

    if len(all_objpts) < 4:
        print(f"\nERROR: Only {len(all_objpts)} valid pairs. Need at least 4. "
              "Check board size and image quality.")
        return

    print(f"\nUsing {len(all_objpts)}/{len(pairs)} valid pairs for calibration.")

    # ── Step 1: Individual camera calibration ────────────────────────────────
    print("\nCalibrating LEFT camera...")
    rms_L, K_L, dist_L, _, _ = cv2.calibrateCamera(
        all_objpts, imgpts_L, img_size, None, None)
    print(f"  RMS: {rms_L:.4f} px  fx={K_L[0,0]:.1f}")

    print("Calibrating RIGHT camera...")
    rms_R, K_R, dist_R, _, _ = cv2.calibrateCamera(
        all_objpts, imgpts_R, img_size, None, None)
    print(f"  RMS: {rms_R:.4f} px  fx={K_R[0,0]:.1f}")

    if rms_L > 2.0 or rms_R > 2.0:
        print("WARNING: High reprojection error (>2.0px). "
              "Consider recapturing with more diverse angles.")

    # ── Step 2: Stereo calibration ────────────────────────────────────────────
    print("\nRunning stereoCalibrate...")
    rms_stereo, K_L, dist_L, K_R, dist_R, R, T, E, F = cv2.stereoCalibrate(
        all_objpts, imgpts_L, imgpts_R,
        K_L.copy(), dist_L.copy(),
        K_R.copy(), dist_R.copy(),
        img_size,
        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 1e-8),
        flags=cv2.CALIB_FIX_INTRINSIC)
    baseline_m = float(np.linalg.norm(T))
    print(f"  Stereo RMS  : {rms_stereo:.4f} px")
    print(f"  Baseline    : {baseline_m * 100:.2f} cm")

    # ── Step 3: Stereo rectification ─────────────────────────────────────────
    R1, R2, P1, P2, Q, ROI1, ROI2 = cv2.stereoRectify(
        K_L, dist_L, K_R, dist_R,
        img_size, R, T,
        alpha=args.alpha, newImageSize=img_size)

    # ── Step 4: Build remap maps ──────────────────────────────────────────────
    map1_L, map2_L = cv2.initUndistortRectifyMap(
        K_L, dist_L, R1, P1, img_size, cv2.CV_32FC1)
    map1_R, map2_R = cv2.initUndistortRectifyMap(
        K_R, dist_R, R2, P2, img_size, cv2.CV_32FC1)

    # ── Step 5: Save ──────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    np.savez(args.out,
             map1_L=map1_L, map2_L=map2_L,
             map1_R=map1_R, map2_R=map2_R,
             Q=Q, R=R, T=T,
             K_L=K_L, dist_L=dist_L,
             K_R=K_R, dist_R=dist_R,
             R1=R1, R2=R2, P1=P1, P2=P2,
             ROI1=np.array(ROI1), ROI2=np.array(ROI2),
             baseline_m=np.array(baseline_m),
             rms_stereo=np.array(rms_stereo))

    kb = os.path.getsize(args.out) / 1024
    print(f"\nSaved to: {args.out}  ({kb:.0f} KB)")
    print("\nUsage in your depth app:")
    print("  data       = np.load('stereo_maps.npz')")
    print("  left_rect  = cv2.remap(left_raw,  data['map1_L'], data['map2_L'], cv2.INTER_LINEAR)")
    print("  right_rect = cv2.remap(right_raw, data['map1_R'], data['map2_R'], cv2.INTER_LINEAR)")
    print("  Q          = data['Q']  # disparity-to-depth matrix")


if __name__ == "__main__":
    main()
