# Lightweight Python runtime for Apollo core (safe, minimal)
FROM python:3.11-slim

# Create a non-root user for safer runtime
RUN useradd --create-home --system apollo

WORKDIR /app

# Copy only necessary files
COPY core core
COPY requirements.txt . 2>/dev/null || true

# Install minimal runtime dependencies if provided
RUN python -m pip install --upgrade pip \
 && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Set environment variables for safe defaults
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APOLLO_ENV=production

# Run as non-root
USER apollo

# Default command — run tests or open a REPL if invoked
CMD ["python", "-c", "import core.sovereignty as s; print('Apollo container ready')"]
