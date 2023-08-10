import speech_recognition as sr
from reminder import ReminderFeature
import dateparser
from text_to_speech import say_message
import requests #pip3 install requests
import os
from datetime import datetime
from random import randint

recognizer = sr.Recognizer()
user_api = os.getenv('WEATHERAPP_KEY', default=None)

def listen_for_command(timeout=5):
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
    
def extract_time_from_command(command):
    """Function to extract the time from the voice command using dateparser"""
    parsed_time = dateparser.parse(command, settings={'PREFER_DATES_FROM': 'future'})
    return parsed_time.strftime('%Y-%m-%d %H:%M') if parsed_time else None

def get_weather(city):
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={user_api}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    if api_data['cod'] == '404':
        say_message(f"Invalid City: {city}, Please check your City name")
    else:
        temp_city = ((api_data['main']['temp']) - 273.15)
        weather_description = api_data['weather'][0]['description']
        humidity = api_data['main']['humidity']
        wind_speed = api_data['wind']['speed']
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

        weather_info = (
            f"Weather Stats for {city} || {date_time}\n"
            f"Current temperature is: {temp_city:.2f} degress Celsius\n"
            f"Current weather description: {weather_description}\n"
            f"Current Humidity: {humidity}%\n"
            f"Current wind speed: {wind_speed} kmph"
        )

        say_message(weather_info)


def say_joke():
    Funjokes = [
        "Why was 6 afraid of 7? Because 7 ate 9. hahaha",
        "Why can't you trust atoms? Because they make up everything. hahaha",
        "Why won’t it hurt if you hit your friend with a 2-liter of soda? Because it’s a soft drink! hahaha",
        "Why did the mushrooms get invited to all the best parties? He was a fun-gi! hahaha",
        "Why do you smear peanut butter on the road? To go with the traffic jam. hahaha",
        "What gets more wet the more it dries? A towel! hahaha",
        "Hear about the new restaurant called Karma? There’s no menu: You get what you deserve. hahaha",
        "What do pampered cows produce? Spoiled milk. hahaha",
        "What does a house wear? Address! hahaha",
    ]
    say_message(Funjokes[randint(0, len(Funjokes) - 1)])

def main():
    """Main function to run Voicemate"""
    say_message("VoiceMate - Your Personal Voice Assistant")

    # Create an instance of the ReminderFeature class
    reminder_feature = ReminderFeature()

    while True:
        command = listen_for_command()
        if command is not None:
            if "set a reminder" in command:
                # Extract the reminder text from the command
                reminder_start_index = command.index("set a reminder") + len("set a reminder")
                reminder_text = command[reminder_start_index:].strip()

                # Extract the time from the command using NLP
                time = extract_time_from_command(command)

                if time:
                    # Call the set_reminder method of the ReminderFeature instance
                    reminder_feature.set_reminder(reminder_text, time)
                else:
                    say_message("Could not extract time from the command. Please try again.")
            elif "weather" in command:
                # Extract the city name from the command
                # Assuming the user says something like "What's the weather in London?"
                words = command.split()
                city_index = words.index("weather") + 1
                city_name = " ".join(words[city_index:])
                get_weather(city_name)
            elif "say a joke" in command:
                say_joke()
            elif "stop assistant" in command:
                say_message("VoiceMate is quitting...")
                break
                
if __name__ == "__main__":
    main()