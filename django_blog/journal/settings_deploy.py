import os

from django.core.exceptions import ImproperlyConfigured

from .settings import *


def required_environment(name):
    value = os.environ.get(name, "")
    if not value.strip():
        raise ImproperlyConfigured(f"Set {name} before starting the deployment.")
    return value


DEBUG = False
SECRET_KEY = required_environment("DJANGO_SECRET_KEY")
if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5 or SECRET_KEY.startswith("django-insecure-"):
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be a strong deployment secret.")

ALLOWED_HOSTS = required_environment("DJANGO_ALLOWED_HOSTS").replace(",", " ").split()
if not ALLOWED_HOSTS or any("*" in host or host.startswith(".") for host in ALLOWED_HOSTS):
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must list exact hostnames.")

database_host = required_environment("POSTGRES_HOST")
database_sslmode = os.environ.get("POSTGRES_SSLMODE", "verify-full")
if database_sslmode != "verify-full" and not (
    database_sslmode == "disable" and database_host in {"127.0.0.1", "::1"}
):
    raise ImproperlyConfigured("PostgreSQL requires verify-full outside the local test stand.")

database_options = {"sslmode": database_sslmode}
if root_certificate := os.environ.get("POSTGRES_SSLROOTCERT"):
    database_options["sslrootcert"] = root_certificate

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": required_environment("POSTGRES_DB"),
        "USER": required_environment("POSTGRES_USER"),
        "PASSWORD": required_environment("POSTGRES_PASSWORD"),
        "HOST": database_host,
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "OPTIONS": database_options,
    },
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

MIDDLEWARE = [MIDDLEWARE[0], "whitenoise.middleware.WhiteNoiseMiddleware", *MIDDLEWARE[1:]]
STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT") or BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
