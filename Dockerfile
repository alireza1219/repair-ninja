FROM python:3.12.2-alpine3.19

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --update --no-cache mysql-client mariadb-dev build-base \
    musl-dev zlib zlib-dev linux-headers

RUN pip install --upgrade pip && \
    pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --dev

COPY . /app/

RUN chmod -R +x /app/scripts

EXPOSE 8000

CMD ["/app/scripts/run.sh"]