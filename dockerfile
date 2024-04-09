# Define an argument for the container number
ARG CONTAINER_NUMBER, PORT_NUMBER

# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install jsonpickle pycryptodome

# Expose port dynamically based on CONTAINER_NUMBER
EXPOSE $PORT_NUMBER

# Define the command to run the Python script
CMD ["sh", "-c", "python main.py 127.0.0.1 $(($PORT_NUMBER))"]