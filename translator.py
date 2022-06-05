import requests
from requests_toolbelt import MultipartEncoder
import uuid
import json
import base64

from functions import read_json_file

def translate(source,output,source_lang,target_lang):
    data = {
      'source': source_lang,
      'target': target_lang,
      'image': (source, open(source, 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
    }
    secrets = read_json_file('secrets.json')
    headers = {
      "Content-Type": m.content_type,
      "X-NCP-APIGW-API-KEY-ID": secrets['X-NCP-APIGW-API-KEY-ID'],
      "X-NCP-APIGW-API-KEY": secrets['X-NCP-APIGW-API-KEY']
    }
    # Request API
    m = MultipartEncoder(data, boundary=uuid.uuid4())
    url = " https://naveropenapi.apigw.ntruss.com/image-to-image/v1/translate"
    res = requests.post(url, headers=headers, data=m.to_string())
    # Deal with Response 
    if res.status_code is not 200:
        print('Status code Error.')
        print(res.status_code)
        print(res.text)
  
    resObj = json.loads(res.text)
    imageStr = resObj.get("data").get("renderedImage")
    imgdata = base64.b64decode(imageStr)
    # Save as image file
    filename = output
    with open(filename, 'wb') as f:
        f.write(imgdata)





if __name__ == '__main__':
    # 이미지 1920x1920 이내로 자르기
    # source폴더의 모든 이미지파일이름 추출(to list)
    pass