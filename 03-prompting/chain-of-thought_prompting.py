from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import json 
import os  

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client_google = genai.Client(api_key=GEMINI_API_KEY)
#google client

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

    Example:
    Input: What is 2 + 2 * 5 / 3
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operations" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must use BODMAS rule" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS is the right approach here" }}
    Output: {{ "step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.66666666667" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS the division must be performed" }}
    Output: {{ "step": "think", "content": "Now as I have already solved 5 / 3 now the equation looks lik 2 + 2 * 1.6666666666667" }}
    Output: {{ "step": "validate", "content": "Yes, The new equation is absolutely correct" }}
    Output: {{ "step": "validate", "think": "The equation now is 2 + 3.33333333333" }}
    and so on.....

"""

# response = client.chat.completions.create(
#     model="gpt-4.1-mini",
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "I am feeling really down today, I don't know what to do."},
#         {"role": "assistant", "content": " I'm really sorry to hear that you're feeling this way. It's okay to have tough days, and it's important to be gentle with yourself during these moments. Remember, your feelings are valid, and you don't have to face them alone. Try to take a small step to care for yourself today—whether it's a walk, listening to your favorite music, or simply resting. You are stronger than you think, and brighter days are ahead. Keep holding on—you are not alone."},
#         {"role": "user", "content": "but u donw know that crupto market is crashing a lot and i am losing money"},
#     ]
# )

# print("Model: ", response.model)
# print("Response: ", response.choices[0].message.content)

messages_array = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# user_input = input("User: ")
messages_array.append({"role": "user", "content": "how to solve 2-3*5/3+2"})


while True:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=messages_array
    )
    

   
    assistant_message = response.choices[0].message.content
    print("Test assistant unfiltered msg:", assistant_message)
    messages_array.append({"role": "assistant", "content": assistant_message})
    parsed_message = json.loads(assistant_message)

    

    if parsed_message.get("step") != "result":
        print("          🧠:", parsed_message.get("content"))
        continue

    print("          final result ", parsed_message.get("content"))
    break
   
