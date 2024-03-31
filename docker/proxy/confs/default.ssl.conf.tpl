server {
    # Listen on port 80 for HTTP requests.
    listen 80;

    # Define the server name(s) for this server block.
    server_name ${DOMAIN} www.${DOMAIN};

    # Location block for serving Let's Encrypt ACME challenge files.
    location /.well-known/acme-challenge/ {
        # Specify the root directory for serving ACME challenge files.
        root /vol/web/;
    }

    # Default location block for all other requests.
    location / {
        # Redirect all HTTP requests to HTTPS.
        return 301 https://$host$request_uri;
    }
}

server {
    # Listen on port 443 for HTTPS requests with SSL/TLS encryption.
    listen      443 ssl;
    # Define the server name(s) for this server block.
    server_name ${DOMAIN} www.${DOMAIN};

    # Specify the SSL certificate and key files.
    ssl_certificate     /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

    # Include additional SSL/TLS options from a separate configuration file.
    include     /etc/nginx/options-ssl-nginx.conf;
    # Specify the path to the Diffie-Hellman parameters file for enhanced security.
    ssl_dhparam /vol/proxy/ssl-dhparams.pem;

    # Add the Strict-Transport-Security header to enforce HTTPS for a specified duration.
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Location block for serving static files.
    location /static {
        alias /vol/web/static;
    }

    # Default location block for all other requests.
    # Which are being handled by Green Unicorn.
    location / {
        # For reference:
        # https://docs.gunicorn.org/en/latest/deploy.html
        # https://github.com/benoitc/gunicorn/blob/master/examples/nginx.conf

        include              /etc/nginx/headers.conf;
        proxy_redirect       off;
        proxy_pass           http://${API_HOST}:${API_PORT};
        client_max_body_size 1M;
    }
}