import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Pass your exact environment variable name
api_key = os.getenv("OPENAI_API_KEY")

print(api_key)
