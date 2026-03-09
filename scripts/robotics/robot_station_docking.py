"""
robot_station_docking.py
-------------------------
Real-time robot docking application using ArUco markers.
A camera-equipped robot approaches a docking station equipped with
an ArUco marker. The script computes:
  - Distance to station (Z depth)
  - Lateral offset (X)
  - Heading error (yaw from rvec)
  - Proportional controller commands (forward, lateral, rotation)
  - Docking state: SEARCHING → ALIGNING → APPROACH → DOCKED

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
    python scripts/robotics/robot_station_docking.py
    python scripts/robotics/robot_station_docking.py --target 1 --calib assets/calibration/camera_calibration.npz

Arguments:
    --calib       Path to the .npz calibration file produced by NB07.
                  If omitted, the script looks for
                  assets/calibration/camera_calibration.npz automatically.
                  Run NB07 first to generate this file for accurate metric commands.
    --target      ArUco marker ID of the docking station to approach first (default: 1).
                  Must be one of the IDs registered in STATIONS (0, 1, or 2).
    --camera      Camera index (default: 0)
    --width       Requested capture width in pixels (default: 1280)
    --height      Requested capture height in pixels (default: 720)

Station registry (edit STATIONS in the script to match your physical setup):
    ID 0  Charging Station  — 15 cm marker, dock at 30 cm
    ID 1  Conveyor A        — 15 cm marker, dock at 25 cm
    ID 2  Conveyor B        — 15 cm marker, dock at 25 cm

How it works, step by step:
    1. Loads camera intrinsics from the calibration file.
    2. Builds an ArUco detector (DICT_4X4_50).
    3. Each frame: detects all ArUco markers and looks for the one with the target ID.
    4. Runs estimatePoseSingleMarkers to get rvec and tvec for the target marker.
    5. Extracts lateral offset (X), depth (Z), and heading (yaw angle from rvec).
    6. A simple proportional controller produces:
         fwd  — forward/backward speed in m/s
         lat  — lateral speed in m/s
         rot  — rotation speed in deg/s
    7. The docking state transitions:
         SEARCHING → marker not visible
         ALIGNING  → marker visible, heading and lateral error being corrected
         APPROACH  → aligned, moving forward to dock distance
         DOCKED    → within tolerance on all axes
    8. Draws a HUD panel at the top showing target station name, distance, lateral,
       heading, and the controller command on each frame. Values turn green when
       they are within tolerance.

Controls:
    Q / Esc       quit the live window
    0 / 1 / 2     switch the target station (immediately re-targets to that ID)

After running:
    No files are saved. The fwd/lat/rot values printed in the HUD are the commands
    you would send to real motor drivers. In a real robot integration, replace the
    draw_hud output step with calls to your robot's motion API.
"""

import cv2
import numpy as np
import os
import time
import argparse
from dataclasses import dataclass
from typing import Optional, Dict

# ── Station Registry ─────────────────────────────────────────────────────────
@dataclass
class Station:
    id:             int
    name:           str
    marker_length:  float   # meters
    dock_distance:  float   # target approach distance (meters)
    dock_tolerance: float   # acceptable position error (meters)

STATIONS: Dict[int, Station] = {
    0: Station(0, "Charging Station", 0.15, 0.30, 0.02),
    1: Station(1, "Conveyor A",       0.15, 0.25, 0.015),
    2: Station(2, "Conveyor B",       0.15, 0.25, 0.015),
}
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_CALIB_PATHS = [
    "assets/calibration/camera_calibration.npz",
    "../assets/calibration/camera_calibration.npz",
]

# P-controller gains
KP_FWD  = 0.5
KP_LAT  = 1.0
KP_HEAD = 2.0
MAX_FWD = 0.3   # m/s
MAX_LAT = 0.15  # m/s
MAX_ROT = 30.0  # deg/s


def parse_args():
    p = argparse.ArgumentParser(description="Robot station docking with ArUco.")
    p.add_argument("--calib",   default=None)
    p.add_argument("--target",  type=int, default=1, help="Initial target station ID")
    p.add_argument("--camera",  type=int, default=0)
    p.add_argument("--width",   type=int, default=1280)
    p.add_argument("--height",  type=int, default=720)
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


def compute_alignment(tvec, rvec, station):
    tx, ty, tz = tvec.flatten()
    R, _ = cv2.Rodrigues(rvec)
    heading_deg = float(np.degrees(np.arctan2(R[0, 2], R[2, 2])))
    tol = station.dock_tolerance
    is_aligned = abs(tx) < tol and abs(heading_deg) < 5.0
    is_at_dist = abs(tz - station.dock_distance) < tol
    return dict(distance=float(tz), lateral=float(tx), vertical=float(ty),
                heading=heading_deg, is_aligned=is_aligned, is_at_dist=is_at_dist)


