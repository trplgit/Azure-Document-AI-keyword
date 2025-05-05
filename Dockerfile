FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001  # or any other port your app uses

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
