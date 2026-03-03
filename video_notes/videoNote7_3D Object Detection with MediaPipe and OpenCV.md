# 30+ FPS 3D Object Detection with MediaPipe (CPU-Based 6D Pose)

Source:
*30+ FPS 3D Object Detection with MediaPipe and OpenCV*
YouTube: [https://www.youtube.com/watch?v=f-Ibri14KMY](https://www.youtube.com/watch?v=f-Ibri14KMY)

Transcript reference: 

---

# What Is This Video About?

Real-time:

* 3D Object Detection
* 6D Pose Estimation
* 3D Bounding Box Drawing

Using:

* MediaPipe
* OpenCV
* CPU only (no GPU)

Performance:
~20–30 FPS on standard CPU 

---

# Terminology Clarification

From transcript + BOP definitions 

---

## 6D Pose Estimation

Find:

* Translation → (X, Y, Z)
* Rotation → orientation

So:

```text id="mp1"
Pose = [R | t]
```

---

## 3D Object Detection

Implies:

* 6D pose
* Plus 3D bounding box

---

## 6D Detection

Usually:

* RGB-D input
* Pose estimation

---

## 6D Localization

Usually:

* Known 3D model
* Estimate pose in scene

---

# MediaPipe Objectron

The model used:

MediaPipe **Objectron**

It can detect:

* Cup
* Shoe
* Other supported objects

Outputs:

* 2D landmarks
* 3D rotation
* 3D translation
* 3D bounding box

---

# Pipeline Overview

1. Capture frame from webcam (OpenCV)
2. Convert BGR → RGB
3. Pass frame to MediaPipe
4. Get 3D detection results
5. Draw:

   * 2D bounding box
   * 3D bounding box
   * Axis (rotation)
6. Compute FPS
7. Display frame

---

# Step-by-Step Code Structure

---

## 1) Imports

```python
import cv2
import mediapipe as mp
import time
```

OpenCV:

* Webcam capture
* Display image

MediaPipe:

* 3D object detection

Time:

* FPS calculation

---

## 2) Initialize Objectron

```python
mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils
```

---

## 3) Configure Objectron

Parameters:

* static_image_mode=False → video mode
* max_num_objects=2
* min_detection_confidence
* min_tracking_confidence
* model_name="Cup" or "Shoe"

These thresholds help:

* Reduce false positives
* Improve stability

If detection fails:
Lower confidence thresholds.

---

## 4) Open Webcam

```python
cap = cv2.VideoCapture(0)
```

---

## 5) Main Loop

```python
while cap.isOpened():
```

---

### Read Frame

```python
success, image = cap.read()
```

---

### Convert BGR → RGB

Important because:

OpenCV = BGR
MediaPipe = RGB

```python
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

---

### Disable Writing (Performance Boost)

```python
image.flags.writeable = False
```

This speeds up processing.

---

### Run Detection

```python
results = objectron.process(image)
```

Everything stored in:

```text
results.detected_objects
```

Contains:

* 2D landmarks
* rotation
* translation

---

### Re-enable Writing

```python
image.flags.writeable = True
```

---

### Convert Back to BGR

So OpenCV can display correctly.

---

# Drawing the 3D Bounding Box

If detections exist:

```python
if results.detected_objects:
```

Loop over detected objects.

---

## Draw 2D Landmarks

```python
mp_drawing.draw_landmarks(
    image,
    detected_object.landmarks_2d,
    mp_objectron.BOX_CONNECTIONS
)
```

This draws:

* 2D bounding box edges

---

## Draw 3D Axis

```python
mp_drawing.draw_axis(
    image,
    detected_object.rotation,
    detected_object.translation
)
```

Uses:

* rotation matrix
* translation vector

This gives:

* 3D coordinate system
* Proper orientation

---

# What Is Actually Being Estimated?

From MediaPipe:

* 3D bounding box corners
* Object rotation
* Object translation

So we get:

```text id="mp2"
R → rotation matrix
t → translation vector
```

Used to draw:

* 3D box
* Axes

---

# FPS Calculation

Measure:

```python
fps = 1 / total_time
```

Display on image.

Observed:

~20–30 FPS on CPU 

Very impressive for CPU.

---

# Demo Observations

Cup detection:

* Works well when handle visible
* Loses detection if handle blocked
* Rotates correctly with object

Shoe detection:

* Tracks orientation
* Some jitter
* Occasional tracking loss

Expected behavior:
Model trained on specific object types.

---

# Strengths

* Real-time on CPU
* No training required
* Easy to integrate
* Stable for supported objects

---

# Limitations

* Limited to supported object categories
* Not zero-shot
* Can lose tracking under occlusion
* Depends on object appearance

---

# Compared to Other Methods

| Method              | Training Required | Custom Objects | Real-Time CPU | Uses RGB-D |
| ------------------- | ----------------- | -------------- | ------------- | ---------- |
| solvePnP            | No                | Yes            | Yes           | Optional   |
| EfficientPose       | Yes               | Yes            | Maybe         | RGB        |
| FreeZe              | No                | Yes (CAD)      | Maybe         | RGB-D      |
| MediaPipe Objectron | Pretrained        | No             | Yes           | RGB        |

---

# When To Use MediaPipe Objectron

Use it when:

* You need quick prototype
* Objects are supported categories
* CPU-only system
* Real-time constraint
* AR demos
* Simple robotics

---

# Full Vision Stack Context

Calibration
→ Undistortion
→ 2D detection
→ 6D pose
→ 3D box drawing

MediaPipe compresses:

Detection + pose estimation
into one API call.

---

# Big Picture Insight

This is:

Pretrained deep learning

* Efficient mobile inference
* CPU-friendly pipeline

It bridges:

Academic 6D pose
and
Deployable real-time systems.

---

## next we can now:

* Compare MediaPipe vs FreeZe vs EfficientPose deeply
* build a unified “6D Pose Methods Master Map” note tying everything together
We are basically building a full 6D perception knowledge tree now 🌳
