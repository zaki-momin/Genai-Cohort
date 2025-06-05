## tiktokan library by OPENAI
## first need to install the tiktokan library 

import tiktoken


enc = tiktoken.encoding_for_model("gpt-4o" )

text = "My name is zakimomin"

tokens = enc.encode(text)

print("Tokens",tokens)


Decoded_text = enc.decode(tokens)
print("Decoded text",Decoded_text)

# Output:
# Tokens [123, 456, 789, 1011, 1213]
# Decoded text My name is zakimomin
# Note: The actual token IDs will vary based on the model and the text.
# Note: The actual token IDs will vary based on the model and the text.
# Note: The tiktoken library is used to tokenize text for OpenAI models.