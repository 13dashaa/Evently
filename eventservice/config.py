from environs import Env


class Settings:
    def __init__(self) -> None:
        self.env = Env()
        self.env.read_env()

        self.DB_HOST: str = self.env.str("POSTGRES_HOST")
        self.DB_PORT: int = self.env.int("POSTGRES_PORT")
        self.DB_NAME: str = self.env.str("POSTGRES_DB")
        self.DB_USER: str = self.env.str("POSTGRES_USER")
        self.DB_PASSWORD: str = self.env.str("POSTGRES_PASSWORD")
        self.DJANGO_SECRET_KEY: str = self.env.str("DJANGO_SECRET_KEY")
        self.CELERY_BROKER_URL: str = self.env.str("CELERY_BROKER_URL")
        self.CELERY_RESULT_BACKEND: str = self.env.str("CELERY_RESULT_BACKEND")
        self.CELERY_TIMEZONE: str = self.env.str("CELERY_TIMEZONE")
        self.AWS_ACCESS_KEY_ID: str = self.env.str("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY: str = self.env.str("AWS_SECRET_ACCESS_KEY")
        self.AWS_DEFAULT_REGION: str = self.env.str("AWS_DEFAULT_REGION")
        self.SERVICES: str = self.env.str("SERVICES")
        self.ENDPOINT_URL: str = self.env.str("ENDPOINT_URL")
        self.SENDER: str = self.env.str("SENDER")
        self.MAX_TRIES: int = int(self.env("MAX_TRIES"))


settings = Settings()
