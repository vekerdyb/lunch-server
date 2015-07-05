FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pyvenv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r requirements.txt
ADD . /app/
