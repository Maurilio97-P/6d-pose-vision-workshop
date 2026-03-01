# 6D Pose Vision Workshop — Complete Course

A hands-on Jupyter notebook course taking you from basic Python to applying 6D pose estimation in real robotics applications.

---

## What You Will Build

By the end of this course you will be able to:

- Calibrate a real camera and understand its intrinsic and extrinsic parameters
- Estimate the 6D pose (3D position + 3D orientation) of objects using classical and deep learning methods
- Use ArUco markers to guide a mobile robot to a docking station
- Detect pallets from a CAD model and compute alignment offsets for a forklift
- Run pose estimation in real time from a webcam feed

---

## Prerequisites

| Topic | Required level |
|---|---|
| Python | Intermediate — OOP basics, dictionaries, loops, list comprehensions |
| Linear algebra | Basic — matrix multiplication, determinants, eigenvalues |
| NumPy | Not required — covered in Part 1 |
| OpenCV | Not required — covered in Parts 2–5 |
| Deep learning | Not required — covered in Part 7 |

---

## Course Structure

```
Part 0 — Getting Started          (notebooks 00–01)
Part 1 — Tools: Jupyter + NumPy   (notebooks 02–03)
Part 2 — OpenCV Foundations       (notebooks 04–05)
Part 3 — Camera Model             (notebooks 06–08)
Part 4 — Classical Pose (solvePnP)(notebooks 09–10)
Part 5 — ArUco Markers            (notebooks 11–15)
Part 6 — Stereo Vision            (notebooks 16–17)
Part 7 — Deep Learning 6D Pose    (notebooks 18–22)
Part 8 — Robotics Projects        (notebooks 23–25)
```

---

## Notebook Index

| # | File | Topic | Time |
|---|---|---|---|
| 00 | `part_0_getting_started/00_welcome_and_roadmap.ipynb` | What is 6D pose, course map, real-world problems | 20 min |
| 01 | `part_0_getting_started/01_environment_setup.ipynb` | venv, conda, pip, CUDA, VSCode, Colab | 30 min |
| 02 | `part_1_tools/02_jupyter_notebooks_101.ipynb` | Cells, kernel, shortcuts, magic commands | 25 min |
| 03 | `part_1_tools/03_numpy_for_cv.ipynb` | Arrays, shapes, dtypes, broadcasting, matplotlib | 45 min |
| 04 | `part_2_opencv_foundations/04_intro_to_opencv.ipynb` | Install, BGR/RGB, imread, VideoCapture, drawing | 40 min |
| 05 | `part_2_opencv_foundations/05_image_operations.ipynb` | Resize, color spaces, filters, edge detection | 50 min |
| 06 | `part_3_camera_model/06_camera_model_theory.ipynb` | Coordinate frames, pinhole, intrinsics K, x=KPX | 60 min |
| 07 | `part_3_camera_model/07_camera_calibration.ipynb` | Chessboard, findChessboardCorners, calibrateCamera | 50 min |
| 08 | `part_3_camera_model/08_distortion_undistortion.ipynb` | Radial/tangential distortion, undistort, remap | 40 min |
| 09 | `part_4_classical_pose/09_solvePnP_explained.ipynb` | 2D-3D correspondences, Levenberg-Marquardt | 55 min |
| 10 | `part_4_classical_pose/10_pose_with_chessboard.ipynb` | Full demo: calibration → solvePnP → 3D cube | 60 min |
| 11 | `part_5_aruco/11_aruco_theory.ipynb` | Binary grids, Hamming distance, dictionaries | 40 min |
| 12 | `part_5_aruco/12_generate_aruco.ipynb` | drawMarker, save PNG, printing tips | 20 min |
| 13 | `part_5_aruco/13_detect_aruco.ipynb` | detectMarkers, corners, IDs, webcam | 35 min |
| 14 | `part_5_aruco/14_aruco_pose_estimation.ipynb` | estimatePoseSingleMarkers, rvec/tvec, drawAxes | 45 min |
| 15 | `part_5_aruco/15_aruco_robotics_app.ipynb` | Full: ArUco at station → alignment offset | 60 min |
| 16 | `part_6_stereo_vision/16_stereo_theory.ipynb` | Epipolar geometry, disparity, depth, Q matrix | 55 min |
| 17 | `part_6_stereo_vision/17_stereo_calibration.ipynb` | stereoCalibrate, rectify, remap | 50 min |
| 18 | `part_7_deep_learning_6d_pose/18_intro_dl_for_cv.ipynb` | Neural networks, inference, pretrained models | 40 min |
| 19 | `part_7_deep_learning_6d_pose/19_mediapipe_objectron.ipynb` | Objectron, 3D bounding boxes, webcam | 45 min |
| 20 | `part_7_deep_learning_6d_pose/20_efficientpose.ipynb` | EfficientNet backbone, rotation/translation heads | 60 min |
| 21 | `part_7_deep_learning_6d_pose/21_foundationpose_freeze.ipynb` | Foundation models, RGB-D, zero-shot | 55 min |
| 22 | `part_7_deep_learning_6d_pose/22_megapose_visp.ipynb` | CAD prep, ViSP integration | 60 min |
| 23 | `part_8_robotics_projects/23_station_alignment_aruco.ipynb` | Full project: ArUco → docking offset | 75 min |
| 24 | `part_8_robotics_projects/24_pallet_detection_pose.ipynb` | CAD + pose → fork/clamp alignment | 75 min |
| 25 | `part_8_robotics_projects/25_capstone_template.ipynb` | Student's own robotics application | — |

