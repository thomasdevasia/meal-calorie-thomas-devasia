from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Calorie Counter API"
    usda_api_key: str = ""
    database_url: str = ""
    jwt_secret: str = ""
    jwt_algo: str = "HS256"
    jwt_expire_minutes: int = 60
    model_config = SettingsConfigDict(env_file=".env")
    redis_url: str = "something"
