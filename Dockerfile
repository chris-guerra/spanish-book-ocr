# Use Python 3.11-alpine as base image
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Install system dependencies including Tesseract OCR and build dependencies
RUN apk add --no-cache \
    tesseract-ocr \
    tesseract-ocr-data-spa \
    poppler-utils \
    # Build dependencies
    gcc \
    musl-dev \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev

# Create non-root user
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

# Copy requirements first to leverage Docker cache
COPY --chown=appuser:appuser requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=appuser:appuser . .

# Create necessary directories
RUN mkdir -p data/input data/output data/tessdata

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Set environment variables
ENV PYTHONPATH=/app
ENV TESSDATA_PREFIX=/usr/share/tessdata

# Command to run the application
CMD ["sh", "-c", "python -m streamlit run app/ui/streamlit_app.py & python -m uvicorn app.api.routes:router --host 0.0.0.0 --port 8000"] 