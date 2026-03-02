# Getting Started with Jupyter Notebooks in VS Code

Video: *Getting Started with Jupyter Notebooks in VS Code*
YouTube: [https://www.youtube.com/watch?v=suAkMeWJ1yE](https://www.youtube.com/watch?v=suAkMeWJ1yE)

---

# 🧠 Why Use Jupyter Inside VS Code?

Instead of:

* Running notebooks in browser
* Switching between editor + notebook

You get:

* ✅ IntelliSense
* ✅ Syntax highlighting
* ✅ Debugging
* ✅ Variable explorer
* ✅ Breakpoints
* ✅ Git integration
* ✅ Same environment as your scripts

It’s much more powerful.

---

# 1️⃣ Install Required Extensions

Open VS Code → Extensions tab.

Install:

### 🔹 Jupyter Extension

Search:

```
Jupyter
```

Install.

---

### 🔹 Python Extension

Search:

```
Python
```

Install.

Why?

Because:

* It connects notebooks to Python environments
* Enables IntelliSense
* Enables debugging

---

# 2️⃣ Create a New Notebook

Open Command Palette:

```
Ctrl + Shift + P
```

Run:

```
Create New Jupyter Notebook
```

Save file:

```
my_first_notebook.ipynb
```

---

# 3️⃣ Select a Kernel (Very Important)

Top right → **Select Kernel**

You’ll see options:

* Global Python
* Virtual environments
* Conda environments
* Existing Jupyter server

Best practice:

> Use a virtual environment, not global Python.

Example:

```
cv_env
data_science_env
```

If prompted, install:

```
ipykernel
```

This package allows VS Code to connect your environment to Jupyter.

---

# 🔥 Run First Cell

Example:

```python
print("Hello World")
```

Run:

* Click ▶
* Or:

```
Ctrl + Alt + Enter
```

---

# 🧱 Notebook Structure in VS Code

## Code Cells

Same behavior as classic Jupyter.

## Markdown Cells

Top toolbar → add Markdown cell.

Used for:

* Section headers
* Explanations
* Notes
* Documentation

---

# 🧠 Outline View (Underrated Feature)

On the side panel:

You’ll see notebook outline.

It acts like:

📚 Table of contents

Based on Markdown headers.

Very useful for:

* Large analysis notebooks
* Reports
* Organized projects

---

# 🧪 Running Multiple Cells

Options available:

* Run All
* Run Above
* Run Below
* Run Section (via Outline)

Much cleaner than browser Jupyter.

---

# 🛑 Interrupting Execution

Top toolbar:

* Interrupt
* Restart kernel
* Go to running cell

Same kernel logic as classic Jupyter.

---

# 🧩 IntelliSense in Notebooks

When typing:

```python
import pandas as pd
pd.
```

You get:

* Autocomplete
* Function signatures
* Hover documentation

Same as writing normal `.py` files.

This is a huge upgrade over browser Jupyter.

---

# 🐞 Debugging Cells (Major Feature)

You can:

* Set breakpoints
* Debug cell
* Step through code
* Inspect variables

To debug:

Cell → Run action menu → **Debug Cell**

This opens full VS Code debugger.

This is something normal Jupyter browser cannot do properly.

---

# 🔎 Variable Explorer

Top toolbar → Variables

You’ll see:

* DataFrames
* Lists
* Arrays
* Dictionaries

You can inspect them visually.

For DataFrames:

You can install:

```
Data Wrangler extension
```

Which allows:

* Sorting
* Filtering
* Cleaning
* Transforming

All visually.

---

# 🧠 Mental Model: VS Code Jupyter vs Browser Jupyter

| Feature             | Browser | VS Code   |
| ------------------- | ------- | --------- |
| Code execution      | Yes     | Yes       |
| IntelliSense        | Limited | Full      |
| Debugger            | Weak    | Full      |
| Git integration     | Basic   | Native    |
| Variable Explorer   | Basic   | Powerful  |
| Production workflow | Meh     | Excellent |

---

# 🎯 Recommended Workflow (Your Stack)

Since you're building:

* Computer Vision projects
* Data Science projects
* Calibration / ArUco experiments

Use this structure:

```
project/
│
├── environment (conda)
├── notebooks/
│     └── experiments.ipynb
├── src/
│     └── production_code.py
```

Use notebook for:

* Testing
* Visualizing
* Prototyping

Use `.py` scripts for:

* Final implementation
* Clean architecture
* Reusable modules

---

# 🔥 Advanced Tips (Important)

### Always Restart & Run All Before Sharing

Because notebooks remember variables.

Execution order matters.

---

### Don’t Use Global Python

Always use:

```
conda activate myenv
```

Then select that environment as kernel.

---

### Install ipykernel if needed

Inside environment:

```bash
conda install ipykernel
```

---

# 🧠 Final Stack Summary

Now your full system looks like:

Anaconda
→ Create env
→ Activate env
→ Open VS Code
→ Select kernel
→ Jupyter notebook
→ Debug + Analyze
→ Move to production `.py`

---


