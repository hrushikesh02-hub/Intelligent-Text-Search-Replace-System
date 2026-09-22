import json
import csv
import os

def generate_txt_report(filepath: str, data: dict) -> bool:
    """Generates a .txt report."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("========================================\n")
            f.write("SEARCH & REPLACE REPORT\n")
            f.write("========================================\n\n")
            
            f.write("Operation:\n")
            f.write(f"{data.get('operation', 'UNKNOWN')}\n\n")
            
            f.write("Search Pattern:\n")
            f.write(f"{data.get('search_pattern', '')}\n\n")
            
            replacement = data.get('replacement', '')
            f.write("Replacement:\n")
            f.write(f"{replacement if replacement else 'Not specified'}\n\n")
            
            f.write("Files Processed:\n")
            f.write(f"{data.get('files_processed', 0)}\n\n")
            
            f.write("Total Matches:\n")
            f.write(f"{data.get('total_matches', 0)}\n\n")
            
            f.write("Total Replacements:\n")
            f.write(f"{data.get('total_replacements', 0)}\n\n")
            
            f.write("----------------------------------------\n")
            f.write("FILE RESULTS\n")
            f.write("----------------------------------------\n\n")
            
            for file_info in data.get('files', []):
                fname = os.path.basename(file_info['file_name'])
                f.write("File:\n")
                f.write(f"{fname}\n\n")
                
                f.write("Status:\n")
                f.write(f"{file_info['status']}\n\n")
                
                if file_info['status'] == 'ERROR':
                    f.write("Error:\n")
                    f.write(f"{file_info.get('error', '')}\n\n")
                
                f.write("Matches:\n")
                f.write(f"{file_info['matches']}\n\n")
                
                f.write("Replacements:\n")
                f.write(f"{file_info['replacements']}\n\n")
                
                match_details = file_info.get('match_details', [])
                if match_details:
                    f.write("----------------------------------------\n")
                    f.write("MATCH DETAILS\n")
                    f.write("----------------------------------------\n\n")
                    
                    for i, m in enumerate(match_details, 1):
                        f.write(f"Match #{i}\n")
                        f.write(f"Matched Text : {m['matched_text']}\n")
                        f.write(f"Line         : {m['line']}\n")
                        f.write(f"Position     : {m['position']}\n\n")
                        
                        f.write(f"Original     : {m['matched_text']}\n")
                        rep = m.get('replacement', '')
                        if rep:
                            f.write(f"Replacement  : {rep}\n")
                        f.write("\n")
                        
            f.write("----------------------------------------\n")
            f.write("END OF REPORT\n")
            f.write("----------------------------------------\n")
            
        return True
    except Exception as e:
        print(f"Failed to generate TXT report: {e}")
        return False

def generate_csv_report(filepath: str, data: dict) -> bool:
    """Generates a .csv report."""
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['File', 'Operation', 'Search Pattern', 'Replacement', 'Match Count', 'Replacement Count', 'Status', 'Line', 'Position', 'Matched Text', 'Replacement Text'])
            
            op = data.get('operation', '')
            pat = data.get('search_pattern', '')
            rep = data.get('replacement', '')
            
            for file_info in data.get('files', []):
                fname = os.path.basename(file_info['file_name'])
                matches = file_info['matches']
                reps = file_info['replacements']
                status = file_info['status']
                
                match_details = file_info.get('match_details', [])
                if match_details:
                    for m in match_details:
                        writer.writerow([
                            fname, op, pat, rep, matches, reps, status,
                            m['line'], m['position'], m['matched_text'], m.get('replacement', '')
                        ])
                else:
                    writer.writerow([
                        fname, op, pat, rep, matches, reps, status,
                        '', '', '', ''
                    ])
        return True
    except Exception as e:
        print(f"Failed to generate CSV report: {e}")
        return False

def generate_json_report(filepath: str, data: dict) -> bool:
    """Generates a .json report."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Failed to generate JSON report: {e}")
        return False
