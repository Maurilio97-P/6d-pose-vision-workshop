"""
forklift_pallet_alignment.py
-----------------------------
Real-time forklift fork alignment using 3 ArUco markers on a Euro pallet.
Detects markers IDs 10, 11, 12 on the pallet face, averages their poses
to get a robust pallet center estimate, then computes fork pocket positions
and outputs 4-axis correction commands (forward, lateral, turn, lift).

Pallet marker layout (front face):
    [M0 ID=10]    [M1 ID=11]    [M2 ID=12]
     -450mm          0mm          +450mm    (from pallet center X)
     +100mm        +100mm         +100mm    (height Y)

Fork pockets:
    Left pocket  X = -275mm
    Right pocket X = +275mm
    Height = -60mm from center marker

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
    python scripts/robotics/forklift_pallet_alignment.py
    python scripts/robotics/forklift_pallet_alignment.py --calib assets/calibration/camera_calibration.npz

Arguments:
    --calib       Path to the .npz calibration file produced by NB07.
                  If omitted, the script looks for
                  assets/calibration/camera_calibration.npz automatically.
                  Run NB07 first to generate this file for accurate metric commands.
    --camera      Camera index (default: 0)
    --width       Requested capture width in pixels (default: 1280)
    --height      Requested capture height in pixels (default: 720)

    To adapt to a different pallet or marker placement, edit the constants
    PALLET_MARKER_IDS and MARKER_POS_IN_PALLET near the top of the script.

How it works, step by step:
    1. Loads camera intrinsics from the calibration file.
    2. Builds an ArUco detector (DICT_4X4_50) for markers IDs 10, 11, 12.
    3. Each frame: detects all ArUco markers and filters for the 3 pallet IDs.
    4. For each detected pallet marker, runs estimatePoseSingleMarkers to get
       its individual rvec and tvec.
    5. Transforms each marker's pose to the pallet center frame (M1 = ID 11) and
       averages all detected markers' translations and rotations. The rotation matrix
       is re-orthogonalized via SVD to ensure it stays a valid rotation matrix.
       Using multiple markers makes the estimate more robust to partial occlusion.
    6. Projects the left and right fork pocket positions into camera space and then
       into the image — shown as circles labeled L and R on the live video.
    7. Computes four alignment errors:
         lateral  — forklift is left/right of the pallet center
         height   — forks are too high or too low
         distance — forklift is too far or too close to the pallet
         heading  — forklift is angled relative to the pallet face
    8. A proportional controller produces four motor commands:
         fwd  — drive forward/backward (m/s)
         lat  — strafe left/right (m/s)
         turn — rotate in place (rad/s)
         lift — raise/lower forks (m/s)
    9. When all four errors are within tolerance, the HUD shows
       "FORKS ALIGNED — ADVANCE SLOWLY".

Controls:
    Q / Esc   quit the live window

After running:
    No files are saved. The fwd/lat/turn/lift values shown in the HUD are the
    commands you would send to a real forklift's drive and lift actuators.
    In a real integration, replace the draw_hud output step with calls to your
    vehicle's motion control API.
"""

import cv2
import numpy as np
import os
import time
import argparse
from dataclasses import dataclass

# ── Pallet configuration ─────────────────────────────────────────────────────
PALLET_MARKER_IDS    = [10, 11, 12]
PALLET_MARKER_SIZE_M = 0.10   # 10 cm markers

# 3D positions of marker CENTERS in pallet frame (meters)
# Origin = M1 (center marker)
MARKER_POS_IN_PALLET = {
    10: np.array([-0.450, 0.100, 0.0]),
    11: np.array([ 0.000, 0.100, 0.0]),
    12: np.array([ 0.450, 0.100, 0.0]),
}

# Fork pocket centers in pallet frame (meters)
LEFT_POCKET  = np.array([-0.275, -0.060, 0.0])
RIGHT_POCKET = np.array([ 0.275, -0.060, 0.0])

# Approach parameters
DOCK_DIST_M      = 0.50   # stop 50cm from pallet face
TOL_LAT_M        = 0.020  # 2 cm lateral
TOL_HEIGHT_M     = 0.015  # 1.5 cm height
TOL_DIST_M       = 0.050  # 5 cm distance
TOL_HEADING_DEG  = 2.0

