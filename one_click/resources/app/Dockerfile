ARG IMAGE=tiangolo/uwsgi-nginx-flask:python3.7

FROM $IMAGE

COPY ./app /app

RUN chmod -R 704 $STATIC_PATH

RUN pip install -r /app/requirements.txt