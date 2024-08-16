from Classifier.config.configuration import ConfigurationManager
from Classifier.components.data_extraction import extraction
from Classifier import logger



STAGE_NAME = "Data extraction stage"

class DataExtractionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_extraction_config = config.get_data_extraction_config()
        data_extraction = extraction(config=data_extraction_config)
        return data_extraction.extract_info()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataExtractionPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

