import openai
import re
from api.settings import OpenAISettings
import logging
import requests
import json

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

logger.info("Session started")
openai_settings = OpenAISettings()  # type: ignore
logger.info(f"Settings loaded: {openai_settings.json()}")
openai.organization = openai_settings.organization_id
openai.api_key = openai_settings.api_secret.get_secret_value()

# messages = [
#     {"role": "system", "content": "Your task is to `Take Meeting Notes`. I will list events that will be occouring in the meeting in the form of CamelCase 'phrases' in English. The format of the events will be like that of Rust Enums. The events may sometimes carry some metadata about the event itself. Which will be available in a `key=value` pair format. You will not give a response. Just an acknowledgement of receiving the event. Until you encounter the `EndSession` event. When you encounter this, you will provide a listed summary with description of all the events that happened."},
#     {"role": "user", "content": "Greetings"},
#     {"role": "user", "content": "MessageUpvoted(msg_id_2007)"},
#     {"role": "user", "content": "Congratulations(name=Jakub)"},
#     {"role": "user", "content": "Congratulations(name=(Rene, Jawad))"},
#     {"role": "user", "content": "GoalsForNextSprint(number=5,carryforward=2,new=3)"},
#     {"role": "user", "content": "EndSession"},
# ]

# # ------------------------------------------------------------------------------------------

# url = "https://api.openai.com/v1/chat/completions"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer {}".format(openai_settings.api_secret.get_secret_value())
# }
# data = {
#     "model": "gpt-3.5-turbo",
#     "messages": messages,
#     "temperature": 0.7
# }

# session = requests.Session()
# response = requests.post(url, headers=headers, data=json.dumps(data))
# print(response.content)


# Initialize the ChatGPT model
# chatgpt = ChatGPT(api_key)
# # List of messages as input
# messages = [
#     {"role": "system", "content": "Your task is to `Take Meeting Notes`. I will list events that will be occouring in the meeting in the form of CamelCase 'phrases' in English. The format of the events will be like that of Rust Enums. The events may sometimes carry some metadata about the event itself. Which will be available in a `key=value` pair format. You will not give a response. Just an acknowledgement of receiving the event. Until you encounter the `EndSession` event. When you encounter this, you will provide a listed summary with description of all the events that happened."},
#     {"role": "user", "content": "Greetings"},
#     {"role": "user", "content": "MessageUpvoted(msg_id_2007)"},
#     {"role": "user", "content": "Congratulations(name=Jakub)"},
#     {"role": "user", "content": "Congratulations(name=(Rene, Jawad))"},
#     {"role": "user", "content": "GoalsForNextSprint(number=5,carryforward=2,new=3)"},
#     {"role": "user", "content": "EndSession"},
# ]

# # Get the model's response
# response = chatgpt.submit_request(messages)

# # Print the result
# print(response["choices"][0]["message"]["content"])
# pattern = re.compile(".*gpt.+")
# print( [model for model in openai.Model.list()['data'] if  pattern.match(model['id'])])
