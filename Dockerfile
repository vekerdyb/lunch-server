FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get install -y postgresql-client-9.4 binutils libproj-dev gdal-bin libpq-dev
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pyvenv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r requirements.txt
ADD . /app/
