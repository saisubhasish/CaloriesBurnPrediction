import yaml
import dill    # To store python object as a file like pkl
import os,sys
import numpy as np
import pandas as pd
from calories.logger import logger
from calories.exception import CalorieException
from calories.config import mongo_client

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:    
        logger.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logger.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logger.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logger.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise CalorieException(e, sys)
    
def write_yaml_file(file_path,data:dict):
    """
    Creating yaml report for validation status of each column
    """
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise CalorieException(e, sys)
    
def convert_columns_float(df:pd.DataFrame)->pd.DataFrame:
    """
    Converting column to float type except target column
    """
    try:
        for column in df.columns:
            df[column]=df[column].astype('float')
        return df
    except Exception as e:
        raise e

def save_object(file_path: str, obj: object) -> None:
    """
    Saving object 
    """
    try:
        logger.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logger.info("Exited the save_object method of utils")
    except Exception as e:
        raise CalorieException(e, sys) from e

def load_object(file_path: str, ) -> object:
    """
    Loading object
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CalorieException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CalorieException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CalorieException(e, sys) from e