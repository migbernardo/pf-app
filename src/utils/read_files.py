import os
import yaml

def read_yaml(file_path:os.path):
    """
    YAML file reader
    :param file_path: file path specified with os.path module
    :return: python object
    """
    with open(file=file_path, mode='r', encoding='utf-8') as stream:
        loaded = yaml.safe_load(stream=stream)
        return loaded

if __name__ == '__main__':

    # run as module: python -m src.utils.read_files

    FILE = os.path.join('src', 'utils', 'data_model.yml')

    loaded_file = read_yaml(file_path=FILE)

    print(loaded_file)