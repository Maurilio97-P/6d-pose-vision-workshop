# ArUco Marker Detection in OpenCV (Real-Time) for AR Apps

Video: *Building an Augmented Reality Application with ArUco Marker Detection in OpenCV*
YouTube: [https://www.youtube.com/watch?v=UlM2bpqo_o0](https://www.youtube.com/watch?v=UlM2bpqo_o0)
Transcript: 

---

## Goal

Open a live webcam feed and:

* Detect ArUco markers
* Draw a bounding box around each marker
* Compute and draw the marker center
* Print/show the marker **ID**

This is the base step before pose estimation (drawing axes / coordinate frames) in the next video. 

---

## Core Idea

OpenCV’s ArUco pipeline:

1. Choose the correct dictionary type (4x4, 5x5, etc.)
2. Detect markers:

   * `corners`
   * `ids`
   * `rejected`

Then use `corners + ids` to visualize detections.

---

# Main Components

## 1) Imports

Modules used:

* numpy
* time
* opencv (cv2)

---

## 2) Choose ArUco Dictionary Type

You must know the marker family you printed.

Examples:

* `DICT_4X4_*`
* `DICT_5X5_*`

If you use the wrong dictionary:

* No detection
* Or only partial detection

In the video:
Small calibration board uses **4x4** markers, and the larger board uses **5x5**, so they switch the dictionary type to match. 

---

## 3) Create the ArUco Dictionary + Detector Parameters

* Get dictionary:

  * `cv2.aruco.Dictionary_get(...)` (or equivalent API)
* Create parameters:

  * `cv2.aruco.DetectorParameters_create()` 

These parameters control detection behavior.

---

# Marker Detection Output

OpenCV returns:

* `corners` = list of corner points for each marker
* `ids` = ID per marker
* `rejected` = candidates that failed marker validation (useful for debugging)

Detection call in transcript:

* `cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)` 

---

# Display Function: Drawing Boxes + Centers + IDs

They use a helper function (conceptually called something like `aruco_display`) that takes:

* corners
* ids
* rejected
* image

---

## Step A - Check if Any Markers Were Detected

If `len(corners) > 0`:

We have detections.

---

## Step B - Flatten IDs

`ids` is usually shaped like `[[1],[2],[3]]`

Flatten to:

`[1, 2, 3]`

This makes it easier to match IDs with corner arrays. 

---

## Step C - Loop Through Each Marker

They iterate using `zip(corners, ids)` to process:

* markerCorner
* markerID

---

## Step D - Extract the 4 Corner Points

Reshape corner array to 4x2:

Then label corners:

* top-left
* top-right
* bottom-right
* bottom-left 

Convert these to integers for drawing.

---

## Step E - Draw Bounding Box

Draw lines between corners:

* TL → TR
* TR → BR
* BR → BL
* BL → TL 

This creates the marker outline.

---

## Step F - Compute Marker Center

Center is computed using TL and BR:

```text id="c_center"
cX = (topLeft.x + bottomRight.x) / 2
cY = (topLeft.y + bottomRight.y) / 2
```

This gives the midpoint of the bounding box. 

---

## Step G - Draw ID Text

Use `cv2.putText(...)` near a corner (often top-left) to label the marker:

* Marker ID
* Helps confirm correct detection

---

# Webcam Setup

They open webcam and set resolution:

* 1280x720 (HD) 

Then run a loop:

1. Read frame
2. Resize frame for processing (they resized to a smaller size for speed)
3. Detect markers
4. Draw detections
5. Show image
6. Quit on `Q`

---

# Observations From Demo

* Very stable detection when markers are sharp and in focus
* Detection fails when:

  * Too far away (blur)
  * Wrong dictionary type
  * Marker too small / low resolution
* Bigger markers are easier to detect at distance
* The program correctly labels many markers with IDs (example IDs 1..34 on the calibration board) 

---

# Practical Debug Checklist

If detection fails:

1. Verify dictionary matches printed markers (4x4 vs 5x5) 
2. Improve focus / lighting
3. Increase marker size
4. Reduce motion blur
5. Check `rejected` markers output

---

# Why This Matters

Once detection works, the next step is pose estimation:

* Use corners + camera calibration (K, dist)
* Compute rvec/tvec
* Draw axes / coordinate frame
* Build AR overlays that stay locked to the marker

This is exactly what the next video promises to build on. 

---

## “next steps” for ArUco Pose Estimation

* estimatePoseSingleMarkers
* rvec/tvec
* drawAxis
* stable coordinate frames
* distance estimation (tvec.z)


