# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requirements al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código al contenedor
COPY app/ app/

# Expone el puerto usado por Flask
EXPOSE 5000

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production


# Usa Gunicorn como servidor WSGI en producción
CMD ["gunicorn", "--timeout", "120", "--bind", "0.0.0.0:5000", "app.api:app"]