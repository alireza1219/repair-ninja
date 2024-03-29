# Repair Ninja 🥷
Repair Ninja simplifies repair tracking and management! It's currently work in progress 😃!

# Development Setup Guide 🧑‍💻

## Running with Docker Compose 🐋

To run the project using Docker Compose, navigate to the project root directory and execute the following command:

```
docker compose -f docker-compose-dev.yaml up
```

You can create a new superuser for the application by running the following command:

```
docker compose -f docker-compose-dev.yaml run --rm dev-api sh -c "python manage.py createsuperuser"
```

Now, you should be able to access the API on http://127.0.0.1:8000.

Smtp4dev is also accessible by navigating to http://127.0.0.1:5000 in your web browser.

## Running with Pipenv 🐍

To run the project using Pipenv, follow these steps:

1. Navigate to the project root directory in your terminal. Install project dependencies using Pipenv by executing the following command:

```
pipenv install
```

2. Create a `.env` file in the project root directory with the following environment variables:

```
REPAIR_NINJA_MODE=DEV
REPAIR_NINJA_DISABLE_DRF_INPUTS=0  # Set to 1 if you're not happy with DRF inputs
REPAIR_NINJA_DB_ENGINE=django.db.backends.mysql
REPAIR_NINJA_DB_NAME=repair_ninja  # Database name
REPAIR_NINJA_DB_HOST=localhost  # Database hostname
REPAIR_NINJA_DB_PORT=3306  # Database port
REPAIR_NINJA_DB_USER=root  # Database username
REPAIR_NINJA_DB_PASSWORD=root  # Database password
REPAIR_NINJA_EMAIL_HOST=localhost  # Email hostname (Port is set to 25 by default)
```

3. Activate the Pipenv shell by running:

```
pipenv shell
```

4. Apply database migrations by executing:

```
python manage.py migrate
```

5. Finally, start the Django development server by running:

```
python manage.py runserver 8000
```

Now, you should be able to access the API on http://127.0.0.1:8000.