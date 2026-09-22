import os
from .regex_engine import create_pattern, replace_text, get_match_details
from utils.backup import create_backup

def read_file(file_path: str) -> tuple[str, str]:
    """Reads a text file. Returns (content, error).
    If successful, error is None. If fails, content is None."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read(), None
    except UnicodeDecodeError:
        return None, "Unsupported encoding. Only UTF-8 is supported."
    except PermissionError:
        return None, "Permission denied."
    except Exception as e:
        return None, str(e)

def write_file(file_path: str, content: str) -> str:
    """Writes content to a file. Returns error message or None."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return None
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return str(e)

def process_file_search(file_path: str, pattern_str: str, is_regex: bool, case_insensitive: bool, whole_word: bool = False) -> dict:
    """Performs a search on a single file. Returns result dictionary."""
    content, error = read_file(file_path)
    if error:
        return {'status': 'ERROR', 'error': error, 'matches': 0, 'replacements': 0, 'match_details': []}
        
    try:
        pattern = create_pattern(pattern_str, is_regex, case_insensitive, whole_word)
        matches, match_details = get_match_details(content, pattern)
        return {
            'status': 'SUCCESS',
            'error': None,
            'matches': matches,
            'replacements': 0,
            'original_text': content,
            'match_details': match_details
        }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e), 'matches': 0, 'replacements': 0, 'match_details': []}

def process_file_replace(file_path: str, pattern_str: str, replacement: str, is_regex: bool, case_insensitive: bool, whole_word: bool = False) -> dict:
    """Performs a search and replace on a single file (modifies file). Returns result dictionary."""
    content, error = read_file(file_path)
    if error:
        return {'status': 'ERROR', 'error': error, 'matches': 0, 'replacements': 0, 'match_details': []}
        
    try:
        pattern = create_pattern(pattern_str, is_regex, case_insensitive, whole_word)
        matches, match_details = get_match_details(content, pattern, replacement)
        if matches == 0:
            return {'status': 'SUCCESS', 'error': None, 'matches': 0, 'replacements': 0, 'match_details': []}
            
        new_text, reps = replace_text(content, pattern, replacement)
        
        # Create backup
        try:
            create_backup(file_path)
        except Exception as e:
            return {'status': 'ERROR', 'error': f"Backup failed: {str(e)}", 'matches': matches, 'replacements': 0, 'match_details': []}
            
        # Write modified
        write_err = write_file(file_path, new_text)
        if write_err:
            return {'status': 'ERROR', 'error': f"Write failed: {write_err}", 'matches': matches, 'replacements': 0, 'match_details': []}
            
        return {
            'status': 'SUCCESS',
            'error': None,
            'matches': matches,
            'replacements': reps,
            'match_details': match_details
        }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e), 'matches': 0, 'replacements': 0, 'match_details': []}
