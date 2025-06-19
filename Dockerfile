# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements if you have them
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port if you're running Chroma or a web service (optional)
EXPOSE 8000
EXPOSE 5500
EXPOSE 5000

# Default command (you can change this to `main.py`, FastAPI, etc.)
CMD ["/start.sh"]
