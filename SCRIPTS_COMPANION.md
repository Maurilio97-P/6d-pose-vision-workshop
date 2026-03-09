# Scripts Companion Guide

**How to use this**: When you finish a notebook and want to run the same workflow with a real camera outside Jupyter, find the script for that notebook here. Each entry covers what the script does, how to set up your environment, and the exact commands to run.

Every script also has this full detail in its own docstring — run `python scripts/<subfolder>/<name>.py --help` for a quick reminder at any time.

---

## Before running any script — environment setup

Scripts run outside Jupyter, so you need a terminal with the virtual environment active. Do this once per machine, then just activate each time you open a new terminal.

```bash
# 1. Create the venv (only once, from the repo root):
python -m venv venv

# 2. Activate it (every time you open a new terminal):
#    Windows:
venv\Scripts\activate
#    macOS / Linux:
source venv/bin/activate

# 3. Install dependencies (only once, after activating):
pip install -r requirements.txt
```

You should see `(venv)` at the start of your terminal prompt. If you don't see it, the venv is not active — the script will fail with `ModuleNotFoundError: No module named 'cv2'`.

---

## Part 3 — Camera Model

### `scripts/calibration/capture_calibration_images.py` · NB07

Opens your webcam and lets you save calibration images by pressing a key — only saves when the chessboard is detected.

**Run:**
```bash
python scripts/calibration/capture_calibration_images.py
```

**Options:**
```
--save-dir  PATH    folder to save images (default: calibration_images/)
--cols      INT     inner corner columns  (default: 9)
--rows      INT     inner corner rows     (default: 6)
--camera    INT     webcam index          (default: 0)
```

**What you see:**
- Live webcam window. When chessboard is detected: green overlay + `DETECTED [S=save | count=0]`
- When not detected: red text `Chessboard not found`

**Controls:** `S` = save frame (only when detected) · `Q` / `Esc` = quit

**Workflow:**
1. Print `assets/calibration/chessboard_9x6.png` on rigid flat board
2. Hold it in front of the camera — wait for green DETECTED overlay
3. Tilt to a new angle → press **S**
4. Repeat at different angles, distances, positions — aim for **15+ images**
5. Frames saved to `calibration_images/` → open NB07 and run `calibrateCamera`

---

### `scripts/pose/undistort_live_video.py` · NB08

Loads your calibration file and applies real-time lens undistortion to a live webcam feed using precomputed remap maps (fast — runs at full frame rate).

**Requires:** calibration file from NB07 (`assets/calibration/camera_calibration.npz`)

**Run:**
```bash
python scripts/pose/undistort_live_video.py
python scripts/pose/undistort_live_video.py --calib assets/calibration/camera_calibration.npz
```

**Options:**
```
--calib   PATH    calibration .npz file (default: assets/calibration/camera_calibration.npz)
--alpha   FLOAT   0 = crop to valid pixels only, 1 = keep full FOV with black borders (default: 0)
--camera  INT     webcam index (default: 0)
```

**Controls:** `S` = toggle split view (raw left / undistorted right) · `Q` / `Esc` = quit

---

## Part 4 — Classical Pose

### `scripts/pose/chessboard_pose_estimation.py` · NB10

Detects chessboard corners in the live feed, runs `solvePnP`, and overlays 3D coordinate axes and an optional cube on the board in real time.

**Requires:** calibration file from NB07 (`assets/calibration/camera_calibration.npz`)

**Run:**
```bash
python scripts/pose/chessboard_pose_estimation.py
```

**Options:**
```
--calib   PATH    calibration .npz file (default: assets/calibration/camera_calibration.npz)
--cols    INT     inner corner columns  (default: 9)
--rows    INT     inner corner rows     (default: 6)
--square  FLOAT   square size in meters (default: 0.03)
--camera  INT     webcam index          (default: 0)
```

**Controls:** `C` = toggle 3D cube overlay · `Q` / `Esc` = quit

> **Note on `--square`:** must match your actual printed square size in meters. Measure one square with a ruler (e.g. 2.5 cm → `--square 0.025`). Only affects the scale of tvec — not K.

---

## Part 5 — ArUco Markers

### `scripts/aruco/generate_aruco_markers.py` · NB12

Batch-generates ArUco marker PNG files ready for printing. No camera needed — runs offline.

**Run:**
```bash
python scripts/aruco/generate_aruco_markers.py
python scripts/aruco/generate_aruco_markers.py --ids 0-9 --size 400 --out assets/aruco_markers/
```

**Options:**
```
--dict    STR     ArUco dictionary (default: DICT_4X4_50)
--ids     STR     marker IDs to generate: single (5), list (0,1,2), or range (0-9) (default: 0-4)
--size    INT     output image size in pixels (default: 400)
--border  INT     border bits around marker (default: 1)
--out     PATH    output folder (default: assets/aruco_markers/)
```

**Output:** one PNG per marker ID, named `aruco_<DICT>_id<N>.png`. Prints the physical size at 300 DPI so you know how large to print.

---

### `scripts/aruco/detect_aruco_live.py` · NB13

Real-time ArUco marker detection from a webcam. Draws detected corners, IDs, and FPS counter.

**Run:**
```bash
python scripts/aruco/detect_aruco_live.py
```

