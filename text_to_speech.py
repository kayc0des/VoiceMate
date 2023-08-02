import pyttsx3

engine = pyttsx3.init()

def respond(response_text):
    # Function to generate speech output for responses
    print(response_text)
    engine.say(response_text)
    engine.runAndWait()