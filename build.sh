#!/usr/bin/env bash
# Exit on error
set -o errexit

# Dependencies install karo
pip install -r requirements.txt

# Static files (CSS/Images) jama karo
python manage.py collectstatic --no-input

# Database migrate karo
python manage.py migrate