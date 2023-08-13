from text_to_speech import respond

class ReminderFeature:
    # Class to handle the voice-activated reminder feature

    def set_reminder(self, reminder_text, time):
        # Method to set a reminder based on voice input
        response = f"Reminder set for '{reminder_text}' at {time}"
        respond(response)