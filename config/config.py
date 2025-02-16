from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str
    sentinel_hosts: str
    redis_master_name: str
    redis_db: int
    neo4j_url: str
    neo4j_user: str
    neo4j_password: str
    jwt_secret_key_buyer: str
    jwt_secret_key_seller: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"

settings = Settings()