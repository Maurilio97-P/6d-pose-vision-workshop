"""
aruco_pose_estimation_live.py
------------------------------
Real-time ArUco marker pose estimation from a webcam.
Detects markers, estimates their 6D pose (rvec, tvec), and draws
coordinate frame axes (Red=X, Green=Y, Blue=Z) on each detected marker.
Overlays distance and lateral offset for each marker.

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
    python scripts/aruco/aruco_pose_estimation_live.py
    python scripts/aruco/aruco_pose_estimation_live.py --calib assets/calibration/camera_calibration.npz
    python scripts/aruco/aruco_pose_estimation_live.py --marker-length 0.15 --dict DICT_5X5_100

Arguments:
    --calib          Path to the .npz calibration file produced by NB07.
                     If omitted, the script looks for
                     assets/calibration/camera_calibration.npz automatically.
                     Without a real calibration file the pose numbers will not be
                     physically accurate (a built-in fallback K is used instead).
    --marker-length  Physical side length of the printed marker in METERS.
                     Measure with a ruler after printing. (default: 0.10 = 10 cm)
    --dict           ArUco dictionary (default: DICT_4X4_50).
                     Must match the dictionary used when generating the markers.
    --camera         Camera index (default: 0)
    --width          Requested capture width in pixels (default: 1280)
    --height         Requested capture height in pixels (default: 720)

How it works, step by step:
    1. Loads camera intrinsics (K, dist) from the calibration file, or falls back
       to a rough default if the file is not found.
    2. Opens the webcam, sets resolution, and builds the ArUco detector.
    3. Each frame: detects markers, then calls estimatePoseSingleMarkers to get a
       rotation vector (rvec) and translation vector (tvec) for each marker.
    4. Draws 3D coordinate axes on each marker: Red = X, Green = Y, Blue = Z.
    5. Overlays text showing the marker ID, distance (depth in cm), and lateral /
       vertical offsets (X, Y) in cm.
    6. Shows FPS and total marker count in the top-left corner.

Controls:
    Q / Esc   quit the live window

After running:
    No files are saved. Use the distance and offset readouts on screen to verify
    that your calibration is accurate and that marker-length is set correctly.
    Accurate calibration data from NB07 is required for reliable metric distances.
"""

import cv2
import numpy as np
import os
import time
import argparse

DICT_MAP = {
    "DICT_4X4_50":   cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100":  cv2.aruco.DICT_4X4_100,
    "DICT_5X5_100":  cv2.aruco.DICT_5X5_100,
    "DICT_6X6_250":  cv2.aruco.DICT_6X6_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
}

DEFAULT_CALIB_PATHS = [
    "assets/calibration/camera_calibration.npz",
    "../assets/calibration/camera_calibration.npz",
]


def parse_args():
    p = argparse.ArgumentParser(description="Real-time ArUco pose estimation.")
    p.add_argument("--calib",         default=None,
                   help="Path to .npz calibration file (from NB07)")
    p.add_argument("--marker-length", type=float, default=0.10,
                   help="Marker side length in meters (default: 0.10 = 10cm)")
    p.add_argument("--dict",          default="DICT_4X4_50",
                   choices=list(DICT_MAP.keys()))
    p.add_argument("--camera",        type=int, default=0)
    p.add_argument("--width",         type=int, default=1280)
    p.add_argument("--height",        type=int, default=720)
    return p.parse_args()


def load_calibration(calib_path):
    """Load K and dist from .npz. Falls back to reasonable defaults."""
    paths_to_try = ([calib_path] if calib_path else []) + DEFAULT_CALIB_PATHS
    for path in paths_to_try:
        if path and os.path.exists(path):
            data = np.load(path)
            # Support both key naming conventions used across notebooks
            K    = data.get("K",             data.get("camera_matrix"))
            dist = data.get("dist",          data.get("dist_coeffs"))
            print(f"Calibration loaded: {path}")
            return K, dist

    print("WARNING: No calibration file found. Using default K (640×480 webcam).")
    print("  Run NB07 and pass --calib path/to/camera_calibration.npz for accuracy.")
    K    = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]], dtype=np.float64)
    dist = np.zeros((1, 5), dtype=np.float64)
    return K, dist


def make_detector(dict_id):
    try:
        d = cv2.aruco.getPredefinedDictionary(dict_id)
        p = cv2.aruco.DetectorParameters()
        p.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
        detector = cv2.aruco.ArucoDetector(d, p)
        return ("new", detector, d, p)
    except AttributeError:
        d = cv2.aruco.Dictionary_get(dict_id)
        p = cv2.aruco.DetectorParameters_create()
        return ("old", None, d, p)


def detect(gray, api_info):
    api_ver, detector, d, p = api_info
    if api_ver == "new":
        return detector.detectMarkers(gray)
    return cv2.aruco.detectMarkers(gray, d, parameters=p)


def main():
    args = parse_args()
    K, dist = load_calibration(args.calib)
    dict_id = DICT_MAP[args.dict]
    api_info = make_detector(dict_id)
    axis_len = args.marker_length * 0.6  # axis lines = 60% of marker side

    print(f"Dictionary    : {args.dict}  API: {api_info[0]}")
    print(f"Marker length : {args.marker_length * 100:.1f} cm")
    print(f"Camera        : {args.camera}  ({args.width}×{args.height})")
    print("Press Q or Esc to quit.")

    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera read failed.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detect(gray, api_info)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, args.marker_length, K, dist)

            for i, (rvec, tvec, mid) in enumerate(zip(rvecs, tvecs, ids.flatten())):
                # Draw 3D axes (Red=X, Green=Y, Blue=Z toward camera)
                cv2.drawFrameAxes(frame, K, dist, rvec, tvec, axis_len)

                tx, ty, tz = tvec.flatten()
                dist_m = np.linalg.norm(tvec)
                pts = corners[i].reshape(4, 2).astype(int)
                label_y = max(pts[:, 1].min() - 10, 15)
                cv2.putText(frame,
                            f"ID={mid}  d={dist_m * 100:.1f}cm",
                            (pts[:, 0].min(), label_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame,
                            f"X={tx * 100:+.1f}  Y={ty * 100:+.1f}  Z={tz * 100:.1f}cm",
                            (pts[:, 0].min(), label_y + 22),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 1)

        # FPS overlay
        now = time.time()
        fps = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now
        n = len(ids.flatten()) if ids is not None else 0
        cv2.putText(frame, f"FPS:{fps:.1f}  Markers:{n}",
                    (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

        cv2.imshow("ArUco Pose Estimation  [Q=quit]", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()
