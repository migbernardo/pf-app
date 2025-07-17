import os
import yaml
import numpy as np

def read_yaml(file_path:os.path):
    """
    YAML file reader
    :param file_path: file path specified with os.path module
    :return: python object
    """
    with open(file=file_path, mode='r', encoding='utf-8') as stream:
        loaded = yaml.safe_load(stream=stream)
        return loaded

def write_yaml(file_path:os.path, data:dict):
    """
    YAML file writer
    :param file_path: file path specified with os.path module
    :param data: data to be written in the yaml file
    :return: python object
    """
    with open(file=file_path, mode='w', encoding='utf-8') as stream:
        yaml.dump(data=data, stream=stream)

def np_dtype_converter(data_types:dict) -> dict:
    """
    Numpy data type converter
    :param data_types: dictionary that contains the column: np dtype
    :return: dictionary of dtypes converted to string
    """
    dtypes = data_types
    for col, dt in dtypes.items():
        if dt == np.dtype('O'):
            dtypes[col] = 'object'
        elif dt == np.dtype('float64'):
            dtypes[col] = 'np.float64'
        elif dt == np.dtype('float32'):
            dtypes[col] = 'np.float32'
        elif dt == np.dtype('int64'):
            dtypes[col] = 'np.int64'
        elif dt == np.dtype('int32'):
            dtypes[col] = 'np.int32'
    return dtypes


if __name__ == '__main__':

    # run as module: python -m src.utils.read_files

    FILE = os.path.join('src', 'utils', 'data_model.yml')

    loaded_file = read_yaml(file_path=FILE)

    print(loaded_file)