# Usa la imagen base de Python 3.8
FROM python:3.8

# Establece el directorio de trabajo en el contenedor
WORKDIR .

# Copia todos los archivos del directorio actual al contenedor
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Establece las variables de ambiente
ENV MYSQL_USER=default_user
ENV MYSQL_PASSWORD=default_password
ENV MYSQL_DATABASE=iris_db
ENV MYSQL_TABLE=iris_dataset

CMD python main.py && python app.py


