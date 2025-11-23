from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "PawPulse"
    VERSION: str = "1.0.0"
    
    # The only one we strictly need right now
    DATABASE_URL: str

    # This tells Pydantic: "Read .env, but if you see extra variables 
    # (like DB_USER) that aren't listed above, just ignore them."
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore" 
    )

settings = Settings()