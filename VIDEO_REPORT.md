# Video Content Report — 6D Pose Vision Workshop

**Date:** 2026-02-27
**Total videos covered:** 15
**Sources:** Two main YouTube creators (Kevin Wood Robotics + a European computer vision tutorial channel)

---

## Overview

The 15 videos form a **complete computer vision and 6D pose estimation curriculum**, progressing from foundational camera math to cutting-edge marker-free deep learning. The content can be grouped into five themes:

| Theme | Videos |
|---|---|
| Camera Calibration | 3, 4, 9, 15 |
| ArUco Marker Pipeline | 1, 12, 13, 14 |
| Classical Pose Estimation | 2 |
| Deep Learning / Marker-Free 6D Pose | 5, 6, 7, 10 |
| OpenCV GPU Setup | 8, 11 |

---

## THEME 1 — Camera Calibration

### Video 3 — Camera Calibration Explained *(Kevin Wood Robotics)*

**What it covers:** A conceptual and practical explanation of camera calibration using a chessboard pattern.

The video starts by defining the three coordinate frames in computer vision:
- **World frame** — where physical objects live in 3D space
- **Camera frame** — the 3D coordinate system from the camera's perspective
- **Image frame** — 2D pixel coordinates on the image plane

The transformation from world to camera uses **extrinsics** (rotation R and translation t). The transformation from camera to image uses **intrinsics** (focal lengths fx, fy and principal point cx, cy, packaged as the 3×3 camera matrix K).

The video explains distortion in detail:
- **Radial distortion** (k1, k2, k3): causes barrel or pincushion warping
- **Tangential distortion** (p1, p2): caused by lens/sensor misalignment

Full distortion vector in OpenCV: `[k1, k2, p1, p2, k3]`

**Practical workflow shown:**
1. Download calibration app from kevinwoodrobotics.com
2. Use a 9×6 inner-corner chessboard (printed or displayed on phone)
3. Capture images at varied angles and distances
4. Run `calibration.py` — Python 3.11, numpy, opencv-python, matplotlib
5. Script outputs `calibration.json` with reprojection error, camera matrix, distortion coefficients, rvecs, tvecs

**Reprojection error thresholds:**
- < 0.5 → Excellent
- < 1.0 → Good
- > 2.0 → Poor

**Tips to improve calibration:** more images, varied angles (avoid degenerate flat case), full chessboard in frame, no blurry images.

---

### Video 4 — OpenCV Python Camera Calibration *(Kevin Wood Robotics)*

**What it covers:** A deeper code-level walkthrough of the calibration pipeline.

This video is more technical than Video 3. The key additions:

**Projection equation:**
```
x = P X    where P = K [R | t]
```

**Coding pipeline:**
1. Set chessboard size — **critical**: count INNER corners only (e.g., rows=6, cols=9)
2. Set termination criteria for `cornerSubPix()` (max iterations + error tolerance)
3. Generate world points (0,0,0), (1,0,0), (2,0,0)... — assume Z=0 plane
4. Loop through images: convert to grayscale → `cv2.findChessboardCorners()` → `cv2.cornerSubPix()` for subpixel accuracy
5. Call `cv2.calibrateCamera()` — returns reprojection error, camera matrix, distortion, rvecs, tvecs

**Demo result from the transcript:** reprojection error ≈ 0.1687 pixels — very good.

**Undistortion section:**
- `cv2.getOptimalNewCameraMatrix(alpha=0)` — crop to valid region only; `alpha=1` — keep all pixels (black borders appear)
- `cv2.undistort()` — simple one-call undistortion
- Visual validation shown with a chocolate bar image: subtle barrel distortion visible only when drawing straight lines over it.

---

### Video 9 — Stereo Vision Camera Calibration *(European tutorial channel)*

**What it covers:** Calibrating a **stereo camera pair** (left + right webcam) for depth estimation.

This video introduces the full stereo pipeline. Key insight from the presenter: calibrate each camera individually first for better results, then combine with stereo calibration.

