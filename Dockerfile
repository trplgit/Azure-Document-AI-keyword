# Step 1: Use the official Python 3.12 image as the base image
FROM python:3.12-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt .

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . .

# Step 6: Expose port 5000 (default Flask port)
EXPOSE 5000

# Step 7: Set environment variables for Flask
ENV FLASK_APP=index  
ENV FLASK_RUN_HOST=0.0.0.0

# Step 8: Run the Flask application
CMD ["flask", "run"]
