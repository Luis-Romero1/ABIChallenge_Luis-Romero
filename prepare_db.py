import os
import mysql.connector
from sklearn.datasets import load_iris

# Conectar a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = db.cursor()

# Crear la base de datos y la tabla si no existen
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DATABASE')}")
cursor.execute(f"USE {os.getenv('MYSQL_DATABASE')}")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS iris_data (
        sepal_length FLOAT,
        sepal_width FLOAT,
        petal_length FLOAT,
        petal_width FLOAT,
        species FLOAT
    )
""")

# Cargar el Iris dataset y llenarlo en la tabla
iris = load_iris()
for i in range(len(iris.data)):
    cursor.execute("""
        INSERT INTO iris_data (sepal_length, sepal_width, petal_length, petal_width, species)
        VALUES (%s, %s, %s, %s, %s)
    """, (*iris.data[i], iris.target_names[iris.target[i]]))

db.commit()
cursor.close()
db.close()
