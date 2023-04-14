import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
DEBUG = ENVIRONMENT == "dev"
HOST = 'localhost' if ENVIRONMENT == "prod" else '0.0.0.0'
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "db")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
