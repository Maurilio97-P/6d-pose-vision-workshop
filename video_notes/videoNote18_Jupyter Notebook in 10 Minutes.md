# Jupyter Notebook in 10 Minutes — Practical Guide

Video: *Jupyter Notebook In 10 Minutes*
YouTube: [https://www.youtube.com/watch?v=H9Iu49E6Mxs](https://www.youtube.com/watch?v=H9Iu49E6Mxs)

---

# 🧠 What Is Jupyter Notebook?

Jupyter Notebook is a tool that lets you combine:

* ✅ Code (usually Python)
* ✅ Text (Markdown)
* ✅ Plots
* ✅ Images
* ✅ Equations
* ✅ Output of your code

All inside your browser.

It’s extremely popular in:

* Data Science
* Machine Learning
* Research
* Education
* Prototyping

---

# 🔄 How Jupyter Works (Under the Hood)

You type code in a cell →
Browser sends it to a notebook server →
Server sends it to a kernel (Python by default) →
Kernel executes →
Result sent back to browser →
Displayed under the cell.

Important concept:

> Your browser is NOT running Python.
> A background server + kernel are doing that.

---

# 🚀 Installing Jupyter

Two common ways:

## Option 1: pip install

```bash
pip install notebook
```

## Option 2 (Recommended for beginners): Anaconda

Install Anaconda →
Open Anaconda Navigator →
Click **Launch Jupyter Notebook**

That starts:

* The notebook server
* Opens your browser
* Shows file dashboard

---

# 📁 The Jupyter Dashboard

When it opens, you see:

* Your file system
* Folders
* Existing notebooks
* Running sessions

Create new notebook:

Top right → **New → Python 3**

---

# 🧾 Notebook Basics

A notebook is made of **cells**.

Two main cell types:

1. Code
2. Markdown

---

# 💻 Code Cells

Example:

```python
1 + 8
```

Run cell:

* Click Run button
* OR Shift + Enter
* OR Ctrl + Enter (Cmd + Enter on Mac)

Result appears **below the cell**.

---

# ⌨️ Important Shortcuts

### Run cell + move down

```
Shift + Enter
```

### Run cell + stay

```
Ctrl + Enter
```

### Edit cell

Press:

```
Enter
```

### Exit editing mode

Press:

```
Esc
```

---

# 🧠 Two Modes (Very Important)

Jupyter has:

### 1️⃣ Edit Mode (green border)

You’re typing inside a cell.

### 2️⃣ Command Mode (blue border)

You’re controlling notebook structure.

If you start typing and nothing happens →
You're probably in command mode.

---

# 🧱 Insert / Delete Cells (Command Mode Only)

### Insert above

Press:

```
A
```

### Insert below

Press:

```
B
```

### Delete cell

Press:

```
D D
```

(Press D twice quickly)

---

# 📝 Markdown Cells

To switch a cell to Markdown:

In command mode:

```
M
```

To switch back to Python:

```
Y
```

---

# ✍️ Markdown Examples

### Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Bullet Points

```markdown
- Item 1
- Item 2
```

Run cell → it renders formatted output.

---

# 🔥 Infinite Loop & Interrupting Kernel

If you run something like:

```python
while True:
    print("hello")
```

It will never stop.

You’ll see:

```
[*]
```

This means the cell is running.

To interrupt:

* Menu → Kernel → Interrupt
* OR press:

```
I I
```

(Double I)

---

# 🔄 Restarting Kernel

If things get weird or variables are messed up:

Menu → Kernel → Restart

This clears all memory.

Important concept:

> Jupyter remembers variables between cells.
> Restarting wipes everything.

---

# 🛑 Stopping Jupyter

### Close notebook:

File → Close and Halt

### Stop server:

Quit from dashboard

Or close terminal where server is running.

---

# 🧠 Why Jupyter Is So Powerful

Because you can:

* Write analysis
* Show plots
* Explain results
* Include equations
* Mix code + explanation
* Build reproducible reports

It’s perfect for:

* Data Science portfolios
* Machine learning experiments
* Teaching
* Exploratory data analysis

---

# ⚡ Mental Model Summary

Notebook = document + code runner
Kernel = Python brain
Cells = execution units
Command mode = notebook control
Edit mode = code typing

---

# 🎯 How This Fits Your Stack

Now your full pipeline looks like:

Conda Environment →
Activate env →
Launch Jupyter →
Select correct kernel →
Run analysis

For your Computer Vision path:

* Calibration experiments
* ArUco testing
* Plotting reprojection error
* Debugging pose estimation

Jupyter is perfect for experimentation before moving to production scripts.

---

## next, we can:
 go deeper into kernels + memory + execution order (this is where people get confused)

