from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import json 
import os  

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API with Google AI Studio key
genai.configure(api_key=GEMINI_API_KEY)
client_google = genai.GenerativeModel('models/gemini-2.0-flash')  # Using the verified working model

client = OpenAI()
# chain-of-thought prompting with OpenAI API and gemini model

SYSTEM_PROMPT = """
    You are an helpfull AI assistant who is specialized in resolving user query.
    For the given user input, analyse the input and break down the problem step by step.

    The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation. 

    Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query,

    Output Format:
    {{ "step": "string", "content": "string" }}

    Example:
    Input: What is 2 + 2
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must go from left to right and add all the operands." }}
    Output: {{ "step": "output", "content": "4" }}
    Output: {{ "step": "validate", "content": "Seems like 4 is correct ans for 2 + 2" }}
    Output: {{ "step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers" }}
"""

messages_array = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

messages_array.append({"role": "user", "content": "how to solve 2-3*5/3+2"})

while True:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=messages_array
    )
    assistant_message = response.choices[0].message.content
    parsed_message = json.loads(assistant_message)
    step = parsed_message.get("step")
    content = parsed_message.get("content")

    # Print OpenAI's response first
    print(f"[OpenAI] step: {step} | content: {content}")

    if step == "validate":
        # For validation steps, use Gemini
        gemini_prompt = f'''You are a validation assistant. Validate the following calculation step.
Return your response in valid JSON format like this example: {{"step": "validate", "content": "your validation here"}}
Be sure to escape any special characters and maintain valid JSON syntax.

Step to validate: {content}'''
        gemini_response = client_google.generate_content(gemini_prompt)
        # Clean up the response - remove code block markers and parse JSON
        cleaned_response = gemini_response.text.strip().replace("```json", "").replace("```", "").strip()
        gemini_json = json.loads(cleaned_response)
        validation_content = gemini_json.get("content")
        print(f"[Gemini] validation response: {validation_content}")
        messages_array.append({"role": "assistant", "content": validation_content})
        continue

    # Add the OpenAI response to message history
    messages_array.append({"role": "assistant", "content": assistant_message})

    # Break only if we reach the result step
    if step == "result":
        print(f"[OpenAI] Final Result | {content}")
        break
