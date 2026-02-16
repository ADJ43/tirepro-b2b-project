FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Railway/Cloud providers set PORT env var
ENV PORT=8080
ENV ENVIRONMENT=production

EXPOSE ${PORT}

# Run uvicorn directly — no wait-for-db needed for Cloud SQL
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
