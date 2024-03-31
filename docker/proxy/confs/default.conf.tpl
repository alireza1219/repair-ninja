# This Nginx server block is intended for the initial setup when SSL certificates
# are prepared. It handles HTTP requests on port 80, redirects all incoming
# requests to HTTPS, and includes a specific location for serving ACME challenge
# files for Let's Encrypt certificate renewal.

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
