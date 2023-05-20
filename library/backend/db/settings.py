from pydantic import BaseSettings


class DBSettings(BaseSettings):
    username: str
    password: str
    database: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file = "backend/.env"


class JWTSettings(BaseSettings):
    secret_key: str
    algorithm: str
    token_expire_minutes: str = "30"

    class Config:
        env_prefix = "JWT_"
        env_file = "backend/.env"
