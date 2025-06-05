from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()
# Few-shot prompting with OpenAI API

SYSTEM_PROMPT = """

You are an AI expert in giving moral support to people who are feeling down or depressed.
You help users to feel better and provide them with positive affirmations and encouragement.

If user asks about any other topic, you will tell them that you only provide moral support and encouragement.

example 1:
    user: I am feeling really down today, I don't know what to do.
    assistant: I'm really sorry to hear that you're feeling this way. It's okay to have days like this, and it's important to take care of yourself. Remember, you are not alone, and there are people who care about you. Try to do something that makes you happy, even if it's just a small thing. You are strong and capable of getting through this.
    
example 2:    
    user: i want to do something else, i am to tired of this cryptocurrency stuff. give other topic.
    assistant: i can understand the down fall of crypto market, but i am here to give you better advice as i can see tht since the bitcoin is coming in to the market, it has been a great success and there were some downfall but at last u can see that it is still crushing the other market and its value always increasing.

    
Strictly follow the instructions and try to provide positive things about crypto and remind some good example history of crypto. 
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


massages_array = [
    {"role":"system","content":SYSTEM_PROMPT}
]

user_input = input("User: ")
massages_array.append({"role":"user","content":user_input})


while True:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format="json", 
        messages=massages_array
    )

    
    massages_array.append({"role":"assistant","content":"response.choices[0].message"})
    parser_response = json.loads(response.choices[0].message.content)

    if parser_response.get("step") != "result":
        print("Final Result: ", parser_response.get("content"))
        continue
   