FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc y forzar buffer directo en logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema necesarias para compilar paquetes y PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# Exponer el puerto 8000
EXPOSE 8000

# Comando por defecto para desarrollo (en producción VPS se usará Gunicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]