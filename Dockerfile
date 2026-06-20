# Gunakan base image Python 3.10
FROM python:3.10-slim

# Set working directory di dalam container
WORKDIR /app

# Install system dependencies yang dibutuhkan oleh OpenCV, EasyOCR, dan InsightFace
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir untuk mengurangi ukuran image Docker
RUN pip install --no-cache-dir -r requirements.txt

# Copy folder BACKEND ke dalam image
COPY ./BACKEND ./BACKEND

# Hugging Face Spaces menjalankan container menggunakan non-root user (uid 1000).
# Kita perlu memastikan folder /app memiliki izin (permission) agar aplikasi 
# dapat mengunduh dan menyimpan model AI (ONNX, EasyOCR) saat pertama kali dijalankan.
ENV HOME=/app
RUN mkdir -p /app/BACKEND/PHOTOS && chmod -R 777 /app

# Expose port default Hugging Face Spaces
EXPOSE 7860

# Jalankan server FastAPI menggunakan uvicorn
CMD ["uvicorn", "BACKEND.main:app", "--host", "0.0.0.0", "--port", "7860"]
