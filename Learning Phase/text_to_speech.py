from gtts import gTTS
from playsound import playsound
import os

def respond(response_text):
    # Function to generate speech output for responses
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    playsound("response.mp3")

def say_message(message):
    # Function to say a specific message using gTTS
    print(message)  # For debugging purposes (optional)
    tts = gTTS(text=message, lang='en')
    tts.save("temp_message.mp3")
    os.system("afplay temp_message.mp3")  # Use "afplay" for macOS audio playback
    os.remove("temp_message.mp3")