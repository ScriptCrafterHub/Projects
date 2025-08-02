import google.generativeai as genai
from config import gemini_api_key

# Configure the Gemini client with your API key
try:
    genai.configure(api_key=gemini_api_key)
except AttributeError:
    print("🚨 Error: 'gemini_api_key' not found in config.py.")
    exit()

# Define the model with a system instruction to set its role
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are a helpful assistant who answers the user about whatever he ask."
)

# Generate the content with a single prompt
response = model.generate_content(
    "Write an email to my boss for resignation."
)

# Print the generated text
print(response.text)