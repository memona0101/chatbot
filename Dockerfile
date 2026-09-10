FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for compilation & git
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install from ai-backend directory
COPY ai-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files from ai-backend
COPY ai-backend/ .

# Ensure start script is executable
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
