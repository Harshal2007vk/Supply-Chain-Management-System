import google.generativeai as genai

# TODO: Paste your API Key here
GEMINI_API_KEY = "Your_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:

    print(f"Error: {e}")
