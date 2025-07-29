### Setup


1. Install [`uv (click me)`](https://docs.astral.sh/uv/getting-started/installation/) or `pip install uv`
2. Create a virtual environement
   ```
   uv venv 
   python -m venv .venv
   python3 -m venv .venv
   ```

3. Install packages
   ```
   uv sync
   ```
4. Activate Virtual Environement
   ```
   source .venv/bin/activate #Unix
   source .venv/Scripts/activate #Windows
   ```

5. You may now run code if you've gotten here. `uv` is a drop in replacement for `pip` 
