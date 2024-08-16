import os
import yaml
import pandas as pd
from Classifier import logger
import json
import joblib
from ensure import ensure_annotations
from sklearn.pipeline import Pipeline
from pathlib import Path
from typing import Any
import base64
import mysql.connector
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, davies_bouldin_score, silhouette_score, calinski_harabasz_score




@ensure_annotations
def read_yaml(path_to_yaml: Path):
    
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
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

        cursor.execute(query)
        field_names = [i[0] for i in cursor.description]
        result = pd.DataFrame(cursor.fetchall(),columns=field_names)
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return result



def fit_ml_models(algo, algo_param, algo_name,x_train,y_train,x_test,y_test):
    # --- Algorithm Pipeline ---
    algo = Pipeline([("algo", algo)])
    
    # --- Apply Grid Search ---
    model = GridSearchCV(algo, param_grid=algo_param, cv=10, verbose=1)
    
    # --- Fitting Model ---
    logger.info(f"Fitting {algo_name}")
    fit_model = model.fit(x_train, y_train)
    
    # --- Model Best Parameters ---
    best_params = model.best_params_
    logger.info("Best Parameters: "+f"{best_params}")
    # --- Best & Final Estimators ---
    best_model = model.best_estimator_
    best_estimator = model.best_estimator_._final_estimator
    best_score = round(model.best_score_, 4)
    logger.info(f"Best Score: "+"{:.3f}".format(best_score))
    # --- Create Prediction for Train & Test ---
    y_pred_train = model.predict(x_train)
    y_pred_test = model.predict(x_test)
    
    # --- Train & Test Accuracy Score ---
    acc_score_train = round(accuracy_score(y_pred_train, y_train)*100, 3)
    acc_score_test = round(accuracy_score(y_pred_test, y_test)*100, 3)
    logger.info(f"Train and Test Accuracy Score for train {acc_score_train} and test {acc_score_test}")
    
    logger.info(f"Finishing training")

    return acc_score_train, acc_score_test, best_score, best_params





@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path):
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


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path):
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

