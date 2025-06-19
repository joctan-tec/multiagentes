#!/bin/bash
chroma run --host 0.0.0.0 --port 8000 &
sleep 3 # Esperar a que ChromaDB esté listo
python app/text_processor/load_pdf.py
python app/api.py
