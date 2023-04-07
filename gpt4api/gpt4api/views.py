from django.shortcuts import render
from django.http import JsonResponse
from app import chatgpt_convo

conversation = []

def chat_view(request):
    if request.method == 'POST':
        # Get the user input from the form
        content = request.POST['content']

        # parse the content into the conversation
        conversation.append({
            'role': 'user',
            'content': content
        })

        # Pass the user input to the GPT-4 model and get the response
        response = chatgpt_convo(conversation)[-1]['content']
        return JsonResponse({'response': response})
    else:
        response = ''

    return render(request, 'index.html', {'response': response})
