from locust import HttpUser, task, between
import random
import string


def generate_random_string(length):
    # Choose characters from letters and digits
    characters = string.ascii_letters + string.digits
    # Generate a random string of the desired length
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)  # Simulate a wait of 1-2 seconds between tasks

    @task
    def classify_text(self):
        long_random_string = generate_random_string(50)
        data = {
            'data': {
                'query': "This is a test query. Random String to avoid cache: " + long_random_string,
                'options': {"multilabel": True, "show_reasoning": True},
                'classes': []
            },
            'temperature': 0.5,
            'model_name': "gpt-3.5-turbo"
        }
        self.client.post("/classify", json=data)  # Ensure your endpoint matches the actual endpoint

    @task(3)  # Three times more likely to run than other tasks
    def check_result(self):
        # Normally you'd store and fetch task IDs to check results
        # This is just a placeholder as implementing stateful interactions is more complex
        task_id = 'your_task_id_here'
        self.client.get(f"/get-result/{task_id}")
