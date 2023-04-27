# base image
FROM python:3.9-slim

#maintainer
LABEL Author="Daniel Tesfai"


# The environment variable ensures that the python
# output to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# switch to the app directory so that everything runs from here
COPY . /app/
COPY requirements.txt /app/
WORKDIR /app/


# #installs the requirements
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python ./src/manage.py runserver 0.0.0.0:8000


# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Create and set working directory
# WORKDIR /app

# # Copy requirements.txt and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the src directory to the container
# COPY src/ /app/

# # Expose the port to listen on
# EXPOSE 8000

# # Run the command to start the server
# #CMD ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]