**Full pipeline:**
1. **Capture images** — a script opens two webcams, press S to save synchronized left/right pairs. ~3–6 image pairs are enough. Chessboard moved to different angles and positions.
2. **Prepare calibration data** — chessboard size 9×6, frame size 640×480. If real square size is known (e.g., 2 cm), multiply object points by 20 (mm) for real-world scale.
3. **Find corners per camera** — `cv2.findChessboardCorners()` + `cv2.cornerSubPix()` separately for left and right.
4. **Calibrate each camera individually** — `cv2.calibrateCamera()` → camera matrix + distortion. Then `cv2.getOptimalNewCameraMatrix()`.
5. **Stereo calibration** — `cv2.stereoCalibrate()` with flag `CALIB_FIX_INTRINSIC` (intrinsics already known, so only estimate R, T, Essential matrix E, Fundamental matrix F between cameras).
6. **Stereo rectification** — `cv2.stereoRectify()` → left/right rectification transforms, projection matrices, and the **Q matrix** (used later for depth reconstruction).
7. **Build remap arrays** — `cv2.initUndistortRectifyMap()` produces `stereoMapL_x/y` and `stereoMapR_x/y`.
8. **Save to XML** — `stereoMap.xml` — do this once, load in any future application.
9. **Apply in real app** — `cv2.remap()` every frame → rectified, undistorted stereo pair.

After rectification, corresponding points fall on the same horizontal scanline, making disparity (and depth) computation straightforward.

---

### Video 15 — Camera Calibration in < 5 Minutes *(Kevin Wood Robotics)*

**What it covers:** A speed-run, pragmatic workflow for camera calibration using two scripts cloned from GitHub.

**Scripts:**
- `get_images.py` — opens webcam, press S to save frames to `images/`, press ESC to exit
- `calibration.py` — loads PNGs, detects corners, calibrates, saves parameters

**Output files:** `cameraMatrix.pickle`, `dist.pickle`, `camera_calibration.pickle` (combined)

**Two undistortion options compared:**
- `cv2.undistort()` — simple, good for single images
- `cv2.remap()` with `cv2.initUndistortRectifyMap()` — faster for real-time video because the mapping is computed once and reused every frame. The presenter confirms remap is visibly faster.

The presenter uses an iPad to display the chessboard. ~10–20 images recommended. Blurry or partial chessboard images should be deleted before running calibration.

**Connection to other work:** This calibration output (pickle files) is a direct dependency for ArUco pose estimation, solvePnP, and any real-world distance measurement.

---

## THEME 2 — ArUco Marker Pipeline

### Video 1 — ArUco Marker Pose Estimation Overview *(Kevin Wood Robotics)*

**What it covers:** A high-level introduction to ArUco markers covering theory, dictionaries, and a live demo.

**What ArUco stands for:** Augmented Reality University of Córdoba.

**How markers work:**
- Square binary grids (NxN cells)
- Each cell is black (0) or white (1)
- Each pattern encodes a unique ID
- A 6×6 grid = 36 bits = up to 2^36 combinations, but only 250 are used per dictionary to ensure markers are visually distinct (maximum Hamming distance)

**Available dictionaries:**
- Grid sizes: 4×4, 5×5, 6×6, 7×7
- Marker counts: 50 to 1000
- Special types: ArUco Original (variable) and AprilTags (16×16 to 36×36 — more robust but heavier)
- ~25 total types

**Choosing a dictionary:**
- 30–50 markers → tabletop AR, small robotics demos
- 100–600 markers → room mapping, indoor localization
- 1000–2000 markers → warehouse, large building robot navigation

**Code structure shown:**
1. **Marker generation** — input: dictionary + marker ID + width → output: 200×200px marker image (save or display on phone)
2. **Detection + pose estimation** — input: camera matrix, distortion, dictionary, video feed → output: marker ID shown, 3D XYZ axes drawn on marker

**Live demo highlights from transcript:**
- Very stable real-time performance; handles fast motion
- Works under glare (visible in demo)
- Works with partial occlusion (hand blocking part of marker) — detection survives until too much of the marker is blocked
- Works at steep tilt angles
- Fails when too much of the marker is covered or extreme tilt occurs

---

### Video 12 — How to Detect ArUco Markers *(European tutorial channel)*

**What it covers:** A full code walkthrough for real-time ArUco marker detection using a webcam.

This is the detection-only step (no pose estimation yet — that comes in Video 14).

