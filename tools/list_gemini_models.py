import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open("models_utf8.txt", "w", encoding="utf-8") as f:
            f.write("Available Models:\n")
            for model in data.get("models", []):
                if "generateContent" in model.get("supportedGenerationMethods", []):
                    f.write(f"- {model['name']}\n")
        print("Models written to models_utf8.txt")
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Exception: {e}")
