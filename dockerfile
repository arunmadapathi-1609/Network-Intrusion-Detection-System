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
# Install Dependencies
# -----------------------------
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy Project Files
# -----------------------------
COPY . .

# -----------------------------
# Expose Ports
# -----------------------------
EXPOSE 8000
EXPOSE 8501

# -----------------------------
# Start FastAPI and Streamlit
# -----------------------------
CMD sh -c "uvicorn src.app.main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app/app.py --server.address=0.0.0.0 --server.port=8501"