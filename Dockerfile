
# Use the official Python image from DockerHub as the base image
FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
CMD ["--url","https://hub.docker.com/repository/docker/tdeans/qr-generator/general"]