# Use the official Python image as the base image
FROM python:latest

# Install Tesseract, Poppler, and their dependencies (for Debian-based systems)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point for the Flask application
ENV FLASK_APP=ocr_server.py

# Expose the port on which the Flask application will run
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
