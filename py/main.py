import os
import openai
import logging


logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_ID = 'gpt-3.5-turbo'

def chatgpt_convo(conversation):
    response = openai.ChatCompletion.create(
        model=MODEL_ID,
        messages=conversation
    )
    return response['choices'][0]._previous['message']['content']


logger.info("Session started")
openai.api_key = API_KEY

conversations = []
conversations.append(
    {
        'role': 'user',
        'content': "X has 2 brothers, A and B. The name of A's father is Y. How many children does Y have?"
    }
)
while True:
    print(chatgpt_convo(conversations))
    print("Going again...")
