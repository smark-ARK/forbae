from pydantic import BaseSettings

class Creds(BaseSettings):
    DATABASE_NAME:str
    DATABASE_USERNAME:str
    DATABASE_PASSWORD:str
    DATABASE_HOSTNAME:str
    DATABASE_PORT:str

settings=Creds(_env_file=".env")