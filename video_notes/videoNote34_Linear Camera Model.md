# Linear Camera Model — Forward Imaging Model (Camera Calibration)

Video: *Linear Camera Model | Camera Calibration*
https://youtu.be/qByYk6JggQU?si=Z2uoFb3W1kPyqtbb
---

# 1. Goal of the Camera Model

To **calibrate a camera**, we need a mathematical model that explains how a **3D point in the world becomes a 2D pixel in the image**.

This process is called the **Forward Imaging Model**.

```text
3D world point → camera coordinates → image projection → pixel coordinates
```

So the pipeline is:

```text
World Coordinates (3D)
        ↓
Camera Coordinates (3D)
        ↓
Perspective Projection
        ↓
Image Coordinates (2D)
        ↓
Pixel Coordinates (u,v)
```

---

# 2. Coordinate Systems

The model uses **two coordinate frames**.

## World Coordinate Frame

Denoted:

```
W
```

A 3D point in the world:

```
X_w = (X_w, Y_w, Z_w)
```

---

## Camera Coordinate Frame

Denoted:

```
C
```

The camera has its own coordinate system.

Important property:

```
Z-axis = optical axis of the camera
```

---

# 3. Camera Geometry

Key parameter:

**Focal length**

```
f
```

Distance between:

```
center of projection
and
image plane
```

---

# 4. Perspective Projection

Once a point is expressed in **camera coordinates**:

```
(Xc, Yc, Zc)
```

We can project it onto the image plane.

Perspective equations:

```
xi / f = Xc / Zc
yi / f = Yc / Zc
```

Rearranged:

```
xi = f * (Xc / Zc)
yi = f * (Yc / Zc)
```

Where:

```
(xi, yi)
```

are coordinates on the **image plane**.

---

# 5. Image Coordinates vs Pixel Coordinates

The projection gives coordinates in **millimeters**.

But cameras measure in **pixels**.

So we convert:

```
(xi, yi) → (u, v)
```

---

# 6. Pixel Density

Define:

```
mx = pixels per mm (x direction)
my = pixels per mm (y direction)
```

Then:

```
u = mx * xi
v = my * yi
```

This converts physical coordinates → pixel coordinates.

---

# 7. Principal Point

Previously we assumed:

```
image center = (0,0)
```

But this is **not true in practice**.

The origin of the pixel coordinate system is usually:

```
top-left corner of the image
```

The optical center location is unknown.

This is called the **principal point**.

```
(ox, oy)
```

So the equations become:

```
u = mx f (Xc / Zc) + ox
v = my f (Yc / Zc) + oy
```

---

# 8. Intrinsic Parameters

Define:

```
fx = mx * f
fy = my * f
```

Now the equations simplify to:

```
u = fx * (Xc / Zc) + ox
v = fy * (Yc / Zc) + oy
```

The parameters:

```
fx
fy
ox
oy
```

are called **intrinsic parameters**.

They describe the **internal geometry of the camera**.

---

# 9. Why fx and fy?

A camera has only one focal length.

But we use two parameters because:

* pixel density may differ in x and y
* pixels may be rectangular.

So:

```
fx ≠ fy
```

in general.

---

# 10. Problem: Nonlinear Model

The equations contain:

```
1 / Zc
```

So the model is **nonlinear**.

Nonlinear models are harder to estimate.

To fix this, we use:

> **Homogeneous coordinates**

---

# 11. Homogeneous Coordinates (2D)

A pixel point:

```
(u, v)
```

can be written as:

```
(u, v, 1)
```

But also:

```
(λu, λv, λ)
```

for any λ ≠ 0.

These are equivalent representations.

This allows easier matrix formulations.

---

# 12. Homogeneous Coordinates (3D)

A 3D point:

```
(X, Y, Z)
```

becomes:

```
(X, Y, Z, 1)
```

This lets us express transformations with matrices.

---

# 13. Intrinsic Matrix

Using homogeneous coordinates we obtain:

```
ũ = M_int * Xc
```

Where:

```
M_int =
[ fx   0   ox ]
[ 0   fy   oy ]
[ 0    0    1 ]
```

This matrix is called the **Intrinsic Matrix**.

It converts:

```
camera coordinates → pixel coordinates
```

---

# 14. Calibration Matrix

The **3×3 matrix inside the intrinsic matrix** is called:

```
K
```

```
K =
[ fx   0   ox ]
[ 0   fy   oy ]
[ 0    0    1 ]
```

Important property:

```
Upper triangular matrix
```

This structure is important when solving calibration equations.

---

# 15. World → Camera Transformation

We still need to map:

```
world coordinates → camera coordinates
```

This uses **extrinsic parameters**.

---

## Rotation Matrix

```
R
```

A **3×3 matrix** describing camera orientation.

---

## Translation Vector

```
t
```

Camera position relative to the world.

---

The transformation is:

```
Xc = R * Xw + t
```

---

# 16. Rotation Matrix Properties

Rotation matrices are **orthonormal**.

Meaning:

```
R^T R = I
```

And:

```
R^-1 = R^T
```

This property simplifies many computations.

---

# 17. Extrinsic Matrix

Using homogeneous coordinates:

```
Xc = M_ext * Xw
```

Where:

```
M_ext =
[ R  t ]
[ 0  1 ]
```

This matrix transforms:

```
world coordinates → camera coordinates
```

---

# 18. Final Camera Model

We combine:

```
Intrinsic matrix
Extrinsic matrix
```

Result:

```
ũ = M_int * M_ext * Xw
```

---

# 19. Projection Matrix

Define:

```
P = M_int * M_ext
```

Then the final equation becomes:

```
ũ = P * Xw
```

Where:

```
P = projection matrix
```

Size:

```
3 × 4
```

---

# 20. Camera Calibration Goal

Calibration means estimating:

```
P
```

This matrix contains **12 parameters**.

Once we know it, we can compute:

```
3D world point → image pixel
```

---

# 21. Decomposing the Projection Matrix

Even better:

The projection matrix can be decomposed into:

```
Intrinsic matrix
Extrinsic matrix
```

This gives:

* camera internal geometry
* camera pose in the world.

---

# Final Big Picture

The **linear camera model** is:

```
Pixel = ProjectionMatrix * WorldPoint
```

Expanded:

```
Pixel = IntrinsicMatrix * ExtrinsicMatrix * WorldPoint
```

So camera calibration finds the parameters that explain:

```
how a 3D scene becomes a 2D image
```

---

what usually follows this lecture:

**DLT Camera Calibration Algorithm**

which explains **how we actually compute the projection matrix from calibration points**.

That is basically the **core math behind OpenCV calibration**.
