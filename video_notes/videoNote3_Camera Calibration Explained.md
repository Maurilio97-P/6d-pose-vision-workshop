## Camera Calibration - Step-by-Step Guide (OpenCV Python)

Source: *Camera Calibration Explained and SIMPLE Step-by-Step Guide!*
YouTube: [https://www.youtube.com/watch?v=Wcnb197g2i0](https://www.youtube.com/watch?v=Wcnb197g2i0)

---

## What Is Camera Calibration?

Camera calibration is the process of:

* Taking chessboard images
* Feeding them into a calibration program
* Computing camera parameters

Output parameters:

* Intrinsics
* Extrinsics
* Distortion coefficients
* Reprojection error

You can then use these parameters to:

* Remove lens distortion
* Perform accurate measurements
* Enable pose estimation
* Improve AR overlays
* Do robotics localization

---

## Coordinate Frames Explained

There are three main frames:

### 1) World Frame

Where the object exists in 3D space.

### 2) Camera Frame

The camera’s 3D coordinate system.

### 3) Image Frame

2D pixel coordinates.

---

## Transformations Between Frames

### World → Camera

This uses **Extrinsics**:

* Rotation (R)
* Translation (t)

Describes:

* Where the camera is
* How it is oriented

---

### Camera → Image

This uses **Intrinsics**:

* Focal length (fx, fy)
* Principal point (cx, cy)

Describes:

* How 3D rays map to pixel coordinates

---

## Mathematical Relationship

We relate world points to image points using:

```id="cal1"
ImagePoint = K [R | t] WorldPoint
```

Where:

* K = Intrinsic matrix
* R, t = Extrinsics

---

## Camera Intrinsics

Intrinsic matrix K:

```id="cal2"
[ fx  0  cx ]
[  0 fy  cy ]
[  0  0   1 ]
```

* fx, fy → focal lengths
* cx, cy → optical center (principal point)

---

## Lens Distortion

Real cameras are NOT perfect.

Two main distortion types:

---

### 1) Radial Distortion (K values)

Causes:

* Barrel distortion (bulges outward)
* Pincushion distortion (curves inward)

Coefficients:

* k1
* k2
* k3

These affect image points radially from center.

---

### 2) Tangential Distortion (P values)

Caused by:

* Lens misalignment
* Sensor tilt

Coefficients:

* p1
* p2

This shifts x and y positions unevenly.

---

## Distortion Coefficients Vector

OpenCV format:

```id="cal3"
[k1, k2, p1, p2, k3]
```

* k’s → radial
* p’s → tangential

---

## Step-by-Step Calibration Process

---

### Step 1: Download Calibration App

Inside project folder:

```
main_folder/
    camera_calibration/
        calibration.py
        chessboard_9x6.png
        demo_images/
```

---

### Step 2: Prepare Chessboard Pattern

Default used:

* 9x6 inner corners

Important:

* If you change size, update code accordingly.

You can:

* Print the chessboard
* Or display on phone

---

### Step 3: Capture Calibration Images

Take many images of chessboard:

Good practices:

* Different angles
* Different distances
* Different parts of the frame
* Cover corners and edges of image
* Avoid blur

Goal:
Maximize geometric diversity.

---

### Step 4: Install Required Python Modules

Used:

* Python 3.11
* numpy
* opencv-python
* matplotlib

Install with:

```id="cal4"
pip install numpy opencv-python matplotlib
```

---

### Step 5: Run Calibration Script

Run:

```id="cal5"
python calibration.py
```

The program:

1. Loads all calibration images
2. Detects chessboard corners
3. Refines corners
4. Solves for camera parameters
5. Displays results
6. Saves JSON output

---

## What the Script Outputs

Inside `calibration.json`:

* Reprojection error
* Camera matrix
* Distortion coefficients
* rvecs
* tvecs

---

## Reprojection Error

What is it?

Difference between:

* Detected image points
* Reprojected 3D points

Lower is better.

Typical good values:

* < 0.5 → Excellent
* < 1.0 → Good
* > 2.0 → Poor

---

## How to Improve Calibration Results

If reprojection error is high:

### 1) Take More Images

More data → better estimation.

---

### 2) Vary Orientation

Don’t just take flat images.

Include:

* Tilted views
* Rotated views
* Close & far

---

### 3) Cover Entire Frame

Make sure chessboard appears in:

* Center
* Corners
* Edges

This improves distortion modeling.

---

### 4) Remove Bad Images

Delete:

* Blurry images
* Cut-off chessboards
* Overexposed images

Garbage in → garbage out.

---

## Why Calibration Is Critical

Without calibration:

* Pose estimation fails
* AR overlays drift
* Measurements are inaccurate
* solvePnP becomes unreliable

Calibration is foundational for:

* Drone vision
* Robotics perception
* SLAM systems
* Industrial measurement

---

## Full Calibration Pipeline Summary

1. Print chessboard
2. Capture multiple images
3. Detect corners
4. Refine corners
5. Solve for intrinsics & distortion
6. Save parameters
7. Use for:

   * Undistortion
   * Pose estimation
   * AR

---

## Big Picture Intuition

Calibration tells the camera:

> “This is how you see the world.”

Once calibrated:

* You can remove distortion
* You can measure real-world distances
* You can compute object pose correctly

It is the foundation of all geometric computer vision.

---

## next:

* try to understand how this concepts connect with each other:

  * Calibration
  * solvePnP
  * ArUco
  * Full robotics vision pipeline

Or we can go full math mode and derive distortion equations 👀
