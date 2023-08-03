import speech_recognition as sr
from reminder import ReminderFeature
import dateparser

recognizer = sr.Recognizer()

def listen_for_command():
    """
    Function to listen for voice commands and convert them to text
    """
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"Command recognized: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand the audio. Please try again.")
        return None
    
def extract_time_from_command(command):
    """Function to extract the time from the voice command using dateparser"""
    parsed_time = dateparser.parse(command, settings={'PREFER_DATES_FROM': 'future'})
    return parsed_time.strftime('%Y-%m-%d %H:%M') if parsed_time else None

def main():
    """Main function to run Voicemate"""
    print("VoiceMate - Your Personal Voice Assistant")

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
                elif "quit" in command:
                    print("VoiceMate is quitting...")
                    break
                else:
                    print("Could not extract time from the command. Please try again.")

if __name__ == "__main__":
    main()