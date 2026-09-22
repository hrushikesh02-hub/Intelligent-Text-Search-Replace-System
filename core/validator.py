import re
import os
from pathlib import Path

def validate_regex(pattern: str, is_regex: bool = True) -> bool:
    """Validates if a given pattern is a valid regular expression."""
    if not pattern:
        return False
    if not is_regex:
        return True # Literal is always valid
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False

def validate_file_exists(file_path: str) -> bool:
    """Validates if a file exists and is a file."""
    path = Path(file_path)
    return path.exists() and path.is_file()

def validate_text_file(file_path: str) -> bool:
    """Validates if a file has a .txt extension."""
    return str(file_path).lower().endswith('.txt')
