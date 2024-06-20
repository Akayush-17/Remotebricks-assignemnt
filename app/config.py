## this config file handles mongodb uri
## secret key for performing hashing 
## hashing algorithm 
## time for which access token is valid 
## all this information is fetched from .env file

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv() 
class Settings(BaseSettings):
    mongodb_uri:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_var =".env"

settings =Settings()        