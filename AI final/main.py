import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np

# Set the API key
openai.api_key = apikey

# Stores the conversation history
chat_history = []

def chat(query):
    global chat_history
    chat_history.append({"role": "user", "content": query})

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent AI assistant named Jarvis."}
            ] + chat_history,
            temperature=0.7
        )
        message = response.choices[0].message.content.strip()
        say(message)
        chat_history.append({"role": "assistant", "content": message})
        return message
    except Exception as e:
        say("Sorry, there was a problem with the AI.")
        print(f"Error: {e}")
        return "Error during chat"

def ai(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        message = response.choices[0].message.content.strip()
        text = f"OpenAI response for Prompt: {prompt} \n\n{'*' * 40}\n\n{message}"

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        safe_name = prompt.replace(" ", "_")[:30]
        filename = f"Openai/{safe_name}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        
        say("Response saved.")
    except Exception as e:
        say("Something went wrong while generating the file.")
        print(f"AI Error: {e}")

def say(text):
    try:
        from win32com.client import Dispatch
        speaker = Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
    except Exception as e:
        print(f"(Speak Failed) {text}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception:
            say("Some error occurred. Please try again.")
            return ""

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I is now online.")

    while True:
        query = takeCommand().lower()

        if not query.strip():
            continue

        # Web commands
        sites = {
            "youtube": "https://www.youtube.com",
            "wikipedia": "https://www.wikipedia.com",
            "google": "https://www.google.com"
        }

        opened = False
        for name, url in sites.items():
            if f"open {name}" in query:
                say(f"Opening {name} sir...")
                webbrowser.open(url)
                opened = True
                break
        if opened:
            continue

        # Music
        if "open music" in query:
            musicPath = "https://youtu.be/HQp0DwtTP18"
            try:
                os.startfile(musicPath)
            except Exception:
                say("Music file not found.")

        # Time
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {minute} minutes.")

        # AI Text Generation
        elif "using artificial intelligence" in query:
            ai(query)

        # Quit
        elif "jarvis quit" in query:
            say("Shutting down sir. Goodbye.")
            break

        # Reset
        elif "reset chat" in query:
            chat_history.clear()
            say("Chat history reset.")

        # Chat as fallback
        else:
            chat(query)
