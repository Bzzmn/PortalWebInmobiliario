# Use the official Python base image
FROM python:3.12.5-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the working directory
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8889

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=inmobiliario.settings
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=False

# Run migrations and then start Django's development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8889"]
