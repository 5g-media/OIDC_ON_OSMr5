#
#   Copyright 2018 EveryUP Srl
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an  BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o5+o2jv(3-dqr(&ia#-@79cgr%xi*s+6xjws^8cxp211ge#buf'
if os.getenv('DJANGO_ENV') == 'prod':
    DEBUG = False
else:
    DEBUG = True
    print DEBUG
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = "authosm.OsmUser"

SITE_NAME = "Open Source MANO"
SHORT_SITE_NAME = "OSM"

LOGIN_URL = '/auth/'
LOGOUT_URL = '/auth/'

VERSION = "0.0.1"


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'authosm',
    'projecthandler',
    'packagehandler',
    'descriptorhandler',
    'vimhandler',
    'instancehandler',
    'sdnctrlhandler',
    'userhandler',
    'netslicehandler'

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'projecthandler.middleware.OsmProjectMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


]

SESSION_ENGINE ='django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3500 #25 min
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = 'sf_t3d.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'template'),
            os.path.join(BASE_DIR, 'projecthandler', 'template'),
            os.path.join(BASE_DIR, 'projecthandler', 'template', 'download'),
            os.path.join(BASE_DIR, 'projecthandler', 'template', 'project'),
            os.path.join(BASE_DIR, 'packagehandler', 'template'),
            os.path.join(BASE_DIR, 'descriptorhandler', 'template'),
            os.path.join(BASE_DIR, 'vimhandler', 'template'),
            os.path.join(BASE_DIR, 'instancehandler', 'template'),
            os.path.join(BASE_DIR, 'sdnctrlhandler', 'template'),
            os.path.join(BASE_DIR, 'userhandler', 'templates'),
            os.path.join(BASE_DIR, 'netslicehandler', 'template'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sf_t3d.context_processor.conf_constants',
            ],
            'libraries':{
                'get': 'sf_t3d.templatetags.get',
                'date_tag': 'sf_t3d.templatetags.datetag',
            }
        },
    },
]

WSGI_APPLICATION = 'sf_t3d.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = ['authosm.backend.OsmBackend']


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.DefaultStorageFinder'
    )
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        os.path.join(BASE_DIR, "static"),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
