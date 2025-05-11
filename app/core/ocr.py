import pytesseract
from pathlib import Path
from PIL import Image
import logging
from typing import Optional, List
from .config import settings

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, language: str = settings.DEFAULT_LANGUAGE):
        self.language = language
        self._ensure_language_data()

    def _ensure_language_data(self) -> None:
        """Ensure the language data file exists in the tessdata directory."""
        language_file = settings.TESSDATA_DIR / f"{self.language}.traineddata"
        if not language_file.exists():
            logger.warning(f"Language data for {self.language} not found in {language_file}")
            # TODO: Implement automatic download of language data

    def process_image(self, image_path: Path) -> str:
        """Process a single image and return the extracted text."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=self.language)
            return text
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def process_pdf(self, pdf_path: Path) -> str:
        """Process a PDF file and return the extracted text."""
        # TODO: Implement PDF processing using pdf2image
        pass

    def get_available_languages(self) -> List[str]:
        """Get list of available language data files."""
        return [f.stem for f in settings.TESSDATA_DIR.glob("*.traineddata")]

    def download_language_data(self, language: str) -> bool:
        """Download language data file from the tessdata repository."""
        # TODO: Implement language data download
        pass 