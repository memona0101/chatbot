FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for compilation & git
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ai-backend/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Copy application files from ai-backend
COPY ai-backend/ .

# Ensure start script is executable
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
