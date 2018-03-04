FROM python:3.6-alpine3.7
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
        bash \
        build-base \
        postgresql-dev \
        libffi-dev \
        libxml2-dev \
        libxslt-dev

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install -r /requirements/develop.txt

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start_dev.sh /start_dev.sh
RUN sed -i 's/\r//' /start_dev.sh
RUN chmod +x /start_dev.sh

VOLUME /app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