def generate_command(err, station):
    if err["is_aligned"] and err["is_at_dist"]:
        return dict(fwd=0, lat=0, rot=0, action="DOCKED")
    dist_err = err["distance"] - station.dock_distance
    fwd = float(np.clip(KP_FWD * dist_err,       -MAX_FWD, MAX_FWD))
    lat = float(np.clip(-KP_LAT * err["lateral"], -MAX_LAT, MAX_LAT))
    rot = float(np.clip(-KP_HEAD * err["heading"],-MAX_ROT, MAX_ROT))
    if err["is_aligned"]:
        action = "APPROACH" if dist_err > 0 else "BACK_UP"
    else:
        action = "ALIGNING"
    return dict(fwd=fwd, lat=lat, rot=rot, action=action)


def draw_hud(frame, station, err, cmd, K, dist, rvec, tvec, target_corner):
    h, w = frame.shape[:2]

    if rvec is not None:
        cv2.drawFrameAxes(frame, K, dist, rvec, tvec, station.marker_length * 0.6)
        if target_corner is not None:
            pts = target_corner.reshape(4, 2).astype(int)
            for i in range(4):
                cv2.line(frame, tuple(pts[i]), tuple(pts[(i+1)%4]), (0,255,255), 3)

    # HUD panel
    cv2.rectangle(frame, (0,0), (w, 165), (0,0,0), -1)
    cv2.rectangle(frame, (0,0), (w, 165), (70,70,70), 1)
    cv2.putText(frame, f"TARGET: {station.name}  (ID={station.id})",
                (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,200,0), 2)

    if err is None:
        cv2.putText(frame, "SEARCHING — marker not visible",
                    (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,100,255), 2)
    else:
        def ok(flag): return (0,220,0) if flag else (0,100,255)
        cv2.putText(frame, f"Dist:    {err['distance']*100:+.1f} cm  (target {station.dock_distance*100:.0f} cm)",
                    (10, 65),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, ok(err["is_at_dist"]), 2)
        cv2.putText(frame, f"Lateral: {err['lateral']*100:+.1f} cm  (target 0 cm)",
                    (10, 93),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, ok(abs(err["lateral"])<station.dock_tolerance), 2)
        cv2.putText(frame, f"Heading: {err['heading']:+.1f} deg  (target 0 deg)",
                    (10, 121), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ok(abs(err["heading"])<5.0), 2)
        if cmd:
            col = (0,220,0) if cmd["action"]=="DOCKED" else (255,200,0)
            cv2.putText(frame,
                        f"CMD: {cmd['action']}  fwd={cmd['fwd']:+.2f}m/s  lat={cmd['lat']:+.2f}m/s  rot={cmd['rot']:+.1f}dps",
                        (10, 152), cv2.FONT_HERSHEY_SIMPLEX, 0.55, col, 2)

    # Camera crosshair
    cv2.line(frame, (w//2-15, h//2), (w//2+15, h//2), (80,80,80), 1)
    cv2.line(frame, (w//2, h//2-15), (w//2, h//2+15), (80,80,80), 1)


def main():
    args = parse_args()
    K, dist = load_calibration(args.calib)
    api_info = make_detector()
    target_id = args.target

    if target_id not in STATIONS:
        print(f"Unknown station ID {target_id}. Valid IDs: {list(STATIONS.keys())}")
        return

    print(f"API        : {api_info[0]}")
    print(f"Target     : station {target_id} ({STATIONS[target_id].name})")
    print("Controls   : Q/Esc=quit  |  0/1/2=switch station")

    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera read failed.")
            break

        station = STATIONS[target_id]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detect(gray, api_info)

        rvec = tvec = target_corner = None
        err = cmd = None

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            for i, mid in enumerate(ids.flatten()):
                if mid == target_id:
                    rv, tv, _ = cv2.aruco.estimatePoseSingleMarkers(
                        [corners[i]], station.marker_length, K, dist)
                    rvec, tvec, target_corner = rv[0], tv[0], corners[i]
                    err = compute_alignment(tvec, rvec, station)
                    cmd = generate_command(err, station)
                    break

        draw_hud(frame, station, err, cmd, K, dist, rvec, tvec, target_corner)

        now = time.time()
        fps = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now
        cv2.putText(frame, f"FPS:{fps:.1f}", (frame.shape[1]-110, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200), 1)

        cv2.imshow("Robot Docking  [Q=quit | 0/1/2=station]", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        if key in (ord("0"), ord("1"), ord("2")):
            new_id = int(chr(key))
            if new_id in STATIONS:
                target_id = new_id
                print(f"Switched target → station {target_id}: {STATIONS[target_id].name}")

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()
