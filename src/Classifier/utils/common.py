import os
import yaml
import pandas as pd
from Classifier import logger
import json
import joblib
from sklearn.pipeline import Pipeline
from pathlib import Path
from typing import Any
import base64
import mysql.connector
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, davies_bouldin_score, silhouette_score, calinski_harabasz_score
from sklearn.datasets import load_iris





def read_yaml(path_to_yaml):
    
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        raise e
    


def create_directories(path_to_directories, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


def conec_database(config):
    try:
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return connection,cursor    

def extract_workbench(config):

    try:
        print(config)
        query = f"SELECT * FROM {config['table']}"
        
                
        config.pop("table")
        
        connection,cursor=conec_database(config)
        # Cargar los datos de Iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        target_names = iris.target_names
        print(target)
        print(data)         
        cursor.execute("SELECT COUNT(*) FROM iris_dataset")
        record_count = cursor.fetchone()[0]

        if record_count == 0:
            
            insert_query = """
                INSERT INTO iris_dataset (sepal_length, sepal_width, petal_length, petal_width, species)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = [
                (float(data[i][0]), float(data[i][1]), float(data[i][2]), float(data[i][3]), float(target[i])) #target_names[target[i]])
                for i in range(len(data))
            ]

        
            cursor.executemany(insert_query, values)
            connection.commit()
        
        
        cursor.execute(query)
        field_names = [i[0] for i in cursor.description]
        result = pd.DataFrame(cursor.fetchall(),columns=field_names)
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
        
    


def fit_ml_models(algo, algo_param, algo_name,x_train,y_train,x_test,y_test):
    
    algo = Pipeline([("algo", algo)])
    
    
    model = GridSearchCV(algo, param_grid=algo_param, cv=10, verbose=1)
    
    
    logger.info(f"Fitting {algo_name}")
    fit_model = model.fit(x_train, y_train)
    
    best_params = model.best_params_
    logger.info("Best Parameters: "+f"{best_params}")
    
    best_model = model.best_estimator_
    best_estimator = model.best_estimator_._final_estimator
    best_score = round(model.best_score_, 4)
    logger.info(f"Best Score: "+"{:.3f}".format(best_score))
    
    y_pred_train = model.predict(x_train)
    y_pred_test = model.predict(x_test)
    
    
    acc_score_train = round(accuracy_score(y_pred_train, y_train)*100, 3)
    acc_score_test = round(accuracy_score(y_pred_test, y_test)*100, 3)
    logger.info(f"Train and Test Accuracy Score for train {acc_score_train} and test {acc_score_test}")
    
    logger.info(f"Finishing training")

    return acc_score_train, acc_score_test, best_score, best_params






def save_json(path, data):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")





def load_json(path):
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)



def save_bin(data, path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")



def load_bin(path):
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