**Options:**
```
--dict      STR    ArUco dictionary (default: DICT_4X4_50)
--camera    INT    webcam index (default: 0)
--width     INT    capture width in pixels (default: 1280)
--height    INT    capture height in pixels (default: 720)
--rejected  FLAG   also show rejected candidates (for debugging detection failures)
```

**Controls:** `Q` / `Esc` = quit

---

### `scripts/aruco/aruco_pose_estimation_live.py` · NB14

Real-time ArUco marker detection + 6D pose estimation. Draws 3D coordinate axes on each detected marker.

**Requires:** calibration file from NB07 (`assets/calibration/camera_calibration.npz`)

**Run:**
```bash
python scripts/aruco/aruco_pose_estimation_live.py
python scripts/aruco/aruco_pose_estimation_live.py --marker-length 0.05
```

**Options:**
```
--calib          PATH     calibration .npz file (default: assets/calibration/camera_calibration.npz)
--marker-length  FLOAT    physical marker side length in meters (default: 0.05 = 5 cm)
--dict           STR      ArUco dictionary (default: DICT_4X4_50)
--camera         INT      webcam index (default: 0)
```

**Controls:** `Q` / `Esc` = quit

> **Note on `--marker-length`:** measure the printed marker's black border edge in meters. Affects tvec scale — wrong value gives wrong distance readout.

---

### `scripts/robotics/robot_station_docking.py` · NB15

Full ArUco-based robot docking demo. Detects a target ArUco marker and runs a P-controller to compute forward/lateral/heading alignment commands. Displays a live HUD with alignment state and command output.

**Requires:** calibration file from NB07 (`assets/calibration/camera_calibration.npz`)

**Run:**
```bash
python scripts/robotics/robot_station_docking.py
python scripts/robotics/robot_station_docking.py --target 0 --marker-length 0.15
```

**Options:**
```
--calib          PATH    calibration .npz file (default: assets/calibration/camera_calibration.npz)
--target         INT     ArUco ID of the docking station marker (default: 0)
--marker-length  FLOAT   physical marker side length in meters (default: 0.15)
--camera         INT     webcam index (default: 0)
```

**Controls:** `0` / `1` / `2` = switch target station ID · `Q` / `Esc` = quit

**States:** `SEARCHING` → `ALIGNING` → `APPROACH` → `DOCKED`

---

## Part 6 — Stereo Vision

### `scripts/calibration/stereo_camera_calibration.py` · NB17

Full stereo calibration pipeline. Takes matched image pairs from two folders and produces rectification maps saved as `stereo_maps.npz`.

**Run:**
```bash
python scripts/calibration/stereo_camera_calibration.py \
    --left-dir  stereo_images/left/ \
    --right-dir stereo_images/right/
```

**Options:**
```
--left-dir   PATH    folder of left camera images
--right-dir  PATH    folder of right camera images
--cols       INT     inner corner columns (default: 9)
--rows       INT     inner corner rows    (default: 6)
--square     FLOAT   square size in meters (default: 0.03)
--out        PATH    output .npz file (default: assets/calibration/stereo_maps.npz)
--alpha      FLOAT   rectification crop factor 0–1 (default: 0)
```

**Output:** `stereo_maps.npz` containing rectification maps for both cameras — feed this into `stereo_depth_live.py`.

---

### `scripts/stereo/stereo_depth_live.py` · NB17

Real-time stereo depth from two cameras using the rectification maps produced by `stereo_camera_calibration.py`. Displays disparity map with `COLORMAP_HOT`.

**Requires:** `stereo_maps.npz` from `stereo_camera_calibration.py`

**Run:**
```bash
python scripts/stereo/stereo_depth_live.py
python scripts/stereo/stereo_depth_live.py --maps assets/calibration/stereo_maps.npz --left 0 --right 1
```

**Options:**
```
--maps       PATH    stereo maps .npz file (default: assets/calibration/stereo_maps.npz)
--left       INT     left camera index  (default: 0)
--right      INT     right camera index (default: 1)
--width      INT     capture width  (default: 640)
--height     INT     capture height (default: 480)
--num-disp   INT     StereoSGBM num disparities, must be multiple of 16 (default: 96)
--block-size INT     StereoSGBM block size, must be odd (default: 11)
```

**Controls:** `D` = cycle display modes (left+depth · rectified pair with epipolar lines · depth only) · `Q` / `Esc` = quit

---

## Part 8 — Robotics Projects

### `scripts/robotics/forklift_pallet_alignment.py` · NB24

Multi-marker pallet pose estimation and 4-axis fork alignment. Detects ArUco markers on a pallet (IDs 10, 11, 12), averages their poses, and computes forward / lateral / turn / lift alignment commands.

**Requires:** calibration file from NB07 (`assets/calibration/camera_calibration.npz`)

**Run:**
```bash
python scripts/robotics/forklift_pallet_alignment.py
```

**Options:**
```
--calib          PATH     calibration .npz file (default: assets/calibration/camera_calibration.npz)
--marker-length  FLOAT    physical marker side length in meters (default: 0.1)
--camera         INT      webcam index (default: 0)
```

**Controls:** `Q` / `Esc` = quit

**Marker IDs:** 10 (left pocket), 11 (center), 12 (right pocket) — edit `MARKER_POS_IN_PALLET` in the script to change the physical layout.

---

*For the theory behind each script, open the corresponding notebook. For a quick reminder of arguments at the terminal, run the script with `--help`.*
