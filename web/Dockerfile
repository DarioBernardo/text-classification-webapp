# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory.
WORKDIR /app

# Copy only the necessary files.
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application.
COPY app.py .
COPY SCHEMAS.py .

# Command to run the application.
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
