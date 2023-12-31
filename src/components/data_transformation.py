import sys
import os
from dataclasses import dataclass

import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
 

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object


@dataclass
class DataTrasformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")


class DataTrasformation:
    def __init__(self):
        self.data_transformation_config_obj = DataTrasformationConfig()

    def get_data_transformer_obj(self):
        try: 
            numerical_columns = ["writing_score","reading_score"]
            categorical_columns  = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course",]


            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            categorical_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            
             
            
            logging.info("numerical columns standard scaling done")
            logging.info("categorical columns scaling and encoding done")

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('categorical_pipeline',categorical_pipeline,categorical_columns)
                ]
            )


            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)
        


    def initiate_data_transformation(self,train_path,test_path):


        try :
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("reading of training and testing data completed")

            preprocessor_obj = self.get_data_transformer_obj()

            target_column_name= "math_score"
            numerical_columns = ["writing_score","reading_score"]


            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]


            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object to training and testing dataframes")

            input_feature_train_array = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessor_obj.transform(input_feature_test_df)


            train_array = np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            test_array  = np.c_[input_feature_test_array,np.array(target_feature_test_df)]

            save_object(
                file_path = self.data_transformation_config_obj.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            logging.info("Saved preprocessing object")

            return (train_array,test_array,self.data_transformation_config_obj.preprocessor_obj_file_path,)

        except Exception as e:
            raise CustomException(e,sys)