from dotenv import load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DB_NAME: str = Field(
        description="Database name",
        validation_alias="DB_NAME",
    )
    DB_USER: str = Field(
        description="Database user",
        validation_alias="DB_USER",
    )
    DB_PASSWORD: SecretStr = Field(
        description="Password for database user",
        validation_alias="DB_PASSWORD",
    )
    DB_HOST: str = Field(
        default="localhost",
        description="Database host",
        validation_alias="DB_HOST",
    )
    DB_PORT: int = Field(
        default=5432,
        description="Database port",
        validation_alias="DB_PORT",
    )

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
