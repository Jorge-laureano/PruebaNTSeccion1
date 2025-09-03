# Imagen base de Python
FROM python:3.13-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY app.py .
COPY etl.py .
COPY data_prueba_tecnica.csv .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Puerto de Flask
EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]
