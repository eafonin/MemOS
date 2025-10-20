# Base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libffi-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set Hugging Face mirror
ENV HF_ENDPOINT=https://hf-mirror.com
ENV PIP_CONSTRAINT=/opt/constraints.txt
ENV PYTHONUNBUFFERED=1
# ENV PIP_NO_CACHE_DIR=1

# Install Python packages
COPY docker-test1/requirements.txt /opt/requirements.txt
COPY docker-test1/constraints.txt /opt/constraints.txt

# upgrade pip first (often reduces resolver backtracks)
RUN pip install --no-cache-dir --upgrade pip \
 && pip install debugpy uvicorn[standard] \
    # install your app requirements from PyPI
 && pip install --no-cache-dir -r /opt/requirements.txt -c /opt/constraints.txt

# Install sentence-transformers for local embeddings
# RUN pip install --no-cache-dir sentence-transformers torch --index-url https://download.pytorch.org/whl/cpu

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/src

COPY src/ /app/src/

# Set Python import path
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000 5678

# Start the docker
# CMD ["uvicorn", "memos.api.product_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["python", "/app/debug_scripts/start_debug.py"]
