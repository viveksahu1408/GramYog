#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# --- Ye Naya Jugaad Hai (Admin Banane ke liye) ---
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin already exists')" | python manage.py shell

# --- YE NAYI LINE HAI (Data Load karne ke liye) ---
#python manage.py loaddata data.json

#python manage.py loaddata data.json || echo "⚠️ Data load failed, skipping..."

# --- YE NAYA CODE HAI (Data Load ke liye) ---
# JSON ki jagah hum seedha Python Script chala rahe hain
python manage.py shell < demo_setup.py