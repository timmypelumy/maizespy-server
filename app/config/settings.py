from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    """ Application Settings """

    app_name: str = "MaizeSpy"
    db_name: str = "MaizeSpyDB"
    db_url: str = "mongodb://localhost:4000"
    debug:  bool = True
    model_config = SettingsConfigDict(env_file=".env")
    allowed_origins: list[str] = ["http://localhost:5173","http://localhost:3000","http://localhost:7000", "https://maizespy.render.com","https://maizespy.com","https://maizespy.xyz","https://www.maizespy.com","https://www.maizespy.xyz","https://www.maizespy.render.com"]
    server_url: str = "http://localhost:7000"
    client_url:  str = "http://localhost:3000"
    support_email: str = "MaizeSpy@myMaizeSpy.xyz"

    ml_model_path :  str = "./spy.h5"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
