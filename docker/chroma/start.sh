#!/bin/bash
# Inicia el servidor Chroma en segundo plano
echo "Iniciando servidor Chroma..."
chroma run --host 0.0.0.0 --port 8000 &

# Espera a que el servidor arranque
sleep 5

# Ejecuta el script que carga los PDFs
echo "Ejecutando carga de PDFs..."
python app/load_pdf.py

# Mantiene el contenedor vivo si es necesario (útil en desarrollo)
tail -f /dev/null
