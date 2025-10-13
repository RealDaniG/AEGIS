# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_HOME=/app \
    TOR_ENABLED=true \
    NODE_TYPE=worker \
    NODE_ID=aegis-node \
    P2P_PORT=8080 \
    API_PORT=8003 \
    WEB_PORT=8081

# Set work directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    tor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-test.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN if [ -f requirements-test.txt ]; then pip install --no-cache-dir -r requirements-test.txt; fi

# Copy application code
COPY . .

# Create directories for data, logs, and config
RUN mkdir -p ${APP_HOME}/data ${APP_HOME}/logs ${APP_HOME}/config

# Expose ports
EXPOSE ${P2P_PORT} ${API_PORT} ${WEB_PORT} 9050 9051

# Copy TOR configuration
COPY deploy/torrc /etc/tor/torrc

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${API_PORT}/health || exit 1

# Create non-root user
RUN adduser --disabled-password --gecos '' aegisuser
RUN chown -R aegisuser:aegisuser ${APP_HOME}
USER aegisuser

# Set entrypoint
ENTRYPOINT ["python", "main.py"]

# Default command
CMD ["start-node"]