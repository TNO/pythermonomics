# How to use the Jupyter Notebook example

## Windows

On windows, you can install the Jupyter Notebook with the following commands:

```powershell
# 1) Create & activate virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install the project with the notebook extra
python -m pip install --upgrade pip
pip install .[notebook]

# 3a) If using browser JupyterLab:
jupyter lab   # opens in the browser

# 3b) If using VS Code:
# - Install "Python" and "Jupyter" extensions.
# - Open the .ipynb and pick the .venv as the kernel.
#   (Only ipykernel is required in the env.)
```

and for Linux:

```bash
# 1) Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Install the project with the notebook extra
python -m pip install --upgrade pip
pip install '.[notebook]'   # quote for zsh

# 3a) Browser JupyterLab:
jupyter lab

# 3b) VS Code:
# - Install "Python" and "Jupyter" extensions.
# - Select the .venv as the kernel (only ipykernel required).
```