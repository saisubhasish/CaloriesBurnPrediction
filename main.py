from calories.entity import config_entity
from calories.components.data_ingestion import DataIngestion
from calories.components.data_validation import DataValidation

def main():
    training_pipeline_config = config_entity.TrainingPipelineConfig()

    #data ingestion         
    data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.to_dict())
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    #data validation
    data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
    data_validation = DataValidation(data_validation_config=data_validation_config,
                data_ingestion_artifact=data_ingestion_artifact)

    data_validation_artifact = data_validation.initiate_data_validation()
if __name__ == "__main__":
    main()