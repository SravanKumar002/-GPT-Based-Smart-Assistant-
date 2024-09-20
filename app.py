from openai import OpenAI
import openai  # Ensure this is here
from apikey import api_data 
import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import time

Model = "gpt-3.5-turbo"  # Use a model you have access to
client = OpenAI(api_key=api_data)

def Reply(question):
    while True:
        try:
            completion = client.chat.completions.create(
                model=Model,
                messages=[
                    {'role': "system", "content": "You are a helpful assistant"},
                    {'role': 'user', 'content': question}
                ],
                max_tokens=200
            )
            answer = completion.choices[0].message.content
            return answer
        except openai.error.OpenAIError as e:  # Catch all OpenAI errors
            print(f"Error: {e}")
            time.sleep(10)  # Optional: wait before retrying

# Text to speech 
# Use the nsss driver for macOS
engine = pyttsx3.init(driverName='nsss')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
speak("Hello, how are you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        print('Listening .......')
        r.pause_threshold = 1  # Wait for 1 sec before considering the end of a phrase
        audio = r.listen(source)
    try: 
        print('Recognizing ....')
        query = r.recognize_google(audio, language='en-in')
        print("User Said: {} \n".format(query))
    except Exception as e:
        print("Say that again .....")
        return "none"  # Return "none" instead of "None" for consistency
    return query

if __name__ == '__main__':
    while True: 
        query = takeCommand().lower()
        if query == 'none':
            continue
        
        ans = Reply(query)
        print(ans)
        speak(ans)
        
        # Specific Browser Related Tasks 
        if "open youtube" in query: 
            webbrowser.open('https://www.youtube.com')  # Added https:// for correct URL format
        if "open google" in query: 
            webbrowser.open('https://www.google.com')  # Added https:// for correct URL format
        if "bye" in query:
            break
