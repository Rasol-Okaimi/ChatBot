import unittest
from chatbot import chatbot_response, suggest_questions

class TestChatbot(unittest.TestCase):

    def test_looking_up_answers(self):
        question = "what is python"
        response = chatbot_response(question)
        self.assertIn("python", response.lower())
        print("test_looking_up_answers is Successful")

    def test_chatbot_response_variant(self):
        response = chatbot_response("what is python programing")
        self.assertIn("python", response.lower())
        print("test_chatbot_response_variant is Successful")

    def test_compound_question(self):
        response = chatbot_response("what is python and what is 2 plus 2")
        self.assertIn("python", response.lower())
        self.assertIn("4", response)
        print("test_compound_question is Successful")

    def test_unknown_question(self):
        response = chatbot_response("who is the king of mars")
        self.assertIn("don't recognize", response.lower())
        print("test_compound_question is Successful")

    def test_suggest_questions(self):
        self.assertEqual(
            suggest_questions("python"),
            ["what is python", "what can you do with python"]
        )
        self.assertIsNone(suggest_questions("unknown"))
        print("test_suggest_questions is Successful")

if __name__ == "__main__":
    unittest.main()
