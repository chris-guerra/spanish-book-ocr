import pytesseract
from pathlib import Path
from PIL import Image
import logging
from typing import Optional, List, Dict, Any
import re
import language_tool_python
from .config import settings
from ..utils.pdf_utils import PDFProcessor

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, language: str = settings.DEFAULT_LANGUAGE):
        self.language = language
        self.language_tool = language_tool_python.LanguageTool(language)
        self.pdf_processor = PDFProcessor()
        self._ensure_language_data()

    def _ensure_language_data(self) -> None:
        """Ensure the language data file exists in the tessdata directory."""
        language_file = settings.TESSDATA_DIR / f"{self.language}.traineddata"
        if not language_file.exists():
            logger.warning(f"Language data for {self.language} not found in {language_file}")
            # TODO: Implement automatic download of language data

    def process_image(self, image_path: Path) -> Dict[str, Any]:
        """
        Process a single image and return the extracted text with confidence.
        
        Args:
            image_path (Path): Path to the image file
            
        Returns:
            Dict[str, Any]: Dictionary containing text and confidence score
        """
        try:
            image = Image.open(image_path)
            ocr_result = pytesseract.image_to_data(
                image,
                lang=self.language,
                output_type=pytesseract.Output.DICT
            )
            text = " ".join(ocr_result['text']).strip()
            confidence = sum(ocr_result['conf']) / max(len(ocr_result['conf']), 1)
            
            # Clean and correct text
            cleaned_text = self.clean_text(text)
            normalized_text = self.normalize_newlines(cleaned_text)
            corrected_text = self.correct_text(normalized_text)
            
            return {
                'text': corrected_text,
                'confidence': confidence,
                'raw_result': ocr_result
            }
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            raise

    def process_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Process a PDF file and return the extracted text for each page.
        
        Args:
            pdf_path (Path): Path to the PDF file
            
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing text and confidence for each page
        """
        try:
            # Create temporary directory for processed images
            temp_dir = settings.DATA_DIR / "temp" / pdf_path.stem
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Process PDF and get paths to processed images
            image_paths = self.pdf_processor.process_pdf(pdf_path, output_dir=temp_dir)
            
            # Process each image with OCR
            results = []
            for i, image_path in enumerate(image_paths):
                ocr_result = self.process_image(image_path)
                results.append({
                    'page_number': i + 1,
                    'text': ocr_result['text'],
                    'confidence': ocr_result['confidence'],
                    'raw_result': ocr_result['raw_result']
                })
                logger.info(f"Processed page {i+1} with OCR")
            
            return results
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
        finally:
            # Clean up temporary files
            if temp_dir.exists():
                for file in temp_dir.glob("*"):
                    file.unlink()
                temp_dir.rmdir()

    def clean_text(self, text: str) -> str:
        """
        Clean the OCR text to remove nonsensical lines and unwanted characters.
        
        Args:
            text (str): Raw OCR text
            
        Returns:
            str: Cleaned text
        """
        lines = text.splitlines()
        cleaned_lines = []

        for line in lines:
            cleaned_line = line.strip()
            # Skip lines with too few alphanumeric characters
            if len(re.findall(r'[a-zA-Z0-9]', cleaned_line)) / max(len(cleaned_line), 1) < 0.5:
                continue
            # Skip very short lines
            if len(cleaned_line) < 3:
                continue
            # Skip lines with repeated characters
            if re.match(r"(.)\1{3,}", cleaned_line):
                continue
            # Remove unwanted characters
            cleaned_line = re.sub(r"[^\w\s,.!?¿¡:\"'()-""–]", "", cleaned_line)
            cleaned_lines.append(cleaned_line)

        return "\n".join(cleaned_lines)

    def normalize_newlines(self, text: str) -> str:
        """
        Normalize newlines in the text.
        
        Args:
            text (str): Text with potentially irregular newlines
            
        Returns:
            str: Text with normalized newlines
        """
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
        text = re.sub(r"\n{2,}", "\n\n", text)
        return text

    def correct_text(self, text: str) -> str:
        """
        Apply language corrections to the text.
        
        Args:
            text (str): Text to correct
            
        Returns:
            str: Corrected text
        """
        matches = self.language_tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        return re.sub(r" {2,}", "\n   ", corrected_text)

    def get_available_languages(self) -> List[str]:
        """Get list of available language data files."""
        return [f.stem for f in settings.TESSDATA_DIR.glob("*.traineddata")]

    def download_language_data(self, language: str) -> bool:
        """Download language data file from the tessdata repository."""
        # TODO: Implement language data download
        pass 