from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import List

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMIN_IDS: List[int]

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()
