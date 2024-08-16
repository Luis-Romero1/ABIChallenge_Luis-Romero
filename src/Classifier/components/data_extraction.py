

from Classifier import logger
# from Classifier.config.configuration import ConfigurationManager as CM
from Classifier.utils.common import extract_workbench

class extraction:
    def __init__(self,config):
        self.config = config
     
    def extract_info(self):

        logger.info(f"Extracting data from database")
        self.data=extract_workbench(self.config)
        logger.info(f"Extracteded data from database")
        return self.data
    
    