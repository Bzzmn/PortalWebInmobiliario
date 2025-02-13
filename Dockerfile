# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and load fixtures in correct order
RUN python manage.py migrate && \
    python manage.py loaddata webPages/fixtures/usuarios.json && \
    python manage.py loaddata webPages/fixtures/tipos_inmueble.json && \
    python manage.py loaddata webPages/fixtures/regiones_comunas.json && \
    python manage.py loaddata webPages/fixtures/inmuebles_adapted.json

# Expose the port the app runs on
EXPOSE ${PORT}

# Create and switch to non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Command to run the application
CMD gunicorn inmobiliario.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --timeout 120 