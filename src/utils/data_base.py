import os
import pandas as pd
import numpy as np
from datetime import datetime
from glob import glob
from src.utils.file_io import read_yaml, write_yaml, np_yaml_dtype_converter, np_python_dtype_converter
from pydantic import BaseModel, create_model
#from typing import Any, Optional

class DataBase:
    """
    A base class to create the application database

    Attributes:
        schema: evaluated database schema
        df: supporting data frame
        mode: create database: "create" or read existing database "read"
        write_schema: write database schema - default false
    """
    def __init__(self, mode:str, data_path:os.path, write_schema:bool=False):
        self.mode = mode
        self.data_path = data_path

        if mode == 'create':
            self.schema = self.read_schema()
            self.df = self.create_df()

        elif mode == 'read':
            self.schema = self.read_schema()
            self.df = self.read_df()

        elif mode != 'read':
            raise ValueError('Select a valid value for mode: "w" or "r"')

        if write_schema:
            self.write_schema()

    def read_schema(self, db_name:str='transaction-db') -> dict:
        """
        Read database data model
        :param db_name: database name - "transaction-db" default
        :return: Schema dictionary with the evaluated data types
        """
        # get latest yml file from data path
        files = glob(os.path.join(self.data_path, '*.yml'))
        file_path = max(files, key=os.path.getmtime)
        data_model = read_yaml(file_path=file_path)
        return {column: eval(datetype) for column, datetype in data_model[db_name].items()}

    def write_schema(self, db_name:str='transaction-db'):
        """
        Write database data model
        :param db_name: database name - "transaction-db" default
        :return: Data model saved in yaml file
        """
        dtypes = self.df.dtypes.to_dict()
        data_model = np_yaml_dtype_converter(data_types=dtypes)
        data_model = {db_name: {col: dt for col, dt in data_model.items()}}
        dt_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.data_path, f'{dt_now}_data_model.yml')
        write_yaml(file_path=file_path, data=data_model)

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

    def insert_transaction(self, request:dict) -> object:
        """
        Insert row into the transaction database
        :param request: request dictionary following the data model schema
        :return: Data frame with a new row inserted
        """
        self.df = self.df._append(request, ignore_index=True)

    def update_transaction(self, request:dict) -> object:
        """
        Update an existing row of the transaction database
        :param request: request dictionary following the data model schema
        :return: Data frame with an updated row
        """
        df_indexes = list(self.df.index)
        row_index = list(request.keys())[0]
        if row_index not in df_indexes:
            raise ValueError('Invalid index')
        self.df.loc[row_index] = request[row_index]

    def delete_transactions(self, row_indexes: list) -> object:
        """
        Delete existing rows of the transaction database
        :param row_indexes: list of row indexes to delete from the database
        :return: Data frame with deleted rows
        """
        df_indexes = list(self.df.index)
        filtered_row_indexes = [index for index in row_indexes if index in df_indexes]
        if len(filtered_row_indexes) != len(row_indexes):
            raise ValueError('Invalid indexes')

        self.df.drop(index=filtered_row_indexes, inplace=True)

    def search_records(self, column: str, value) -> list:
        """
         Search rows based on specific column values
         :param column: column to search
         :param value: value to search of the selected column
         :return: list of indexes for matched search criteria
         """
        indexes = list(self.df[column].loc[lambda x: x == value].index)
        return indexes

if __name__ == '__main__':

    # run as module: python -m src.utils.read_files

    data_dir = os.path.join('src', 'data')

    db = DataBase(mode='read', data_path=data_dir)

    #db.write_df()

    #db.df = db.df._append({'date': '2025-01-04', 'amount': 14.68, 'description': 'sushi', 'category': 'restaurant'}, ignore_index=True)

    db.insert_transaction({'date': '2025-01-04', 'amount': 14.68, 'description': 'sushi', 'category': 'restaurant'})

    db.insert_transaction({'date': '2025-01-06', 'amount': 1.99, 'description': 'tooth paste', 'category': 'personal'})

    db.update_transaction({0: {'date': '2025-01-06', 'amount': 7.68, 'category': 'restaurant'}})

    #db.delete_transactions(row_indexes=[0])

    model_schema = {col: (type, None) for col, type in np_python_dtype_converter(data_types=db.schema).items()}

    print(model_schema)

    model =  create_model('Transaction', **model_schema)

    print(model)

    #model.model_construct(db.schema)

    #print(db.schema)

    #print(db.df.info())

    #print(db.df)

    print(model.model_validate({'date': '2025', 'amount': 4.56, 'description': 'tooth paste', 'category': 'other'}))

    print(model.model_fields)