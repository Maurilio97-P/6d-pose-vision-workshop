# Video Companion Guide

**How to use this**: Before opening a notebook, watch the videos listed for it first.
The videos give you the visual + intuition side. The notebooks then go deep on the code and math.
You don't need to take notes while watching — just let it sink in, then crack open the notebook.

---

## Part 0 — Getting Started

### NB 00 · Welcome & Roadmap
> No video needed. Just open the notebook and read through it.

### NB 01 · Environment Setup
Watch these **before** Section 2 (venv vs conda) — they show Anaconda and conda environments in action, which makes the comparison in the notebook much easier to follow:

1. **Getting started with Anaconda and Python on Windows** *(Anaconda install, environments, Git Bash setup)*
   https://www.youtube.com/watch?v=4DQGBQMvwZo
   *~15 min — covers installing Anaconda, creating environments, and why you never develop in `base`*

2. **Set up Conda virtual environment for data science projects** *(Miniconda, create/activate/install workflow)*
   https://www.youtube.com/watch?v=gVfTT8o9PyQ
   *~10 min — clean walkthrough of conda create, activate, install, and using environments in VS Code*

> **Only if you want GPU support for Part 7 (optional — skip now, come back when you reach Part 7):**
>
> 1. **Installing OpenCV with GPU for Python using VS Code and CUDA** — full deep-dive (CMake, CUDA flags, build from source)
>    https://youtu.be/HsuKxjQhFU0
> 2. **Quick Install OpenCV with GPU (CUDA) Support** — faster walkthrough of the same process
>    https://youtu.be/d8Jx6zO1yw0

---

## Part 1 — Tools

### NB 02 · Jupyter Notebooks 101
Watch one or more of these **before** the notebook — they show Jupyter in action so the interface isn't new when you start running cells:

1. **Jupyter Notebook in 10 Minutes** *(fastest general intro)*
   https://www.youtube.com/watch?v=H9Iu49E6Mxs
   *~10 min — cells, modes, shortcuts, kernel — everything you need to get started*

