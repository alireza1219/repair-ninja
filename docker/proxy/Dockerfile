FROM nginx:1.25.4-alpine

COPY ./confs/* /etc/nginx/
COPY ./scripts/run.sh /run.sh

ENV API_HOST=api
ENV API_PORT=8000

RUN apk add --update --no-cache openssl

RUN chmod +x /run.sh

CMD ["/run.sh"]