# P-controller gains
KP_FWD  = 0.30;  MAX_FWD  = 0.15   # m/s  (slow near pallet)
KP_LAT  = 1.00;  MAX_LAT  = 0.20   # m/s
KP_TURN = 0.05;  MAX_TURN = 0.30   # rad/s
KP_LIFT = 0.80;  MAX_LIFT = 0.10   # m/s
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_CALIB_PATHS = [
    "assets/calibration/camera_calibration.npz",
    "../assets/calibration/camera_calibration.npz",
]


def parse_args():
    p = argparse.ArgumentParser(description="Forklift pallet alignment with ArUco.")
    p.add_argument("--calib",  default=None)
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
    print("WARNING: Using default K.")
    return np.array([[600,0,320],[0,600,240],[0,0,1]], dtype=np.float64), np.zeros((1,5))


def make_detector():
    try:
        d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        p = cv2.aruco.DetectorParameters()
        p.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
        detector = cv2.aruco.ArucoDetector(d, p)
        return ("new", detector, d, p)
    except AttributeError:
        d = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        p = cv2.aruco.DetectorParameters_create()
        return ("old", None, d, p)


def detect(gray, api_info):
    api_ver, detector, d, p = api_info
    if api_ver == "new":
        return detector.detectMarkers(gray)
    return cv2.aruco.detectMarkers(gray, d, parameters=p)


def average_pallet_pose(detected_markers):
    """
    Estimate pallet center pose (M1 frame) by averaging all detected
    pallet markers, transforming each to the center frame first.
    detected_markers: {marker_id: (rvec, tvec)}
    Returns (R_avg, t_avg) or (None, None)
    """
    translations, rotations = [], []
    for mid, (rvec, tvec) in detected_markers.items():
        if mid not in MARKER_POS_IN_PALLET:
            continue
        R, _ = cv2.Rodrigues(rvec)
        t = tvec.flatten()
        # Offset from this marker to center marker (M1)
        offset = MARKER_POS_IN_PALLET[11] - MARKER_POS_IN_PALLET[mid]
        t_center = t + R @ offset
        translations.append(t_center)
        rotations.append(R)

    if not translations:
        return None, None

    t_avg = np.mean(translations, axis=0)
    R_avg = np.mean(rotations, axis=0)
    # Re-orthogonalize via SVD
    U, _, Vt = np.linalg.svd(R_avg)
    R_avg = U @ Vt
    if np.linalg.det(R_avg) < 0:
        U[:, -1] *= -1
        R_avg = U @ Vt

    return R_avg, t_avg


def compute_fork_alignment(R_pallet, t_pallet):
    def xform(pt):
        return R_pallet @ pt + t_pallet

    L = xform(LEFT_POCKET)
    R = xform(RIGHT_POCKET)
    mid = (L + R) / 2

    lateral_m  = float(mid[0])
    height_m   = float(mid[1])
    distance_m = float(t_pallet[2])
    heading_deg = float(np.degrees(np.arctan2(R_pallet[0, 2], R_pallet[2, 2])))

    is_aligned = (
        abs(lateral_m)   < TOL_LAT_M    and
        abs(height_m)    < TOL_HEIGHT_M and
        abs(distance_m - DOCK_DIST_M) < TOL_DIST_M and
        abs(heading_deg) < TOL_HEADING_DEG
    )
    return dict(lateral=lateral_m, height=height_m,
                distance=distance_m, heading=heading_deg,
                is_aligned=is_aligned, left_cam=L, right_cam=R)


def generate_forklift_command(fa):
    if fa["is_aligned"]:
        return dict(fwd=0, lat=0, turn=0, lift=0, msg="FORKS ALIGNED — ADVANCE SLOWLY")

    dist_err = fa["distance"] - DOCK_DIST_M
    fwd  = float(np.clip(KP_FWD  * dist_err,           -MAX_FWD,  MAX_FWD))
    lat  = float(np.clip(-KP_LAT  * fa["lateral"],      -MAX_LAT,  MAX_LAT))
    turn = float(np.clip(-KP_TURN * fa["heading"],      -MAX_TURN, MAX_TURN))
    lift = float(np.clip(-KP_LIFT * fa["height"],       -MAX_LIFT, MAX_LIFT))
    msg  = (f"lat={fa['lateral']*100:+.1f}cm  ht={fa['height']*100:+.1f}cm  "
            f"dist={fa['distance']*100:.0f}cm  hdg={fa['heading']:+.1f}deg")
    return dict(fwd=fwd, lat=lat, turn=turn, lift=lift, msg=msg)


