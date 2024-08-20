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
        
    def load_model(self):
        self.model=joblib.load(self.config_tra["trained_model_path"])

    def connect_db(self):
        
        self.config_con.pop("table")
        self.db, self.cursor = conec_database(self.config_con)

    
    def predict(self):
        
        data = request.json
        inputs = data['inputs']
        predictions = self.model.predict(inputs)
        curr_time=time.time()
        
        for i, pred in enumerate(predictions):
            self.cursor.execute("""
                INSERT INTO predictions (sepal_length, sepal_width, petal_length, petal_width, pred_species, time_pred)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (*inputs[i], pred, curr_time))
        self.db.commit()

        return jsonify({'predictions': predictions.tolist()})

    def setup_routes(self):
        
        self.app.add_url_rule('/predict', view_func=self.predict, methods=['POST'])

    def run(self):
        
        self.setup_routes()
        self.app.run(debug=True)

    def api_tot(self):
        self.load_model()
        self.connect_db()
        self.run()
