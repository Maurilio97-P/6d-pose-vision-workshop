# Stereo Vision Camera Calibration with OpenCV (Python)

Source: *Stereo Vision Camera Calibration with OpenCV: How to Calibrate your Camera with Python Script*
YouTube: [https://www.youtube.com/watch?v=yKypaVl6qQo](https://www.youtube.com/watch?v=yKypaVl6qQo)
Transcript: 

---

## Goal

Calibrate a stereo setup (Left camera + Right camera) so we can:

* Undistort both images
* Rectify both images (align epipolar lines)
* Save stereo maps
* Use the rectified pair for depth/disparity later

Key idea:
You calibrate each camera first, then combine them into stereo calibration for best results. 

---

## Big Picture Pipeline

1. Capture calibration images (left + right) with chessboard
2. Calibrate Left camera (intrinsics + distortion)
3. Calibrate Right camera (intrinsics + distortion)
4. Stereo calibrate (R, T between cameras)
5. Stereo rectify (compute rectification transforms + projection matrices + Q)
6. Build undistort/rectify maps
7. Save maps to XML
8. Load maps in your real application and `remap()` both streams

---

## Why Rectification Matters

Even if cameras aren’t perfectly aligned physically, rectification makes them aligned in software. 

After rectification:

* Corresponding points are on the same horizontal line
* Only disparity in X matters
* Depth becomes easier and more accurate

---

## Step 1 - Capture Calibration Images

Use a script that:

* Opens two webcams (`cap` and `cap2`)
* Shows both frames
* When you press **S**, it saves images to:

  * `images/stereoLeft/`
  * `images/stereoRight/`
* When you press **Q** or **ESC**, it exits

You only need around **3 to 6 image pairs** with chessboard at different angles and positions. 

Tips from the video:

* Rotate, tilt, translate the chessboard
* Cover different parts of image
* Slight misalignment is OK because rectification fixes it later 

---

## Step 2 - Prepare Calibration Variables

### Chessboard size

Inner corners:

* `9 x 6` in the example 

### Frame size

Example:

* `640 x 480` 

### Object points (3D world points)

This is the chessboard grid in 3D, usually on plane Z=0.

Important detail:
If you know the real square size, multiply by it to improve accuracy.

Example in video:

* 2 cm squares
* multiply by 20 (mm) 

So object points become real-world scaled.

---

## Step 3 - Find Chessboard Corners for Each Camera

For each image:

1. Read image
2. Convert to grayscale
3. Find corners with:

* `cv2.findChessboardCorners(gray, chessboardSize)`

4. Refine corners with:

* `cv2.cornerSubPix(...)`

5. Store:

* object points (same for left/right)
* image points (separate for left and right)

Also draw corners on the image to visually confirm detection. 

---

## Step 4 - Calibrate Each Camera Individually

Use OpenCV:

* `cv2.calibrateCamera(objectPoints, imagePoints, frameSize, ...)`

Returns (per camera):

* camera matrix (intrinsics)
* distortion coefficients
* rvecs
* tvecs

Then compute:

* `cv2.getOptimalNewCameraMatrix(...)`

This gives an improved matrix for undistortion. 

---

## Step 5 - Stereo Calibration (Combine Both Cameras)

Use:

* `cv2.stereoCalibrate(...)`

In the video:
They use the flag:

* `CALIB_FIX_INTRINSIC`

Meaning:
Intrinsics and distortion are fixed, and the method estimates only:

* Rotation (R)
* Translation (T)
* Essential matrix (E)
* Fundamental matrix (F) 

Why do this?
Because you already calibrated each camera individually.

---

## Step 6 - Stereo Rectification

Use:

* `cv2.stereoRectify(...)`

This computes:

* Rectification transforms for left and right
* Projection matrices for left and right
* Q matrix (used later for depth reconstruction)
* ROI regions

This is what aligns both images. 

---

## Step 7 - Build Undistort + Rectify Maps

Use:

* `cv2.initUndistortRectifyMap(...)`

This creates mapping arrays (per camera):

* `stereoMapL_x`, `stereoMapL_y`
* `stereoMapR_x`, `stereoMapR_y`

These maps describe how to warp each frame so it becomes:

* undistorted
* rectified 

---

## Step 8 - Save Maps to File (XML)

Save maps once:

* `stereoMap.xml`

Write:

* left x/y maps
* right x/y maps 

Important:
You only need to calibrate once (unless camera positions change).

---

## Step 9 - Load Maps in Your Actual Stereo App

In the stereo vision application:

1. Load `stereoMap.xml`
2. Open both cameras again
3. For every frame pair, apply:

* `cv2.remap(frameLeft, stereoMapL_x, stereoMapL_y, ...)`
* `cv2.remap(frameRight, stereoMapR_x, stereoMapR_y, ...)`

Now both frames are rectified and ready for:

* disparity computation
* depth estimation
* tracking

The rectified image may look “cropped” or “weird” at edges because rectification warps the image. 

---

## Key Takeaways

* Calibrate left and right cameras individually first (better results)
* Stereo calibration gives you R, T between cameras
* Rectification aligns the image pair to make disparity valid
* Save rectification maps to XML
* Use `remap()` every frame for real-time rectified stereo stream
* After this, you can compute depth reliably

---

## next, investigate

* Disparity concept
* Block matching (StereoBM/StereoSGBM)
* Depth formula using baseline and focal length
* How Q matrix fits in