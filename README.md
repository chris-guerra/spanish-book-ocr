# Spanish Book OCR

## Project Overview
This project aims to convert scanned PDF books into text files using OCR technology, with a focus on Spanish language support but extensible to other languages.

## Technical Stack
- FastAPI for the backend API
- Streamlit for the user interface
- Tesseract OCR for text recognition
- Docker for containerization
- Python as the main programming language

## Project Structure
```
spanish-book-ocr/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── ocr.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── streamlit_app.py
│   └── utils/
│       ├── __init__.py
│       └── pdf_utils.py
├── data/
│   ├── input/
│   ├── output/
│   └── tessdata/
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_ocr.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env
```

## Key Features
1. PDF Upload and Processing
   - Support for multi-page PDFs
   - Image preprocessing for better OCR results
   - Progress tracking during conversion

2. OCR Processing
   - Default Spanish language support
   - Ability to download and use other language models
   - Configurable OCR parameters

3. User Interface
   - Simple file upload interface
   - Progress indicators
   - Download converted text files
   - Language selection

4. API Endpoints
   - `/upload` - Upload PDF file
   - `/convert` - Convert PDF to text
   - `/languages` - List available languages
   - `/download/{language}` - Download language model

## Implementation Steps
1. Set up project structure and dependencies
2. Implement PDF processing utilities
3. Create OCR core functionality
4. Develop FastAPI endpoints
5. Build Streamlit interface
6. Create Docker configuration
7. Add language model management
8. Implement error handling and logging
9. Add tests
10. Create documentation

## Important Notes
- Tesseract language data files are automatically fetched from: https://github.com/tesseract-ocr/tessdata/tree/main
- For CPU-only PyTorch installation:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
  ```

## Getting Started
[To be added]

## Contributing
[To be added]

## License
[To be added]