**Code structure:**
1. Import numpy, time, cv2
2. Choose the ArUco dictionary type (must match the printed marker — e.g., `DICT_4X4_*`)
3. `cv2.aruco.Dictionary_get(aruco_type)` → dictionary object
4. `cv2.aruco.DetectorParameters_create()` → detector parameters
5. `cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)` → returns `corners`, `ids`, `rejected`

**Display function logic:**
- Check `len(corners) > 0`
- Flatten the IDs array (shape `[[1],[2],...]` → `[1, 2, ...]`)
- Zip corners and IDs, loop through each marker
- Extract 4 corner points (top-left, top-right, bottom-right, bottom-left)
- Draw bounding box lines (4 edges)
- Compute center: `cX = (TL.x + BR.x) / 2`, `cY = (TL.y + BR.y) / 2`
- Draw marker ID text with `cv2.putText()`

**Webcam setup:** 1280×720 (HD). Frames resized for processing speed.

**Key observation from demo:** The presenter has two calibration boards — a small one with 4×4 markers and a large one with 5×5 markers. Switching from the small to the large board caused detection failure until the dictionary type was changed from `DICT_4X4` to `DICT_5X5`. This is highlighted as a critical practical gotcha.

**Debug checklist if detection fails:**
1. Verify dictionary matches printed markers
2. Improve focus/lighting
3. Increase marker size
4. Reduce motion blur
5. Inspect the `rejected` output

---

### Video 13 — Generate ArUco Markers *(European tutorial channel)*

**What it covers:** Short practical video showing how to programmatically create ArUco marker images with OpenCV.

