from pathlib import Path
from typing import List, Optional
import pdf2image
from PIL import Image
import logging
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, dpi: int = 300):
        """
        Initialize PDF processor with specified DPI for image conversion.
        
        Args:
            dpi (int): DPI resolution for PDF to image conversion. Default is 300.
        """
        self.dpi = dpi

    def convert_pdf_to_images(self, pdf_path: Path) -> List[Image.Image]:
        """
        Convert PDF pages to PIL Image objects.
        
        Args:
            pdf_path (Path): Path to the PDF file
            
        Returns:
            List[Image.Image]: List of PIL Image objects, one for each page
        """
        try:
            logger.info(f"Converting PDF to images: {pdf_path}")
            images = pdf2image.convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt='png'
            )
            logger.info(f"Successfully converted {len(images)} pages")
            return images
        except Exception as e:
            logger.error(f"Error converting PDF to images: {str(e)}")
            raise

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results using OpenCV.
        
        Args:
            image (Image.Image): Input image to preprocess
            
        Returns:
            Image.Image: Preprocessed image
        """
        try:
            # Convert PIL Image to OpenCV format
            img_array = np.array(image)
            img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian blur for noise reduction
            img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
            
            # Apply Otsu's thresholding
            _, img_binary = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Convert back to PIL Image
            return Image.fromarray(img_binary)
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise

    def process_pdf(self, pdf_path: Path, output_dir: Optional[Path] = None) -> List[Path]:
        """
        Process PDF file: convert to images and preprocess them.
        
        Args:
            pdf_path (Path): Path to the PDF file
            output_dir (Optional[Path]): Directory to save processed images
            
        Returns:
            List[Path]: List of paths to processed images
        """
        try:
            # Convert PDF to images
            images = self.convert_pdf_to_images(pdf_path)
            output_paths = []
            
            for i, img in enumerate(images):
                # Preprocess image
                processed_img = self.preprocess_image(img)
                
                # Save processed image if output directory is provided
                if output_dir:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    output_path = output_dir / f"page_{i+1}.png"
                    processed_img.save(output_path)
                    output_paths.append(output_path)
                
                logger.info(f"Processed page {i+1}")
            
            return output_paths
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise 