from pydantic import BaseSettings

class EnvJWTSettings(BaseSettings):
    secret_key: str
    algorithm: str
    token_expire_minutes: str = "30"

    class Config:
        env_prefix = "JWT_"
        env_file = "backend/.env"
