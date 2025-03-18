from .base import *
from dotenv import load_dotenv

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "expense_tracker",
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}