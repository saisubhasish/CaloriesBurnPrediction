import sys 
import numpy as np
import pandas as pd
from typing import Optional
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler    # To normalize the data

from calories import utils
from calories.logger import logging
from calories.entity import artifact_entity,config_entity
from calories.exception import CalorieException
from calories.config import TARGET_COLUMN


class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_validation_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise CalorieException(e, sys)
    def feature_encoding(self,df:pd.DataFrame)->Optional[pd.DataFrame]:
        """
        This function will replace the categorical data of each column to numerical (Array type)

        df : Accepts a pandas dataframe
        =========================================================================================
        returns Pandas Dataframe after converting to numerical value
        """
        try:
            logging.info("Replacing 'female' to 0 and 'male' to 1 'Gender' column")
            df['Gender'] = df['Gender'].replace({'female':0, 'male':1})
            return df

        except Exception as e:
            raise CalorieException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:     # Attributes of this class will be same across all the object 
        try:
            robust_scaler =  StandardScaler()
            pipeline = Pipeline(steps=[
                    ('StandardScaler',robust_scaler)  # To normalize the data
                ])
            return pipeline
        except Exception as e:
            raise CalorieException(e, sys)
    
    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            logging.info("Reading training and testing file")
            train_df = pd.read_csv(self.data_validation_artifact.train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)

            logging.info("Converting female to 0 and male to 1")
            train_df = self.feature_encoding(train_df)
            test_df = self.feature_encoding(test_df)

            logging.info("Converting columns to float")
            train_df = utils.convert_columns_float(df=train_df)
            test_df = utils.convert_columns_float(df=test_df)
            
            # Selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            # Selecting target feature for train and test dataframe
            target_feature_train_arr = train_df[TARGET_COLUMN]
            target_feature_test_arr = test_df[TARGET_COLUMN]

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            # Transforming input features
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)  # Transformaing input features to array
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)

            # Target encoder
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]    # concatenated array
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            # Save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)

            # Saving object
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipleine)

            # Preparing Artifact
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path)

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
            
        except Exception as e:
            raise CalorieException(e, sys)