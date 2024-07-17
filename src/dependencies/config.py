from typing import List

from starlette.config import Config

from starlette.datastructures import CommaSeparatedStrings
from pydantic_settings import BaseSettings, SettingsConfigDict

###
# Properties configurations 
###

class Settings(BaseSettings):
    APP_TITLE:str = 'Graphql Student test'
    ENV_STATE:str
    DB_URL: str 
    SECRET_KEY: str
    DEBUG: bool = False
    #prefix
    API_PREFIX:str  
    ROUTE_PREFIX_V1:str
    #jwt
    JWT_TOKEN_PREFIX:str 
    ALGORITHM:str   
    ACCESS_TOKEN_EXPIRE_MINUTES:int     
    REFRESH_TOKEN_EXPIRE_DAYS:int   
    
    ALLOWED_HOSTS:List    
     
    model_config = SettingsConfigDict(env_file=('.env'),extra='ignore')


settings = Settings()

API_PREFIX = settings.API_PREFIX
APP_TITLE = settings.APP_TITLE
DATABASE_URI  = settings.DB_URL
  
SECRET_KEY = settings.SECRET_KEY 
ALGORITHM = settings.ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
JWT_TOKEN_PREFIX = settings.JWT_TOKEN_PREFIX  
 
config = Config(".env")

ROUTE_PREFIX_V1 = settings.ROUTE_PREFIX_V1 
ALLOWED_HOSTS = settings.ALLOWED_HOSTS 

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
) 
 
print(settings.model_dump())


