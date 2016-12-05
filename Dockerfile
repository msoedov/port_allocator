FROM python:3
MAINTAINER Alex Myasoedov <msoedov@gmail.com>

ENV WRK /code
WORKDIR $WRK
COPY requirements.txt   $WRK/

RUN pip install -r requirements.txt

VOLUME $WRK/
