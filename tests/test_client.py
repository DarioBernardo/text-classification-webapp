import unittest
from unittest.mock import patch
from client.client import classify_text_polling, _submit_task, _check_result

class TestClient(unittest.TestCase):

    @patch('client.client.requests.post')
    def test_submit_task(self, mock_post):
        # Mock the response from the server
        mock_post.return_value.status_code = 202
        mock_post.return_value.json.return_value = {'task_id': '123'}
        task_id = _submit_task('http://localhost:5050', {'text': 'test', 'temperature': 0.5, 'model_name': 'gpt-3.5-turbo'})
        self.assertEqual(task_id, '123')

    @patch('client.client.requests.get')
    def test_check_result(self, mock_get):
        # Mock the response from the server
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'status': 'completed', 'data': {'result': 6.0}}
        result = _check_result('http://localhost:5050', '123', 1)
        self.assertEqual(result, {'result': 6.0})

    @patch('client.client._submit_task')
    @patch('client.client._check_result')
    def test_classify_text_polling(self, mock_check_result, mock_submit_task):
        # Mock the responses from the helper functions
        mock_submit_task.return_value = '123'
        mock_check_result.return_value = {'result': 6.0}
        result = classify_text_polling('test', 0.5, 'gpt-3.5-turbo', 'http://localhost:5050', 1)
        self.assertEqual(result, {'result': 6.0})

if __name__ == '__main__':
    unittest.main()