# Public chat with Django channels in Django 2.2.2

This is a simple public chat with register and login, people can talk with others connected users. if a user is logged in another device, the previous session is closed.

It works with Django 2.2.2, Python 3.6.8 and channels 2.2.0

## It needs the following:
Install `requirements.txt`, `redis server` and `migrations`, you need execute these commands:

```
sudo apt install redis-server
python manage.py makemigrations
python manage.py migrate
```

and execute server:

```
python manage.py runserver
```