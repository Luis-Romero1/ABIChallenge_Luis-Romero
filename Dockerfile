# Usar una imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el código de la aplicación primero
COPY . .

# Ahora instalar las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Establecer el comando de inicio por defecto
CMD ["python", "main.py"]