**Full code shown:**
```python
import numpy as np
import cv2

aruco_type = cv2.aruco.DICT_4X4_50
marker_id = 1
tag_size = 1000

arucoDict = cv2.aruco.Dictionary_get(aruco_type)
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
cv2.aruco.drawMarker(arucoDict, marker_id, tag_size, tag, 1)
cv2.imwrite("aruco_1.png", tag)
cv2.imshow("ArUco Marker", tag)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Key points:**
- Dictionary and marker ID must match what the detection code expects
- Switching from `DICT_4X4_50` to `DICT_5X5_250` changes the visual appearance of the marker — and detection must use the same type
- Larger markers (500–1000px when printed) → better detection at distance
- Use matte paper, high contrast, flat mounting for best physical results
- You can loop to generate a full set of unique IDs for a system

**Why ArUco is powerful for pose:** once detected, you have 4 known corner points + known square geometry + known real-world size → solvePnP internally → reliable 6D pose.

---

### Video 14 — ArUco Marker Pose Estimation in OpenCV *(European tutorial channel)*

**What it covers:** Extending ArUco detection (Video 12) with actual 6D pose estimation — drawing coordinate axes on detected markers.

**Critical requirement:** camera must be calibrated first. Without `cameraMatrix` and `distCoeffs`, pose will be inaccurate or unstable.

**Pose estimation pipeline:**
1. Convert frame to grayscale
2. Get ArUco dictionary (same type as markers)
3. Create detector parameters
4. `cv2.aruco.detectMarkers()` — same as Video 12
5. For each detected marker, call:

```python
rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(
    corners[i],
    marker_length,   # real-world size in meters, e.g., 0.05
    cameraMatrix,
    distCoeffs
)
```

6. Draw axes with `cv2.drawFrameAxes()` → Red=X, Green=Y, Blue=Z

**Understanding the outputs:**
- `rvec` — Rodrigues rotation vector. Convert to rotation matrix: `R, _ = cv2.Rodrigues(rvec)`
- `tvec` — `[X, Y, Z]` translation. Z = depth from camera. This gives depth with just ONE camera — no stereo needed.

**Live demo from transcript:**
- The blue axis remains perpendicular to the marker plane even when tilted — the presenter uses this as the visual proof that pose estimation is working correctly
- Both the small (4×4) and large (5×5) calibration boards tested
- Very robust rotation and tilt tracking

**Comparison to solvePnP:** ArUco internally uses PnP, but ArUco is easier because it provides known square geometry and automatic corner correspondence. The presenter notes it can be more robust than basic PnP setups.

**Applications enabled:** attach marker to robot tool, estimate camera pose, track objects in 3D, build AR overlays, measure distances, estimate orientation.

---

## THEME 3 — Classical Pose Estimation

### Video 2 — OpenCV Python Pose Estimation *(Kevin Wood Robotics)*

**What it covers:** The mathematical and code foundations of pose estimation using a chessboard and `solvePnP` — the core algorithm behind all marker-based pose estimation.

**Conceptual foundation:**
```
Image Points = Projection Matrix × World Points
x_image = K [R | t] X_world
```

Where K = camera intrinsics, R = rotation, t = translation.

**What `solvePnP` does:** given known 3D world points and their corresponding 2D image points, it finds `rvec` and `tvec` that minimize **reprojection error** (the difference between where points actually appear in the image vs. where the estimated pose predicts they should appear).

**Default solver:** iterative Levenberg-Marquardt — a nonlinear gradient descent method that uses the Jacobian at each step. Other available methods: DLT (Direct Linear Transform), SVD-based.

**Code flow:**
1. Load calibration data from `.npz` file (camera matrix + distortion)
2. Loop through chessboard images
3. Grayscale → `cv2.findChessboardCorners()` → `cv2.cornerSubPix()` for subpixel accuracy
4. `cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)` → rvec, tvec
5. `cv2.projectPoints()` → reproject 3D axis/cube points back to 2D
6. Draw axes (X=Red, Y=Green, Z=Blue) or cube

**Drawing the cube:**
1. Define 8 cube corner points in 3D
2. Project with `projectPoints()`
3. Draw bottom plane (green), vertical edges, top plane

**Visual validation:** as the camera moves between calibration images, the cube rotates correctly — confirming the pose estimation and calibration are both working.

**Key equation illustrated:**
```
objectPoints (M×3 world coords)
imagePoints  (M×2 detected pixels)
→ solvePnP → rvec, tvec
→ projectPoints → draw visualization
```

---

## THEME 4 — Deep Learning / Marker-Free 6D Pose

### Video 5 — 6D Pose Estimation WITHOUT MARKERS *(Kevin Wood Robotics)*

**What it covers:** A comprehensive survey of modern marker-free 6D pose estimation, covering EfficientPose and FoundationPose.

**6D Pose definition:** 3 DOF translation (X, Y, Z) + 3 DOF rotation = full rigid body pose, expressed as `[R | t]`. Rotation can be represented as rotation matrix, axis-angle, quaternion, Euler angles, or Rodrigues vector.

**Rodrigues rotation intuition:** decompose vector v into parallel and perpendicular components relative to rotation axis, rotate the perpendicular component by angle θ, recombine.

**Classical pipeline (old way):**
1. 2D object detection (bounding box)
2. Use 2D–3D correspondences → solvePnP
Problem: two-step → slower and fragile.

---

**EfficientPose:**
- Based on EfficientDet (state-of-the-art 2D detector)
- Adds two extra subnetworks: **Rotation Net** and **Translation Net**, running in parallel with Class Net and Box Net
- Each pose net has: initial regression → iterative refinement using stacked convolution layers
- Everything learned end-to-end — no explicit PnP solving
- Trained on LineMOD / Occlusion / COCO datasets

**Live demo from transcript:** real-time XYZ tracking and orientation tracking shown on a bottle. Z value visibly changes as object moves toward/away from camera. The presenter notes you may need to retrain for your own object if not in the dataset.

**Robotic application shown:** robot arm grasping — 6D pose directly determines gripper rotation and position for bin picking or assembly.

**AR application shown:** virtual ball rolling on a book surface, overlayed using the estimated pose to maintain spatial lock.

---

**FoundationPose:**
Supports all four combinations:
1. Model-based estimation
2. Model-based tracking
3. Model-free estimation
4. Model-free tracking

Most older models only handle ONE of these.

**Architecture highlights:**
- Inputs: RGB or RGB-D image + textured CAD model OR reference images
- Synthetic data training via: text prompt → diffusion model → 3D model → physics engine → path-traced realistic render (reduces need for manual annotation)
- Neural object modeling: multiple views → NeRF-like 3D model → pose hypothesis generation using Transformers + attention
- Pose selection: rank pose candidates via self-attention → pick best

---

**Datasets mentioned:**
- **LineMOD** — most common, small, often augmented with viewpoint rotation
- **YCB-Video** — larger, used for manipulation research
- **BOP Benchmark** — standard benchmark aggregating many datasets

---

### Video 6 — 3D Object Detection WITHOUT Training (FreeZe) *(Kevin Wood Robotics)*

**What it covers:** FreeZe — a training-free, zero-shot 6D pose estimation method that works on **unseen** objects.

**Terminology clarification (from BOP Benchmark definitions):**
- **6D Pose Estimation** = find translation + rotation
- **3D Object Detection** = 6D pose + 3D bounding box
- **6D Detection** = RGB-D input + pose estimation
- **6D Localization** = known 3D model + estimate pose in scene
- **Seen vs Unseen** = model trained on object vs model never seen object before

**FreeZe = Training-Free Zero-Shot 6D Pose Estimation with Geometric and Vision Foundation Models**

**Why it matters:** traditional deep models require object-specific training, dataset labeling, and retraining for new objects. FreeZe needs no training and no fine-tuning.

**Pipeline:**
- Input: 3D CAD model + RGB-D scene image
- Left branch (model side): 3D model → render to 2D → DINO-like foundation model → visual features → back to 3D. Parallel: generate textureless point cloud → geometric features. Fuse both.
- Right branch (scene side): RGB-D crop → foundation model → visual features → convert to 3D using depth. Plus: 2D → 3D point cloud → geometric features. Fuse both.
- **Registration:** RANSAC (Random Sample Consensus — robust to outliers, finds best rigid alignment) → outputs final `[R | t]`

**Benchmark results from transcript:** FreeZe ranks #3 in 6D detection of unseen objects and #7 in 6D localization of unseen objects. Competitors include MegaPose, GigaPose, SAM-6D, FoundationPose.

**Demo observations:** objects in RGB-D video are projected with correct 6D pose; occasional spin artifacts; generally stable. Works for AR overlays, robotic grasping, object alignment.

**Comparison table (from notes):**

| Method | Needs Training | Needs Markers | Needs CAD Model | Zero-Shot |
|---|---|---|---|---|
| solvePnP | No | Yes (corners) | No | No |
| EfficientPose | Yes | No | Sometimes | No |
| FoundationPose | Yes | No | Optional | Limited |
| FreeZe | No | No | Yes | Yes |

**Big insight:** FreeZe blends classical geometry (RANSAC) with modern foundation model features — a convergence of paradigms.

---

### Video 7 — 3D Object Detection with MediaPipe and OpenCV *(European tutorial channel)*

**What it covers:** Using **MediaPipe Objectron** to achieve real-time 3D object detection and pose estimation on CPU only (no GPU).

**Performance:** ~20–30 FPS on a standard CPU — impressive for a deep learning method.

**MediaPipe Objectron outputs for each detected object:**
- 2D landmarks (bounding box corners)
- 3D rotation matrix
- 3D translation vector
- 3D bounding box in 3D space

**Code structure:**
```python
import cv2
import mediapipe as mp
import time

mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

objectron = mp_objectron.Objectron(
    static_image_mode=False,
    max_num_objects=2,
    min_detection_confidence=...,
    min_tracking_confidence=...,
    model_name="Cup"  # or "Shoe"
)
```

**Main loop:**
1. `cap.read()` → raw frame
2. Convert BGR → RGB (OpenCV=BGR, MediaPipe=RGB)
3. `image.flags.writeable = False` (performance boost — passes by reference)
4. `results = objectron.process(image)` — everything in `results.detected_objects`
5. Re-enable writeable
6. Convert back to BGR
7. Draw 2D landmarks: `mp_drawing.draw_landmarks(..., mp_objectron.BOX_CONNECTIONS)`
8. Draw 3D axis: `mp_drawing.draw_axis(image, detected_object.rotation, detected_object.translation)`
9. Compute FPS: `1 / total_time`

**Demo observations from transcript:**
- Cup detection works well when handle is visible; loses detection when handle is blocked
- Shoe detection tracks orientation, some jitter, occasional tracking loss
- Both rotations correctly follow the objects

**Limitations:** fixed set of supported object categories (cup, shoe, etc.); not zero-shot; occlusion sensitivity.

**Comparison table (from notes):**

| Method | Training Required | Custom Objects | Real-Time CPU | Uses RGB-D |
|---|---|---|---|---|
| solvePnP | No | Yes | Yes | Optional |
| EfficientPose | Yes | Yes | Maybe | RGB |
| FreeZe | No | Yes (CAD) | Maybe | RGB-D |
| MediaPipe Objectron | Pretrained | No | Yes | RGB |

---

### Video 10 — 3D Object Detection with EfficientPose in OpenCV *(European tutorial channel)*

**What it covers:** A practical live implementation of EfficientPose — running 6D pose estimation on a webcam in real time.

**Setup requirements:**
- Python 3.7
- TensorFlow 1.x (in a separate Anaconda environment — TF1 and TF2 are hard to mix)
- Optional: NVIDIA GPU with CUDA (`CUDA_VISIBLE_DEVICES=0`)

**Model outputs:** `boxes, scores, labels, rotation, translation` — full 6D detection in a single forward pass.

**Inference pipeline:**
1. Open webcam with `cv2.VideoCapture`
2. Read frame → make a copy for display
3. Preprocess (resize + normalize + camera intrinsic scaling)
4. `model.predict_on_batch(input_list)` → boxes, scores, labels, rotation, translation
5. Post-process: filter by confidence threshold (e.g., 0.5) and label index
6. Draw: 2D bounding box, class name, rotation values, translation values

**Label filtering detail from transcript:** COCO label 46 = "cup". Presenter filters with `if label == 46`. You can pass a list of label indices for multi-object detection.

**Camera matrix note:** the demo uses the LineMOD dataset's camera matrix. For real applications, use your own calibrated camera matrix for accurate pose values.

**Demo behavior:**
- When cup is held still: rotation and translation values stabilize
- When cup moves: values update accordingly
- Bounding box flickers slightly; pose updates remain reasonable
- If the cup moves out of frame or is occluded, tracking is lost

**Architecture recap:** EfficientNet backbone → parallel Class/Box/Rotation/Translation heads → everything learned, no explicit PnP needed.

---

## THEME 5 — OpenCV GPU Setup

### Video 8 — Installing OpenCV with GPU (Full Guide) *(European tutorial channel)*

**What it covers:** Full step-by-step guide to building OpenCV from source with CUDA and cuDNN support for Python.

**Why pip install doesn't work:** `pip install opencv-python` gives a CPU-only build with no CUDA, no cuDNN, no DNN GPU backend.

**Prerequisites:**
- Visual Studio 2019 with C++ tools (NOT 2022 — critical gotcha)
- CUDA Toolkit (example: 11.3)
- cuDNN (example: 8.2)
- CMake
- Anaconda Python 3.8 (added to PATH)
- OpenCV 4.5.2 source + OpenCV_contrib 4.5.2 (versions must match exactly)

**Folder structure:**
```
opencv_python/
    opencv-4.5.2/      ← source
    opencv_contrib-4.5.2/  ← extra modules
    build/             ← empty, fill by CMake
