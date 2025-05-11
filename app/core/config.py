from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Base directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    INPUT_DIR: Path = DATA_DIR / "input"
    OUTPUT_DIR: Path = DATA_DIR / "output"
    TESSDATA_DIR: Path = DATA_DIR / "tessdata"

    # Default OCR settings
    DEFAULT_LANGUAGE: str = "spa"
    TESSDATA_URL: str = "https://github.com/tesseract-ocr/tessdata/raw/main"

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Spanish Book OCR"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Create necessary directories if they don't exist
for directory in [settings.INPUT_DIR, settings.OUTPUT_DIR, settings.TESSDATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 