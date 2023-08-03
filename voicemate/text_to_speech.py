from gtts import gTTS
from playsound import playsound

def respond(response_text):
    # Function to generate speech output for responses
    print(response_text)
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")
    playsound("response.mp3")