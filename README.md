# voting-system

## setup

```
$ touch config.py
```

```
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///voting.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'development key'
SERVER_ROOT = '127.0.0.1:5000'
MAIL_FROM_ADDRESS = 'admin@example.com'
POST_MARK_API_KEY = '00000000-0000-0000-0000-000000000000'
```

## launch

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py init_db
$ python manage.py runserver
$ open http://localhost:5000/
```