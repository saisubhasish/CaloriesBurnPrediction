import os,sys
import numpy as np
import pandas as pd 
from calories import utils
from calories.logger import logger
from calories.exception import CalorieException
from sklearn.model_selection import train_test_split
from calories.entity import config_entity, artifact_entity

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig ):
        '''
        Storing the input to a variable to use in pipeline
        '''
        try:
            logger.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CalorieException(e, sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        """
        This function takes Input: Database name and collection name
        and returns output: feature store file, train file and test file
        """
        try:
            logger.info(f"Exporting collection data as pandas dataframe")
            # Exporting collection data as pandas dataframe
            df:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)

            logger.info("Save data in feature store")
            # Save data in feature store
            logger.info("Create feature store folder if not available")
            #Create feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logger.info("Save df to feature store folder")
            # Save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logger.info("split dataset into train and test set")
            # split dataset into train and test set
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=42)
            
            logger.info("create dataset directory folder if not available")
            # Create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logger.info("Saving train df and test df to dataset folder")
            # Saving train df and test df to dataset folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            # Prepare artifact  
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logger.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise CalorieException(error_message=e, error_detail=sys)