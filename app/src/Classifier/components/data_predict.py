from flask import Flask, request, jsonify
import pickle
import mysql.connector
import os
import joblib
from Classifier.utils.common import conec_database 
import time

class PredictAPI:
    def __init__(self, config):
        self.config_tra = config["training"]
        self.config_con=config["extraction"]
        self.app = Flask(__name__)
        #self.model = self.load_model()
        #self.db, self.cursor = self.connect_db()

    def load_model(self):
        # Cargar el modelo entrenado desde un archivo .pkl
        # model_path = self.config.get("model_path", "modelo_entrenado.pkl")
        self.model=joblib.load(self.config_tra["trained_model_path"])

    def connect_db(self):
        # Conectar a la base de datos utilizando las variables de entorno o configuración
        self.config_con.pop("table")
        self.db, self.cursor = conec_database(self.config_con)

    
    def predict(self):
        # Método para manejar la predicción desde la API
        data = request.json
        inputs = data['inputs']
        predictions = self.model.predict(inputs)
        curr_time=time.time()
        # Guardar las predicciones y entradas en la base de datos
        for i, pred in enumerate(predictions):
            self.cursor.execute("""
                INSERT INTO predictions (sepal_length, sepal_width, petal_length, petal_width, pred_species, time_pred)
                VALUES (%s, %s, %s, %s, %s, %f)
            """, (*inputs[i], pred, curr_time))
        self.db.commit()

        return jsonify({'predictions': predictions.tolist()})

    def setup_routes(self):
        # Configurar la ruta para la API de predicción
        self.app.add_url_rule('/predict', view_func=self.predict, methods=['POST'])

    def run(self):
        # Método para correr la API
        self.setup_routes()
        self.app.run(debug=True)

    def api_tot(self):
        self.load_model()
        self.connect_db()
        self.run()

        # api = PredictAPI(self.config)
        # api.run()
# if __name__ == '__main__':
#     # Configuración que podría ser cargada desde un archivo o entorno
#     config = {
#         "model_path": "modelo_entrenado.pkl",
#         "db_host": "localhost",
#         "db_user": "tu_usuario",
#         "db_password": "tu_contraseña",
#         "db_name": "nombre_base_datos"
#     }

    # Inicializar y correr la API
    # load_model()
    # connect_db()
    # api = PredictAPI(config)
    # api.run()