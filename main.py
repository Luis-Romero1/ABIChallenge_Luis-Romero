from Classifier import logger
from Classifier.pipeline.Stage_01_data_extraction import DataExtractionPipeline
from Classifier.pipeline.Stage_02_data_train import ModelTrainingPipeline



STAGE_NAME = "Data Extraction stage"


try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataExtractionPipeline()
    df=obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

print(df)


STAGE_NAME = "Training"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_training= ModelTrainingPipeline()
   model_training.main(df)
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

