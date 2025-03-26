# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.6
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-privileged user
USER appuser

# Copy source files
COPY . .

# Expose app port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
