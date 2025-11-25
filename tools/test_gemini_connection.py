import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    print(f"Testing Gemini API with key: {api_key[:5]}...{api_key[-5:]}")
    
    # Using gemini-2.0-pro-exp
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro-exp:generateContent?key={api_key}"
    
    prompt = "Hello, are you working? Please reply with a short JSON object."
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 100,
            "responseMimeType": "application/json"
        }
    }
    
    max_retries = 3
    base_delay = 2
    
    print(f"Sending request to: {url}")
    
    for attempt in range(max_retries + 1):
        try:
            start_time = time.time()
            response = requests.post(url, json=payload, timeout=30)
            duration = time.time() - start_time
            
            print(f"Attempt {attempt+1}: Status Code {response.status_code} (took {duration:.2f}s)")
            
            if response.status_code == 200:
                data = response.json()
                print("Success! Response:")
                print(data)
                return
            elif response.status_code == 503:
                print(f"503 Service Unavailable: {response.text}")
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    print(f"Retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    print("Max retries reached.")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return
                
        except Exception as e:
            print(f"Exception: {e}")
            return

if __name__ == "__main__":
    test_gemini()
