from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    fmp_api_key: str
    alpha_api_key: str
    massive_api_key: str
    redis_url: str
    frontend_url: str
    

    model_config = {
        "env_file": ".env"
    }


settings = Settings()