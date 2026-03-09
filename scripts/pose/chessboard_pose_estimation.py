"""
chessboard_pose_estimation.py
------------------------------
Real-time chessboard pose estimation from a webcam.
Detects a printed chessboard, runs solvePnP to get the 6D pose (rvec, tvec),
then draws 3D coordinate axes and an optional cube sitting on the board.

Usage:
    python scripts/chessboard_pose_estimation.py
    python scripts/chessboard_pose_estimation.py --cols 9 --rows 6 --square 0.025
    python scripts/chessboard_pose_estimation.py --calib assets/calibration/camera_calibration.npz

Controls:
    Q / Esc   quit
    C         toggle cube overlay on/off

Arguments:
    --calib       Path to .npz calibration file from NB07
    --cols        Inner corner columns (default: 9)
    --rows        Inner corner rows    (default: 6)
    --square      Square side length in METERS (default: 0.025 = 2.5 cm)
    --camera      Camera index (default: 0)
    --width       Capture width (default: 1280)
    --height      Capture height (default: 720)

Tip: Print the chessboard from NB07 (assets/calibration/chessboard_9x6.png).
     Measure your actual printed square size with a ruler.

Requirements: opencv-contrib-python, numpy
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
    p = argparse.ArgumentParser(description="Real-time chessboard pose estimation.")
    p.add_argument("--calib",   default=None)
    p.add_argument("--cols",    type=int,   default=9,     help="Inner corner columns")
    p.add_argument("--rows",    type=int,   default=6,     help="Inner corner rows")
    p.add_argument("--square",  type=float, default=0.025, help="Square side in meters")
    p.add_argument("--camera",  type=int,   default=0)
    p.add_argument("--width",   type=int,   default=1280)
    p.add_argument("--height",  type=int,   default=720)
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
    print("WARNING: No calibration file. Using default K.")
    K    = np.array([[720, 0, 320], [0, 720, 240], [0, 0, 1]], dtype=np.float64)
    dist = np.zeros((1, 5))
    return K, dist


def build_objp(cols, rows, square_size):
    objp = np.zeros((cols * rows, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)
    objp *= square_size
    return objp


def draw_axes(img, rvec, tvec, K, dist, length):
    pts, _ = cv2.projectPoints(
        np.float32([[0,0,0],[length,0,0],[0,length,0],[0,0,-length]]),
        rvec, tvec, K, dist)
    pts = pts.reshape(-1, 2).astype(int)
    o = tuple(pts[0])
    cv2.arrowedLine(img, o, tuple(pts[1]), (0,0,255), 3, tipLength=0.2)   # X red
    cv2.arrowedLine(img, o, tuple(pts[2]), (0,255,0), 3, tipLength=0.2)   # Y green
    cv2.arrowedLine(img, o, tuple(pts[3]), (255,0,0), 3, tipLength=0.2)   # Z blue
    for pt, lbl, col in zip(pts[1:], "XYZ", [(0,0,255),(0,255,0),(255,0,0)]):
        cv2.putText(img, lbl, tuple(pt), cv2.FONT_HERSHEY_SIMPLEX, 0.7, col, 2)


def draw_cube(img, rvec, tvec, K, dist, size, ox=0, oy=0):
    s = size
    cube_pts = np.float32([
        [ox,   oy,   0],[ox+s,oy,   0],[ox+s,oy+s,0],[ox,   oy+s,0],
        [ox,   oy,  -s],[ox+s,oy,  -s],[ox+s,oy+s,-s],[ox,  oy+s,-s]])
    pts, _ = cv2.projectPoints(cube_pts, rvec, tvec, K, dist)
    pts = pts.reshape(-1, 2).astype(int)
    for i in range(4):
        cv2.line(img, tuple(pts[i]), tuple(pts[(i+1)%4]),   (0,200,0), 2)
        cv2.line(img, tuple(pts[i+4]), tuple(pts[(i+1)%4+4]), (200,100,0), 2)
        cv2.line(img, tuple(pts[i]),  tuple(pts[i+4]),      (200,200,200), 1)


def main():
    args = parse_args()
    K, dist = load_calibration(args.calib)

    board_size = (args.cols, args.rows)
    objp = build_objp(args.cols, args.rows, args.square)
    axis_len  = args.square * 3
    cube_size = args.square * 3
    criteria  = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    print(f"Board      : {args.cols}×{args.rows} inner corners")
    print(f"Square     : {args.square*100:.1f} cm  "
          f"→ board {args.cols*args.square*100:.1f}cm × {args.rows*args.square*100:.1f}cm")
    print(f"Camera     : {args.camera}  ({args.width}×{args.height})")
    print("Controls   : Q/Esc=quit  |  C=toggle cube")

    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    show_cube = True
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera read failed.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, board_size, None)

        now  = time.time()
        fps  = 1.0 / max(now - prev_time, 1e-6)
        prev_time = now

        if found:
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            cv2.drawChessboardCorners(frame, board_size, corners, found)

            ret_pnp, rvec, tvec = cv2.solvePnP(
                objp, corners, K, dist, flags=cv2.SOLVEPNP_ITERATIVE)

            if ret_pnp:
                draw_axes(frame, rvec, tvec, K, dist, axis_len)
                if show_cube:
                    draw_cube(frame, rvec, tvec, K, dist, cube_size,
                              ox=args.square * 2, oy=args.square)

                tx, ty, tz = tvec.flatten()
                cv2.putText(frame,
                            f"Z={tz*100:.1f}cm  X={tx*100:+.1f}  Y={ty*100:+.1f}",
                            (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
        else:
            cv2.putText(frame, "Hold chessboard in view...",
                        (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,100,255), 2)

        cv2.putText(frame, f"FPS:{fps:.1f}  Cube:{'ON' if show_cube else 'OFF'}",
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 1)

        cv2.imshow("Chessboard Pose  [Q=quit | C=cube]", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        if key == ord("c"):
            show_cube = not show_cube

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()
