import os
import json
from typing import Tuple
def get_files_in_dir(path:str)->list:
    return os.listdir(path)

def get_dir_and_name_from_path(path:str) -> Tuple[str, str]:
    """
    Ex) "/tmp/d/a.dat" -> '/tmp/d', 'a.dat'
    """
    return os.path.split(path)

def read_json_file(path)->dict:
    with open(path) as f:
       data = json.load(f)
    return data

def clean_dir(path:str):
    files_in_dir = get_files_in_dir(path)
    for file in files_in_dir:
        os.remove(path+file)
        print(path+file, 'is removed.')
    print('Clear succeed.')

if __name__ == '__main__':
    # list = get_files_in_dir("images/")
    # print(list)
    # print(read_json_file('secrets.json'))
    # print(type(read_json_file('secrets.json')))
    # print(read_json_file('secrets.json')['X-NCP-APIGW-API-KEY-ID'])
    # print(read_json_file('secrets.json')['X-NCP-APIGW-API-KEY'])
    clean_dir('images/')