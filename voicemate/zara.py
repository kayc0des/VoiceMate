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

    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.root = tk.Tk()
        self.root.title("VoiceMate")

        self.robot_label = tk.Label(self.root, text="🤖", font=("Arial", 240))
        self.robot_label.config(fg="black")  # Initial color
        self.robot_label.pack()

        self.close_button = tk.Button(self.root, text="Close", command=self.close_window)
        self.close_button.pack()

        self.root.after(0, self.start_main_loop)  # Start main loop after GUI setup

        self.root.mainloop()

    def start_main_loop(self):
        say_message("Hi, I'm Zara")

        while True:
            user_input = self.listen_for_command()

            if user_input is None:
                continue

            response = self.reply(user_input)
            say_message(response)

            intent = self.predict_intent(user_input)
            if intent == "leaving":
                break

            self.root.update()  # Update the GUI
            self.root.after(100)  # Delay to prevent GUI from becoming unresponsive

    def close_window(self):
        self.root.destroy()

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

# Example usage
if __name__ == "__main__":
    assistant = Assistant()