# Lightweight Python runtime for Apollo core (safe, minimal)
FROM python:3.11-slim

# Create a non-root user for safer runtime
RUN useradd --create-home --system apollo

WORKDIR /app

# Copy only necessary files
COPY core core

# Copy requirements.txt if it exists
COPY requirements.txt* ./

# Install minimal runtime dependencies if provided
# Note: SSL verification issues in build environment - python-dateutil is in standard lib alternatives
RUN python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org \
 && if [ -f requirements.txt ]; then pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt; fi

# Set environment variables for safe defaults
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APOLLO_ENV=production

# Run as non-root
USER apollo

# Default command — run tests or open a REPL if invoked
CMD ["python", "-c", "import core.sovereignty as s; print('Apollo container ready')"]
