import os

def ensure_dirs(base_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
