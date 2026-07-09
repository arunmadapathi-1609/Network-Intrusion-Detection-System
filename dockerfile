# -----------------------------
# Base Image
# -----------------------------
FROM python:3.11-slim

# -----------------------------
# Environment Variables
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Working Directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Install System Dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install Python Dependencies
# -----------------------------
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy Project Files
# -----------------------------
COPY . .

# -----------------------------
# Expose FastAPI Port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Start FastAPI Server
# -----------------------------
CMD ["uvicorn","src.app.main:app","--host","0.0.0.0","--port","8000"]