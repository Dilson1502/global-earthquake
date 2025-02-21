# Stage 1: Build Dependencies
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements-devel.txt .
RUN pip install --no-cache-dir -r requirements-devel.txt

# Stage 2: Create Final Image
FROM python:3.9-slim

WORKDIR /app

# Create a non-root user and group (for security)
RUN groupadd -r myuser && useradd -r -g myuser myuser

# Copy only the necessary files from the builder stage
COPY --from=builder /app/requirements-devel.txt .
COPY --from=builder /app/./. .
COPY . .

# Switch to the non-root user
USER myuser

# Set environment variables (best practice is to pass these at runtime, but can be set here if needed)
# Example: ENV DIRECTORY_PATH /path/inside/container

# Expose the port
EXPOSE 5005

# Healthcheck (for production)
HEALTHCHECK --interval=30s --timeout=10s --retries=5 CMD ["python", "-c", "import requests; requests.get('http://localhost:5005/healthcheck')"] # Create a /healthcheck endpoint in your app

# Start the application (remove --reload for production!)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "5005"]  # No --reload in production!