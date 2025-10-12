# AEGIS-Conscience Network Dockerfile
# Multi-stage build for production deployment

# Build stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install TOR for onion services
RUN apt-get update && apt-get install -y \
    tor \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash aegis
USER aegis

# Expose ports
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); result = sock.connect_ex(('localhost', 8080)); sock.close(); exit(0 if result == 0 else 1)"

# Default command
CMD ["python", "main.py"]