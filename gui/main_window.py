import os
import sys

# Ensure the root directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QLineEdit, QCheckBox, QComboBox, 
    QTextEdit, QFileDialog, QMessageBox, QGroupBox, QSplitter
)
from PySide6.QtCore import Qt

from core.validator import validate_regex
from core.file_processor import process_file_search, process_file_replace
from core.regex_engine import create_pattern, replace_text
from reports.report_generator import generate_txt_report, generate_csv_report, generate_json_report

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intelligent Text Search & Replace")
        self.resize(800, 600)
        
        self.selected_files = []
        self.last_results = None
        
        self.init_ui()
        
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Splitter for Files and Search panels
        top_splitter = QSplitter(Qt.Horizontal)
        
        # --- Left Panel: Files ---
        files_widget = QWidget()
        files_layout = QVBoxLayout(files_widget)
        
        btn_layout = QHBoxLayout()
        self.btn_open_file = QPushButton("Open File")
        self.btn_select_folder = QPushButton("Select Folder")
        self.btn_clear_files = QPushButton("Clear")
        
        self.btn_open_file.clicked.connect(self.on_open_file)
        self.btn_select_folder.clicked.connect(self.on_select_folder)
        self.btn_clear_files.clicked.connect(self.on_clear_files)
        
        btn_layout.addWidget(self.btn_open_file)
        btn_layout.addWidget(self.btn_select_folder)
        btn_layout.addWidget(self.btn_clear_files)
        
        self.list_files = QListWidget()
        
        files_layout.addWidget(QLabel("Selected Files:"))
        files_layout.addLayout(btn_layout)
        files_layout.addWidget(self.list_files)
        
        top_splitter.addWidget(files_widget)
        
        # --- Right Panel: Search & Replace ---
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        
        self.combo_examples = QComboBox()
        self.combo_examples.addItem("Regex Examples (Select one)")
        self.combo_examples.addItem("Email|\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b")
        self.combo_examples.addItem("10-Digit Phone|\\b\\d{10}\\b")
        self.combo_examples.addItem("Number|\\b\\d+\\b")
        self.combo_examples.addItem("Date (dd/mm/yyyy)|\\b\\d{2}/\\d{2}/\\d{4}\\b")
        self.combo_examples.addItem("Repeated Word|\\b(\\w+)\\s+\\1\\b")
        self.combo_examples.currentIndexChanged.connect(self.on_example_selected)
        
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Enter search pattern...")
        
        self.txt_replace = QLineEdit()
        self.txt_replace.setPlaceholderText("Enter replacement text...")
        
        self.chk_regex = QCheckBox("Regular Expression")
        self.chk_regex.setChecked(True)
        self.chk_case = QCheckBox("Case Insensitive")
        self.chk_word = QCheckBox("Whole Word")
        
        search_layout.addWidget(self.combo_examples)
        search_layout.addWidget(QLabel("Search Pattern:"))
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(QLabel("Replacement Text:"))
        search_layout.addWidget(self.txt_replace)
        search_layout.addWidget(self.chk_regex)
        search_layout.addWidget(self.chk_case)
        search_layout.addWidget(self.chk_word)
        
        action_layout = QHBoxLayout()
        self.btn_search = QPushButton("Search")
        self.btn_preview = QPushButton("Preview")
        self.btn_replace = QPushButton("Replace")
        
        self.btn_search.clicked.connect(self.on_search)
        self.btn_preview.clicked.connect(self.on_preview)
        self.btn_replace.clicked.connect(self.on_replace)
        
        action_layout.addWidget(self.btn_search)
        action_layout.addWidget(self.btn_preview)
        action_layout.addWidget(self.btn_replace)
        
        search_layout.addLayout(action_layout)
        search_layout.addStretch()
        
        top_splitter.addWidget(search_widget)
        
        # Give even space to both
        top_splitter.setSizes([400, 400])
        
        # --- Bottom Panel: Results ---
        self.txt_results = QTextEdit()
        self.txt_results.setReadOnly(True)
        
        bottom_layout = QHBoxLayout()
        self.btn_report = QPushButton("Generate Report")
        self.btn_report.clicked.connect(self.on_generate_report)
        
        self.btn_clear_results = QPushButton("Clear Results")
        self.btn_clear_results.clicked.connect(self.on_clear_results)
        
        bottom_layout.addWidget(self.btn_report)
        bottom_layout.addWidget(self.btn_clear_results)
        bottom_layout.addStretch()
        
        main_layout.addWidget(top_splitter, 1)
        main_layout.addWidget(QLabel("Results / Preview:"))
        main_layout.addWidget(self.txt_results, 1)
        main_layout.addLayout(bottom_layout)
        
    def on_example_selected(self, index):
        if index > 0:
            text = self.combo_examples.itemText(index)
            pattern = text.split("|")[1]
            self.txt_search.setText(pattern)
            self.chk_regex.setChecked(True)

    def on_open_file(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open Text Files", "", "Text Files (*.txt);;All Files (*)")
        if files:
            for f in files:
                if f not in self.selected_files:
                    self.selected_files.append(f)
                    self.list_files.addItem(os.path.basename(f))

    def on_select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            for f in os.listdir(folder):
                if f.lower().endswith(".txt"):
                    full_path = os.path.join(folder, f)
                    # Normalize slashes for consistency
                    full_path = full_path.replace("\\", "/")
                    if full_path not in self.selected_files:
                        self.selected_files.append(full_path)
                        self.list_files.addItem(f)

    def on_clear_files(self):
        self.selected_files.clear()
        self.list_files.clear()
        self.txt_results.clear()
        self.last_results = None

    def on_clear_results(self):
        self.txt_results.clear()
        self.last_results = None

    def validate_inputs(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Warning", "Please select at least one text file.")
            return False
            
        pattern = self.txt_search.text()
        if not pattern:
            QMessageBox.warning(self, "Warning", "Search pattern cannot be empty.")
            return False
            
        if self.chk_regex.isChecked():
            if not validate_regex(pattern, True):
                QMessageBox.warning(self, "Warning", "Invalid Regular Expression.\nPlease check your pattern and try again.")
                return False
                
        return True

    def on_search(self):
        if not self.validate_inputs():
            return
            
        pattern = self.txt_search.text()
        is_regex = self.chk_regex.isChecked()
        is_case = self.chk_case.isChecked()
        is_word = self.chk_word.isChecked()
        
        results = {
            'operation': 'SEARCH',
            'search_pattern': pattern,
            'replacement': '',
            'files_processed': 0,
            'total_matches': 0,
            'total_replacements': 0,
            'status': 'SUCCESS',
            'files': []
        }
        
        output = "RESULTS\n========================================\n\n"
        
        for f in self.selected_files:
            res = process_file_search(f, pattern, is_regex, is_case, is_word)
            results['files_processed'] += 1
            results['total_matches'] += res['matches']
            
            f_info = {
                'file_name': f,
                'matches': res['matches'],
                'replacements': 0,
                'status': res['status'],
                'error': res['error'],
                'match_details': res.get('match_details', [])
            }
            results['files'].append(f_info)
            
            fname = os.path.basename(f)
            if res['status'] == 'SUCCESS':
                output += f"✓ {fname}\n"
                if res['matches'] > 0:
                    output += "---------------------------------------------------------------\n"
                    output += f"{'File':<25} {'Line':<7} {'Matched Text'}\n"
                    output += "---------------------------------------------------------------\n"
                    for m in res.get('match_details', []):
                        m_text = m['matched_text'].replace('\n', '\\n')
                        if len(m_text) > 30: m_text = m_text[:27] + "..."
                        f_short = fname if len(fname) <= 24 else fname[:21] + "..."
                        output += f"{f_short:<25} {m['line']:<7} {m_text}\n"
                    output += "---------------------------------------------------------------\n"
                output += f"  Matches: {res['matches']}\n  Replacements: 0\n  Status: SUCCESS\n\n"
            else:
                output += f"✗ {fname}\n  Matches: 0\n  Replacements: 0\n  Status: ERROR\n  Reason: {res['error']}\n\n"
                results['status'] = 'WITH_ERRORS'
                
        output += f"Files Processed : {results['files_processed']}\n"
        output += f"Total Matches   : {results['total_matches']}\n"
        output += f"Total Replaced  : 0\n\n"
        output += f"Status          : {results['status']}\n"
        
        self.txt_results.setText(output)
        self.last_results = results

    def on_preview(self):
        if not self.validate_inputs():
            return
            
        pattern = self.txt_search.text()
        replacement = self.txt_replace.text()
        is_regex = self.chk_regex.isChecked()
        is_case = self.chk_case.isChecked()
        is_word = self.chk_word.isChecked()
        
        output = "PREVIEW\n========================================\n\n"
        total_matches = 0
        total_reps = 0
        
        for f in self.selected_files:
            from core.file_processor import read_file
            from core.regex_engine import get_match_details
            content, error = read_file(f)
            fname = os.path.basename(f)
            
            if error:
                output += f"FILE: {fname}\nError: {error}\n"
                output += "-"*40 + "\n\n"
                continue
                
            pat = create_pattern(pattern, is_regex, is_case, is_word)
            matches, match_details = get_match_details(content, pat, replacement)
            
            if matches > 0:
                output += f"File: {fname}\n\n"
                for i, m in enumerate(match_details, 1):
                    output += f"Match #{i}\n"
                    output += f"Line: {m['line']}\n"
                    output += f"Position: {m['position']}\n"
                    output += f"Original     : {m['matched_text']}\n"
                    output += f"Replacement  : {m.get('replacement', '')}\n\n"
                    
                total_matches += matches
                total_reps += matches # Preview assumes 1 rep per match
            else:
                output += f"File: {fname} (No matches)\n\n"
                
        output += f"Total Matches: {total_matches}\n"
        output += f"Total Replacements: {total_reps}\n\n"
        output += "No files were modified.\n"
                
        self.txt_results.setText(output)
        self.last_results = None # Preview doesn't generate a report

    def on_replace(self):
        if not self.validate_inputs():
            return
            
        pattern = self.txt_search.text()
        replacement = self.txt_replace.text()
        is_regex = self.chk_regex.isChecked()
        is_case = self.chk_case.isChecked()
        is_word = self.chk_word.isChecked()
        
        if not replacement:
            reply = QMessageBox.question(self, "Confirm Empty Replacement", 
                                        "The replacement field is empty.\nMatched text will be removed.\nContinue?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
                
        # Calculate counts
        files_to_modify = 0
        total_matches = 0
        total_reps_expected = 0
        
        for f in self.selected_files:
            res = process_file_search(f, pattern, is_regex, is_case, is_word)
            if res['status'] == 'SUCCESS' and res['matches'] > 0:
                files_to_modify += 1
                total_matches += res['matches']
                
                pat = create_pattern(pattern, is_regex, is_case, is_word)
                _, reps = replace_text(res['original_text'], pat, replacement)
                total_reps_expected += reps
                
        if files_to_modify == 0:
            QMessageBox.information(self, "Information", "No matches found in selected files.")
            return
            
        msg = f"Files to modify: {files_to_modify}\nTotal matches: {total_matches}\nTotal replacements: {total_reps_expected}\n\nA backup (.bak) will be created before modification.\n\nDo you want to continue?"
        reply = QMessageBox.question(self, "Confirm Replacement", msg, QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return
            
        # Execute Replacement
        results = {
            'operation': 'REPLACE',
            'search_pattern': pattern,
            'replacement': replacement,
            'files_processed': 0,
            'total_matches': 0,
            'total_replacements': 0,
            'status': 'SUCCESS',
            'files': []
        }
        
        output_details = ""
        
        for f in self.selected_files:
            res = process_file_replace(f, pattern, replacement, is_regex, is_case, is_word)
            results['files_processed'] += 1
            results['total_matches'] += res['matches']
            results['total_replacements'] += res['replacements']
            
            f_info = {
                'file_name': f,
                'matches': res['matches'],
                'replacements': res['replacements'],
                'status': res['status'],
                'error': res['error'],
                'match_details': res.get('match_details', [])
            }
            results['files'].append(f_info)
            
            fname = os.path.basename(f)
            if res['status'] == 'SUCCESS':
                output_details += f"File: {fname}\n\n"
                if res['matches'] > 0:
                    for i, m in enumerate(res.get('match_details', []), 1):
                        output_details += f"Match #{i}\nLine: {m['line']}\nChanged:\n{m['matched_text']}\n        ↓\n{m.get('replacement', '')}\n\n"
                output_details += f"Total Replacements: {res['replacements']}\nBackup Created: YES\nStatus: SUCCESS\n\n"
                output_details += "========================================\n\n"
            else:
                output_details += f"File: {fname}\nStatus: ERROR\nReason: {res['error']}\n\n========================================\n\n"
                results['status'] = 'WITH_ERRORS'
                
        output_header = f"REPLACEMENT RESULTS\n========================================\n\n"
        
        summary = f"Files Processed : {results['files_processed']}\n"
        summary += f"Total Matches   : {results['total_matches']}\n"
        summary += f"Total Replaced  : {results['total_replacements']}\n\n"
        summary += f"Status          : {results['status']}\n\n"
        
        self.txt_results.setText(output_header + output_details + summary)
        self.last_results = results
        
    def on_generate_report(self):
        if not self.last_results:
            QMessageBox.warning(self, "Warning", "Please perform a Search or Replace operation before generating a report.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Text Files (*.txt);;CSV Files (*.csv);;JSON Files (*.json)")
        if not file_path:
            return
            
        ext = file_path.lower()
        success = False
        if ext.endswith(".txt"):
            success = generate_txt_report(file_path, self.last_results)
        elif ext.endswith(".csv"):
            success = generate_csv_report(file_path, self.last_results)
        elif ext.endswith(".json"):
            success = generate_json_report(file_path, self.last_results)
        else:
            # Default to txt
            success = generate_txt_report(file_path + ".txt", self.last_results)
            
        if success:
            QMessageBox.information(self, "Success", "Report generated successfully.")
        else:
            QMessageBox.critical(self, "Error", "Failed to generate report.")
