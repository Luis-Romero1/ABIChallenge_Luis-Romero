# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./app /app

RUN python main.py

# Exponer el puerto en el que corre la aplicación
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "app.py"]
