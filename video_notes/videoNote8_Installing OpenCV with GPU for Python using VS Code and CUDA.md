# Installing OpenCV with CUDA (GPU) for Python

Source:
**OpenCV GPU: Installing OpenCV with GPU for Python using VS Code and CUDA**
Transcript reference: 

---

# What Is This Video About?

Goal:

Build **OpenCV from source** with:

* CUDA support
* cuDNN support
* Python 3 (Anaconda)
* DNN module GPU acceleration
* FAST_MATH enabled

So you can use:

```python
from cv2 import cuda
```

And run OpenCV GPU operations.

---

# Why Build From Source?

Because:

`pip install opencv-python`

❌ Does NOT include CUDA
❌ Does NOT include cuDNN
❌ Does NOT include GPU DNN

Prebuilt wheels = CPU only.

To enable GPU → you must build from source.

---

# High-Level Pipeline

1. Install prerequisites
2. Download OpenCV source
3. Download OpenCV contrib
4. Install Anaconda (Python 3.8)
5. Configure with CMake
6. Enable CUDA flags
7. Generate build files
8. Compile (1–2 hours)
9. Install
10. Verify with `cv2.cuda`

---

# Prerequisites

From transcript :

You need:

* Visual Studio 2019 (C++ tools)
* CUDA Toolkit (example: 11.3)
* cuDNN (example: 8.2)
* CMake
* Anaconda (Python 3.8)

---

# Step 1 – Download OpenCV Source

Go to GitHub:

* OpenCV repo
* Choose version (example: 4.5.2 in video)
* Download ZIP

Then:

Download **opencv_contrib**
→ Must match EXACT same version

Example:

```
opencv-4.5.2
opencv_contrib-4.5.2
```

Version mismatch = build failure.

---

# Step 2 – Install Anaconda

Video uses:

Python 3.8
64-bit
Windows 10

Important setting:

✔ Add Anaconda to PATH

Why?

Because CMake must find:

* Python executable
* Include directory
* Python libs
* NumPy

---

# Step 3 – Folder Structure

Inside your user directory:

```
opencv_python/
    opencv/
    opencv_contrib/
    build/
```

* opencv = source
* contrib = extra modules
* build = empty folder for binaries

---

# Step 4 – Open CMake GUI

Configure:

### Source folder:

```
opencv/
```

### Build folder:

```
opencv_python/build/
```

Generator:

```
Visual Studio 16 2019
x64
```

Then press:

Configure

---

# Common Python Error (Very Important)

At first configuration:

Python 3 may be unavailable.

This happens because:

* NumPy version outdated
* Python interpreter not properly linked

Fix:

Open Anaconda Prompt:

```bash
pip install --upgrade numpy
```

Then:

Re-configure in CMake.

Now Python 3 should appear as available 

---

# Step 5 – Link Python Properly

In CMake:

Make sure these are correct:

* PYTHON3_EXECUTABLE → Anaconda python.exe
* PYTHON3_INCLUDE_DIR
* PYTHON3_LIBRARY
* NumPy include directory

If these are wrong:
Import cv2 will fail later.

---

# Step 6 – Enable CUDA

Search in CMake:

```
WITH_CUDA
```

Enable it ✔

Then enable:

```
OPENCV_DNN_CUDA
```

Enable FAST_MATH:

```
ENABLE_FAST_MATH
CUDA_FAST_MATH
```

Also enable:

```
BUILD_opencv_world
```

---

# Step 7 – Add Contrib Modules

Set:

```
OPENCV_EXTRA_MODULES_PATH
```

Point to:

```
opencv_contrib/modules
```

Without this:
DNN module may fail.

---

# Step 8 – Set GPU Architecture

Important:

Find your GPU compute capability.

Example in video:

GTX 1060 → 6.1 

RTX 2060 → 7.5

Set:

```
CUDA_ARCH_BIN = 6.1
```

Delete other values.

Wrong architecture = inefficient or broken build.

---

# Step 9 – Build Type

Set:

```
Release
```

Not Debug.

---

# Step 10 – Final Configure

Press:

Configure
Generate

Now CMake generates build files inside:

```
build/
```

---

# Step 11 – Compile & Install

Open Anaconda Prompt.

Run:

```bash
cmake --build "path_to_build" --target install --config Release
```

This:

* Compiles OpenCV
* Links CUDA
* Installs cv2 module

Build time:

⏳ 1–2 hours 

Warnings during build = normal.

---

# Step 12 – Verify Installation

Open Anaconda Prompt:

```python
import cv2
from cv2 import cuda
cuda.printCudaDeviceInfo(0)
```

If working:

You’ll see:

* Device count
* GPU name
* Memory
* CUDA driver version

Example from transcript:

* GTX 1060
* 6GB
* CUDA 11.3 

If no error → SUCCESS.

---

# Using in VS Code

Important:

Select correct interpreter.

In VS Code bottom bar:

Choose:

```
Anaconda Python 3.8
```

If you choose system Python:

ImportError.

---

# What You Now Have

After successful build:

You can use:

* cv2.cuda_GpuMat
* cv2.cuda.resize
* cv2.cuda.canny
* DNN module with CUDA backend

Example:

```python
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
```

Now your DNN runs on GPU.

---

# What This Unlocks For You

Now you can combine:

* OpenCV preprocessing on GPU
* Deep learning inference (DNN)
* Real-time pipelines
* Stereo + DNN
* Object detection with GPU acceleration

This is critical for:

* Robotics
* Autonomous systems
* Real-time tracking
* Industrial vision

---

# Key Insight

OpenCV GPU ≠ Automatic speed boost.

Only CUDA-enabled modules use GPU.

Regular functions:

```python
cv2.resize()
```

→ CPU

CUDA version:

```python
cv2.cuda.resize()
```

→ GPU

You must explicitly use cuda namespace.

---

# Big Picture Connection

Now your stack looks like:

Camera
→ CUDA preprocessing
→ DNN inference (CUDA backend)
→ Pose estimation
→ 3D logic

Fully GPU accelerated.

---

## next we can:

* Design a full CUDA OpenCV pipeline
* Compare PyTorch vs OpenCV DNN performance
* Or build a real-time GPU object detector architecture

Your CV stack is leveling up HARD now 🚀
