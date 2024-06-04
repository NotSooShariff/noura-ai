from dotenv import load_dotenv
import os
from groq import Groq
from PIL import ImageGrab, Image
import cv2
import pyperclip
import google.generativeai as genai

web_cam = cv2.VideoCapture(0)
load_dotenv()

groq_api_key = os.environ.get('GROQ_API_KEY')
google_api_key = os.environ.get('GOOGLE_GENAI_API_KEY')
openai_api_key = os.environ.get('OPENAI_API_KEY')

groq_client = Groq(api_key=groq_api_key)
genai.configure(api_key=google_api_key)

generation_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048
}

safety_settings = [
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_NONE'
    },
]

model = genai.GenerativeModel('gemini-1.5-flash-latest',
                              generation_config=generation_config,
                              safety_settings=safety_settings)

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

def web_cam_capture():
    if not web_cam.isOpened():
        print("Error: Camera Failed")
        exit()

    path = 'webcam.jpg'
    ret, frame = web_cam.read()
    cv2.imwrite(path, frame)

def get_clipboard_text():
    clipboard_content = pyperclip.paste()
    if isinstance( clipboard_content, str):
        return clipboard_content
    else: 
        print('No clipboard data found')
        return None

def vision_prompt(prompt, photo_path):
    img = Image.open(photo_path)
    prompt = (
        'You are the vision analysis AI that provides semantic meaning from images to provide context '
        'to send to another AI that will create a response to the user. Do not respond as the AI assistant'
        'to the user. Instead take the user prompt input and try to extract all meaning from the photo'
        'relevant to the user prompt. Then generate as much objective data about the image for the AI'
        f'assistant who will respond to the user. \n USER PROMPT: {prompt}'
    )

    response = model.generate_content([prompt, img])
    return response.text


prompt = input("USER: ")
response = groq_prompt(prompt)
function_response = function_call(prompt)
print(function_response)
