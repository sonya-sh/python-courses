#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python3 manage.py flush --no-input
# python3 online_school/manage.py migrate

exec "$@"