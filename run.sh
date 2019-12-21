#!/bin/bash

# Apply migrations
/usr/local/bin/alembic -c /opt/flask-restplus-demo/alembic.ini upgrade head

# Run application
uwsgi --http 0.0.0.0:5000 --module egl.app:app --processes 1 --threads 8