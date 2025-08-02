import speech_recognition as sr
import os
import webbrowser
import datetime
import google.generativeai as genai
from config import gemini_api_key

# --- Gemini AI Configuration ---
# Configure the generative AI library with your API key
try:
    genai.configure(api_key=gemini_api_key)
except AttributeError:
    print("🚨 Error: Gemini API Key not found in config.py.")
    print("Please create a config.py file with your gemini_api_key.")
    exit()

# System instruction to define the AI's personality
system_instruction = "You are an intelligent, witty, and helpful AI assistant named Jarvis, inspired by the AI from the Iron Man movies."

# Create the Gemini Pro model
# 'gemini-1.5-flash' is fast and capable for chat.
gemini_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction
)

# Start a chat session for continuous conversation
# This object will automatically manage the conversation history
gemini_chat_session = gemini_model.start_chat(history=[])


# --- Refactored Functions to use Gemini ---

def chat(query):
    """Handles continuous conversation with Jarvis."""
    print("Jarvis is thinking...")
    try:
        # Send the user's query to the ongoing chat session
        response = gemini_chat_session.send_message(query)
        message = response.text
        say(message)
        return message
    except Exception as e:
        error_message = "Sorry, I had a problem communicating with my core intelligence."
        say(error_message)
        print(f"Error in chat function: {e}")
        return error_message

def ai(prompt):
    """For one-off AI generation tasks that are saved to a file."""
    print("Generating text...")
    try:
        # Use generate_content for a single, non-chat request
        response = gemini_model.generate_content(prompt)
        message = response.text

        text = f"Gemini response for Prompt: {prompt}\n\n{'*' * 40}\n\n{message}"

        # Create a directory if it doesn't exist
        if not os.path.exists("Gemini_Responses"):
            os.mkdir("Gemini_Responses")

        safe_name = prompt.replace(" ", "_")[:30]
        filename = f"Gemini_Responses/{safe_name}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        say("I have generated the response and saved it to a file.")
    except Exception as e:
        say("I failed to generate the response.")
        print(f"Error in ai function: {e}")


# --- Your Original Helper Functions (with minor improvements) ---

def say(text):
    """Text-to-speech function for Windows."""
    try:
        from win32com.client import Dispatch
        speaker = Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
    except ImportError:
        print(f"win32com not found. Cannot speak. Printing instead: {text}")
    except Exception as e:
        print(f"(Speak Failed) {text}\nError: {e}")


def takeCommand():
    """Listens for a command and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            # say("I didn't catch that. Could you please repeat?")
            return ""
        except Exception as e:
            say("A speech recognition error occurred.")
            print(f"Error in takeCommand: {e}")
            return ""


# --- Main Execution Loop ---

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I is now online and connected to Gemini.")

    while True:
        query = takeCommand().lower()

        if not query.strip():
            continue

        # Corrected the YouTube URL
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

        if "open music" in query:
            musicPath = "https://youtu.be/HQp0DwtTP18"
            try:
                os.startfile(musicPath)
            except Exception:
                say("Music file not found, sir.")

        elif "the time" in query:
            # Preserved your original phrasing
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} bajke {minute} minutes.")

        elif "using artificial intelligence" in query:
            ai(prompt=query) # Pass the full query as the prompt

        elif "quit" in query:
            say("Shutting down sir. It was a pleasure. Goodbye.")
            break

        elif "reset chat" in query:
            # Re-initialize the chat session to clear history
            gemini_chat_session = gemini_model.start_chat(history=[])
            say("Chat history has been reset. We can start a new conversation.")

        else:
            chat(query)