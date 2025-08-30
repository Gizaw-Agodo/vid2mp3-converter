from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    MONGODB_HOST: str = "host.minikube.internal"
    MONGODB_PORT: int = 27017
    MONGODB_MP3_DB: str = "mp3s"
    MONGODB_VIDEO_DB: str = "videos"
    auth_service_url: str = "http://auth-service:8000"
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def mongodb_url(self) -> str:
        return f"mongodb://{self.MONGODB_HOST}:{self.MONGODB_PORT}"
     
    model_config = SettingsConfigDict(env_file='.env', extra="ignore")


config = Settings()