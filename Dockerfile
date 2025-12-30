FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir mcp redis python-dotenv

# Copy application
COPY redis_mcp_server.py .
COPY seed_data.py .
COPY .env.example .env

# Expose port for HTTP transport (optional)
EXPOSE 8000

# Default command
CMD ["python", "redis_mcp_server.py"]
