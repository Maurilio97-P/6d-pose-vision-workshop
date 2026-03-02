# NumPy vs SciPy

Video: *NumPy vs SciPy*
YouTube: [https://www.youtube.com/watch?v=l3s-_8uTBVA](https://www.youtube.com/watch?v=l3s-_8uTBVA)

---

# 1️⃣ Big Picture

Both **NumPy** and **SciPy** are essential math libraries in Python.

They overlap.

They complement each other.

They are NOT competitors.

Important:

> SciPy is built on top of NumPy.

If you're using SciPy, you're also using NumPy underneath.

---

# 2️⃣ NumPy — Numerical Python

NumPy stands for:

> Numerical Python

It is designed to:

* Work with large multi-dimensional arrays
* Perform high-speed mathematical operations

---

## 🔹 Multi-Dimensional Arrays

NumPy’s core structure is the **ndarray**.

You can think of:

* 1D array → simple row of numbers
* 2D array → table (rows and columns)
* 3D array → cube (x, y, z)
* nD array → tensor

Example real-world uses:

* 3D graphics → (x, y, z) coordinates
* Time series → one axis represents time
* Machine learning → tensors

---

## 🔹 What NumPy Can Do

NumPy supports:

### Basic math

* Addition
* Subtraction
* Squaring
* Multiplication

### Statistical operations

* Mean
* Median
* Standard deviation

### Linear algebra

* Matrix operations

### Image processing

Images are multi-dimensional arrays:

* Height
* Width
* Color channels

NumPy can manipulate these efficiently.

---

# 3️⃣ SciPy — Scientific Python

SciPy stands for:

> Scientific Python

It extends NumPy.

Think of it as:

> NumPy+

SciPy uses NumPy arrays and adds:

* Advanced scientific routines
* More specialized mathematical tools

---

# 4️⃣ What SciPy Adds

SciPy focuses on advanced scientific computing.

It includes modules for:

* Numerical integration
* Interpolation
* Optimization
* Signal processing
* Linear algebra
* Advanced statistics

---

# 5️⃣ Example: Interpolation

Interpolation = estimating unknown values between known values.

---

## 🔹 NumPy Interpolation

NumPy supports:

```python
np.interp()
```

This performs:

> Linear interpolation

It fits straight lines between data points.

Fast. Simple. Efficient.

Good for basic use cases.

---

## 🔹 SciPy Interpolation

SciPy supports:

* Cubic interpolation
* Cubic spline interpolation

Instead of straight lines:

> It fits smooth curves.

This is better when:

* Data is non-linear
* You need higher accuracy

---

# 6️⃣ Practical Use Cases

## ✅ Use NumPy When:

* Performing numerical operations
* Doing statistical analysis
* Manipulating arrays
* Working with images
* Reshaping data
* Running simulations

Example:

Image processing:

```text
Image → 3D NumPy array (height, width, channels)
```

NumPy can:

* Apply filters
* Transform pixels
* Modify channels

---

## ✅ Use SciPy When:

You need advanced scientific tools.

### Signal processing

SciPy includes:

* Fast Fourier Transform (FFT)

FFT converts:

Time domain → Frequency domain

Useful in:

* Audio processing
* Communications
* Physics

---

### Optimization

Example:

Designing an aircraft wing.

Goal:

* Minimize drag
* Respect weight constraints

SciPy has optimization routines to solve such problems.

---

# 7️⃣ Efficiency

Both libraries are:

* Highly optimized
* Efficient with memory
* Designed for large datasets

They minimize:

* CPU usage
* Memory usage

That’s why they’re widely used in:

* Data science
* Physics
* Engineering
* Machine learning

---

# 8️⃣ Core Difference

Think of it like this:

NumPy = Fast numerical engine
SciPy = Advanced scientific toolbox

---

## 🔹 NumPy

* Focus: Numerical arrays
* Core math
* Statistics
* Basic linear algebra
* Foundation layer

---

## 🔹 SciPy

* Focus: Scientific computing
* Advanced math routines
* Signal processing
* Optimization
* Specialized algorithms

---

# 9️⃣ Conceptual Relationship

```text
NumPy → Base layer (arrays + math)

SciPy → Built on top of NumPy (adds scientific tools)
```

If you use SciPy:

You are using NumPy internally.

---

# 🔟 Summary Table

| Feature                  | NumPy            | SciPy                   |
| ------------------------ | ---------------- | ----------------------- |
| Meaning                  | Numerical Python | Scientific Python       |
| Core focus               | Arrays & math    | Scientific algorithms   |
| Multi-dimensional arrays | Yes              | Uses NumPy arrays       |
| Interpolation            | Linear           | Cubic, spline, advanced |
| Signal processing        | Basic            | Advanced                |
| Optimization             | Limited          | Advanced routines       |
| Built on NumPy           | —                | Yes                     |

---

# 1️⃣1️⃣ Mental Model

If you're:

* Doing raw math → NumPy
* Doing signal analysis → SciPy
* Running optimization problems → SciPy
* Handling large numeric arrays → NumPy

---

# 1️⃣2️⃣ Final Takeaway

There is no battle.

It’s not:

> NumPy vs SciPy

It’s:

> NumPy + SciPy

Use NumPy for numerical computation.

Use SciPy when your problem becomes more scientific and specialized.

---

## next level

We can now:

* Compare NumPy vs Pandas vs SciPy in one clean mental map
* Build a mini scientific workflow example
* Dive into SciPy modules (optimize, signal, integrate)
* Or connect this directly to ML / CV applications