---

## Navigation

- **[INDEX.ipynb](INDEX.ipynb)** — clickable table of contents for all 25 notebooks (start here if you're browsing in JupyterLab)
- **[VIDEO_COMPANION.md](VIDEO_COMPANION.md)** — which YouTube videos to watch before each notebook, with direct links

---

## How to Run

### Option A — Google Colab (recommended for beginners)

1. Open any notebook on GitHub and click **"Open in Colab"**
2. Each notebook detects Colab automatically and installs its own dependencies
3. For GPU-heavy notebooks (Part 7+): Runtime → Change runtime type → T4 GPU

### Option B — Local with venv

```bash
# Clone or download this repository
cd course

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter lab
```

### Option C — Docker (required for NB 20 · EfficientPose only)

Most of the course runs fine with Options A or B. The one exception is **Notebook 20 (EfficientPose)**, which requires TensorFlow 1.14 — an old version that conflicts with modern Python environments. Docker is the cleanest solution.

> **New to Docker?** NB 01 introduces it briefly, and NB 20 has a full plain-English explainer with step-by-step install instructions. You don't need to set it up until you reach NB 20.

```bash
# Install Docker Desktop first: https://www.docker.com/products/docker-desktop
# Then pull the TF1 GPU image and run EfficientPose inside it:

docker pull tensorflow/tensorflow:1.14.0-gpu-py3

docker run --gpus all -it \
    -v $(pwd):/workspace \
    tensorflow/tensorflow:1.14.0-gpu-py3 \
    /bin/bash
```

For FoundationPose (NB 21), Docker is optional — a conda environment works too. See NB 21 for details.

---

## Assets

```
assets/
    images/        — sample images used across notebooks
    calibration/   — saved calibration data (.npz, .json)
    models/        — CAD models (.obj/.mtl)
    aruco_markers/ — pre-generated marker PNGs (4x4, 5x5, 6x6)
```

---

## Grounded in Real Video Notes

This course is built on 15 curated video notes covering real implementations. Each notebook has recommended videos to watch first — see **[VIDEO_COMPANION.md](VIDEO_COMPANION.md)** for the full list with links.

Topics covered across the videos:

- ArUco marker pose estimation workflows
- Camera calibration (chessboard, <5 min method)
- OpenCV GPU installation with CUDA
- solvePnP and 6D pose pipelines
- MediaPipe Objectron, EfficientPose, FoundationPose, FreeZe, MegaPose
- Stereo vision calibration
- Full robotics station docking demos

---

*Questions? Issues? Open a GitHub issue or reach out to your instructor.*
