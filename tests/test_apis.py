import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apis.apis import app, generate_essay_from_prompt

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass


    def test_generate_essay_from_prompt(self):
        # Test the generate_essay_from_prompt function
        user_prompt = "Test prompt"
        generated_essay = generate_essay_from_prompt(user_prompt)
        
        # Perform assertions to check the correctness of generated_essay
        self.assertIsNotNone(generated_essay)
        self.assertIsInstance(generated_essay, str)
    
    def test_generate_essay_endpoint(self):
        # Test the /generate_essay endpoint
        user_prompt = {"prompt": "Test prompt"}
        response = self.app.post('/generate_essay', json=user_prompt)
        data = response.get_json()
        
        # Perform assertions on the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("essay", data)
        self.assertIsInstance(data["essay"], str)


    def test_upload_csv_endpoint(self):
        # Test the /upload_csv endpoint with a CSV file
        with open('a.csv', 'rb') as f:
            response = self.app.post('/upload_csv', data={'file': f})
            data = response.get_json()
        
        # Perform assertions on the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "CSV file uploaded successfully")

    def test_generate_essay_from_prompt(self):
        print("Running test_generate_essay_from_prompt") 

