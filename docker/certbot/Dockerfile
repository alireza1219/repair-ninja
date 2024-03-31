FROM certbot/certbot:v2.9.0

COPY certify-init.sh /opt/

RUN chmod +x /opt/certify-init.sh

ENTRYPOINT []

CMD ["certbot", "renew"]