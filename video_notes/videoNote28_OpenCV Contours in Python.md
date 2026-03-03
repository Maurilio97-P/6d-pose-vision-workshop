# OpenCV Contours in Python — Complete Notes

Video: *Contornos de Python de OpenCV*
https://youtu.be/LMamYJYnws8?si=1Nte9fIJVqzmYaJj

---

# 1️⃣ What Are Contours?

A contour is:

> A piecewise collection of line segments or curves that describe the outline of an object.

In simple terms:

* A contour traces the boundary of a shape.
* It follows connected pixel regions.
* It closes the loop around an object.

Think of it as:

> Border-following around a region of interest.

---

# 2️⃣ Why Do We Need Contours?

Contours are used for:

* Object detection
* Segmentation
* Shape analysis
* Measuring object properties
* Region extraction

They help us describe and analyze objects in an image.

---

# 3️⃣ How Contours Work

The idea is:

1. Detect a region of connected pixels.
2. Follow the boundary.
3. Close the loop.
4. Store that boundary as a contour.

You repeat this for all regions in the image.

OpenCV handles this using:

```python
cv2.findContours()
```

---

# 4️⃣ Basic Setup in Python

Imports:

```python id="zskp1f"
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
```

---

# 5️⃣ Reading the Image (Grayscale)

```python id="k9aj8e"
image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
```

Contours usually work best on:

> Binary or grayscale images.

---

# 6️⃣ Preprocessing Before Finding Contours

## Step 1 — Thresholding

Convert to binary image:

```python id="k0s7ud"
_, thresh = cv.threshold(image, 65, 255, cv.THRESH_BINARY)
```

---

## Step 2 — Dilation (Optional)

Helps emphasize boundaries:

```python id="a2n7ft"
kernel = np.ones((7,7), np.uint8)
thresh = cv.dilate(thresh, kernel)
```

---

# 7️⃣ Finding Contours

```python id="h7pz0o"
contours, hierarchy = cv.findContours(
    thresh,
    cv.RETR_TREE,
    cv.CHAIN_APPROX_SIMPLE
)
```

### Parameters:

### Retrieval mode:

* `cv.RETR_TREE`

  * Retrieves all contours.
  * Preserves hierarchy (contours inside contours).

### Approximation mode:

* `cv.CHAIN_APPROX_SIMPLE`

  * Stores only essential contour points.
  * Compresses horizontal/vertical segments.

---

# 8️⃣ Drawing Contours

```python id="f7x4eo"
cv.drawContours(image, contours, -1, (0,0,255), 3)
```

Arguments:

* `-1` → draw all contours
* `(0,0,255)` → red color
* `3` → thickness

---

# 9️⃣ Important Contour Properties

---

## 🔹 1. Center of Mass (Centroid)

Using moments:

```python id="3kt1ru"
M = cv.moments(contours[0])
cx = int(M["m10"] / M["m00"])
cy = int(M["m01"] / M["m00"])
```

This gives:

> The centroid of the contour.

---

## 🔹 2. Area

```python id="fktz5a"
area = cv.contourArea(contours[0])
```

---

## 🔹 3. Perimeter

```python id="7xq93v"
perimeter = cv.arcLength(contours[0], True)
```

`True` means the contour is closed.

---

# 🔟 Contour Approximation

Used to simplify contour shape.

### Define epsilon:

```python id="39t2qg"
epsilon = 0.02 * perimeter
```

### Approximate:

```python id="ghp3s8"
approx = cv.approxPolyDP(contours[0], epsilon, True)
```

This reduces:

> Number of points describing the shape.

Useful for:

* Shape detection
* Polygon detection

---

# 1️⃣1️⃣ Convex Hull

Convex hull is:

> The smallest convex shape that encloses the contour.

```python id="2kvazl"
hull = cv.convexHull(contours[0])
```

It removes inward dents.

Useful for:

* Shape analysis
* Solidity calculation

---

# 1️⃣2️⃣ Bounding Rectangle

Get rectangle around object:

```python id="7a0nwp"
x, y, w, h = cv.boundingRect(contours[0])
```

Draw it:

```python id="d3k6nz"
cv.rectangle(image, (x,y), (x+w, y+h), (255,255,255), 2)
```

Useful for:

* Object localization
* Cropping

---

# 1️⃣3️⃣ Additional Contour Features

---

## 🔹 Aspect Ratio

```python id="rth79k"
aspect_ratio = w / h
```

---

## 🔹 Extent

How much of bounding box is filled:

```python id="j3ax7k"
extent = area / (w * h)
```

---

## 🔹 Solidity

How filled the shape is:

```python id="cnbxw1"
solidity = area / cv.contourArea(hull)
```

---

## 🔹 Equivalent Diameter

Diameter of circle with same area:

```python id="m7ev3k"
equivalent_diameter = np.sqrt(4 * area / np.pi)
```

---

## 🔹 Fit Ellipse

Useful for orientation:

```python id="o7qfnt"
ellipse = cv.fitEllipse(contours[0])
```

This gives:

* Center
* Major axis
* Minor axis
* Rotation angle

Useful for:

* Object alignment
* Angle detection

---

# 1️⃣4️⃣ Mental Model

```text
Binary Image
      ↓
Find Contours
      ↓
Extract shape properties
      ↓
Analyze object
```

Contours transform:

> Pixels → Geometric shape representation

---

# 🚀 Why This Is Powerful

Contours allow you to:

* Detect shapes
* Measure objects
* Compute orientation
* Identify defects
* Perform segmentation
* Build object detection pipelines

Contours are foundational in:

* Industrial inspection
* Robotics
* Medical imaging
* Autonomous systems
* Classic computer vision

---

# 🧠 Big Picture

Image Processing → Prepare image
Contours → Extract shape
Computer Vision → Interpret shape

---

## next level 

We can now:
* Build a full contour detection mini-project
* Detect specific shapes (triangle, square, circle)
* Combine contours with thresholding and morphology
* Or connect contours to object detection pipelines