def draw_hud(frame, fa, cmd, K, dist_coeffs, R_pallet, t_pallet,
             all_corners, all_ids, detected_marker_corners):
    h, w = frame.shape[:2]

    # Draw all detected markers
    if all_ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, all_corners, all_ids)

    # Highlight pallet markers + pocket targets
    if R_pallet is not None:
        rvec, _ = cv2.Rodrigues(R_pallet)
        cv2.drawFrameAxes(frame, K, dist_coeffs, rvec,
                          t_pallet.astype(np.float32), 0.08)

        if fa is not None:
            # Project pocket centers to image
            for pt_3d, label in [(fa["left_cam"], "L"), (fa["right_cam"], "R")]:
                pt_2d, _ = cv2.projectPoints(
                    pt_3d.reshape(1,1,3).astype(np.float32),
                    rvec, t_pallet.astype(np.float32), K, dist_coeffs)
                pt_2d = tuple(pt_2d.reshape(2).astype(int))
                cv2.circle(frame, pt_2d, 14, (0, 255, 100), 2)
                cv2.putText(frame, label, (pt_2d[0]-6, pt_2d[1]+5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,100), 2)

    # HUD panel
    cv2.rectangle(frame, (0,0), (w, 175), (0,0,0), -1)
    cv2.rectangle(frame, (0,0), (w, 175), (70,70,70), 1)
    cv2.putText(frame, "FORKLIFT PALLET ALIGNMENT",
                (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,200,0), 2)

    if fa is None:
        cv2.putText(frame, "SEARCHING — no pallet markers visible",
                    (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,100,255), 2)
    else:
        def ok(flag): return (0,220,0) if flag else (0,100,255)
        cv2.putText(frame, f"Distance: {fa['distance']*100:.1f}cm  (target {DOCK_DIST_M*100:.0f}cm)",
                    (10, 65),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, ok(abs(fa['distance']-DOCK_DIST_M)<TOL_DIST_M), 2)
        cv2.putText(frame, f"Lateral:  {fa['lateral']*100:+.1f}cm",
                    (10, 93),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, ok(abs(fa['lateral'])<TOL_LAT_M), 2)
        cv2.putText(frame, f"Height:   {fa['height']*100:+.1f}cm",
                    (10, 121), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ok(abs(fa['height'])<TOL_HEIGHT_M), 2)
        cv2.putText(frame, f"Heading:  {fa['heading']:+.1f}deg",
                    (10, 149), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ok(abs(fa['heading'])<TOL_HEADING_DEG), 2)
        if cmd:
            col = (0,220,0) if fa["is_aligned"] else (255,200,0)
            cv2.putText(frame, cmd["msg"],
                        (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 1)


def main():
    args = parse_args()
    K, dist_coeffs = load_calibration(args.calib)
    api_info = make_detector()

    print(f"API        : {api_info[0]}")
    print(f"Pallet IDs : {PALLET_MARKER_IDS}  (marker size {PALLET_MARKER_SIZE_M*100:.0f}cm)")
    print(f"Camera     : {args.camera}  ({args.width}×{args.height})")
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

        R_pallet = t_pallet = None
        fa = cmd = None
        detected_marker_corners = {}

        if ids is not None:
            flat_ids = ids.flatten()
            # Collect pose for each pallet marker visible
            detected = {}
            for i, mid in enumerate(flat_ids):
                if mid in PALLET_MARKER_IDS:
                    rv, tv, _ = cv2.aruco.estimatePoseSingleMarkers(
                        [corners[i]], PALLET_MARKER_SIZE_M, K, dist_coeffs)
                    detected[int(mid)] = (rv[0].flatten(), tv[0].flatten())
                    detected_marker_corners[int(mid)] = corners[i]

            if detected:
                R_pallet, t_pallet = average_pallet_pose(detected)
                if R_pallet is not None:
                    fa  = compute_fork_alignment(R_pallet, t_pallet)
                    cmd = generate_forklift_command(fa)

        draw_hud(frame, fa, cmd, K, dist_coeffs, R_pallet, t_pallet,
                 corners, ids, detected_marker_corners)

        now = time.time()
        fps = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now
        n_pallet = len(detected_marker_corners) if detected_marker_corners else 0
        cv2.putText(frame, f"FPS:{fps:.1f}  Pallet markers:{n_pallet}/3",
                    (frame.shape[1]-300, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 1)

        cv2.imshow("Forklift Pallet Alignment  [Q=quit]", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()
