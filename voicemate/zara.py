from intent_classification import IntentClassifier
import json
import random
from text_to_speech import say_message
import speech_recognition as sr
import sys
import subprocess
import tkinter as tk
import threading
import time

recognizer = sr.Recognizer()
intent_classifier = IntentClassifier()

class Assistant:

    def __init__(self, name):
        self.name = name
        self.recognizer = sr.Recognizer()

        """self.robot_label = tk.Label(name, text="🤖", font=("Arial", 240))
        self.robot_label.config(fg="black")  # Initial color
        self.robot_label.pack()"""

        # Start a thread to change the robot color when say_message is called
        #threading.Thread(target=self.change_color_thread).start()

    def listen_for_command(self):
        """
        Function to listen for voice commands and convert them to text
        """
        with sr.Microphone() as source:
            #print("Listening for a command...")
            say_message("Listening for a command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"Command recognized: {command}")
                return command
            except sr.UnknownValueError:
                say_message("Could not understand the audio. Please try again.")
                return None
            except sr.WaitTimeoutError:
                say_message("Shutting down VoiceMate...")
                return "shutdown"
        
        
    def reply(self, text):
        intent = self.predict_intent(text)
        response = self.generate_response(intent)
        return response

    def predict_intent(self, text):
        predicted_intent = intent_classifier.predict(text)
        return predicted_intent

    def generate_response(self, intent):
        with open("response.json", "r") as json_file:
            responses = json.load(json_file)
        
        if intent == "chrome":
             self.handle_open_intent()
             response = "Opening Chrome"
             return response
        else:
            # Get the list of responses for the intent, or use the default list
            response_list = responses.get(intent, responses["default"])

            # Select a random response from the list
            response = random.choice(response_list)
            return response
    
    def handle_open_intent(self):
        if sys.platform == "win32":  # Windows
            subprocess.run(["start", "chrome"])
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", "-a", "Google Chrome"])
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.run(["google-chrome"])
        else:
            say_message("Sorry, I cannot open Google Chrome on this platform.")

def main_loop():
    say_message("Hi, I'm Zara")

    while True:
        assistant = Assistant("Zara")
        user_input = assistant.listen_for_command()

        if user_input is None:
            continue

        response = assistant.reply(user_input)
        say_message(response)
        
        intent = assistant.predict_intent(user_input) 
        if intent == "leaving":
            break

# Example usage
if __name__ == "__main__":
    main_loop()