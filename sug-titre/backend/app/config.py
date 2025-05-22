import os
from dotenv import load_dotenv
#from pydantic import BaseSettings

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

class Settings ():
    PROJECT_NAME: str = "Video Idea Generator"
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"

    # Exemple : clé API externe ou DB
    RAPID_API_KEY: str = os.getenv("RAPID_API_KEY", "")
    PORT: int = int(os.getenv("PORT", 8000))
    RAPID_API_URL: str = os.getenv("RAPID_API_URL", "")
    RAPID_API_HOST: str = os.getenv("RAPID_API_HOST", "")
    
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY","") 
    YOUTUBE_API_URL : str = os.getenv("YOUTUBE_API_URL","")
    
    @property
    def HEADERS(self):
        return {
            "X-RapidAPI-Key": self.RAPID_API_KEY,
            "X-RapidAPI-Host": self.RAPID_API_HOST
        }

    class Config:
        env_file = ".env"
   

settings = Settings()