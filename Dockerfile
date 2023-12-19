# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install build-essential, pkg-config, and libmariadb-dev
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y pkg-config && \
    apt-get install -y libmariadb-dev

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=init.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
