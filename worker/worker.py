from typing import Dict, Any

import redis
import json
import time
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_task(task_data) -> Dict[str, Any]:
    """
    Process the task.
    :param task_data: The task data to process. Contains the text to classify, temperature and model name to use.
    :return:
    """
    text = task_data['text']
    temperature = float(task_data['temperature'])
    result = len(text) * temperature
    logging.info(f"Processed task: Length of text * Temperature = {result}")
    time.sleep(5)
    return {"result": result}


redis_url = 'redis://redis:6379'
r = redis.Redis.from_url(redis_url)

logging.info("Worker started, waiting for tasks.")

while True:
    try:
        # Blocking pop to get the task
        _, task_json = r.blpop('tasks')
        json_task_data = json.loads(task_json)
        logging.info(f"Received task: {json_task_data}")
        result = process_task(json_task_data)
        r.set(json_task_data['task_id'], json.dumps(result), ex=60 * 60 * 24)  # Store the result for 24 hours
    except Exception as e:
        logging.error(f"Error processing task: {e}")
        continue
