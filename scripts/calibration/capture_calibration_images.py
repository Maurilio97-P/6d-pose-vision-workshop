"""
capture_calibration_images.py
------------------------------
Live webcam script to capture chessboard calibration images.

Usage:
    python scripts/capture_calibration_images.py

Controls:
    S   — save current frame (only when chessboard is detected)
    Q   — quit

After capture, run notebook 07 or your own calibrateCamera script
on the saved images.

Requirements: opencv-contrib-python
"""

import cv2
import os
import argparse

# ── Config ──────────────────────────────────────────────────────────────────
DEFAULT_SAVE_DIR    = "calibration_images"
DEFAULT_BOARD_COLS  = 9   # inner corners (columns)
DEFAULT_BOARD_ROWS  = 6   # inner corners (rows)
DEFAULT_CAMERA_IDX  = 0
# ────────────────────────────────────────────────────────────────────────────


def parse_args():
    p = argparse.ArgumentParser(description="Capture chessboard calibration images.")
    p.add_argument("--save-dir",  default=DEFAULT_SAVE_DIR,   help="Folder to save images")
    p.add_argument("--cols",      type=int, default=DEFAULT_BOARD_COLS, help="Inner corner columns")
    p.add_argument("--rows",      type=int, default=DEFAULT_BOARD_ROWS, help="Inner corner rows")
    p.add_argument("--camera",    type=int, default=DEFAULT_CAMERA_IDX, help="Camera index")
    return p.parse_args()


def main():
    args = parse_args()
    board_size = (args.cols, args.rows)

    os.makedirs(args.save_dir, exist_ok=True)

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"ERROR: Could not open camera {args.camera}")
        return

    count = 0
    print(f"Board size : {args.cols}x{args.rows} inner corners")
    print(f"Save dir   : {args.save_dir}/")
    print(f"Controls   : S = save frame | Q = quit")
    print(f"Tip        : vary angles, distances, and positions — aim for 15+ images")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, board_size, None)

        display = frame.copy()
        if found:
            cv2.drawChessboardCorners(display, board_size, corners, found)
            msg = f"DETECTED  [S=save | count={count}]"
            cv2.putText(display, msg, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 0), 2)
        else:
            cv2.putText(display, "Chessboard not found", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 220), 2)

        cv2.imshow("Calibration Capture — S=save  Q=quit", display)
        key = cv2.waitKey(30) & 0xFF

        if key == ord('s') and found:
            path = os.path.join(args.save_dir, f"calib_{count:04d}.jpg")
            cv2.imwrite(path, frame)
            count += 1
            print(f"  Saved {path}")
        elif key in (ord('q'), 27):   # Q or Esc
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nDone. Captured {count} images to '{args.save_dir}/'")
    if count < 6:
        print("WARNING: Fewer than 6 images — calibration may be unreliable.")


if __name__ == "__main__":
    main()
