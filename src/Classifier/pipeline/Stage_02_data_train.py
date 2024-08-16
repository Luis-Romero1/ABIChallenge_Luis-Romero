from Classifier.config.configuration import ConfigurationManager as CM
from Classifier.components.data_train import pass_train
from Classifier import logger



STAGE_NAME = "Training"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self,df):
        training_config = CM().get_data_training_config()
        training = pass_train(training_config,df)
        training.prepare_data()
        training.run_train()

if __name__ == '__main__':
    try:
        logger.info(f"-------------------")
        logger.info(f"******** stage {STAGE_NAME} started *********")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f"******** stage {STAGE_NAME} completed *********\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
        
