# base image
FROM python:3.9-slim

#maintainer
LABEL Author="Daniel Tesfai"


# The environment variable ensures that the python
# output to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# switch to the app directory so that everything runs from here
COPY ./src /app
COPY requirements.txt /app
WORKDIR /app


#installs the requirements
RUN pip install -r requirements.txt 

CMD python ./src/manage.py runserver 8000