```

**CMake configuration steps:**
1. Source → `opencv/` folder; Build → `build/` folder
2. Generator: Visual Studio 16 2019, x64
3. First configure — Python 3 may not appear (common error)
4. Fix: upgrade numpy via `pip install --upgrade numpy` in Anaconda prompt, then reconfigure
5. Link Python correctly: PYTHON3_EXECUTABLE, PYTHON3_INCLUDE_DIR, PYTHON3_LIBRARY, NumPy path
6. Enable: `WITH_CUDA`, `OPENCV_DNN_CUDA`, `ENABLE_FAST_MATH`, `CUDA_FAST_MATH`, `BUILD_opencv_world`
7. Set `OPENCV_EXTRA_MODULES_PATH` → `opencv_contrib/modules`
8. Set `CUDA_ARCH_BIN` to your GPU's compute capability (GTX 1060 → 6.1, RTX 2060 → 7.5)
9. Build type: Release only
10. Final Configure → Generate

**Build command:**
```bash
cmake --build "path_to_build" --target install --config Release
```
Build time: 1–2 hours. Many warnings during build are normal.

**Verification:**
```python
import cv2
from cv2 import cuda
cuda.printCudaDeviceInfo(0)
```
Output: device count, GPU name, memory, CUDA driver version.

**VS Code setup:** select the Anaconda Python 3.8 interpreter at the bottom bar (selecting system Python causes ImportError).

**What you unlock:**
```python
# Explicit GPU operations
cv2.cuda.resize()     # GPU version
cv2.resize()          # CPU version (unchanged)

