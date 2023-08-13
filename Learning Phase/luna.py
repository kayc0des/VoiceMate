import sys
import numpy as np
import threading
import tkinter as tk
from gtts import gTTS
from playsound import playsound
import os

import speech_recognition as sr
from text_to_speech import say_message

from neuralintents import GenericAssistant


class Assistant:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        #self.assistant = GenericAssistant("intents.json", intent_methods={"file": self.create_file}).train_model()
        self.assistant = GenericAssistant("intents.json").train_model()
        self.assistant.save_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="🤖", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

    def create_file(self):
        with open("somefile.txt", "w") as f:
            f.write("New File")

    def speak(self, message):
        # Function to say a specific message using gTTS
        print(message)  # For debugging purposes (optional)
        tts = gTTS(text=message, lang='en')
        tts.save("temp_message.mp3")
        os.system("afplay temp_message.mp3")  # Use "afplay" for macOS audio playback
        os.remove("temp_message.mp3")

    def update_label(self, color):
        self.label.config(fg=color)

    def run_assistant(self):
        while True:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.recognizer.listen(source)

                    text = self.recognizer.recognize_google(audio).lower()

                    if "hey jake" in text:
                        #self.label.config(fg="red")
                        audio = self.recognizer.listen(source)
                        text = self.recognizer.recognize_google(audio).lower()
                        if text == "stop":
                            self.speak("Bye")
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speak(response)
                        #self.root.after(0, self.update_label, "black")
            except sr.UnknownValueError:
                #self.root.after(0, self.update_label, "black")
                continue

Assistant()

