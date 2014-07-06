"""
Django settings for fooding project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUTH_PROFILE_MODULE = "food.UserProfile"

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ym#q#v04yh=wz&nq--0eiq)u9=!_1svubf&6fmw1=b__sy5ck+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
	#'social_auth',
    #'django.contrib.staticfiles',
    'food',
    'tastypie',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	BASE_DIR+'fooding/food/templates'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.messages.context_processors.messages',
)

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DB_PATH = BASE_DIR+'fooding/fooding.db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/Users/chris/fooding/fooding.db',
    }
}

BASE_DIR = '/home/chris/'

MEDIA_ROOT = BASE_DIR+'fooding/media/'

MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR+'fooding/static/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR+'fooding/staticfiles/',
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
