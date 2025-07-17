import os
import pandas as pd
import numpy as np
from datetime import datetime
from glob import glob
from src.utils.file_io import read_yaml, write_yaml, np_dtype_converter

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
            self.write_schema()

        elif mode != 'r':
            raise ValueError('Select a valid value for mode: "w" or "r"')

    def read_schema(self) -> dict:
        """
        Data model parser
        :return: Schema dictionary with the evaluated data types
        """
        return {column: eval(datetype) for column, datetype in self.data_model.items()}

    def write_schema(self, db_name:str='transaction-db'):
        """
        Write database data model
        :param db_name: database name - "transaction-db" default
        :return: Data model saved in yaml file
        """
        dtypes = self.df.dtypes.to_dict()
        data_model = np_dtype_converter(data_types=dtypes)
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
        Delete an existing row of the transaction database
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

    dm_file = os.path.join('src', 'utils', 'data_model.yml')

    loaded_file = read_yaml(file_path=dm_file)

    loaded_data_model = loaded_file['transaction-db']

    data_dir = os.path.join('src', 'data')

    db = DataBase(data_model=loaded_data_model, mode='r', data_path=data_dir)

    #db.write_df()

    #db.df = db.df._append({'date': '2025-01-04', 'amount': 14.68, 'description': 'sushi', 'category': 'restaurant'}, ignore_index=True)

    db.insert_transaction({'date': '2025-01-04', 'amount': 14.68, 'description': 'sushi', 'category': 'restaurant'})

    db.insert_transaction({'date': '2025-01-06', 'amount': 1.99, 'description': 'tooth paste', 'category': 'personal'})

    db.update_transaction({0: {'date': '2025-01-06', 'amount': 7.68, 'category': 'restaurant'}})

    #db.delete_transactions(row_indexes=[0])

    print(db.df.info())

    print(db.df)

    #print(list(db.df['date'].loc[lambda x: x == '2025-01-06'].index))