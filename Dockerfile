# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install --no-cache-dir --upgrade uvicorn['standard']

CMD ["python", "main.py", "0.0.0.0"]