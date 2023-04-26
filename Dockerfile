
FROM python:3.8-slim
LABEL Author="Daniel Tesfai"
COPY ./requirements.txt /requirements.txt
COPY ./src /app
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    /py/bin/python manage.py makemigrations && \
    # /py/bin/python manage.py makemigrations users && \
    # /py/bin/python manage.py makemigrations surveys && \
    /py/bin/python manage.py migrate
    # /py/bin/python manage.py migrate users && \
    # /py/bin/python manage.py migrate surveys && \
    # /py/bin/python manage.py migrate --run-syncdb


ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 core.wsgi:application








# # base image
# FROM python:3.9-slim

# #maintainer
# LABEL Author="Daniel Tesfai"


# # The environment variable ensures that the python
# # output to the terminal without buffering it first
# ENV PYTHONUNBUFFERED 1

# # switch to the app directory so that everything runs from here
# WORKDIR /app
# COPY requirements.txt /app/requirements.txt

# #installs the requirements
# RUN pip install -r requirements.txt
# COPY . /app

# # command to run the project
# CMD python manage.py runserver 0.0.0.0:19000

