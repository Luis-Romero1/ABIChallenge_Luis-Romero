import os
from Classifier.constants import *
from Classifier.utils.common import read_yaml, create_directories

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config["artifact_root"]])
    
    def get_data_extraction_config(self):
        config = self.config["data_extraction"]

        data_extraction_config = {"user":"iris1",#os.getenv("DB_USER"),
            "password":"Xi25_PS6iww9os?z3",#os.getenv("DB_PASSWORD"),
            "host":"iris-db-instance.c3kq6wgkc2hl.us-east-1.rds.amazonaws.com",#os.getenv("DB_HOST"),
            "database":config["database"],
            "table":config["table"] }

        return data_extraction_config
    

    def get_data_training_config(self):
        self.config["training"]["root_dir"]=Path(self.config["training"]["root_dir"])
        self.config["training"]["trained_model_path"]=Path(self.config["training"]["trained_model_path"])
        data_training_config = {"params":self.params,
                              "training":self.config["training"]}

        return data_training_config

