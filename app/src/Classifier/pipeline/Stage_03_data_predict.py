from Classifier.config.configuration import ConfigurationManager as CM
from Classifier.components.data_predict import PredictAPI
from Classifier import logger



STAGE_NAME = "Predict"

class ModelPredictPipeline:
    def __init__(self):
        pass

    def main(self):
        predict_config = {"training":CM().get_data_training_config()["training"],
                            "extraction":CM().get_data_extraction_config()}

        training = PredictAPI(predict_config)
        training.api_tot()
        

if __name__ == '__main__':
    try:
        logger.info(f"-------------------")
        logger.info(f"******** stage {STAGE_NAME} started *********")
        obj = ModelPredictPipeline()
        obj.main()
        logger.info(f"******** stage {STAGE_NAME} completed *********\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
