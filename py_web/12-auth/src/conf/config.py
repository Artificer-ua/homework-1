POSTGRES_HOST = "10.10.5.13"
POSTGRES_PORT = "5432"
POSTGRES_DATABASE = "pyweb17_hw12"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "pass"


class Config:
    # protocol://username:password@host:port/db_name
    DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"


config = Config
