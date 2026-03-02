# Getting Started with Anaconda + Python on Windows

Video: *Getting started with Anaconda and Python on Windows*
YouTube: [https://www.youtube.com/watch?v=4DQGBQMvwZo](https://www.youtube.com/watch?v=4DQGBQMvwZo)

---

# 1️⃣ Install Anaconda

### Download

Go to:

```
https://anaconda.com/download
```

Download Windows version.

### Important Install Option

During installation:

✔️ **Check: "Add Anaconda3 to my PATH environment variable"**

It says "not recommended" — but for development it’s extremely useful.

---

# 2️⃣ Launch Anaconda Navigator

After install:

* Open **Anaconda Navigator**
* You’ll see bundled tools:

  * Jupyter Notebook
  * Spyder
  * VS Code
  * etc.

But the key concept is:

# 🧠 Environments

Environments = isolated Python workspaces.

Think of them as containers.

You can have:

* One environment for computer vision
* One for game dev
* One for data science
* Each with different package versions

By default, you have:

```
(base)
```

But best practice:

> ❌ Do NOT develop inside base
> ✅ Create a new environment per project

---

# 3️⃣ Install Git Bash (Highly Recommended)

Instead of using:

* Windows CMD
* PowerShell

Use:

👉 **Git Bash**

Download from:

```
https://git-scm.com/download/win
```

Why?

Because:

* Unix-style commands
* Same commands as Linux/macOS
* Most tutorials assume Unix-style shell

During install:

* Leave defaults
* Choose VS Code as default editor (if you use it)
* Choose default branch name = `main`

---

# 4️⃣ Initialize Conda in Git Bash

Open Git Bash.

Run:

```bash
conda init bash
```

Then:

* Close Git Bash
* Reopen it

You should now see:

```
(base)
```

at the beginning of your prompt.

That means Conda is active.

---

# 5️⃣ Create a New Environment

Create new environment:

```bash
conda create --name demo
```

Activate it:

```bash
conda activate demo
```

Now your prompt shows:

```
(demo)
```

You are now isolated from base.

---

# 6️⃣ Install Python in the Environment

```bash
conda install python
```

Confirm with:

```bash
conda list
```

Check which Python you're using:

```bash
which python
python --version
```

You’ll see it's inside:

```
.../anaconda3/envs/demo/
```

---

# 7️⃣ Environment Switching (Very Important Concept)

Deactivate:

```bash
conda deactivate
```

Now you're back in:

```
(base)
```

Check version:

```bash
python --version
```

It may be a different Python version.

This proves:

⚡ Environments can run different versions of Python and packages.

---

# 8️⃣ Run Your First Python Script

Create file:

```
demo.py
```

Inside:

```python
print("hello world")
```

In Git Bash:

```bash
cd ~/Desktop
python demo.py
```

Output:

```
hello world
```

You now have Python running in your environment.

---

# 9️⃣ Installing External Packages

Example script uses:

* `requests`
* `beautifulsoup4`

If you try running without installing:

You get:

```
ModuleNotFoundError: No module named 'requests'
```

Install packages:

```bash
conda install requests
conda install beautifulsoup4
```

Confirm:

```bash
conda list
```

Run again:

```bash
python demo.py
```

Now it works.

---

# 🔟 Where Do Packages Come From?

Two main sources:

### Conda packages

From:

```
conda-forge
```

### Pip packages

From:

```
PyPI
```

You can also use:

```bash
pip install package_name
```

Even inside Conda environments.

---

# 🔥 Core Commands You Must Remember

### Create environment

```bash
conda create --name myenv
```

### Activate

```bash
conda activate myenv
```

### Deactivate

```bash
conda deactivate
```

### Install package

```bash
conda install package_name
```

### List installed packages

```bash
conda list
```

### Check python path

```bash
which python
```

---

# 🧠 Mental Model Summary

Anaconda = package + environment manager
Conda = command line tool
Git Bash = proper Unix-style shell
Environment = isolated project container

---

# 🎯 Why This Matters for You

For your CV / OpenCV / pose estimation learning:

You’ll likely create environments like:

```
cv-env
aruco-env
yolo-env
```

Each with:

* Different OpenCV versions
* Different CUDA setups
* Different dependencies

This prevents:

* Dependency conflicts
* Version mismatches
* Broken installs

---

