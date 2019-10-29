#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

python /code/manage.py makemigrations
python /code/manage.py migrate
python /code/manage.py runserver 0.0.0.0:8000
