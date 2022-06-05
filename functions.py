import os
import json
def get_files_in_dir(path:str)->list:
    return os.listdir(path)

def read_json_file(path)->dict:
    with open(path) as f:
       data = json.load(f)
    return data
    
if __name__ == '__main__':
    # list = get_files_in_dir("output/")
    # print(list)
    print(read_json_file('secrets.json'))
    print(type(read_json_file('secrets.json')))
    print(read_json_file('secrets.json')['X-NCP-APIGW-API-KEY-ID'])
    print(read_json_file('secrets.json')['X-NCP-APIGW-API-KEY'])