# Camera Calibration with ChArUco Boards (OpenCV)

Video: *How to calibrate a camera using ChArUco boards*
https://youtu.be/EUvco3rjUdQ?si=f92x9E5rnwwZgZtH
---

# 1. What is Camera Calibration?

**Camera calibration** is the process of estimating the real parameters of a camera.

It allows us to:

* Correct **lens distortion**
* Compute **intrinsic parameters**
* Compute **extrinsic parameters**
* Improve accuracy in computer vision algorithms

A common issue without calibration:

* Straight lines appear **curved**, especially near image boundaries.

This happens often with:

* wide-angle lenses
* fisheye lenses.

---

# 2. Why Calibration is Important

Even if you have **multiple identical cameras**, they are never perfectly identical.

Each camera will have small variations in:

* lens alignment
* sensor placement
* distortion

Therefore:

> Each camera should be calibrated individually.

Calibration allows us to estimate:

* intrinsic parameters
* distortion coefficients
* camera pose relative to objects.

---

# 3. Camera Calibration Pipeline

Typical workflow:

```
Capture calibration images
        ↓
Detect board pattern
        ↓
Estimate camera parameters
        ↓
Save calibration results
        ↓
Use parameters in CV applications
```

This calibration only needs to be done **once per camera**.

---

# 4. Capturing Calibration Images

A **calibration board** is required.

In this tutorial a **ChArUco board** is used.

ChArUco boards combine:

* **ArUco markers**
* **checkerboard patterns**

Advantages:

* more robust detection
* higher precision
* unique marker identification

---

## Capturing frames with Python

Open a camera stream:

```python
cap = cv2.VideoCapture(0)
```

Read frames:

```python
ret, frame = cap.read()
```

Save images when pressing **S**:

```python
cv2.imwrite("output/frame.jpg", frame)
```

Controls:

* **S** → save frame
* **ESC** → exit program

Images are stored in an **output directory**.

---

# 5. How Many Images Are Needed

Recommended:

```
10 – 20 images
```

Important guidelines:

* move the board across the image
* change orientation
* vary distance
* cover different regions of the frame

The board should cover **roughly half of the image area**.

---

# 6. Uploading Images to Calibration Software

After capturing images:

1. Upload them to the calibration software.
2. The software detects ChArUco markers automatically.
3. It estimates camera parameters.

This process usually takes only a few seconds.

---

# 7. Board Parameters

The calibration software needs the board specifications.

Example parameters:

```
Columns: 18
Rows: 11
Square size
Marker size
Dictionary: 4x4_100
```

Explanation:

* The dictionary defines the marker family.
* Each marker has a **unique ID**.

Example:

```
ArUco marker IDs: 0,1,2,3,...
```

Unique IDs help detect the board reliably.

---

# 8. Calibration Results

The software generates a **JSON file** containing calibration data.

Main outputs:

### Intrinsic Parameters

Camera matrix:

```
[ fx  0  cx ]
[ 0  fy  cy ]
[ 0   0   1 ]
```

Where:

* `fx`, `fy` → focal length
* `cx`, `cy` → optical center

---

### Distortion Coefficients

Used to correct lens distortion.

Typical distortions:

* **Barrel distortion**
* **Pincushion distortion**

---

### Rotation and Translation Vectors

These describe:

* orientation of the calibration board
* position relative to the camera

Used for:

* pose estimation
* 3D reconstruction.

---

# 9. Reprojection Error

One of the most important metrics.

**Reprojection error** measures calibration accuracy.

Goal:

```
As close to 0 as possible
```

Typical good values:

```
< 0.2
```

If an image produces high error:

* remove it
* recalibrate.

Outliers can degrade results.

---

# 10. 3D Visualization

The calibration tool can display:

* camera position
* board poses
* spatial relationship between them

This helps verify that:

* boards are captured from multiple orientations.

---

# 11. Using Calibration Data in OpenCV

Load the JSON calibration data.

Extract:

* camera matrix
* distortion coefficients

These are used for **image undistortion**.

---

# 12. Correcting Image Distortion

Open an image:

```python
img = cv2.imread("image.jpg")
```

Compute optimal camera matrix:

```python
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(...)
```

Undistort the image:

```python
undistorted = cv2.undistort(img, camera_matrix, dist_coeffs)
```

---

# 13. Cropping After Undistortion

After distortion correction:

* some regions become invalid
* the image may be slightly cropped

The **ROI (Region of Interest)** defines the usable region.

---

# 14. Visual Difference

Without calibration:

* edges bend
* geometry is distorted

After calibration:

* straight lines become straight
* geometry is corrected

This effect is especially visible in:

* fisheye lenses
* wide field-of-view cameras.

---

# 15. Applications of Camera Calibration

Calibration is fundamental for many computer vision tasks:

* robotics
* SLAM
* augmented reality
* stereo vision
* pose estimation
* 3D reconstruction
* object localization

Without calibration:

> geometric measurements in images become unreliable.

---

# Key Idea

Camera calibration converts:

```
Distorted image measurements
```

into

```
A geometric model of the camera
```

This enables **accurate spatial reasoning in computer vision systems**.

---

If you want bro, the **next concept that usually comes right after this** (and many CV tutorials assume you know it) is:

* **Pinhole Camera Model**
* **Camera Matrix math**
* **Homography**
* **3D pose estimation**

These are the **core geometry concepts of computer vision**. I can make you a super clear note for that too.
