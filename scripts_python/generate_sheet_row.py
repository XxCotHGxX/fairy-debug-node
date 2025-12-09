import argparse
import json
import os
import sys
import csv
import io
from pathlib import Path

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def read_jsonl(path):
    content = read_file(path)
    if content:
        try:
            # Try parsing as a single JSON object first (as seen in examples)
            return json.loads(content)
        except json.JSONDecodeError:
            # If that fails, try parsing line by line (traditional JSONL)
            lines = content.strip().split('\n')
            if lines:
                try:
                    return json.loads(lines[-1]) # Return the last line as it usually contains the result
                except json.JSONDecodeError:
                    return None
    return None

def generate_row_data(comp_id, row_id, step, root_path=".", proposed_analysis=""):
    root = Path(root_path)
    
    # Define file paths
    code_path = root / "code" / f"{comp_id}_{row_id}_{step}.py"
    log_path = root / "logs" / row_id / f"{step}.jsonl"
    bugfix_path = root / "logs" / row_id / f"step{step}_{row_id}_bugfix.txt"
    fixed_code_path = root / "code" / f"{comp_id}_{row_id}_{step+1}.py"
    fixed_log_path = root / "logs" / row_id / f"{step+1}.jsonl"

    # Read contents
    code_content = read_file(code_path) or ""
    log_data = read_jsonl(log_path)
    bugfix_content = read_file(bugfix_path) or ""
    fixed_code_content = read_file(fixed_code_path) or ""
    fixed_log_data = read_jsonl(fixed_log_path)

    # Process Log Data (Step N)
    term_out = "[]"
    exec_time = ""
    output_logs = ""
    bug_confirmed = "FALSE"
    
    if log_data:
        term_out = json.dumps(log_data.get("stdout", []), indent=None)
        exec_time = str(log_data.get("exec_time", ""))
        output_logs = json.dumps(log_data, indent=2)
        if not log_data.get("success", False):
            bug_confirmed = "TRUE"

    # Process Bugfix Data
    revised_analysis = ""
    revised_plan = ""
    if bugfix_content:
        parts = bugfix_content.split("**Bug Fix Plan**")
        revised_analysis = parts[0].strip()
        if len(parts) > 1:
            revised_plan = "**Bug Fix Plan**" + parts[1]

    # Process Fixed Log Data (Step N+1)
    output_logs_after_fix = ""
    bug_fixed = "TRUE" # Hardcoded as per user request
    
    if fixed_log_data:
        output_logs_after_fix = json.dumps(fixed_log_data, indent=2)

    # Derived Columns
    if step > 0:
        bug_confirmed = "TRUE"
        proposed_debug_analysis_accurate = "N/A"
        initial_bug_reproducible = "N/A"
        bug_fixed = "TRUE"
    else:
        # Step 0 Logic
        # Try to get score from LM Studio
        try:
            # Add tools to path to import client
            tools_dir = root / "tools"
            if str(tools_dir) not in sys.path:
                sys.path.append(str(tools_dir))
            
            import lm_studio_client
            
            # We need the original analysis from the spreadsheet guide or similar
            # But since we don't have easy access to the spreadsheet here, we might need to rely on 
            # what's available. 
            # Ideally, this script would take the 'proposed_analysis' as an argument.
            # For now, we'll use a placeholder or try to extract it if possible.
            # Since we can't easily get the *client's* proposed analysis from the file system alone
            # (it's in the spreadsheet), we might have to skip this or ask the user to provide it.
            
            # HOWEVER, looking at the previous hardcoded logic, it seems we just want to automate the *decision*.
            # If we don't have the analysis text, we can't score it.
            # Let's check if we can pass it in.
            
            # For this implementation, we will default to "1" but print a message 
            # that we need the analysis text to be accurate.
            # Wait, the user wants this automated. 
            # The 'proposed_debug_analysis_accurate' is about the *client's* analysis.
            # That analysis is usually in the 'analysis' column of the spreadsheet (Column E).
            # This script doesn't seem to read the spreadsheet.
            
            # Let's look at how we can get it. 
            # If we can't get it, we must fallback to "1".
            
            # Check if analysis was passed directly (from UI)
            if proposed_analysis:
                print(f"Using analysis passed from UI...")
            else:
                # Fallback to file search if not passed
                analysis_path = root / "logs" / row_id / "analysis_0.json"
                if analysis_path.exists():
                    try:
                        with open(analysis_path, 'r', encoding='utf-8') as f:
                            analysis_data = json.load(f)
                            proposed_analysis = analysis_data.get("analysis", "") or analysis_data.get("content", "")
                    except:
                        pass
            
            if proposed_analysis:
                print(f"Querying LM Studio for score on Step 0...")
                proposed_debug_analysis_accurate = lm_studio_client.get_analysis_score(
                    code_content, 
                    output_logs, 
                    proposed_analysis
                )
            else:
                print("No proposed analysis found. Defaulting score to 1.")
                proposed_debug_analysis_accurate = "1" # Default if no analysis found
                
        except Exception as e:
            print(f"LM Studio integration failed: {e}")
            proposed_debug_analysis_accurate = "1" # Fallback

        initial_bug_reproducible = "TRUE" if bug_confirmed == "TRUE" else "FALSE"
        # bug_fixed is already TRUE from above
    
    all_bugs_fixed = bug_fixed # Simplified logic

    # Prepare row data dictionary
    row_dict = {
        "code": code_content,
        "_term_out": term_out,
        "exec_time": exec_time,
        "output_logs": output_logs,
        "bug_confirmed": bug_confirmed,
        "proposed_debug_analysis_accurate": proposed_debug_analysis_accurate,
        "initial_bug_reproducible": initial_bug_reproducible,
        "bug_fixed": bug_fixed,
        "all_bugs_fixed": all_bugs_fixed,
        "revised_analysis": revised_analysis,
        "revised_plan": revised_plan,
        "debug_step": str(step),
        "current_debug_code": fixed_code_content,
        "output_logs_after_fix": output_logs_after_fix
    }

    # Prepare row list for CSV writer
    row_list = [
        row_dict["code"],
        row_dict["_term_out"],
        row_dict["exec_time"],
        row_dict["output_logs"],
        row_dict["bug_confirmed"],
        row_dict["proposed_debug_analysis_accurate"],
        row_dict["initial_bug_reproducible"],
        row_dict["bug_fixed"],
        row_dict["all_bugs_fixed"],
        row_dict["revised_analysis"],
        row_dict["revised_plan"],
        row_dict["debug_step"],
        row_dict["current_debug_code"],
        row_dict["output_logs_after_fix"]
    ]

    # Use csv module for robust TSV generation
    output = io.StringIO()
    # Use excel-tab dialect which is standard for TSV
    # lineterminator='\n' ensures we don't get extra \r that might confuse some clipboards
    writer = csv.writer(output, dialect='excel-tab', lineterminator='\n')
    
    row_list = [
        row_dict["code"],
        row_dict["_term_out"],
        row_dict["exec_time"],
        row_dict["output_logs"],
        row_dict["bug_confirmed"],
        row_dict["proposed_debug_analysis_accurate"],
        row_dict["initial_bug_reproducible"],
        row_dict["bug_fixed"],
        row_dict["all_bugs_fixed"],
        row_dict["revised_analysis"],
        row_dict["revised_plan"],
        row_dict["debug_step"],
        row_dict["current_debug_code"],
        row_dict["output_logs_after_fix"]
    ]
    
    writer.writerow(row_list)
    raw_string = output.getvalue().strip() # Remove the trailing newline added by writerow
    
    return row_dict, raw_string

def main():
    parser = argparse.ArgumentParser(description="Generate Google Sheets row from debug artifacts")
    parser.add_argument("competition_id", help="Competition ID")
    parser.add_argument("datarow_id", help="Datarow ID")
    parser.add_argument("step", type=int, help="Debug step number")
    parser.add_argument("--root", default=".", help="Root directory of the project")

    args = parser.parse_args()

    _, raw_string = generate_row_data(args.competition_id, args.datarow_id, args.step, args.root)
    print(raw_string)

if __name__ == "__main__":
    main()
