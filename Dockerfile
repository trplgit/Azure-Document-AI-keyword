# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the port (adjust if the app runs on a different port)
EXPOSE 8992
EXPOSE 80

# Set environment variables (optional, or load via .env file)
ENV PYTHONUNBUFFERED=1

# Command to run the app (adjust if needed, e.g., uvicorn or gunicorn for FastAPI/Flask)
CMD ["python", "app.py"]
