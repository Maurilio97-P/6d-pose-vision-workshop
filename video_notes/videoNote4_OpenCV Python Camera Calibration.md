## OpenCV Python Camera Calibration (Intrinsic, Extrinsic, Distortion)

Source: *OpenCV Python Camera Calibration (Intrinsic, Extrinsic, Distortion)*
YouTube: [https://www.youtube.com/watch?v=H5qbRTikxI4](https://www.youtube.com/watch?v=H5qbRTikxI4)

Transcript reference: 

---

## What Is Camera Calibration?

Camera calibration is the process of estimating:

* Intrinsic parameters
* Extrinsic parameters
* Distortion coefficients

So that we can:

* Correct image distortion
* Perform accurate pose estimation
* Enable AR / SLAM
* Do 3D reconstruction
* Measure real-world distances

---

## Camera Model Overview

We have:

* World point → 3D space
* Camera center
* Image plane → 2D pixels

The goal:

Project a 3D world point correctly onto the image plane.

---

## Projection Equation

Core equation:

```
x = P X
```

Where:

* X → world point (X, Y, Z, 1)
* x → image point (u, v)
* P → projection matrix (3×4)

---

## Decomposing the Projection Matrix

The projection matrix P can be split into:

```
P = K [R | t]
```

Where:

### K → Intrinsics (3×3)

Contains:

* fx, fy → focal length
* cx, cy → principal point (image center)

---

### [R | t] → Extrinsics

* R → rotation (3×3 matrix)
* t → translation (3×1 vector)

In OpenCV:

* rvec → 3×1 (Rodrigues rotation vector)
* tvec → 3×1

---

## Intrinsic Parameters

Intrinsic matrix:

```
[ fx  0  cx ]
[  0 fy  cy ]
[  0  0   1 ]
```

* fx, fy → scaling factors in pixels
* cx, cy → optical center

---

## Distortion Parameters

Real lenses distort images.

OpenCV uses:

```
[k1, k2, p1, p2, k3]
```

### Radial Distortion (k1, k2, k3)

Causes:

* Barrel distortion
* Pincushion distortion

Image curves outward or inward.

---

### Tangential Distortion (p1, p2)

Caused by:

* Lens misalignment
* Sensor tilt

Shifts pixel coordinates unevenly.

---

## Why We Need Calibration

Without calibration:

* Images are geometrically incorrect
* Pose estimation becomes inaccurate
* AR overlays drift
* SLAM fails

Calibration gives us:

* Accurate geometry
* Undistorted images
* Reliable 3D reconstruction

---

## How Calibration Works (Algorithm Intuition)

Step 1:
Take multiple chessboard images.

Step 2:
Detect inner chessboard corners.

Step 3:
Associate:

* Known world coordinates
* Detected image coordinates

Step 4:
Solve a system of equations:

```
A x = 0
```

Step 5:
Compute:

* Camera matrix
* Distortion coefficients
* rvecs
* tvecs

This is essentially solving for the projection matrix parameters.

---

## Important Assumption

For chessboard calibration:

We assume:

```
Z = 0
```

Because the chessboard lies on a plane.

This simplifies the system significantly.

---

## Coding Pipeline Overview

---

### 1) Import Modules

* numpy
* cv2
* etc.

---

### 2) Define Chessboard Size

Very important:

Number of INNER corners only.

Example:

```
rows = 6
cols = 9
```

Miscounting corners = calibration failure.

---

### 3) Set Termination Criteria

Used in `cornerSubPix()`:

Criteria includes:

* Max iterations
* Error tolerance

---

### 4) Generate World Points

Create placeholder 3D coordinates:

```
(0,0,0)
(1,0,0)
(2,0,0)
...
```

These are ideal chessboard coordinates.

---

### 5) Detect Chessboard Corners

For each image:

1. Convert to grayscale
2. Use:

```
cv2.findChessboardCorners()
```

Returns:

* Success flag
* Corners array

---

### 6) Refine Corners

Use:

```
cv2.cornerSubPix()
```

This improves corner accuracy to subpixel level.

Very important for precision.

---

### 7) Calibrate Camera

Call:

```
cv2.calibrateCamera()
```

Inputs:

* objectPoints (world)
* imagePoints (image)
* image size

Returns:

* reprojection error
* camera matrix
* distortion coefficients
* rvecs
* tvecs

---

## Reprojection Error

Definition:

Difference between:

* Observed image points
* Reprojected points using estimated parameters

In the example:

Reprojection error ≈ 0.1687 pixels 

That is very good.

Lower is better.

---

## Calibration Best Practices

From transcript + practical advice :

* Use at least 10 images
* Vary orientation (tilt, rotate)
* Use different depths
* Avoid blurry images
* Ensure full chessboard visible
* Avoid all images in same plane (degenerate case)

Degenerate case:
If all views are nearly identical → solver struggles.

---

## Removing Distortion

After calibration:

Use:

```
cv2.getOptimalNewCameraMatrix()
```

Alpha parameter:

* 0 → crop to valid region only
* 1 → retain all pixels (may include black borders)

---

Then:

```
cv2.undistort()
```

Inputs:

* image
* camera matrix
* distortion coefficients

Output:

* undistorted image

---

## Visual Validation

In the example:

* Straight lines appear slightly curved
* After undistortion → straight edges align correctly

Even subtle distortion becomes visible when drawing straight lines.

---

## Full Calibration + Undistortion Pipeline

1. Capture chessboard images
2. Detect inner corners
3. Refine corners
4. Solve calibration
5. Save parameters
6. Load parameters later
7. Undistort new images
8. Use for pose estimation / AR

---

## Big Picture Vision Pipeline

Calibration → Undistortion → Pose Estimation → AR / Robotics

Without calibration:

Everything downstream becomes unreliable.

---

## next:

try to understand how everything connects:

* Calibration
* Distortion
* solvePnP
* ArUco
* Full 3D vision stack

Basically this is an entire computer vision robotics pipeline, think of its architecture 