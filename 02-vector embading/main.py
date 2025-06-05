from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI()

text_input = "My name is zakimomin"

response = client.embeddings.create(
    input=text_input,
    model="text-embedding-3-small"
)

print("length",len(response.data[0].embedding))