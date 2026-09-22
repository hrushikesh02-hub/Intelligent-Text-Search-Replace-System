# Intelligent Text Search & Replace System

## Problem Statement
Manually searching and replacing text patterns (like emails, phone numbers, dates) across multiple files is time-consuming and error-prone. This application solves the problem by automating the search and replace workflow using Regular Expressions across multiple files at once.

## Objectives
- Regex-based searching
- Automated replacement
- Batch processing
- Custom patterns
- Reporting
- Reduction of manual effort

## Features
- Search text using Regular Expressions or literal text
- Automatically replace matched text across multiple files
- Support for case-insensitive search
- Safe preview of changes before modifying files
- Automatic backup creation (`.bak`) before replacement
- Export reports in TXT, CSV, or JSON formats
- Ready-to-use regex examples (Email, Phone, Date, etc.)

## Technology Stack
- **Python 3**: Core language.
- **PySide6**: Used for the modern Graphical User Interface.
- **re**: Built-in regex engine.
- **pathlib & os**: File and directory operations.
- **csv & json**: Generating structured reports.
- **shutil**: Creating reliable file backups.

## Project Structure
```
IntelligentTextSearchReplace/
│
├── main.py
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── core/
│   ├── __init__.py
│   ├── regex_engine.py
│   ├── file_processor.py
│   └── validator.py
├── reports/
│   ├── __init__.py
│   └── report_generator.py
├── utils/
│   ├── __init__.py
│   └── backup.py
├── sample_files/
│   ├── sample1.txt
│   ├── sample2.txt
│   └── sample3.txt
├── tests/
│   ├── __init__.py
│   ├── test_regex.py
│   └── test_file_processor.py
├── requirements.txt
└── README.md
```

## Installation
```bash
python -m venv venv
```
Windows:
```bash
venv\Scripts\activate
```
Then:
```bash
pip install -r requirements.txt
```

## How to Run
```bash
python main.py
```

## How Regex Search Works
Regular expressions (Regex) are patterns used to match character combinations in strings. 
For example, `\d+` matches one or more digits. The application uses Python's `re.finditer()` to locate all occurrences and highlight matches.

## How Batch Processing Works
When you select multiple files or a folder, the application loops through each file and applies the exact same Regex pattern. It tracks successes and failures independently, ensuring that one problematic file (e.g., permission denied) doesn't stop the entire process.

## Replacement Example
Search:
```
\b\d{10}\b
```
Replacement:
```
[PHONE]
```
Effect: All 10-digit phone numbers in the selected files will be replaced with the literal text "[PHONE]".

## Example Regex Patterns
- **Email**: `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b`
- **10-Digit Phone**: `\b\d{10}\b`
- **Number**: `\b\d+\b`
- **Date**: `\b\d{2}/\d{2}/\d{4}\b`
- **Repeated Word**: `\b(\w+)\s+\1\b`
- **Whitespace**: `\s+`
- **URL**: `https?://[^\s]+`

## Reports
After executing a Search or Replace, you can generate a report summarizing the operation:
- **TXT**: A human-readable text summary.
- **CSV**: A tabular format perfect for Excel.
- **JSON**: Structured data useful for programmatic parsing.

## Backup
Before any replacement is performed, the system copies the original file to a new file with a `.bak` extension. This prevents accidental data loss.

## Testing
```bash
python -m unittest discover
```

## Future Scope
- More file formats (PDF, DOCX)
- Advanced encoding detection
- Search history
- Side-by-side diff view
- Undo functionality
- Larger file optimization
