from typing import Dict, Any, List

import requests
import time


def _submit_task(url, data):
    """
    Submit a task to the server and return the task ID.
    :param url: The URL of the server.
    :param data: The data to submit.
    """
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url + '/classify', json=data, headers=headers)
    if response.status_code == 202:
        return response.json()['task_id']
    else:
        raise Exception("Failed to submit task: " + response.text)


def _check_result(url, task_id, interval, max_attempts: int = 15) -> Dict[str, Any]:
    """
    Poll the server for results at a given interval. If the task is completed, return the result.
    :param url: The URL of the server.
    :param task_id: The task ID to check.
    :param interval: The polling interval in seconds.
    :return: The result of the task.
    """
    counter = 1
    while counter <= max_attempts:
        print(f"Checking task: {task_id}\t pool attempt: {counter} of {max_attempts}")
        response = requests.get(url + f'/get-result/{task_id}')
        counter += 1
        if response.status_code == 200:
            json = response.json()
            if json['status'] == 'completed':
                return json['data']
            else:
                raise Exception("Something wrong with the Task response format: " + str(json))
        elif response.status_code != 202:
            raise Exception("Error fetching results: " + response.text)
        time.sleep(interval)

    raise Exception("Task did not complete in time.")


def classify_text_polling(
        text: str,
        options: Dict[str, Any],
        classes: List[Dict[str, Any]],
        temperature: float = 0.0,
        model_name: str = "gpt-3.5-turbo",
        server_url: str = 'http://localhost:8000',
        polling_interval: int = 1,
        max_attempts: int = 15
) -> Dict[str, Any]:
    """
    Classify the text using the server and poll for the result.
    :param options: Dictionary of options for the classification, for example: {"multilabel": true, "show_reasoning": true}
    :param classes: List of classes to classify the text into. Each class dictionary should have the following keys: "class_id", "class_name" and "class_description".
    :param text: The text to classify.
    :param temperature: The temperature parameter for the model
    :param model_name: The model name to use
    :param server_url: The server URL.
    :param polling_interval: The polling interval in seconds.
    :param max_attempts: The maximum number of polling attempts.
    :return:
    """

    print("Submitting task...")
    payload = {
        'query': text,
        'options': options,
        'classes': classes
    }
    task_id = _submit_task(server_url, {'data': payload, 'temperature': temperature, 'model_name': model_name})
    print(f"Task submitted. Task ID: {task_id}")
    result = _check_result(server_url, task_id, polling_interval, max_attempts)
    return result
