# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxrender1 \
    libsm6 \
    libxext6 \
    && apt-get clean

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install PyTorch and its dependencies from the specified index URL
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy and install other Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Default command to run
CMD ["python", "app/main.py"]