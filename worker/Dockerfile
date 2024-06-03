# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory.
WORKDIR /worker

# Environment configuration.
COPY requirements.txt .

# Install necessary libraries.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the worker script.
COPY worker.py .
COPY models.py .
COPY prompt_single_class.txt .
COPY prompt_multiclass.txt .
COPY logger_config.py .

# Define the command to run the worker.
CMD ["python", "worker.py"]
