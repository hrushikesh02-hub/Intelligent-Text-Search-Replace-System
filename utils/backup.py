import os
import shutil
from pathlib import Path

def create_backup(file_path: str) -> str:
    """Creates a backup of a file appending .bak extension.
    Returns the backup path.
    Raises exception if backup fails."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    backup_path = str(path) + ".bak"
    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        raise OSError(f"Failed to create backup for {file_path}: {e}")
