# Use a stable official Python slim base image
FROM python:3.11-slim

# Set environment system variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="."

WORKDIR /app

# Install system dependencies (needed for compiling C++ bindings if needed, e.g. for kuzu/lancedb)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source tree
COPY . .

# Expose port
EXPOSE 8000

# Start server lifespan boot
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
