import unittest
from unittest.mock import patch, Mock
from zara import Assistant

class TestAssistant(unittest.TestCase):

    @patch("assistant.sr.Recognizer")
    @patch("assistant.tk.Tk")
    @patch("assistant.say_message")
    def setUp(self, mock_say_message, mock_tk, mock_recognizer):
        self.assistant = Assistant()
        self.mock_recognizer_instance = mock_recognizer.return_value
        self.mock_tk_instance = mock_tk.return_value

    def test_listen_for_command_with_command(self):
        self.mock_recognizer_instance.listen.return_value = Mock()
        self.mock_recognizer_instance.recognize_google.return_value = "hello"
        result = self.assistant.listen_for_command()
        self.assertEqual(result, "hello")

    def test_listen_for_command_without_command(self):
        self.mock_recognizer_instance.listen.return_value = Mock()
        self.mock_recognizer_instance.recognize_google.side_effect = sr.UnknownValueError()
        result = self.assistant.listen_for_command()
        self.assertIsNone(result)

    def test_reply_chrome_intent(self):
        self.assistant.predict_intent = Mock(return_value="chrome")
        self.assistant.handle_open_intent = Mock()
        response = self.assistant.reply("open chrome")
        self.assertEqual(response, "Opening Chrome")
        self.assistant.handle_open_intent.assert_called_once()

    def test_reply_file_intent(self):
        self.assistant.predict_intent = Mock(return_value="file")
        self.assistant.create_sample_file = Mock(return_value="Sample file created at path")
        response = self.assistant.reply("create a file")
        self.assertEqual(response, "Creating a file for you")
        self.assistant.create_sample_file.assert_called_once()

if __name__ == "__main__":
    unittest.main()