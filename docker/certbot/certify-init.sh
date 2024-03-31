#!/bin/sh

set -e

until nc -z proxy 80; do
    echo "⏳ Waiting for the proxy server to be available..."
    sleep 5s
done

echo "🧩 Retrieving the certificate (ACME Challenge)..."

certbot certonly \
    --webroot \
    --webroot-path "/vol/web/" \
    -d "$DOMAIN" \
    --email $EMAIL \
    --rsa-key-size 4096 \
    --agree-tos \
    --noninteractive
