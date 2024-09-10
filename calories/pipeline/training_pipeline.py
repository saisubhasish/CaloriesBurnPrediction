import os, sys

from calories.logger import logging
from calories.exception import CalorieException
from calories.utils import get_collection_as_dataframe

from calories.entity import config_entity, artifact_entity
from calories.entity.config_entity import DataIngestionConfig
from calories.entity.config_entity import DataValidationConfig
from calories.entity.config_entity import DataTransformationConfig

from calories.components.data_ingestion import DataIngestion
from calories.components.data_validation import DataValidation
from calories.components.model_pusher import ModelPusher
from calories.components.data_transformation import DataTransformation
from calories.components.model_trainer import ModelTrainer
from calories.components.model_evaluation import ModelEvaluation





def start_training_pipeline():
     try:
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

         #data transformation
         data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
         data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
         data_validation_artifact=data_validation_artifact)
         data_transformation_artifact = data_transformation.initiate_data_transformation()

         #model trainer
         model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
         model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
         model_trainer_artifact = model_trainer.initiate_model_trainer()

         #model evaluation
         model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
         model_eval  = ModelEvaluation(model_eval_config=model_eval_config,
         data_ingestion_artifact=data_ingestion_artifact,
         data_transformation_artifact=data_transformation_artifact,
         model_trainer_artifact=model_trainer_artifact)
         model_eval_artifact = model_eval.initiate_model_evaluation()

         # Model Pusher
         model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config)

         model_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
                  data_transformation_artifact=data_transformation_artifact,
                  model_trainer_artifact=model_trainer_artifact)

         model_pusher_artifact = model_pusher.initiate_model_pusher()

     except Exception as e:
          raise ThyroidException(error_message=e, error_detail=sys)