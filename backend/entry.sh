#!/bin/sh

gunicorn --workers=1 -b=0.0.0.0:8000 extractor.wsgi:application
