from .settings import *

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
       'NAME': 'db.sqlite',                      # Or path to database file if using sqlite3.
       'USER': '',                      # Not used with sqlite3.
       'PASSWORD': '',                  # Not used with sqlite3.
       'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
       'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
   }

}

ADMINS = (
       ('???', '???'),
)

SECRET_KEY = '3wx&u1c%9ncuqj-o8ivej*=68#%_6wfep!t0=ej2msoyvo9ylv'

ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'en-gb'

# Path Config
STATIC_URL = '/static/'
# STATIC_ROOT = '???'
MEDIA_URL = '/static/media/'
# MEDIA_ROOT = '???/media/'

# Email Config
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST = 'smtp.???.com'
# EMAIL_HOST_USER = '???'
# EMAIL_HOST_PASSWORD = '???'
# DEFAULT_FROM_EMAIL = '???'
# SERVER_EMAIL = '???'

# Feed Settings
FEED_AUTHOR_NAME = None
FEED_AUTHOR_EMAIL = None
FEED_AUTHOR_LINK = None
