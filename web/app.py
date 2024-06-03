from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import redis
import json
import hashlib

from SCHEMAS import input_schema

app = Flask(__name__)
redis_url = 'redis://redis:6379'
r = redis.Redis.from_url(redis_url)


@app.route('/classify', methods=['POST'])
def classify():
    """
    Endpoint to classify the data
    """
    content = request.json
    data = content['data']
    temperature = content['temperature']
    model_name = content['model_name']

    if not data or (temperature > 1 or temperature < 0 or temperature is None) or not model_name:
        return jsonify({"message": "Invalid input"}), 400

    try:
        validate(instance=data, schema=input_schema)
    except ValidationError as e:
        return jsonify({"message": "Request Validation Error: " + str(e)}), 400

    task_id = generate_unique_key(data, temperature, model_name)
    task_data = {'task_id': task_id, 'data': data, 'temperature': temperature, 'model_name': model_name}

    if r.exists(task_id):
        return jsonify({"task_id": task_id, "message": "Task was already processed, using cache."}), 202

    r.rpush('tasks', json.dumps(task_data))
    return jsonify({"task_id": task_id, "message": "Task has been queued"}), 202


def generate_unique_key(task_data, temperature, model_name):
    # Example: Use a combination of task-specific fields to generate a key
    task_string = json.dumps({'data': task_data, 'temperature': temperature, 'model_name': model_name})
    return hashlib.md5(task_string.encode()).hexdigest()


@app.route('/get-result/<task_id>', methods=['GET'])
def get_result(task_id):
    """
    Endpoint to get the result of the task
    :param task_id: The task id to get the result for
    :return:
    """
    result = r.get(task_id)
    if result:
        return jsonify({"status": "completed", "data": json.loads(result)}), 200
    else:
        return jsonify({"status": "not_found", "data": None}), 202


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
