import os
from boto3.session import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = os.environ.get('HOSTS', '*').split(',')

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "graphene_django",
    "corsheaders"
]

APPLICATION_APPS = [
    "poetaster",
    "api.v1",
    "common",
    "authors",
    "texts",
    "nlp",
    "plumbing",
]

INSTALLED_APPS = (
    DJANGO_APPS + THIRD_PARTY_APPS + APPLICATION_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "poetaster.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dsc_produce.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": 5432,
    },
    # "alchemy": {
    #     "ENGINE": "django.db.backends.sqlalchemy",
    #     "NAME": "postgres",
    #     "USER": "postgres",
    #     "HOST": "db",
    #     "PORT": 5432,
    # }
}

NLP = {
    "BACKEND": "poetaster.nlp.backends.SpacyBackend"
}

GRAPHENE = {
    'SCHEMA': 'poetaster.api.v1.schema.schema',
}

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    "http://local.poetaster.io:8666"
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', 'us-east-1')
boto3_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_REGION_NAME)

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_BROKER_TRANSPORT = os.environ.get("CELERY_BROKER_TRANSPORT")
CELERY_BROKER_HEARTBEAT = None
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_ROUTES = {
    "texts.*": {"queue": "texts"}
}

NLP_CCG_2_LAMBDA_URL = os.environ.get("CCG_2_LAMBDA_URL")
