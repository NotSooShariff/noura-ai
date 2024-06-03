from dotenv import load_dotenv
import os
from groq import Groq
from PIL import ImageGrab

load_dotenv()

groq_api_key = os.environ.get('GROQ_API_KEY')
google_api_key = os.environ.get('GOOGLE_GENAI_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

groq_client = Groq(api_key=groq_api_key)

def groq_prompt(prompt):
    convo = [{'role': 'user', 'content': prompt}]
    chat_completion = groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message

    return response.content

def function_call(prompt):
    system_message = (
        'You are an AI function calling model. You will determine whether extracting the users clipboard content,  '
        'taking a screenshot, reading emails, capturing the webcam or calling no functions is best for a voice assistant to respond '
        'to the users prompt. The webcam can be assumed to be a normal laptop webcam facing the user. You will '
        'respond with only one selection from the list: ["extract clipboard", "take screenshot", "capture webcam","read emails", "None"] \n'
        'Do not respond with anything but the most logical selection from that list with no explanations. Format the function call name exactly as I listed'
    )

    function_convo = [{'role': 'system', 'content': system_message},
                      {'role': 'user', 'content': prompt}]

    chat_completion = groq_client.chat.completions.create(messages=function_convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message

    return response.content

def take_screenshot():
    path = 'screenshot.jpg'
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15)



prompt = input("USER: ")
response = groq_prompt(prompt)
function_response = function_call(prompt)
print(function_response)