"""
undistort_live_video.py
------------------------
Real-time lens distortion removal from a webcam feed.
Precomputes undistortion maps ONCE at startup, then applies them per frame
with cv2.remap() — 3-5x faster than calling cv2.undistort() every frame.

Displays raw and undistorted frames side-by-side. Notice how straight
edges in the real world (walls, doors) become straight in the right pane.

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
    python scripts/pose/undistort_live_video.py
    python scripts/pose/undistort_live_video.py --calib assets/calibration/camera_calibration.npz
    python scripts/pose/undistort_live_video.py --alpha 1   # keep full FOV (black borders)

Arguments:
    --calib   Path to the .npz calibration file produced by NB07.
              If omitted, the script looks for
              assets/calibration/camera_calibration.npz automatically.
              Without a real calibration file a synthetic distortion is used —
              run NB07 first to generate assets/calibration/camera_calibration.npz.
    --alpha   Controls how the undistorted image is cropped.
              0 = crop to only the valid (non-black) pixel region (default).
              1 = keep the full field of view, which leaves black borders.
    --camera  Camera index (default: 0)
    --width   Requested capture width in pixels (default: 1280)
    --height  Requested capture height in pixels (default: 720)

How it works, step by step:
    1. Loads camera intrinsics (K, dist) from the calibration file.
    2. Calls getOptimalNewCameraMatrix to compute a new K_new for the undistorted
       image, then initUndistortRectifyMap to build per-pixel remap tables.
       This heavy computation runs once at startup.
    3. Each frame: applies cv2.remap using the precomputed tables — this is very
       fast and runs at full camera frame rate.
    4. Labels each pane ("RAW" / "UNDISTORTED") and overlays the current FPS.
    5. In side-by-side mode the two half-size images are shown next to each other
       so you can directly compare them. Look at straight edges (door frames, walls)
       — they should curve in the raw view and be straight in the right pane.

Controls:
    Q / Esc   quit the live window
    S         toggle between side-by-side view and undistorted-only full-screen view

After running:
    No files are saved. The corrected K_new matrix is printed to the terminal at
    startup. If you use undistorted frames in a downstream pipeline (ArUco detection,
    solvePnP), use K_new as your camera matrix and pass dist=zeros — the distortion
    has already been removed by remap.
"""

import cv2
import numpy as np
import os
import time
import argparse

DEFAULT_CALIB_PATHS = [
    "assets/calibration/camera_calibration.npz",
    "../assets/calibration/camera_calibration.npz",
]


def parse_args():
    p = argparse.ArgumentParser(description="Real-time lens undistortion.")
    p.add_argument("--calib",  default=None, help="Path to .npz calibration file")
    p.add_argument("--alpha",  type=float, default=0.0,
                   help="0=crop to valid pixels (no black borders), 1=keep full FOV")
    p.add_argument("--camera", type=int, default=0)
    p.add_argument("--width",  type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    return p.parse_args()


def load_calibration(calib_path):
    paths_to_try = ([calib_path] if calib_path else []) + DEFAULT_CALIB_PATHS
    for path in paths_to_try:
        if path and os.path.exists(path):
            data = np.load(path)
            K    = data.get("K",    data.get("camera_matrix"))
            dist = data.get("dist", data.get("dist_coeffs"))
            print(f"Calibration loaded: {path}")
            return K, dist

    print("WARNING: No calibration file found. Using default K (pass --calib for real results).")
    K    = np.array([[800, 0, 640], [0, 800, 360], [0, 0, 1]], dtype=np.float64)
    dist = np.array([-0.3, 0.1, 0.001, 0.002, -0.05])
    return K, dist


def main():
    args = parse_args()
    K, dist = load_calibration(args.calib)

    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    # Read actual capture size (may differ from requested)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ── Precompute undistortion maps ONCE ────────────────────────────────────
    K_new, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), args.alpha)
    mapx, mapy = cv2.initUndistortRectifyMap(
        K, dist, None, K_new, (w, h), cv2.CV_32FC1)
    # ─────────────────────────────────────────────────────────────────────────

    print(f"Camera     : {args.camera}  actual size {w}×{h}")
    print(f"alpha      : {args.alpha}  ({'no black borders' if args.alpha == 0 else 'full FOV'})")
    print(f"K_new      : fx={K_new[0,0]:.1f}  fy={K_new[1,1]:.1f}  "
          f"cx={K_new[0,2]:.1f}  cy={K_new[1,2]:.1f}")
    print(f"Valid ROI  : {roi}")
    print("TIP: Use K_new and dist=zeros for solvePnP/ArUco on undistorted frames.")
    print("Controls: Q/Esc = quit  |  S = toggle split view")

    side_by_side = True
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera read failed.")
            break

        # ── Apply maps (very fast — just a lookup) ────────────────────────
        undistorted = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        # ─────────────────────────────────────────────────────────────────

        now = time.time()
        fps = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now

        # Annotate
        for img, label in [(frame, "RAW"), (undistorted, "UNDISTORTED")]:
            cv2.putText(img, label, (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 220, 255), 2)
        cv2.putText(undistorted, f"FPS:{fps:.1f}", (w - 130, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

        if side_by_side:
            raw_small   = cv2.resize(frame,       (w // 2, h // 2))
            undist_small = cv2.resize(undistorted, (w // 2, h // 2))
            display = np.hstack([raw_small, undist_small])
        else:
            display = undistorted

        cv2.imshow("Undistortion  [Q=quit | S=split]", display)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        if key == ord("s"):
            side_by_side = not side_by_side

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()
