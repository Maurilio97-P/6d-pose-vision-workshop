# Set Up Conda Virtual Environment for Data Science (Step-by-Step)

Video: *Set up Conda virtual environment for data science projects*
YouTube: [https://www.youtube.com/watch?v=gVfTT8o9PyQ](https://www.youtube.com/watch?v=gVfTT8o9PyQ)

---

# 🎯 Why Virtual Environments Matter

If this ever comes up in an interview:

> A virtual environment is a dedicated space where you install Python packages specific to one project without affecting other projects or the global environment.

### Example Problem Without Environments

Project A needs:

```
pandas==1.2
```

Project B needs:

```
pandas==1.5
```

If installed globally → 💥 things break.

If installed in separate environments → ✅ everything works.

---

# 🧠 Why Use Conda Instead of venv?

Two common options:

1. Python built-in `venv`
2. Conda

### Why Conda is popular in Data Science:

* Manages environments
* Manages packages
* Handles complex dependencies (NumPy, pandas, matplotlib)
* Easier for scientific stacks

---

# 1️⃣ Install Conda (Miniconda Recommended)

Go to:

```
https://docs.conda.io/projects/conda/en/stable/
```

Download the stable version for your OS.

Install it normally.

---

# 2️⃣ Verify Conda Installed

Open:

* Terminal (Mac/Linux)
* Command Prompt (Windows)

Run:

```bash
conda -v
```

If you see a version number → you're good.

Example:

```
conda 24.x.x
```

---

# 3️⃣ Create a New Environment

Best practice:

> Create a new environment for every project.

Basic syntax:

```bash
conda create --name myenv
```

Example from video:

```bash
conda create --name maggie_data_projects
```

Press:

```
y
```

to confirm.

---

# 🔥 Optional: Specify Python Version

If you need a specific version:

```bash
conda create --name myenv python=3.10
```

Very useful when:

* Following tutorials
* Matching production environments
* Avoiding version conflicts

---

# 4️⃣ Activate the Environment

```bash
conda activate maggie_data_projects
```

Your prompt changes from:

```
(base)
```

to:

```
(maggie_data_projects)
```

That prefix tells you which environment you're in.

---

# 5️⃣ Deactivate Environment

When done:

```bash
conda deactivate
```

Returns to:

```
(base)
```

Important:

❌ Do NOT type the environment name after deactivate
Just:

```bash
conda deactivate
```

---

# 6️⃣ Install Packages Inside Environment

Activate first:

```bash
conda activate maggie_data_projects
```

Then install:

```bash
conda install seaborn
```

Press:

```
y
```

Now seaborn is installed **only inside this environment**.

Next time you activate it → it’s already there.

---

# 🧠 Core Conda Commands Summary

### Create environment

```bash
conda create --name myenv
```

### Create with Python version

```bash
conda create --name myenv python=3.10
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

### Check installed packages

```bash
conda list
```

---

# 🖥 Using Conda Environment in VS Code

Two ways.

---

## Method 1: Select Kernel (Recommended)

Open a Jupyter Notebook in VS Code.

When you click "Run", it asks:

> Select Kernel

Choose the environment you created:

```
Python (maggie_data_projects)
```

Now notebook runs using that environment.

---

## Method 2: Activate via VS Code Terminal

Inside VS Code:

Terminal → New Terminal

Then:

```bash
conda activate maggie_data_projects
```

Now anything you run inside VS Code uses that environment.

---

# 🎯 Real Portfolio Setup Strategy (Best Practice)

For Data Science Portfolio:

Create separate environments like:

```
bike_share_env
house_price_env
nlp_sentiment_env
```

Each contains:

* Its own pandas version
* Its own sklearn version
* Its own visualization stack

This makes your projects:

* Cleaner
* Reproducible
* Professional

---

# ⚡ What This Means for YOU

You now understand:

Anaconda = package + environment manager
Conda = command line tool
Environment = isolated project workspace

And now your full stack looks like:

Anaconda → Environment → Install packages → VS Code → Jupyter → Build project

---

