import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("API Key:", "..." + GEMINI_API_KEY[-4:] if GEMINI_API_KEY else "Not found")  # Only show last 4 chars for security

# Configure the library
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel('models/gemini-2.0-flash')

try:
    # Simple test prompt
    response = model.generate_content("What is 2+2? Reply in one sentence.")
    print("\nTesting Gemini API connection...")
    print("Response:", response.text)
except Exception as e:
    print("\nError occurred:", str(e))
