from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    MYSQL_HOST : str = ''
    MYSQL_PORT : int  = 3306
    MYSQL_USER : str = ''
    MYSQL_PASSWORD : str = ''
    MYSQL_DB : str = ''
    ACCESS_TOKEN_EXPIRE_MINUTES : int  = 60
    ACCESS_SECRET_KEY : str = 'test'
    

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    
    @property
    def database_url(self) -> str:
        return f"mysql+mysqldb://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

settings = Config()
    