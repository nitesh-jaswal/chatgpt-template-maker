"""
This script prompts the user for a question on the terminal and hits openai API to get a response from the model.

    Example Usage:
    (Note: The response to the above question will differ based on whether the chosen model is 3.5 or 4.)
        User: I'm in my house. On the top of my chair in the living room is a coffee cup. Inside the coffee cup is a thimble. Inside the thimble is a single diamond. I move the chair to my bedroom. Then I put the coffee cup on the bed. Then I turn the the cup upside down. Then I return it to rightside-up, and place the coffee cup on the kitchen counter. Where is my diamond?

        Bot (gpt-3.5-turbo): The diamond is inside the thimble, which is inside the coffee cup, which is on the kitchen counter.

        Bot (gpt-4): Your diamond is most likely on the bed since you turned the coffee cup upside down while it was on the bed, causing the diamond to fall out of the thimble and onto the bed.
"""

import os
import openai
import logging
from flask import Flask, request, jsonify, render_template

logger = logging.getLogger()
logging.basicConfig(level=logging.WARN)

# Hard-code which model to use
MODEL_ID = 'gpt-4'

app = Flask(__name__)
conversation = []


def chatgpt_convo(conversation):
    response = openai.ChatCompletion.create(
        model=MODEL_ID,
        messages=conversation
    )
    conversation.append(
        {
            "role": "assistant",
            "content": response['choices'][0]['message']['content']
        }
    )
    return conversation


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    if "OPENAI_API_KEY" in os.environ:
        API_KEY = os.environ["OPENAI_API_KEY"]
    else:
        # Ask user for input
        API_KEY = input("Please enter the value for OPENAI_API_KEY: ")

    openai.api_key = API_KEY

    content = request.form['content']
    if content.lower() == 'exit':
        return jsonify({'response': "Bot: Goodbye! If you have any more questions or need assistance in the future, feel free to ask. Have a great day!"})
    conversation.append({
        'role': 'user',
        'content': content
    })
    response = chatgpt_convo(conversation)[-1]['content']
    return {'response': response}


def main():
    logger.info("Session started")
    app.run(debug=True)


if __name__ == '__main__':
    main()
