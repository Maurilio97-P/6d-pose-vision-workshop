# Camera Calibration — Estimating the Projection Matrix

Video: *Camera Calibration*
https://youtu.be/GUbWsXU1mac?si=gEeYXRU7Tkynk-mY

This one is important because it explains **how we actually compute the projection matrix during camera calibration**.

---

# 1. Goal of Camera Calibration

From the previous lecture we obtained the **linear camera model**:

```text
ũ = P Xw
```

Where:

* **Xw** → 3D world point (homogeneous coordinates)
* **ũ** → image pixel coordinates (homogeneous)
* **P** → projection matrix (3×4)

Camera calibration means:

```text
Estimate the projection matrix P
```

Once we know **P**, we know the mapping:

```text
3D world point → 2D image pixel
```

---

# 2. Using an Object with Known Geometry

To estimate **P**, we need an object whose **3D structure is known**.

Example:

* calibration cube
* checkerboard
* calibration board

The important requirement:

```text
We know the 3D coordinates of feature points.
```

Example point on cube:

```text
World coordinates:
(Xw, Yw, Zw) = (0, 3, 4)
```

---

# 3. Image Correspondences

For each feature point we know:

### 3D position in world

```text
(Xw, Yw, Zw)
```

### 2D position in image

```text
(u, v)
```

Example:

```text
World point: (0, 3, 4)
Image pixel: (56, 115)
```

So we have:

```text
3D → 2D correspondences
```

---

# 4. Collecting Many Correspondences

We repeat this for many points.

Example:

```text
Point 1 → (X1,Y1,Z1) ↔ (u1,v1)
Point 2 → (X2,Y2,Z2) ↔ (u2,v2)
Point 3 → (X3,Y3,Z3) ↔ (u3,v3)
...
Point n → (Xn,Yn,Zn) ↔ (un,vn)
```

These correspondences can be obtained:

* manually (clicking points)
* automatically (pattern detection).

---

# 5. Camera Model Equation

Using the projection matrix:

```text
ũ = P Xw
```

Where:

```text
P =
[ p1 p2 p3 p4 ]
[ p5 p6 p7 p8 ]
[ p9 p10 p11 p12 ]
```

The matrix **P has 12 parameters**.

These are the unknowns we want to estimate.

---

# 6. Expanding the Equations

For each point **i** we get two equations:

```text
ui = function(P, Xi, Yi, Zi)
vi = function(P, Xi, Yi, Zi)
```

So every point contributes:

```text
2 equations
```

---

# 7. Writing the System in Matrix Form

All equations can be written as:

```text
A p = 0
```

Where:

* **A** → known matrix built from correspondences
* **p** → vector containing the 12 elements of P

```text
p = [p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12]^T
```

So we want to solve:

```text
A p = 0
```

---

# 8. Important Property: Scale Ambiguity

Homogeneous coordinates introduce **scale ambiguity**.

Meaning:

```text
P and kP produce the same image
```

for any non-zero scalar **k**.

So:

```text
P ≡ kP
```

Both produce identical projections.

---

# 9. Intuition for Scale Ambiguity

Imagine:

* doubling the size of the world
* doubling the camera size
* doubling focal length

The resulting image would look exactly the same.

Therefore:

```text
Projection matrix is defined only up to scale.
```

---

# 10. Fixing the Scale

To remove ambiguity we impose a constraint.

Two options:

Option 1

```text
Set one parameter of P = 1
```

Option 2 (preferred)

```text
||p||² = 1
```

Meaning the projection vector has **unit length**.

---

# 11. Optimization Problem

Now we solve:

```text
minimize ||A p||²
subject to ||p||² = 1
```

This is called a:

```text
Constrained least squares problem
```

---

# 12. Writing the Loss Function

The objective becomes:

```text
||A p||² = pᵀ Aᵀ A p
```

Constraint:

```text
pᵀ p = 1
```

Using Lagrange multipliers:

```text
L = pᵀ Aᵀ A p − λ(pᵀp − 1)
```

---

# 13. Solving the Optimization

Take derivative with respect to **p**:

```text
(Aᵀ A) p = λ p
```

This is a classic **eigenvalue problem**.

---

# 14. Final Solution

The optimal **p** is:

```text
Eigenvector of (AᵀA)
with the smallest eigenvalue
```

Once we obtain **p**, we reshape it into:

```text
Projection matrix P (3×4)
```

---

# 15. Result of Calibration

After computing **P** we know:

```text
World point → Image pixel mapping
```

Later we can **decompose P** into:

```text
P = K [R | t]
```

Where:

* **K** → intrinsic matrix
* **R** → rotation matrix
* **t** → translation vector

---

# Big Picture

Camera calibration works like this:

```text
Known 3D points
        ↓
Detect their pixel positions
        ↓
Build matrix A
        ↓
Solve eigenvalue problem
        ↓
Find projection matrix P
```

This method is the basis of:

```text
Direct Linear Transformation (DLT)
```

which is widely used in camera calibration.

---

## **next concept after this lecture** (which is extremely important in computer vision) is:

**Decomposing the projection matrix**

```text
P → K, R, t
```

That’s where we recover:

* focal length
* camera center
* camera orientation

which is basically **the full camera geometry**.
