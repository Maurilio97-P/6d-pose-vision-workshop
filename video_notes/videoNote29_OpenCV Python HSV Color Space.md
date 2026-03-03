# OpenCV Python — HSV Color Space (Complete Notes)

Video: *OpenCV Python HSV Color Space*
YouTube: [https://www.youtube.com/watch?v=G3PW5ysKDxc](https://www.youtube.com/watch?v=G3PW5ysKDxc)

---

# 1️⃣ What Is HSV?

HSV stands for:

* **H** → Hue
* **S** → Saturation
* **V** → Value

It is a different way of representing color compared to RGB.

---

# 2️⃣ Understanding HSV Intuitively

Think of HSV as a cone.

## 🎨 Hue (H)

* Represents the **type of color**
* Measured around a circle
* In OpenCV: **0 to 180**
* In theory: **0 to 360 degrees**

OpenCV divides hue by 2 (so 360 → 180).

Hue is the **angle** around the color wheel.

Examples:

* 0 → Red
* 60 → Yellow
* 120 → Green
* 240 → Blue

---

## 🌊 Saturation (S)

* Represents **color intensity**
* Radius of the cone
* Range: 0 to 255

Low saturation → washed out (grayish)
High saturation → vivid color

You can think of it as:

> Adding water to paint (more water = lower saturation)

---

## 💡 Value (V)

* Represents **brightness**
* Vertical axis of the cone
* Range: 0 to 255

Low value → dark
High value → bright

Value = intensity of light.

---

# 3️⃣ Why Use HSV Instead of RGB?

RGB:

* Hard to interpret numerically.
* Lighting changes affect all three channels.

HSV:

* More intuitive.
* Separates color from brightness.
* Better for segmentation under different lighting.

Main advantage:

> Easier color-based segmentation.

---

# 4️⃣ HSV Conversion in OpenCV

OpenCV loads images in BGR.

To convert:

```python
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
```

The result:

* Same image size
* 3 channels
* But now channels are:

  * H
  * S
  * V

---

# 5️⃣ HSV Segmentation Concept

Color segmentation means:

> Extract pixels that fall inside a specific HSV range.

We define:

* Lower bound
* Upper bound

Then create a mask.

---

# 6️⃣ Defining HSV Bounds

Example:

```python
lower = np.array([h_min, s_min, v_min])
upper = np.array([h_max, s_max, v_max])
```

Important:

Hue in OpenCV → 0 to 180
So if you want 0–20 degrees:

You must divide by 2.

Example:

```python
lower = np.array([0, 50, 50])
upper = np.array([10, 120, 100])
```

---

# 7️⃣ Creating the Mask

```python
mask = cv.inRange(hsv, lower, upper)
```

What this does:

For each pixel:

If:

```text
lower <= pixel <= upper
```

Then:

* Output pixel = 255 (white)

Else:

* Output pixel = 0 (black)

Result:

Binary mask image.

---

# 8️⃣ Visualizing the Mask

```python
cv.imshow("Mask", mask)
cv.waitKey(0)
```

White areas = detected region
Black areas = ignored region

---

# 9️⃣ Real Example: Cat Ear Segmentation

Goal:

Extract pinkish ear region.

Steps:

1. Convert to HSV
2. Inspect HSV values
3. Choose hue range around pink
4. Choose moderate saturation
5. Choose value range to avoid dark fur
6. Apply mask

Tuning V (value) is important because:

* Too low → includes dark fur
* Too high → may exclude shadowed areas

HSV helps isolate color even with lighting variations.

---

# 🔟 Understanding the HSV Algorithm

HSV is computed from RGB by:

1. Normalize RGB
2. Compute:

   * Cmax = max(R,G,B)
   * Cmin = min(R,G,B)
   * Delta = Cmax - Cmin

Hue depends on which channel is max:

* If R is max → use formula 1
* If G is max → use formula 2
* If B is max → use formula 3

Saturation:

```text
S = Delta / Cmax
```

Value:

```text
V = Cmax
```

---

# 1️⃣1️⃣ Why HSV Works Better for Segmentation

RGB mixes:

* Color
* Brightness
* Lighting

HSV separates:

* Hue → actual color
* Saturation → purity
* Value → brightness

So we can:

* Ignore brightness variations
* Focus only on color

That’s powerful for:

* Object detection
* Skin detection
* Fruit detection
* Robotics color tracking

---

# 1️⃣2️⃣ Mental Model

```text
RGB = How much red, green, blue light?
HSV = What color? How intense? How bright?
```

HSV is closer to human perception.

---

# 1️⃣3️⃣ Practical Tips

✔ Always convert BGR → HSV
✔ Use a color picker tool to inspect values
✔ Remember Hue range is 0–180 in OpenCV
✔ Tune saturation and value to avoid noise
✔ Use dilation/erosion after mask to clean results

---

# 1️⃣4️⃣ Big Picture

HSV segmentation pipeline:

```text
Image (BGR)
    ↓
Convert to HSV
    ↓
Define color range
    ↓
cv.inRange()
    ↓
Binary mask
    ↓
Extract object
```

This is foundational for:

* Color tracking
* Real-time object detection
* Robotics vision
* Industrial sorting

---

# 🚀 Where This Connects

HSV segmentation is:

Image Processing → thresholding
Contours → extract shapes
Computer Vision → interpret shapes

It’s one of the most common classical CV pipelines.

---

## next level

We can now:
* Combine HSV + contours
* Build real-time color tracking
* Detect multiple colors
* Connect HSV segmentation to object detection
