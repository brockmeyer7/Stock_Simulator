from pathlib import Path
import io
import os       
from urllib.parse import urlparse 
import environ  
import google.auth
from google.cloud import secretmanager as sm

# Pull django-environ settings file, stored in Secret Manager
SETTINGS_NAME = "application_settings"

_, project = google.auth.default()
client = sm.SecretManagerServiceClient()
name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

env = environ.Env()
env.read_env(io.StringIO(payload))

# Load Django secret key value via django-environ
# SECURITY WARNING: keep the Django secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# Load DEBUG value via django-environ
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
else:
    ALLOWED_HOSTS = ["*"]

# Load DATABASES value via django-environ
DATABASES = {"default": env.db()}

# Define static paths
BASE_DIR = Path(__file__).resolve().parent.parent
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = [os.path.join(BASE_DIR, "static")]
STATIC_URL = '/static/'

# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"


# Application definition

INSTALLED_APPS = [
    'stock_simulator.apps.StockSimulatorConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'stock_simulator.User'

LOGIN_URL = '/login'

LOGIN_REDIRECT_URL = '/login'