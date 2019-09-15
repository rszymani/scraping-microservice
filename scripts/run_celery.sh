#!/bin/bash
cd /app
celery -A API.celery worker --loglevel=info
