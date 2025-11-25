# Model Interaction Protocol & Instructions

## Project Overview
This is a debugging workflow system for ML competition code submissions. The goal is to run client-provided buggy code on a GPU cluster, identify bugs, fix them, and document the process in a structured spreadsheet format.

## 1. Primary Goal
The objective is to run the provided client code on the GPU cluster for **6 minutes (600 seconds)** without it throwing an error.
- If it runs for >6 minutes, it is considered "Passed" (No Repro).
- If it throws an error before that, we must debug and fix it.

## 2. Environment & Tools

### Required Setup
- **VPN**: Must be **ON** to bypass ISP blocks on `ngrok`.
- **Credentials**: Stored in `.env` (`TOKEN`, `SERVER_URL`, `LM_STUDIO_URL` - optional, defaults to localhost:1234).
- **LM Studio**: Local model server running (default: `http://localhost:1234/v1/chat/completions`).
- **Submission Tool**: 
  - Use the **Fairy Debugger UI** (running on `localhost:8000` via `python tools/fairy_ui/server.py`).
  - It uses `gpu_submit.sh` under the hood.
  - **Live Terminal**: Watch the UI for "Status: Running on GPU..."

### File Structure
```
fairy-debug-node/
├── code/                    # Python files to debug (format: <competition_id>_<datarow_id>_<debug_step>.py)
├── logs/                    # Execution logs
│   └── <datarow_id>/
│       ├── <debug_step>.jsonl      # Final results
│       └── <debug_step>.raw.log   # Terminal output
├── analysis/                # Analysis files (optional)
├── tools/fairy_ui/          # Web UI application
│   ├── server.py            # FastAPI backend
│   └── templates/
│       └── index.html       # Frontend UI
├── gpu_submit.sh            # Submission script (DO NOT modify unnecessarily)
└── .env                     # Credentials
```

### File Naming Convention
- **Format**: `<competition_id>_<datarow_id>_<debug_step>.py`
- **Example**: `iwildcam-2020-fgvc7_86b26f9301124e8289d9ace20dba6162_0.py`
- **Parts**:
  - `competition_id`: The Kaggle competition name
  - `datarow_id`: Unique identifier for this data row
  - `debug_step`: 0 = initial buggy code, 1 = first fix, 2 = second fix, etc.

## 3. Spreadsheet Column Requirements

The user fills out a Google Sheet with these exact column names (case-sensitive):

| Column Name | Type | Description |
|-------------|------|-------------|
| `datarow_id` | String | Unique identifier |
| `competition_id` | String | Competition name |
| `original_plan` | Text | Client's initial bug analysis |
| `analysis` | Text | Client's original analysis |
| `code` | Text | Original buggy code |
| `output_logs` | JSON | Initial error log |
| `bug_confirmed` | Boolean | TRUE if error occurred |
| `proposed_debug_analysis_accurate` | Integer | 0, 1, or 2 (accuracy score) |
| `initial_bug_reproducible` | Boolean | TRUE if client's bug was reproduced |
| `bug_fixed` | Boolean | TRUE if fixed successfully |
| `all_bugs_fixed` | Boolean | TRUE only on final step |
| `revised_analysis` | Text | Single paragraph, 3rd person |
| `revised_plan` | Text | Markdown format: **Bug Fix Plan** + numbered list |
| `debug_step` | Integer | 0, 1, 2, etc. |
| `current_debug_code` | Text | The fixed code (with bug fix applied) |
| `output_logs_after_fix` | JSON | Log from successful run |

## 4. Scenario A: Code Runs Successfully (>6 Minutes)
If the code runs for over 6 minutes without crashing (even if it's just training epochs endlessly), **STOP** the job (Ctrl+C or Cancel in UI) and fill the spreadsheet exactly as follows:

| Column | Value |
| :--- | :--- |
| **revised_analysis** | "The code executed successfully for over 6 minutes without throwing any errors." |
| **revised_plan** | `N/A` |
| **bug_confirmed** | `FALSE` |
| **bug_fixed** | `TRUE` |
| **proposed_debug_analysis_accurate** | `0` |
| **initial_bug_reproducible** | `FALSE` |
| **all_bugs_fixed** | `TRUE` |
| **current_debug_code** | `N/A` |
| **output_logs_after_fix** | `N/A` |

*Note: Do NOT theorize about why it didn't fail (e.g., don't mention environment). Just state facts.*

## 5. Scenario B: Code Throws an Error (Actual Bug)

### Workflow
1. **Analyze**: Identify the root cause from the log file.
2. **Plan**: Create a numbered **Bug Fix Plan** (strict format).
3. **Fix**: Modify the Python file (minimal changes only).
4. **Verify**: Re-run on GPU.
5. **Document**: Fill spreadsheet with all required fields.

