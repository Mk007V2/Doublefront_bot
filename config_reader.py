from pydantic import BaseSettings, SecretStr
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):
    bot_token: SecretStr
    elite_ids: list
    group_id:int
    class Config:
        env_file = BASE_DIR+'/.env'
        env_file_encoding = 'utf-8'

config = Settings()
