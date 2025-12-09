import requests
import json
import time

# LM Studio default URL
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

def get_analysis_score(code, logs, analysis, model="local-model"):
    """
    Queries LM Studio to determine the PROPOSED_DEBUG_ANALYSIS_ACCURATE score (0, 1, or 2).
    
    Args:
        code (str): The original buggy code.
        logs (str): The error logs from the run.
        analysis (str): The proposed analysis to evaluate.
        model (str): The model identifier to use (default: "local-model").
        
    Returns:
        str: "0", "1", or "2" based on the evaluation, or "1" if error/timeout.
    """
    
    system_prompt = """
You are an expert code debugger and judge. Your task is to evaluate the accuracy of a "Proposed Debug Analysis" against the actual code and error logs.
You must assign a score of 0, 1, or 2 based on the following strict criteria:

SCORE 0:
- The client-quoted bug was NOT thrown ever.
- The analysis is completely wrong or irrelevant.

SCORE 1:
- The client-quoted bug was accurate but thrown in a later debug_step (not the immediate one).
- The quoted bug was correct but the analysis/description was lacking or vague.
- The general class of error is correct (e.g., ValueError) but the actual content/details don't match.
- The bug is related to internet access or environmental issues that cannot be reproduced locally.

SCORE 2:
- The client-quoted analysis and bug is completely correct and accurate for the immediate error.

OUTPUT FORMAT:
You must output ONLY a single number: 0, 1, or 2. Do not add any explanation or text.
"""

    user_prompt = f"""
CODE:
```python
{code[:10000]} # Truncated if too long
```

LOGS:
```
{logs[:5000]} # Truncated if too long
```

PROPOSED ANALYSIS:
"{analysis}"

Based on the code and logs, evaluate the accuracy of the Proposed Analysis.
Return ONLY the score (0, 1, or 2).
"""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1, # Low temperature for deterministic output
        "max_tokens": 10
    }

    try:
        # Increased timeout to 120s as per user request
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Extract the first digit found
            import re
            match = re.search(r'[0-1-2]', content)
            if match:
                return match.group(0)
            else:
                print(f"[LM Studio] Could not parse score from response: {content}")
                return "1" # Fallback
        else:
            print(f"[LM Studio] Error: {response.status_code} - {response.text}")
            return "1" # Fallback

    except requests.exceptions.ConnectionError:
        print("[LM Studio] Connection failed. Is LM Studio running on port 1234?")
        return "1" # Fallback
    except Exception as e:
        print(f"[LM Studio] Exception: {e}")
        return "1" # Fallback

if __name__ == "__main__":
    # Simple test
    print("Testing LM Studio connection...")
    score = get_analysis_score("print('hello')", "Error: NameError", "The code fails because of a NameError")
    print(f"Score: {score}")