# DNN on GPU
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
```

**Key insight:** OpenCV GPU ≠ automatic speed boost. Only functions in the `cv2.cuda` namespace use the GPU. You must explicitly call them.

---

### Video 11 — Easy OpenCV with CUDA (Quick Version) *(European tutorial channel)*

**What it covers:** Same content as Video 8 but condensed into a faster, less-detailed walkthrough.

**Key differences vs Video 8:**
- Skips the installation of Visual Studio, CUDA, CMake (references a companion video instead)
- Shows GPU compute capability for two GPUs simultaneously: 6.1 (GTX 1060) and 8.6 (RTX 3060)
- Focuses on common mistakes checklist

**Common pitfalls:**
- Wrong Visual Studio version (must be 2019)
- CUDA version mismatch
- Wrong GPU compute capability in `CUDA_ARCH_BIN`
- NumPy not detected (fix: upgrade numpy)
- Using pip-installed OpenCV instead of compiled version

**Verification shown:** `RTX 3060` GPU detected, CUDA driver 11.3, memory and clock speed info printed.

**Use case for this video:** someone who already went through Video 8 and wants a quick reference for a second machine, or someone comfortable with the prerequisites who wants to skip the explanations.

---

## Supplementary Notes (misc_notes.md)

The misc notes contain two additional references that don't belong to the 15 main videos but are highly relevant to the workshop's broader theme.

---

### Supplementary A — YOLO + Intel RealSense for Real-World Position Estimation

**Source:** YouTube video (24,794 views, published August 2021)
**Code:** available via Google Drive link in the notes

**What it is:** A tutorial on estimating the **real-world 3D position (XYZ)** of objects using a combination of YOLO object detection and an Intel RealSense RGB-D camera.

**How it differs from everything else in the workshop:** All 15 main videos either use monocular cameras (where depth must be inferred from geometry, markers, or a neural network) or a stereo pair. This approach uses a **RealSense depth camera**, which directly measures depth per pixel via structured light or time-of-flight. YOLO provides the 2D bounding box (where is the object in the image), and RealSense provides the depth at that location — together they give real-world X, Y, Z without any pose solving.

**Stack used:**
- Python 3.6.8
- tensorflow-gpu 1.14.0
- keras 2.1.5
- h5py 2.9.0
- numpy 1.17.2
- opencv-contrib-python 4.2.0.34

**Why this is relevant to the workshop:** it represents a third paradigm for 3D localization, distinct from the two covered in the main videos:

| Paradigm | Depth Source | Example |
|---|---|---|
| Marker/geometry-based | Inferred (known size + PnP) | ArUco, solvePnP |
| Deep learning monocular | Learned | EfficientPose, MediaPipe |
| RGB-D camera | Direct hardware measurement | YOLO + RealSense |

The RealSense approach is the simplest to use for position (XYZ only) but doesn't give full 6D pose (orientation) out of the box — it would need to be combined with a pose estimation method for that.

---

### Supplementary B — MegaPose + ViSP: Online 6D Pose Tracking

**Source:** YouTube comments extracted from a video titled *"Object 6D pose estimation with MegaPose — Online 6D object pose tracking"*

**What it is:** A community discussion around deploying **MegaPose** for real-time 6D object pose tracking using the **ViSP (Visual Servoing Platform)** library. MegaPose was one of the benchmark competitors mentioned in Video 6 (FreeZe paper comparison).

**Context:** MegaPose is a foundation-model-based 6D pose estimator developed by Labbe et al. Like FoundationPose, it uses a 3D CAD model as input and can generalize to new objects without retraining. ViSP is a robotics/vision library (INRIA, France) used for visual servoing and object tracking.

**Key practical insight from the comment thread:**

A community member (Xuban) reported being stuck for a month trying to get MegaPose + ViSP working. The specific failure: **MegaPose not rendering the object texture**. The fix, provided by a user who successfully ran MegaPose6D with ViSP (Afonso Castro):

> You must prepare your CAD model folder **before** attempting any ViSP/MegaPose setup.

**Required folder structure:**
```
your_object/
    model.obj       ← 3D geometry
    model.mtl       ← material definition
    texture.jpg     ← texture image