### revised_plan Format
```markdown
**Bug Fix Plan**
1. Line 105: Replace `.toarray()` with `np.asarray()` to handle both dense matrix and sparse matrix outputs safely.
2. Line 106: Ensure centroid is converted to 1-D array using `.A.ravel()` before dot product.
```

**CRITICAL**: 
- Must start with `**Bug Fix Plan**` (with asterisks)
- Numbered list (1., 2., 3.)
- NO code blocks (```python) inside the plan
- NO triple backticks anywhere
- Each item must include specific line numbers

### revised_analysis Format
- Single paragraph (2-4 sentences)
- Third person only ("The code fails..." NOT "I found...")
- Include: exact error message, line number, root cause, technical explanation
- Mention specific line numbers and code constructs

### Spreadsheet Values
- **revised_analysis**: Single detailed paragraph (3rd person).
- **revised_plan**: The numbered plan above.
- **bug_confirmed**: `TRUE`
- **bug_fixed**: `TRUE` (if verification passes).
- **proposed_debug_analysis_accurate**: 
    - `2` if client was right.
    - `1` if client was close/right location but wrong fix.
    - `0` if client was totally wrong.
- **initial_bug_reproducible**: `TRUE` (if you saw the error).
- **output_logs_after_fix**: Paste content of the final `.jsonl` log.
- **current_debug_code**: Paste the full fixed Python code.

## 6. Fairy Debugger UI

### Purpose
Web-based interface (`localhost:8000`) that automates:
- File creation with correct naming
- GPU job submission
- Live terminal output streaming
- AI-generated analysis (via LM Studio)
- Fixed code display

### Key Features
- **Input Fields**: Competition ID, Datarow ID, Debug Step, Code, Original Plan
- **Action Buttons**: 
  - "Run on GPU" - Submits job
  - "Stop" - Cancels running job
  - "No Repro (>6m)" - Marks as passed without error
- **Output Panes**:
  - Verification grid (5 boolean/ternary values with exact column names)
  - `revised_analysis` (with copy button)
  - `revised_plan` (with copy button)
  - `current_debug_code` (shows fixed code from `debug_step + 1` file)
  - `output_logs_after_fix` (final JSON log)

### LM Studio Integration
- **Model**: Uses local LM Studio model (default: `qwen3-coder-30b`)
- **Endpoint**: `http://localhost:1234/v1/chat/completions` (configurable via `.env`)
- **Prompt**: Simplified, focused on JSON output
- **Temperature**: 0.1 (for consistent JSON)
- **Max Tokens**: 1500 (to prevent incomplete responses)
- **Output**: Must return valid JSON with 7 required fields

### Required JSON Fields from LM Studio
```json
{
  "revised_analysis": "...",
  "revised_plan": "...",
  "bug_confirmed": true/false,
  "bug_fixed": true/false,
  "proposed_debug_analysis_accurate": 0/1/2,
  "initial_bug_reproducible": true/false,
  "all_bugs_fixed": true/false
}
```

**Note**: The model should NOT generate `fixed_code` field. Fixed code is created manually by the user and stored in `code/<competition_id>_<datarow_id>_<debug_step+1>.py`.

## 7. File Management & Skipping
- **Automatic Skipping**: `gpu_submit.sh` skips files if a log exists in `logs/<datarow_id>/<debug_step>.jsonl`.
- **Manual Skip**: To force the system to skip a file (e.g., after a >6 min run), create a placeholder log file:
  ```bash
  echo '{"status":"skipped"}' > logs/<datarow_id>/<debug_step>.jsonl
  ```
- **Re-running**: The UI automatically deletes the specific log file for the step you are running to force a re-run.
- **GPU Conservation**: The UI does NOT use `--force` flag to avoid re-submitting all files. Only the current file is submitted.

## 8. Code Styling Rules
- Generated code should be messy but runnable.
- Comments should be useful but include occasional typos, spacing errors, and "cool slang".
- **Do not** leave "AI signatures" (perfect grammar, overly formal comments).
- **Bug Fix Comments**: When creating fixed code files, add comments like `#***BUG FIX***` or `# FIX: ...` to mark the changes.

## 9. Log Format Requirements

### Expected Log Structure
The `gpu_submit.sh` script generates logs in `logs/<datarow_id>/<debug_step>.jsonl` with this structure:
```json
{
  "success": true/false,
  "exit_code": 0/1,
  "timed_out": false,
  "exec_time": 2.55,
  "valid_solution": true/false,
  "validation_fitness": null,
  "test_fitness": 0.93412,
  "error_output": [],
  "stdout": [
    "Line 1 of output",
    "Line 2 of output",
    "Execution time: 2 seconds (time limit is 6 minutes)."
  ]
}
```

**Important**: The `stdout` field should be an array of strings (not a single string with `\n`). The `gpu_submit.sh` script handles this formatting.

## 10. Common Issues & Solutions

### Issue: LM Studio generates duplicate/incomplete JSON
**Solution**: The parser extracts the FIRST complete JSON object. If issues persist, check:
- Temperature too high (should be 0.1)
- Max tokens too high (should be 1500)
- Prompt too complex (should be simplified)

### Issue: Missing fields showing "-" in UI
**Solution**: The prompt now requires all 7 fields. If still missing, the server auto-fills defaults:
- Booleans → `false`
- `proposed_debug_analysis_accurate` → `0`
- Strings → `""`

### Issue: Fixed code not appearing
**Solution**: 
- Fixed code is created MANUALLY by the user (not generated by LM Studio)
- The UI loads code from `code/<competition_id>_<datarow_id>_<debug_step+1>.py`
- User creates the fixed file after getting the analysis

### Issue: VPN/Network errors
**Solution**: 
- Ensure VPN is ON
- Check `SERVER_URL` in `.env` is correct
- Verify `ngrok` tunnel is active (if using ngrok)

## 11. User Expectations

### Critical Rules
1. **Minimal Fixes**: Only fix the specific bug. Do NOT overhaul the code.
2. **One Bug Per Step**: If a NEW unrelated bug appears, create a NEW row with incremented `debug_step`.
3. **Documentation First**: Always fill spreadsheet cells BEFORE moving to next bug.
4. **No Theorizing**: For "No Repro" cases, just state facts. Don't explain why it didn't fail.
5. **Column Names**: Must match spreadsheet EXACTLY (case-sensitive).
6. **N/A Usage**: Use `N/A` for empty fields in "No Repro" scenarios, not blank.
7. **Single Row Per Fix**: If a bug can be fixed with one change, use ONE row (not multiple rows).

### Workflow Priority
1. Run code on GPU
2. Analyze error (if any)
3. Generate analysis via LM Studio (via UI)
4. Create fixed code file manually with incremented `debug_step`
5. Fill spreadsheet with all required fields
6. Move to next step/row

## 12. LM Studio Prompt Structure

The prompt sent to LM Studio is:
- **Simplified** (not verbose)
- **Focused** on JSON output
- **Includes**: Context, error log (truncated to 2000 chars), code excerpt (truncated to 3000 chars), clear JSON example
- **Emphasizes**: "Return ONLY the JSON, nothing else"
- **Temperature**: 0.1 for consistency
- **Max Tokens**: 1500 to prevent incomplete responses
- **System Message**: "You are an expert AI debugger for ML competitions. Analyze execution results and provide JSON output."

## 13. Server Endpoints

### Key API Endpoints
- `POST /api/run` - Submit job to GPU
- `GET /api/logs/{datarow_id}/{debug_step}` - Get live terminal output
- `GET /api/status/{datarow_id}/{debug_step}` - Check job status
- `POST /api/cancel/{datarow_id}/{debug_step}` - Cancel running job
- `POST /api/analyze` - Generate analysis via LM Studio
- `POST /api/mark_no_repro` - Mark as "No Repro" (>6m)
- `GET /api/code/{competition_id}/{datarow_id}/{debug_step}` - Get code file

## 14. Important Notes

- **DO NOT modify `gpu_submit.sh`** unless explicitly requested. User wants to keep it the same.
- **GPU Time Conservation**: Never use `--force` flag. Only submit files that don't have logs.
- **File Preservation**: Do NOT delete user's code files. Only create new ones with incremented `debug_step`.
- **Log Formatting**: Ensure `stdout` is formatted as array of strings, not single string with newlines.
- **Column Labels**: UI labels must match spreadsheet column names EXACTLY.
- **Fixed Code Generation**: LM Studio does NOT generate fixed code. User creates it manually based on the `revised_plan`.

## 15. Restart Checklist

When starting a new session:
1. Check `.env` has `TOKEN`, `SERVER_URL`, `LM_STUDIO_URL` (optional, defaults to localhost:1234)
2. Ensure LM Studio is running with a model loaded
3. Start Fairy Debugger: `python tools/fairy_ui/server.py`
4. Open browser to `http://localhost:8000`
5. Verify VPN is ON (if using ngrok)
6. Test with a simple job to ensure everything works

## 16. Debugging Process Example

### Step 0 (Initial Bug)
1. User pastes buggy code into UI
2. Clicks "Run on GPU"
3. Job fails with error
4. UI calls LM Studio for analysis
5. User gets `revised_analysis` and `revised_plan`
6. User manually creates `code/<competition_id>_<datarow_id>_1.py` with fixes
7. User fills spreadsheet row for step 0

### Step 1 (First Fix)
1. User updates Debug Step to `1` in UI
2. Pastes fixed code into UI
3. Clicks "Run on GPU"
4. If successful: Fill spreadsheet with `bug_fixed: TRUE`
5. If new error: Create step 2 file and repeat
