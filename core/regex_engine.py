import re

def create_pattern(pattern_str: str, is_regex: bool, case_insensitive: bool, whole_word: bool = False) -> re.Pattern:
    """Creates a compiled regex pattern."""
    flags = 0
    if case_insensitive:
        flags |= re.IGNORECASE
        
    if not is_regex:
        pattern_str = re.escape(pattern_str)
        
    if whole_word:
        pattern_str = fr"\b{pattern_str}\b"
        
    return re.compile(pattern_str, flags)

def get_match_details(text: str, pattern: re.Pattern, replacement: str = None) -> tuple[int, list]:
    """
    Searches text for matches and extracts detailed info.
    Returns a tuple of (match_count, list_of_match_dicts).
    """
    matches = []
    for match in pattern.finditer(text):
        start = match.start()
        
        # Calculate line number (1-based)
        line = text.count('\n', 0, start) + 1
        
        # Calculate character position in line (1-based)
        last_newline = text.rfind('\n', 0, start)
        position = start - last_newline if last_newline != -1 else start + 1
        
        matched_text = match.group()
        
        detail = {
            'matched_text': matched_text,
            'line': line,
            'position': position,
        }
        
        if replacement is not None:
            # Determine the replacement string for this specific match.
            # Using re.sub on just the matched text will work unless we have complex lookbehinds,
            # but using match.expand(replacement) is the proper way.
            try:
                replaced_text = match.expand(replacement)
            except re.error:
                # Fallback if expand fails (e.g., bad group ref)
                replaced_text, _ = pattern.subn(replacement, matched_text)
            detail['replacement'] = replaced_text
            
        matches.append(detail)
        
    return len(matches), matches

def count_matches(text: str, pattern: re.Pattern) -> int:
    """Counts the number of matches in a text."""
    # We could still use findall, but if called, it's fine.
    return len(pattern.findall(text))

def replace_text(text: str, pattern: re.Pattern, replacement: str) -> tuple[str, int]:
    """Replaces matched text.
    Returns a tuple of (new_text, replacement_count)."""
    new_text, count = pattern.subn(replacement, text)
    return new_text, count
