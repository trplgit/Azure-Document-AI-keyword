# Use official slim Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5001

# Set environment variable for Flask app
ENV FLASK_APP=app
ENV FLASK_RUN_PORT=5001
ENV FLASK_RUN_HOST=0.0.0.0

# Run the app with Flask CLI
CMD ["flask", "run"]
