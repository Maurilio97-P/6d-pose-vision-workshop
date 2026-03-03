
# Installing OpenCV with GPU (CUDA) Support — Full Notes

Video: *Instalación rápida y sencilla de OpenCV Python con GPU CUDA*
https://youtu.be/d8Jx6zO1yw0?si=VjsrbPY5OSVfX881
---

# 1️⃣ Goal

Build OpenCV from source with:

* ✅ NVIDIA CUDA support
* ✅ GPU acceleration
* ✅ Python (Anaconda)
* ✅ Visual Studio 2019

Result:

```python
from cv2 import cuda
```

And use:

```python
cuda.printCudaDeviceInfo(0)
```

If this works → GPU OpenCV build succeeded.

---

# 2️⃣ Why Build OpenCV with CUDA?

Default OpenCV (pip install opencv-python):

* ❌ No CUDA support
* ❌ CPU only

Building from source:

* ✅ Access GPU acceleration
* ✅ Faster processing
* ✅ Useful for:

  * Large image pipelines
  * Real-time processing
  * Deep learning preprocessing
  * High-resolution video

---

# 3️⃣ Required Tools

You need:

### 🔹 1. CUDA Toolkit

Download from NVIDIA website.

Must match:

* Your GPU architecture
* Your driver version

---

### 🔹 2. CMake

Used to configure and generate build files.

Download latest version.

---

### 🔹 3. Visual Studio 2019

⚠ Important:
Do NOT use Visual Studio 2022.

Must install:

* VS 2019 Community Edition

---

### 🔹 4. Anaconda (Python)

Used to:

* Manage Python
* Build OpenCV for Python
* Handle NumPy

Make sure:

* Python path is in environment variables.

---

### 🔹 5. OpenCV Source Code

Download:

* OpenCV repository
* OpenCV_contrib repository

Important:

Versions must match.

Example:

* OpenCV 4.5.2
* opencv_contrib 4.5.2

---

# 4️⃣ Folder Structure

You should have:

```text
opencv_gpu/
│
├── opencv/
├── opencv_contrib/
└── build/   ← empty
```

The build folder must be empty before starting.

---

# 5️⃣ CMake Configuration

Open CMake GUI.

### Step 1 — Set Paths

* Source: opencv folder
* Build: build folder

Click Configure.

Choose:

* Visual Studio 2019
* x64 architecture

---

# 6️⃣ Important CMake Flags

After first configure, enable:

### ✅ WITH_CUDA

```text
WITH_CUDA = ON
```

---

### ✅ CUDA_FAST_MATH

```text
CUDA_FAST_MATH = ON
```

Faster GPU calculations.

---

### ✅ BUILD_opencv_world

Creates unified OpenCV library.

---

### ✅ OPENCV_EXTRA_MODULES_PATH

Set this to:

```text
opencv_contrib/modules
```

---

# 7️⃣ Python Configuration

In CMake:

Make sure you see:

```text
Python 3:
  Interpreter
  Library
  NumPy
```

If NumPy missing:

Run:

```bash
pip install numpy --upgrade
```

Then reconfigure.

---

# 8️⃣ CUDA Architecture (Very Important)

Set:

```text
CUDA_ARCH_BIN
```

Based on your GPU.

Example:

* GTX 10xx → 6.1
* RTX 30xx → 8.6

Find architecture on:
Wikipedia CUDA compute capability table.

Example:

```text
6.1;8.6
```

If wrong → build may fail or underperform.

---

# 9️⃣ Build Configuration

Disable Debug.

Use:

```text
Release mode only
```

Then:

1. Configure again
2. Generate

---

# 🔟 Build with CMake (Command Line)

Open Anaconda Prompt.

Run:

```bash
cmake --build . --target INSTALL --config Release
```

Inside build folder.

⚠ This may take:

* 1 to 2 hours
* Depending on CPU

Expect:

* Many warnings
* Some errors

As long as it completes → OK.

---

# 1️⃣1️⃣ Verify Installation

Open Anaconda Prompt:

```bash
python
```

Then:

```python
import cv2
from cv2 import cuda
```

If no error → good.

Then:

```python
cuda.printCudaDeviceInfo(0)
```

If GPU info prints → success.

Example output:

* GPU name
* Memory
* Clock speed
* CUDA version

---

# 1️⃣2️⃣ What Just Happened?

You built OpenCV from source:

```text
Source Code
    ↓
CMake Config
    ↓
Visual Studio Build
    ↓
CUDA-enabled OpenCV
    ↓
Python Binding
```

Now:

```text
cv2.cuda
```

Is available.

---

# 1️⃣3️⃣ Why This Is Powerful

Now you can use:

* cv2.cuda_GpuMat
* CUDA filters
* GPU resizing
* GPU color conversion
* GPU feature detection

Massive speedup for:

* Video pipelines
* High-res processing
* Batch image operations

---

# 1️⃣4️⃣ Important Reality Check

Not all OpenCV functions have CUDA versions.

You must use:

```python
cv2.cuda.*
```

Explicitly.

If you call normal OpenCV:

It runs on CPU.

---

# 1️⃣5️⃣ Common Mistakes

❌ Using Visual Studio 2022
❌ Forgetting opencv_contrib
❌ Wrong CUDA architecture
❌ Debug + Release mix
❌ Missing NumPy

---

# 1️⃣6️⃣ Mental Model

Default OpenCV:

```text
CPU only
```

Custom build:

```text
CPU + GPU acceleration
```

---

# 🚀 Big Picture

Now your OpenCV stack becomes:

```text
NumPy → CPU arrays
OpenCV → CPU vision
OpenCV + CUDA → GPU vision
Deep Learning → Optional
```

This is closer to:

* Production pipelines
* Industrial vision
* High-performance CV systems

---

## next level 

We can now:

* Compare CPU vs GPU performance
* Build a GPU accelerated video pipeline
* Combine CUDA + HSV + Contours
* Connect this to YOLO inference optimization
