# Base image with Python
FROM python:3.11.11-slim

# Set working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install system-level dependencies for Kokoro TTS
RUN apt-get update && apt-get install -y \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
