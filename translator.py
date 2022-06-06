import requests
from requests_toolbelt import MultipartEncoder
import uuid
import json
import base64
import os
from PIL import Image
from functions import read_json_file


def translate_PILimg(img:Image.Image) -> Image.Image:
  """
  파파고 이미지번역을 이용하기 위해 임시로 파일을 만들어 번역 후
  다시 이미지데이터로 변환해서 반환.

  Args:
      img (Image.Image): 이 이미지데이터를 번역합니다.

  Returns:
      Image.Image: 번역된 이미지데이터를 반환합니다.
  """
  temp_file_path = 'temp/temp.png'
  translated_file_path = 'temp/translated.png'
  # 이미지를 파일로 다운
  print('Create temp file...')
  img.save(temp_file_path, 'png')
  # 파일에 대해 번역
  print('Translating the file...')
  translate(source=temp_file_path, output=translated_file_path, source_lang='ko', target_lang='ja')
  # 파일을 이미지로 변환
  translated_img = Image.open(translated_file_path)
  # 파일 삭제
  print('Remove temp files...')
  os.remove(temp_file_path)
  os.remove(translated_file_path)
  # 반환
  return translated_img

def translate(source:str,output:str,source_lang:str,target_lang:str):
    data = {
      'source': source_lang,
      'target': target_lang,
      'image': (source, open(source, 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
    }
    secrets = read_json_file('secrets.json')
    m = MultipartEncoder(data, boundary=uuid.uuid4())
    headers = {
      "Content-Type": m.content_type,
      "X-NCP-APIGW-API-KEY-ID": secrets['X-NCP-APIGW-API-KEY-ID'],
      "X-NCP-APIGW-API-KEY": secrets['X-NCP-APIGW-API-KEY']
    }
    # Request API
    url = " https://naveropenapi.apigw.ntruss.com/image-to-image/v1/translate"
    res = requests.post(url, headers=headers, data=m.to_string())
    # Deal with Response 
    if res.status_code != 200:
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
    print('Translate succeed.')





if __name__ == '__main__':
    # 이미지 1920x1920 이내로 자르기
    # source폴더의 모든 이미지파일이름 추출(to list)
    source_img = Image.open('source/crownford1.jpg')
    translated_img = translate_PILimg(source_img)

    pass