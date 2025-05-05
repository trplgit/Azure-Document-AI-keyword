FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

ENV PYTHONUNBUFFERED=1

# Use Gunicorn as a production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]

