from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)  # Simulate a wait of 1-2 seconds between tasks

    @task
    def classify_text(self):
        data = {
            'data': {
                'query': "This is a test query",
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
