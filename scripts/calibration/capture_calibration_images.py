"""
capture_calibration_images.py
------------------------------
Live webcam script to capture chessboard calibration images.

Usage (run from the repo root):
    python scripts/calibration/capture_calibration_images.py

Optional arguments:
    --save-dir  PATH    folder to save images (default: calibration_images/)
    --cols      INT     inner corner columns  (default: 9)
    --rows      INT     inner corner rows     (default: 6)
    --camera    INT     webcam index          (default: 0)

Example — custom board and output folder:
    python scripts/calibration/capture_calibration_images.py --cols 9 --rows 6 --save-dir my_calib_imgs

How it works, step by step:
    1. Opens your webcam and shows a live video window titled:
           Calibration Capture — S=save  Q=quit

    2. Every frame it runs findChessboardCorners on the live feed:
       - Chessboard detected → draws the colored corner grid overlay + green text:
             DETECTED  [S=save | count=0]
       - Not detected → red text:
             Chessboard not found

    3. You control when to save:
       - Press S → saves the raw frame (no overlay) as calib_0000.jpg.
                   Counter increments. Only works when chessboard is detected —
                   pressing S with no board visible does nothing.
       - Press Q or Esc → closes the window and exits.

    4. On exit, prints a summary:
           Done. Captured 15 images to 'calibration_images/'
       If fewer than 6 images were saved, a warning is printed.

Practical workflow:
    - Print chessboard_9x6.png and glue it to something flat and rigid
    - Hold the board in front of the camera
    - Wait for the green DETECTED overlay
    - Tilt the board to a new angle → press S
    - Move closer/further, tilt up/down/left/right — aim for 15+ images
    - Cover the corners of the frame, not just the center
    - Take your time — blurry frames will hurt calibration quality

After capture:
    Run notebook 07 (or cv2.calibrateCamera) pointing at the saved folder.

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