2. **Getting Started with Jupyter Notebooks in VS Code** *(if you're running locally in VS Code)*
   https://www.youtube.com/watch?v=suAkMeWJ1yE
   *~15 min — kernel selection, IntelliSense, variable explorer, debugger — major upgrade over browser Jupyter*

3. **Cómo usar Jupyter Notebook y qué es JupyterLab** *(Spanish)*
   https://www.youtube.com/watch?v=CwbMaSkKDZg
   *~12 min — covers the Notebook vs JupyterLab distinction, cells, markdown, kernels — in Spanish*

### NB 03 · NumPy for CV
Watch VN21 and VN22 **before** the notebook — they build the mental model (arrays as numbers, images as arrays) that the whole notebook depends on. VN23 and VN24 are short orientation videos worth watching if you're wondering where NumPy fits relative to the rest of the Python ecosystem:

1. **What is NumPy and Why?** *(why lists aren't enough, vectorized operations, ndarray)*
   https://www.youtube.com/watch?v=SqhVpJSHuyI
   *~10 min — explains why NumPy exists and what makes it fast*

2. **NumPy for Images** *(images as 3D arrays, slicing channels, histograms)*
   https://www.youtube.com/watch?v=7V909wyeOQY
   *~15 min — the most directly relevant video to this notebook; watch this one above all*

3. **NumPy vs Pandas** *(when to use each — Pandas is built on NumPy)*
   https://www.youtube.com/watch?v=KHoEbRH46Zk
   *~10 min — answers "should I use Pandas instead?" before you start wondering*

4. **NumPy vs SciPy** *(SciPy extends NumPy — used in calibration)*
   https://www.youtube.com/watch?v=l3s-_8uTBVA
   *~10 min — useful context since SciPy appears in this course's requirements.txt*

---

## Part 2 — OpenCV Foundations

### NB 04 · Intro to OpenCV
Watch all three **before** the notebook — they give you the concept, the landscape, and the setup in the right order:

1. **Image Processing VS Computer Vision: What's The Difference?** *(conceptual framing)*
   https://www.youtube.com/watch?v=pcxhj5KFI6M
   *~8 min — clarifies what OpenCV is actually doing: image in → image out (processing) vs image in → information out (vision)*

2. **OpenCV Tutorial in 5 Minutes — All Modules Overview** *(landscape map)*
   https://www.youtube.com/watch?v=PeMM80WimN4
   *~5 min — walks through every OpenCV module so you know what exists before diving into any one part*

3. **How to Install OpenCV for Python** *(setup + the cv2 naming quirk)*
   https://youtu.be/M6jukmppMqU
   *~10 min — covers `pip install opencv-python` and the gotcha: you install "opencv-python" but import it as `cv2`*

### NB 05 · Image Operations
This notebook covers HSV, thresholding, and morphological operations. Watch VN29 and VN31 before the color space section. VN28 and VN30 show where the skills you build here eventually lead:

1. **OpenCV Python HSV Color Space** *(why HSV beats RGB for segmentation)*
   https://www.youtube.com/watch?v=G3PW5ysKDxc
   *~15 min — Hue/Saturation/Value intuition, cv.inRange() masking, practical color segmentation*

2. **Detección de color con Python y OpenCV usando HSV** *(Spanish — real-time color detection)*
   https://youtu.be/aFNDh5k3SjU
   *~12 min — same HSV concept with a live webcam color tracker demo, in Spanish*

3. **OpenCV Contours in Python** *(where thresholding + morphology lead)*
   https://youtu.be/LMamYJYnws8
   *~20 min — findContours, drawContours, bounding rects, moments — the natural next step after binary images*

4. **OpenCV Python Histogram Backprojection** *(advanced HSV masking)*
   https://www.youtube.com/watch?v=aOHStBqEFlQ
   *~15 min — using an ROI histogram to find similar regions in a full image; deeper payoff of HSV masking*

---

## Part 3 — Camera Model

### NB 06 · Camera Model Theory
Watch this **before** the notebook. It's the best visual explanation of the pinhole model, intrinsic matrix, and why calibration matters:

**Camera Calibration Explained and SIMPLE Step-by-Step Guide!**
https://www.youtube.com/watch?v=Wcnb197g2i0
*~15 min — watch the whole thing, it maps 1:1 with NB 06*

---

### NB 07 · Camera Calibration
Watch both — first one is theory context, second is the hands-on code:

1. **Camera Calibration in less than 5 Minutes with OpenCV** *(quick practical overview)*
   https://www.youtube.com/watch?v=_-BTKiamRTg
   *~5 min — watch this first, it shows the full workflow fast*

2. **OpenCV Python Camera Calibration (Intrinsic, Extrinsic, Distortion)** *(deeper dive)*
   https://www.youtube.com/watch?v=H5qbRTikxI4
   *~20 min — goes deeper into what K, dist coefficients mean*

---

### NB 08 · Distortion & Undistortion
> Same videos as NB 07 cover this. No extra video needed.

---

## Part 4 — Classical Pose Estimation

### NB 09 · solvePnP Explained
### NB 10 · Pose with Chessboard
Watch this before both notebooks — it shows solvePnP in action with real objects:

**OpenCV Python Pose Estimation for Objects (Algorithm and Code)**
https://www.youtube.com/watch?v=bs81DNsMrnM
*~20 min — covers 2D-3D correspondences, rvec, tvec, and drawFrameAxes*

---

## Part 5 — ArUco Markers

### NB 11 · ArUco Theory
### NB 15 · ArUco Robotics App
Watch this for a full end-to-end demo before diving into the theory:

**ArUco Marker Pose Estimation and Detection in Real-Time using OpenCV Python**
https://www.youtube.com/watch?v=bS00Vs09Upw
*~25 min — see the full pipeline working before you learn to build it*

---

### NB 12 · Generate ArUco
**Generate ArUco Markers for Detection and Pose Estimation with OpenCV**
https://youtu.be/sg1bVJBjbng?si=E6pw53-D06sHjfrg
*~10 min — watch before generating your marker set*

---

### NB 13 · Detect ArUco
**Building an Augmented Reality Application with ArUco Marker Detection in OpenCV**
https://www.youtube.com/watch?v=UlM2bpqo_o0
*~20 min — shows detection + AR overlay, good visual context before NB 13*

---

### NB 14 · ArUco Pose Estimation
> The video from NB 11 (`bS00Vs09Upw`) covers this well. Re-watch the pose section if needed.
> Also search: *"ArUco Marker Pose Estimation in OpenCV"* for a shorter dedicated video.

---

## Part 6 — Stereo Vision

### NB 16 · Stereo Theory
### NB 17 · Stereo Calibration
Watch this before both notebooks — covers the full stereo calibration workflow in OpenCV:

**Stereo Vision Camera Calibration with OpenCV: How to Calibrate your Camera with Python Script**
https://www.youtube.com/watch?v=yKypaVl6qQo
*~30 min — walks through the exact same 8-step pipeline used in NB 17*

---

## Part 7 — Deep Learning 6D Pose

### NB 18 · Intro to DL for CV
**3D Object Detection and Pose Estimation with Deep Learning in OpenCV Python**
https://youtu.be/R7zWFy7JmXc?si=dc5IrrhyiZrzGSQ4
*~15 min — gives you context on why DL methods beat classical for generalization*

> **⚙️ GPU setup reminder:** If you plan to run Part 7 locally with an NVIDIA GPU, this is the right moment to set up GPU-accelerated OpenCV. Colab users can skip — T4 GPU is handled automatically.
> - Full guide (VN8): https://youtu.be/HsuKxjQhFU0
> - Quick guide (VN32): https://youtu.be/d8Jx6zO1yw0

---

### NB 19 · MediaPipe Objectron
**3D Object Detection with MediaPipe and OpenCV**
https://www.youtube.com/watch?v=f-Ibri14KMY
*~15 min — shows Objectron running live, good visual context before the deprecated API notebook*

---

### NB 20 · EfficientPose
Watch this — it covers both EfficientPose architecture and why it's better than the 2-step PnP approach:

**6D Pose Estimation WITHOUT MARKERS for 3D Object Detection via FoundationPose & EfficientPose**
https://www.youtube.com/watch?v=mlXs5kIQ5p4
*~20 min — watch the EfficientPose section specifically (first half of video)*

---

### NB 21 · FoundationPose & FreeZe
Watch **both** — they cover the two methods in this notebook:

1. **6D Pose Estimation WITHOUT MARKERS** *(FoundationPose section)*
   https://www.youtube.com/watch?v=mlXs5kIQ5p4
   *Same video as NB 20 — this time focus on the FoundationPose section (second half)*

2. **3D Object Detection (6D Pose Estimation) without Training using FreeZe**
   https://www.youtube.com/watch?v=Mgmt93kXK_4
   *~15 min — dedicated to FreeZe, explains the two-branch architecture visually*

---

### NB 22 · MegaPose + ViSP
> No dedicated video captured for MegaPose specifically.
> Search YouTube: *"MegaPose 6D pose estimation"* or *"ViSP tracking tutorial"*
> The setup section in the notebook has the official ViSP tutorial link.

---

## Part 8 — Robotics Projects

### NB 23 · Station Alignment (ArUco)
### NB 24 · Pallet Detection & Fork Alignment
### NB 25 · Capstone Template

> These are project notebooks — no new concepts to preview with video.
> Before starting, re-watch whichever earlier video feels rusty for your chosen method.
> **Suggested refreshers:**
> - ArUco path → re-watch `bS00Vs09Upw`
> - DL/zero-shot path → re-watch `mlXs5kIQ5p4` + `Mgmt93kXK_4`

---

## Quick Video Reference Table

| Video | URL | Best before |
|-------|-----|-------------|
| Getting started with Anaconda and Python on Windows | https://www.youtube.com/watch?v=4DQGBQMvwZo | NB 01 |
| Installing OpenCV with GPU for Python using VS Code and CUDA | https://youtu.be/HsuKxjQhFU0 | NB 01 (optional GPU) |
| Quick Install OpenCV with GPU (CUDA) Support | https://youtu.be/d8Jx6zO1yw0 | NB 01 (optional GPU) |
| Set up Conda virtual environment for data science projects | https://www.youtube.com/watch?v=gVfTT8o9PyQ | NB 01 |
| Jupyter Notebook in 10 Minutes | https://www.youtube.com/watch?v=H9Iu49E6Mxs | NB 02 |
| Getting Started with Jupyter Notebooks in VS Code | https://www.youtube.com/watch?v=suAkMeWJ1yE | NB 02 |
| Cómo usar Jupyter Notebook y qué es JupyterLab (Spanish) | https://www.youtube.com/watch?v=CwbMaSkKDZg | NB 02 |
| What is NumPy and Why? | https://www.youtube.com/watch?v=SqhVpJSHuyI | NB 03 |
| NumPy for Images | https://www.youtube.com/watch?v=7V909wyeOQY | NB 03 |
| NumPy vs Pandas | https://www.youtube.com/watch?v=KHoEbRH46Zk | NB 03 |
| NumPy vs SciPy | https://www.youtube.com/watch?v=l3s-_8uTBVA | NB 03 |
| Image Processing VS Computer Vision | https://www.youtube.com/watch?v=pcxhj5KFI6M | NB 04 |
| OpenCV Tutorial in 5 Minutes — All Modules Overview | https://www.youtube.com/watch?v=PeMM80WimN4 | NB 04 |
| How to Install OpenCV for Python | https://youtu.be/M6jukmppMqU | NB 04 |
| OpenCV Python HSV Color Space | https://www.youtube.com/watch?v=G3PW5ysKDxc | NB 05 |
| Detección de color con OpenCV usando HSV (Spanish) | https://youtu.be/aFNDh5k3SjU | NB 05 |
| OpenCV Contours in Python | https://youtu.be/LMamYJYnws8 | NB 05 |
| OpenCV Python Histogram Backprojection | https://www.youtube.com/watch?v=aOHStBqEFlQ | NB 05 |
| Camera Calibration Explained | https://www.youtube.com/watch?v=Wcnb197g2i0 | NB 06 |
| Camera Calibration in < 5 min | https://www.youtube.com/watch?v=_-BTKiamRTg | NB 07 |
| OpenCV Camera Calibration (deep dive) | https://www.youtube.com/watch?v=H5qbRTikxI4 | NB 07–08 |
| OpenCV Pose Estimation for Objects | https://www.youtube.com/watch?v=bs81DNsMrnM | NB 09–10 |
| ArUco Pose Estimation Real-Time | https://www.youtube.com/watch?v=bS00Vs09Upw | NB 11–15 |
| Generate ArUco Markers | https://youtu.be/sg1bVJBjbng?si=E6pw53-D06sHjfrg | NB 12 |
| ArUco Detection for AR Apps | https://www.youtube.com/watch?v=UlM2bpqo_o0 | NB 13 |
| Stereo Vision Camera Calibration | https://www.youtube.com/watch?v=yKypaVl6qQo | NB 16–17 |
| DL for CV: 3D Object Detection | https://youtu.be/R7zWFy7JmXc?si=dc5IrrhyiZrzGSQ4 | NB 18 |
| MediaPipe 3D Object Detection | https://www.youtube.com/watch?v=f-Ibri14KMY | NB 19 |
| 6D Pose WITHOUT MARKERS (EfficientPose + FoundationPose) | https://www.youtube.com/watch?v=mlXs5kIQ5p4 | NB 20–21 |
| FreeZe: Zero-shot 6D Pose | https://www.youtube.com/watch?v=Mgmt93kXK_4 | NB 21 |
