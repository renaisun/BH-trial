
python manage.py makemigrations
python manage.py migrate
#python manage.py runserver 0.0.0.0:8123
gunicorn -c config/gunicorn/dev.py