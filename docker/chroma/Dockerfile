FROM python:3.11-slim

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia los requirements y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia la app y el script de inicio
COPY app/ app/
COPY start.sh .

# Asegura permisos
RUN chmod +x start.sh

# Exponer el puerto del servidor Chroma
EXPOSE 8000

# Ejecutar el script de arranque
CMD ["./start.sh"]