```

- `model.obj` and `model.mtl` can be created with **Blender** (free, open-source 3D modeling tool)
- `texture.jpg` can be photographed from the real object or sourced from a texture library (e.g., BlenderKit for material-matched textures)
- Only after this folder is complete should you proceed to set up ViSP and MegaPose

Reference implementation: [afonsocastro/visp on GitHub](https://github.com/afonsocastro/visp/tree/master/tutorial/tracking/dnn/data/models/wood_block)
ViSP MegaPose tutorial: [visp-doc.inria.fr — tutorial-tracking-megapose](https://visp-doc.inria.fr/doxygen/visp-daily/tutorial-tracking-megapose.html)

**Community opinion on FoundationPose vs MegaPose:** one commenter explicitly asked why the video author didn't use FoundationPose instead, calling it "more powerful." This aligns with the benchmarks shown in Video 6, where FoundationPose consistently ranks higher than MegaPose. However, MegaPose may be preferred in some workflows because of better ViSP integration and longer community support.

**How this fits in the 6D pose landscape:**

| Model | Zero-Shot | Needs CAD | Tracking | ViSP Integration |
|---|---|---|---|---|
| MegaPose | Limited | Yes | Yes | Yes (via tutorial) |
| FoundationPose | Limited | Optional | Yes | Not directly |
| FreeZe | Yes | Yes | No (estimation only) | No |
| EfficientPose | No | No | No | No |

---

## How the Videos Connect — Learning Path

The 15 videos form a coherent learning arc:

```
FOUNDATION
  └── Camera Calibration (Videos 3, 4, 15)
        ├── Understand K, R, t, distortion
        ├── Run calibration code
        └── Save parameters (pickle / npz / JSON)

CLASSICAL GEOMETRY
  └── solvePnP with Chessboard (Video 2)
        ├── World points → image points
        ├── Minimize reprojection error
        └── Draw axes / 3D cube

MARKER-BASED PIPELINE
  └── ArUco (Videos 12, 13, 14 → demo in Video 1)
        ├── Generate markers (Video 13)
        ├── Detect markers + IDs (Video 12)
        └── Pose estimation with estimatePoseSingleMarkers (Video 14)

STEREO EXTENSION
  └── Stereo Calibration (Video 9)
        ├── Calibrate two cameras individually
        ├── Stereo calibrate → R, T between cameras
        ├── Rectify → aligned stereo pair
        └── Save stereoMap.xml for depth pipelines

GPU SETUP
  └── OpenCV with CUDA (Videos 8, 11)
        ├── Build from source
        └── Enable DNN CUDA backend

MODERN / MARKER-FREE
  └── MediaPipe Objectron (Video 7) — easy CPU baseline
  └── EfficientPose (Videos 5, 10) — single-network DL
  └── FoundationPose (Video 5) — foundation model, model-based+free
  └── FreeZe (Video 6) — zero-shot, no training, geometry + foundation models
```

---

## Key Technical Patterns Seen Across Videos

| Concept | Where it appears |
|---|---|
| Camera matrix K (intrinsics) | Videos 2, 3, 4, 9, 14, 15 |
| Distortion coefficients | Videos 3, 4, 9, 14, 15 |
| solvePnP / reprojection error | Videos 2, 3, 4, 14 |
| rvec / tvec (6D pose output) | Videos 1, 2, 5, 10, 14 |
| cornerSubPix (subpixel accuracy) | Videos 2, 4, 9 |
| Rodrigues rotation representation | Videos 5, 14 |
| RANSAC | Video 6 |
| cv2.remap vs cv2.undistort | Videos 4, 9, 15 |
| Confidence threshold tuning | Videos 7, 10 |
| Real-time FPS measurement | Videos 7, 10 |
| Anaconda environment isolation | Videos 8, 10, 11 |
