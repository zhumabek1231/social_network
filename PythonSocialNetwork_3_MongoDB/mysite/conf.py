from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    mongodb_url:str = 'mongodb+srv://olzobaevdzumabek_db_user:EvCCuWf6Yl8grN0e@cluster0.sr1nc4b.mongodb.net/?appName=Cluster0'
    mongodb_name:str = 'mongo_db'

    auth_service_url:str = 'http://127.0.0.1:8000'
    post_service_url: str = 'http://127.0.0.1:8001'

    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding='utf-8',
        extra ='ignore'
    )

settings = Settings()