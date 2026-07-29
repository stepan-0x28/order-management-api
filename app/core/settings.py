from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_host: str
    database_name: str
    database_username: str
    database_password: str

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.database_username}:{self.database_password}'
            f'@{self.database_host}/{self.database_name}'
        )

    database_pool_pre_ping: bool
    database_pool_recycle: int
    database_pool_size: int
    database_max_overflow: int

    uvicorn_host: str
    uvicorn_port: int
    uvicorn_root_path: str

    token_signing_key: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
