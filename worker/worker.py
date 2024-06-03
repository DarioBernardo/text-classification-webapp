from typing import Dict, Any
from models import OpenAILanguageModel

import redis
import json
import time
# Setup basic configuration for logging
from logger_config import setup_logger

logger = setup_logger(__name__)



def process_task(task_data) -> Dict[str, Any]:
    """
    Process the task.
    :param task_data: The task data to process. Contains the text to classify, temperature and model name to use.
    :return:
    """
    payload = task_data['data']
    text = payload['query']
    temperature = float(task_data['temperature'])
    model_name = task_data['model_name']

    # # UNCOMMENT THIS BLOCK TO TEST THE WORKER WITH LOCUST FOR LOAD TESTING
    # result = len(text) * temperature
    # logging.info(f"Processed task: Length of text * Temperature = {result}")
    # time.sleep(5)
    # return {"result": result}

    # COMMENT THIS BLOCK TO TEST THE WORKER WITH LOCUST FOR LOAD TESTING
    model = OpenAILanguageModel(model_name)
    response = model.classify_text(text, payload['options'], payload['classes'], temperature)
    logger.debug(f"Response: {response}")

    return response


redis_url = 'redis://redis:6379'
r = redis.Redis.from_url(redis_url)

logger.info("Worker started, waiting for tasks.")

while True:
    try:
        # Blocking pop to get the task
        _, task_json = r.blpop('tasks')
        json_task_data = json.loads(task_json)
        logger.info(f"Received task: {json_task_data}")
        result = process_task(json_task_data)
        r.set(json_task_data['task_id'], json.dumps(result), ex=60 * 60 * 24)  # Store the result for 24 hours
    except Exception as e:
        logger.error(f"Error processing task: {e}")
        continue
