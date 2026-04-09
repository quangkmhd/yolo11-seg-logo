# Base image with CUDA support for YOLO
FROM ultralytics/ultralytics:latest

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose Gradio port
EXPOSE 7860

# Default command: launch the web app
ENTRYPOINT ["python", "main.py"]
CMD ["serve"]
