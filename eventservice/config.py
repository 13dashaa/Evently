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


settings = Settings()
