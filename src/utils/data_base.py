import os
import pandas as pd
import numpy as np
from datetime import datetime
from glob import glob
from src.utils.read_files import read_yaml

class DataBase:
    """
    A base class to create the application database

    Attributes:
        schema: evaluated database schema
        df: supporting data frame
        mode: create database: "w" or read existing database "r"
    """
    def __init__(self, data_model:dict, mode:str, data_path:os.path):
        self.mode = mode
        self.data_path = data_path

        if mode == 'w':
            self.data_model = data_model
            self.schema = self.read_schema()
            self.df = self.create_df()

        elif mode == 'r':
            self.df = self.read_df()

        elif mode != 'r':
            raise ValueError('Select a valid value for mode: "w" or "r"')

    def read_schema(self) -> dict:
        """
        Data model parser
        :return: Schema dictionary with the evaluated data types
        """
        return {column: eval(datetype) for column, datetype in self.data_model.items()}

    #def write_schema(self):
        #return

    def create_df(self) -> pd.DataFrame:
        """
        Create database data frame
        :return: Empty pandas data frame based on the defined schema
        """
        df_columns = pd.DataFrame(columns=list(self.schema.keys()))
        df_schema = df_columns.astype(dtype=self.schema)
        return df_schema

    def read_df(self) -> pd.DataFrame:
        """
        Read database data frame
        :return: Pandas data frame based on the parquet file
        """
        # get latest parquet file from data path
        files = glob(os.path.join(self.data_path, '*.parquet'))
        file_path = max(files, key=os.path.getmtime)
        df = pd.read_parquet(path=file_path, engine='fastparquet')
        return df

    def write_df(self):
        """
        write database data frame
        :return: Parquet file of the pandas data frame with timestamp naming
        """
        dt_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.data_path, f'{dt_now}_db.parquet')
        self.df.to_parquet(path=file_path, engine='fastparquet', compression='gzip')

    def insert_transaction(self, request:dict):
        self.df = self.df._append(request, ignore_index=True)

    def update_transaction(self, request:dict):
        self.df = self.df._append(request, ignore_index=True)

    def delete_transaction(self, request: dict):
        self.df = self.df._append(request, ignore_index=True)

if __name__ == '__main__':

    # run as module: python -m src.utils.read_files

    dm_file = os.path.join('src', 'utils', 'data_model.yml')

    loaded_file = read_yaml(file_path=dm_file)

    loaded_data_model = loaded_file['transaction-db']

    data_dir = os.path.join('src', 'data')

    db = DataBase(data_model=loaded_data_model, mode='r', data_path=data_dir)

    #db.write_df()

    #db.df = db.df._append({'date': '2025-01-04', 'amount': 14.68, 'description': 'sushi', 'category': 'restaurant'}, ignore_index=True)

    #db.insert_transaction({'date': '2025-01-04', 'amount': 14.68, 'description': 'sushi', 'category': 'restaurant'})

    db.insert_transaction({'date': '2025-01-06', 'amount': 7.68, 'category': 'restaurant'})

    print(db.df.info())

    print(db.df)