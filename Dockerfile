# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (optional: in case your packages need build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the port your app runs on
EXPOSE 5001

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start the app using Gunicorn (adjust if your app file or app object is named differently)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
