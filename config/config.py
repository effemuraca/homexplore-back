from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str
    redis_host: str
    redis_port: int
    redis_db: int
    neo4j_url: str
    neo4j_user: str
    neo4j_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"

settings = Settings()