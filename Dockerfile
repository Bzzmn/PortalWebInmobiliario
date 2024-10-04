# Use the official Python base image
FROM python:3.12.5-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Recoger archivos estáticos
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 80 8888

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=inmobiliario.settings
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=False

# Corre las migraciones y después inicia Nginx y Django
CMD ["sh", "-c", "python manage.py migrate && nginx && python manage.py runserver 0.0.0.0:8888"]