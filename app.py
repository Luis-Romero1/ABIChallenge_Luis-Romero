from Classifier.pipeline.Stage_03_data_predict import ModelPredictPipeline
from Classifier import logger

STAGE_NAME = "Predict"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
   model_predict= ModelPredictPipeline()
   model_predict.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

