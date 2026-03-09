"""
detect_aruco_live.py
---------------------
Real-time ArUco marker detection from a webcam feed.
Draws bounding boxes, corner points, and marker IDs on every frame.

Usage:
    python scripts/detect_aruco_live.py
    python scripts/detect_aruco_live.py --dict DICT_5X5_100 --camera 1

Controls:
    Q / Esc   quit

Arguments:
    --dict      ArUco dictionary (default: DICT_4X4_50)
    --camera    Camera index (default: 0)
    --width     Capture width (default: 1280)
    --height    Capture height (default: 720)
    --rejected  Show rejected candidates in red (default: off)

Requirements: opencv-contrib-python
"""

import cv2
import numpy as np
import time
import argparse

DICT_MAP = {
    "DICT_4X4_50":   cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100":  cv2.aruco.DICT_4X4_100,
    "DICT_5X5_100":  cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250":  cv2.aruco.DICT_5X5_250,
    "DICT_6X6_250":  cv2.aruco.DICT_6X6_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
}


def parse_args():
    p = argparse.ArgumentParser(description="Real-time ArUco marker detection.")
    p.add_argument("--dict",     default="DICT_4X4_50", choices=list(DICT_MAP.keys()))
    p.add_argument("--camera",   type=int, default=0)
    p.add_argument("--width",    type=int, default=1280)
    p.add_argument("--height",   type=int, default=720)
    p.add_argument("--rejected", action="store_true", help="Show rejected candidates")
    return p.parse_args()


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


def draw_detections(frame, corners, ids, rejected, show_rejected):
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        for corner_set, mid in zip(corners, ids.flatten()):
            pts = corner_set.reshape(4, 2).astype(int)
            cx = int(pts[:, 0].mean())
            cy = int(pts[:, 1].mean())
            cv2.putText(frame, f"ID:{mid}", (cx - 20, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    if show_rejected and rejected:
        for r in rejected:
            pts = r.reshape(4, 2).astype(int)
            for i in range(4):
                cv2.line(frame, tuple(pts[i]), tuple(pts[(i + 1) % 4]),
                         (0, 0, 200), 1)


def main():
    args = parse_args()
    dict_id = DICT_MAP[args.dict]
    api_info = make_detector(dict_id)
    print(f"Dictionary : {args.dict}  API: {api_info[0]}")
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
        corners, ids, rejected = detect(gray, api_info)

        draw_detections(frame, corners, ids, rejected, args.rejected)

        # FPS + count overlay
        now = time.time()
        fps = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now
        n = len(ids.flatten()) if ids is not None else 0
        cv2.putText(frame, f"FPS:{fps:.1f}  Markers:{n}",
                    (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

        cv2.imshow("ArUco Detection  [Q=quit]", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()
