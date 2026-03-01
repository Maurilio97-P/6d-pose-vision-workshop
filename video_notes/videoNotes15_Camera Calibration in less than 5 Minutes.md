Broooo got you 😈🔥 — this one is the **fast practical camera calibration workflow** (capture chessboard images → run 
# Camera Calibration in < 5 Minutes (OpenCV)

Video: **Camera Calibration in less than 5 Minutes with OpenCV**
YouTube: [https://www.youtube.com/watch?v=_-BTKiamRTg](https://www.youtube.com/watch?v=_-BTKiamRTg)

---

## Goal

Calibrate a camera quickly so you can reuse the calibration parameters in your own projects.

Output files:

* `cameraMatrix.pickle`
* `dist.pickle`
* `camera_calibration.pickle` (combined)

Then you can:

* Undistort images
* Improve measurement accuracy
* Improve pose estimation (ArUco / solvePnP / etc.)

---

## High-Level Workflow

1. Clone repo that contains scripts (capture + calibration)
2. Capture 10–20 chessboard images with webcam
3. Run calibration script
4. Save camera parameters to `.pickle`
5. Use parameters in your real app:

   * `cv2.undistort()` (simple)
   * `cv2.remap()` (faster for real-time)

---

## Step 1 - Get the Code (GitHub)

The video uses a repo with two scripts:

* `get_images.py` (capture chessboard images)
* `calibration.py` (compute cameraMatrix + distCoeffs)

Clone repo:

* Copy repo URL
* Open Anaconda Prompt
* `git clone <repo_url>`
* Open folder in VS Code

---

## Step 2 - Create an `images/` Folder

Inside the repo:

* Create a folder named: `images`
* This folder will store the captured chessboard images

---

## Step 3 - Capture Calibration Images (`get_images.py`)

What the capture script does:

* Opens webcam in a `while` loop
* Shows live feed
* If you press **S** → saves a frame into `images/`
* If you press **ESC** → exits + releases camera

Chessboard source:

* Can be printed on paper
* Or displayed on an iPad/phone screen (video uses iPad)

Capture strategy:

* Rotate chessboard
* Move it around the frame
* Different angles and positions

Recommended count:

* About **10 to 20 images**

After capture:

* You can delete bad images (blurry, partial chessboard, etc.)

---

## Step 4 - Configure Calibration Script (`calibration.py`)

Before running calibration, set:

### Chessboard size

* Number of inner corners (example: 9x6 in many demos)
* Must match your chessboard pattern

### Frame size

* The resolution of your captured images (example: 640x480, 1280x720, etc.)

Then the script:

* Loads all PNG images in `images/`
* Detects chessboard corners
* Runs camera calibration
* Prints the **total reprojection error**

---

## Step 5 - Outputs Saved to Pickle

After calibration completes, it saves:

* `camera_calibration.pickle` (combined file)
* `cameraMatrix.pickle` (intrinsics only)
* `dist.pickle` (distortion coefficients only)

These files are meant to be loaded in your future projects.

---

## Step 6 - Undistortion Options

Once you have:

* `cameraMatrix`
* `distCoeffs`

You can undistort frames in two main ways.

---

### Option A: `cv2.undistort()` (simple)

Use when:

* Single images
* Not performance-critical

Conceptually:

* One function call
* Easy to use

---

### Option B: `cv2.remap()` (faster for real-time)

Use when:

* Video / webcam streaming
* Real-time applications

Why faster?

Because you compute the remap once:

* `cv2.initUndistortRectifyMap(...)`

Then for every frame you do:

* `cv2.remap(frame, mapx, mapy, ...)`

So you avoid recomputing the math each frame.

Key takeaway from video:

* `remap()` is faster than `undistort()` for real-time use.

---

## How to Use These Files in Your Own App

Typical flow:

1. Load pickles
2. Apply undistortion to every frame
3. Continue with your pipeline (pose estimation, detection, measurement)

This becomes mandatory if you want stable 6D pose work (ArUco / solvePnP).

---

## What “Total Error” Means

The script prints a total reprojection error.

Interpretation:

* Lower error = better calibration
* High error usually means:

  * Too few images
  * Not enough angle variety
  * Blurry images
  * Chessboard partially out of frame

---

## Quick Quality Checklist

If calibration looks bad:

* Capture more images
* More extreme angles (tilt/rotate)
* Cover corners of the image frame (not only center)
* Remove blurry images
* Ensure full chessboard visible

---

## Why This Matters (Connection to Your Other Notes)

Camera calibration is a dependency for:

* ArUco pose estimation (rvec/tvec)
* solvePnP
* Stereo depth
* 3D object detection metrics
* Any measurement you want in real-world units

If calibration is wrong, pose estimation looks “jittery” or wrong scale.

---