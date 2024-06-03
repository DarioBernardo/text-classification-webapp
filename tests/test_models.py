import unittest
import os
import sys
from unittest.mock import patch

# add web folder to the path
sys.path.append(os.path.abspath('worker'))

from models import OpenAILanguageModel


class TestOpenAILanguageModel(unittest.TestCase):

    @patch('web.models.OpenAI')
    @patch('web.models.extract_response')
    def test_classify_text_mock(self, mock_extract_response, mock_openai):
        # Set the return value of extract_response
        mock_extract_response.return_value = {'result': 'class_name', 'reasoning': 'reason for the classification'}

        model = OpenAILanguageModel('gpt-3.5-turbo', prompt_path='web/prompt.txt')
        text = "This is a test text"
        options = {"multilabel": True, "show_reasoning": True}
        classes = [
            {"class_id": "1", "class_name": "Class 1", "class_description": "This is class 1"},
            {"class_id": "2", "class_name": "Class 2", "class_description": "This is class 2"},
            {"class_id": "3", "class_name": "Class 3", "class_description": "This is class 3"}
        ]
        temperature = 0.5
        debug = True

        result = model.classify_text(text, options, classes, temperature, debug)
        self.assertEqual(result, {'result': 'class_name', 'reasoning': 'reason for the classification'})


    @unittest.skip("This test will fail if the OpenAI API key is not set")
    def test_classify_test_for_real_single_class(self):
        #### NOTE: This test will fail because the OpenAI API key is not set ###
        # You can set the OPENAI_API_KEY environment variable to your API key to run this test
        model = OpenAILanguageModel('gpt-3.5-turbo')
        classes = [
            {
                "class_id": "Y1",
                "class_name": "Yes",
                "class_description": "User responded with an affirmative"
            },
            {
                "class_id": "N1",
                "class_name": "No",
                "class_description": "User responded with a negative"
            }
        ]
        options = {"multilabel": False, "show_reasoning": True}
        temperature = 0.0

        text = "I consent to the processing of my personal data"
        result = model.classify_text(text, options, classes, temperature)
        print(result)
        self.assertIsNotNone(result)
        expected_result = ["Y1"]
        self.assertEqual(result['result'], expected_result, f"Expected {expected_result}, got {result['result']}")

    @unittest.skip("This test will fail if the OpenAI API key is not set")
    def test_classify_test_for_real_multiclass(self):
        #### NOTE: This test will fail because the OpenAI API key is not set ###
        # You can set the OPENAI_API_KEY environment variable to your API key to run this test
        model = OpenAILanguageModel('gpt-3.5-turbo')
        classes = [
            {
                "class_id": "I1",
                "class_name": "Inform",
                "class_description": "The user is providing a piece of information"
            },
            {
                "class_id": "R1",
                "class_name": "Request",
                "class_description": "The user is requesting something"
            },
            {
                "class_id": "Q1",
                "class_name": "Question",
                "class_description": "The user is asking a question to gain information"
            },
            {
                "class_id": "C1",
                "class_name": "Command",
                "class_description": "The user is giving a command or directive"
            },
            {
                "class_id": "A1",
                "class_name": "Agreement",
                "class_description": "The user is agreeing with something that has been said"
            },
            {
                "class_id": "D1",
                "class_name": "Disagreement",
                "class_description": "The user is disagreeing with something that has been said"
            },
            {
                "class_id": "T1",
                "class_name": "Thanks",
                "class_description": "The user is expressing gratitude"
            },
            {
                "class_id": "Ap1",
                "class_name": "Apology",
                "class_description": "The user is apologizing for an action or statement"
            },
            {
                "class_id": "S1",
                "class_name": "Suggestion",
                "class_description": "The user is suggesting a course of action"
            },
            {
                "class_id": "F1",
                "class_name": "Feedback",
                "class_description": "The user is providing feedback or evaluation"
            }
        ]
        options = {"multilabel": True, "show_reasoning": True}
        temperature = 0.0

        text = "I'm going to Tottenham Court Road, can you tell me how to get there?"
        result = model.classify_text(text, options, classes, temperature)
        print(result)
        self.assertIsNotNone(result)
        expected_result = {("I1", "R1"), ("I1", "Q1")}
        self.assertIn(tuple(result['result']), expected_result, f"Expected {expected_result}, got {result['result']}")

if __name__ == '__main__':
    unittest.main()