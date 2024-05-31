# text-classification-webapp
Simple text classification into predefined classes using LLMs. The application is build as a webapp using Flask. It also contains a simple client to interact with the webapp.

## Architecture
TODO

## Launch the webapp
To launch the webapp, you need to have `Docker` installed on your machine. You can launch the server using the following command:
```bash
docker-compose up --build
```

## Client
The client is a simple python script that sends a request to the webapp to classify the text. The client is located in the `client` directory. You can see the example_usage.ipynb notebook to see how to use the client.

## Tests

### Load test
I have created a simple load test using `locust` to test the performance of the webapp. The test is located in the `tests` directory. To run the test, you need to install `locust` using the following command:
```bash
pip install locust
```
Then, you can run the test using the following command:
```bash
locust --host=http://localhost:5050
```
After running the command, you can open the browser and go to `http://localhost:8089` to start the test.
I have tested the webapp using my local machine and tested the performance of the webapp with requests of 1000 requests per second. The webapp was able to handle the requests without any issues.
#### NOTE:
It is likely that after the load test, you will have to flush the redis queue. You can do that by running the following command:
```bash
docker exec -it text-classification-webapp_redis_1 redis-cli flushall
```
Check if `text-classification-webapp_redis_1` is the name of your redis instance. Substitute it with the correct name if it is different.

### Unit tests
To run the unit tests, you need to install the requirements, and then you can run the tests using the following command:
```bash 
pyton -m unittest discover
```

## Future work
 - Add more tests
 - Build a simple frontend for the webapp in JS ad React