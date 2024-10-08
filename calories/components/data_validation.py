import os,sys 
import pandas as pd
from scipy.stats import ks_2samp    # Compares the continuous distribution of two independent columns
from typing import Optional

from calories import utils
from calories.logger import logging
from calories.exception import CalorieException
from calories.entity import artifact_entity,config_entity


class DataValidation:
    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise CalorieException(e, sys)
    def drop_unnecessary_columns(self, df:pd.DataFrame, report_key_name:str)->Optional[pd.DataFrame]:
        """
        This function will drop unnecessary columns from dataframe
        
        df : Accepts a pandas dataframe
        =========================================================================================
        returns Pandas Dataframe by dropping 'Ussr_ID' column
        """
        try:
            drop_columns = ['User_ID']
            logging.info(f"UnnecessaColumns dropped: {drop_columns}")
            self.validation_error[report_key_name] = drop_columns
            drop_columns = df[drop_columns]
            df.drop(columns=drop_columns, axis=1, inplace=True)
            return df
            
        except Exception as e:
            raise CalorieException(e, sys)
        
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        """
        This function checks if required columns exists or not by comparing current df with base df and returns
        output as True and False
        """
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:    
                if base_column not in current_columns:
                    logging.info(f"Column: [{base_column} is not available.]")
                    missing_columns.append(base_column)

            # Return False if there are missing columns in current df other wise True
            if len(missing_columns)>0:
                self.validation_error[report_key_name]=missing_columns
                return False    
            return True
            
        except Exception as e:
            raise CalorieException(e, sys)

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report=dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]
                # Null hypothesis : Both column data has same distribution
                
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)   # Comparing the continuous distribution

                if same_distribution.pvalue>0.05:
                    # We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    # Different distribution                    
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }

            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise CalorieException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info("Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            
            logging.info(f"There are {base_df.isnull().sum()} null values in base df")
            #base_df has 0 null values")

            logging.info("Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("Drop unnecessary columns")
            base_df = self.drop_unnecessary_columns(df=base_df, report_key_name="base_df")
            train_df = self.drop_unnecessary_columns(df=train_df, report_key_name="train_df")
            test_df = self.drop_unnecessary_columns(df=test_df, report_key_name="test_df")

            logging.info("Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info("Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:     # If True
                logging.info("As all column are available in train df hence detecting data drift in train dataframe")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:     # If True
                logging.info("As all column are available in test df hence detecting data drift test dataframe")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")

            logging.info("create dataset directory folder if not available for validated train file and test file")
            # Create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_validation_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Saving validated train df and test df to dataset folder")
            # Saving validated train df and test df to dataset folder
            train_df.to_csv(path_or_buf=self.data_validation_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_validation_config.test_file_path,index=False,header=True)
            
            # Write the report
            logging.info("Writing report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)   # valiadtion_error: drop columns, missing columns, drift report

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path, 
            train_file_path=self.data_validation_config.train_file_path, test_file_path=self.data_validation_config.test_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CalorieException(e, sys)