# NumPy for Images

Video: *Python Tutorial: NumPy for images*
YouTube: [https://www.youtube.com/watch?v=7V909wyeOQY](https://www.youtube.com/watch?v=7V909wyeOQY)

---

# 1️⃣ Images Are NumPy Arrays

When you load an image using something like:

```python
plt.imread("image.jpg")
```

The result is:

> A NumPy ndarray

Images are represented as **multi-dimensional NumPy arrays**.

That means all NumPy operations work directly on images.

---

# 2️⃣ How Images Are Represented

A color image has:

* Height (rows)
* Width (columns)
* Color channels (RGB)

So its shape looks like:

```python
(height, width, 3)
```

Example from the video:

```
(426, 640, 3)
```

Meaning:

* 426 pixels high
* 640 pixels wide
* 3 color channels (Red, Green, Blue)

Total pixels:

```
426 × 640 = 170,920 pixels
```

---

# 3️⃣ Accessing Color Channels (Slicing)

Since images are NumPy arrays, you can slice them.

To get the **red channel**:

```python
red = image[:, :, 0]
```

* `:` → keep all rows
* `:` → keep all columns
* `0` → select red layer

Similarly:

```python
green = image[:, :, 1]
blue = image[:, :, 2]
```

Each channel contains intensity values.

---

# 4️⃣ Displaying Channels

You can display channels using Matplotlib:

```python
plt.imshow(red, cmap="gray")
```

Using different color maps lets you visualize:

* Intensity distribution
* Bright vs dark regions

Each channel has its own intensity distribution.

---

# 5️⃣ Getting Image Shape

Just like any NumPy array:

```python
image.shape
```

Returns:

```
(height, width, channels)
```

This is extremely important in:

* Computer Vision
* Image preprocessing
* Neural networks

---

# 6️⃣ Flipping Images

NumPy provides simple methods for flipping.

### Flip vertically:

```python
np.flipud(image)
```

### Flip horizontally:

```python
np.fliplr(image)
```

These operations manipulate the array structure directly.

---

# 7️⃣ Image Histogram

A histogram shows:

> How many pixels exist at each intensity value.

Pixel intensities range from:

```
0   → pure black  
255 → pure white
```

If an image is dark:

* Most pixel values are between 0–50

If an image is bright:

* Most pixel values are between 200–255

---

# 8️⃣ RGB Histograms

For color images:

Each channel has its own histogram:

* Red histogram
* Green histogram
* Blue histogram

This tells us:

* Color dominance
* Brightness distribution
* Contrast levels

---

# 9️⃣ Creating Histograms in Matplotlib

Steps:

### 1️⃣ Extract channel

```python
red = image[:, :, 0]
```

### 2️⃣ Flatten it

```python
red_flat = red.ravel()
```

Why flatten?

Because histogram expects a 1D array.

---

### 3️⃣ Plot histogram

```python
plt.hist(red_flat, bins=256)
```

Why 256 bins?

Because pixel values go from:

```
0 to 255 → 256 possible values
```

---

# 🔟 Why Histograms Matter

Histograms are used to:

* Analyze brightness
* Analyze contrast
* Equalize images
* Perform thresholding
* Detect features
* Preprocess images for ML

They are fundamental in **Computer Vision**.

---

# 🧠 Mental Model

An image is just:

> A 3D NumPy array

Operations like:

* Slicing
* Flipping
* Reshaping
* Histogram computation

Are simply NumPy operations.

---

# 🚀 Why This Is Important for You

If you’re going into:

* Computer Vision
* OpenCV
* Pose Estimation
* Deep Learning
* Image preprocessing

Then understanding:

> Images = NumPy arrays

Is absolutely foundational.

---

## next step 

We can go deeper into:

* How OpenCV stores images (BGR vs RGB)
* Converting color spaces
* Cropping using slicing
* Thresholding
* Image normalization for neural networks
* Broadcasting tricks for image manipulation
