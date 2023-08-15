from intent_classification import IntentClassifier
import json
import random
from text_to_speech import say_message
import speech_recognition as sr
import sys
import subprocess
import tkinter as tk
import platform
import threading
import time
import os

recognizer = sr.Recognizer() #Creating an instance of the Recognizer class
intent_classifier = IntentClassifier()

class Assistant:

    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.root = tk.Tk()
        self.root.title("Zara by VoiceMate")

        self.robot_label = tk.Label(self.root, text="👧🏾", font=("Arial", 120))
        self.robot_label.config(fg="black")  # Initial color
        self.robot_label.pack()

        self.close_button = tk.Button(self.root, text="Close", command=self.close_window)
        self.close_button.pack()

        self.root.after(0, self.start_main_loop)  # Start main loop after GUI setup

        self.root.mainloop()

    def start_main_loop(self):
        say_message("Hi, I'm Zara")

        while True:
            user_input = self.listen_for_command() #It listens and converts user speech command to text and saves it in user_input

            if user_input is None:
                continue

            response = self.reply(user_input) #If user_input then call the reply method
            say_message(response)

            intent = self.predict_intent(user_input)
            if intent == "leaving":
                self.close_window() 
                break

            self.root.update()  # Update the GUI
            self.root.after(100)  # Delay to prevent GUI from becoming unresponsive

    def close_window(self):
        self.root.destroy()

    def play_beep(self):
        if platform.system() == "Darwin": # macOS
            os.system("afplay beep.wav")
        elif platform.system() == "Windows": # Windows
            os.system("start wmplayer beep.wav")

    def listen_for_command(self, timeout=5):
        """
        Function to listen for voice commands and convert them to text
        """
        with sr.Microphone() as source:
            #print("Listening for a command...")
            #say_message("Listening for a command...")
            self.play_beep()
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
        intent = self.predict_intent(text) #Intent Classification to predict user intent 
        response = self.generate_response(intent) #it calls the generate response method of the Assistant Class
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
        elif intent == "file":
            self.create_sample_file()
            response = "Creating a file for you"
            return response
        elif intent == "kill":
            self.kill_all_processes()
            response = "Killing all process! Goodbye"
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

    def create_sample_file(self):
        file_name = "sample_zara.txt"
    
        if platform.system() == "Darwin":  # macOS
            desktop_path = os.path.expanduser("~/Desktop")
            file_path = os.path.join(desktop_path, file_name)
        elif platform.system() == "Windows":  # Windows
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, file_name)
        else:
            return "Sorry, creating files is not supported on this platform."
    
        try:
            with open(file_path, "w") as file:
                file.write("This is a sample file created by Zara.")
                return f"Sample file created at {file_path}"
        except Exception as e:
            return f"Error creating sample file: {e}"
        
    def kill_all_processes(self):
        if platform.system() == "Windows":
            subprocess.run("taskkill /F /FI \"STATUS eq RUNNING\"", shell=True)
        elif platform.system() == "Darwin":
            os.system("osascript -e 'tell application \"System Events\" to set visible of every application process to false'")
        else:
            say_message("Sorry, killing all processes is not supported on this platform.")


# Example usage
if __name__ == "__main__":
    assistant = Assistant()