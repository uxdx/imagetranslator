from cgitb import small
import requests
from requests_toolbelt import MultipartEncoder
import uuid
import json
import base64
import os
from PIL import Image
from functions import read_json_file
from image_functions import combine_img, devide_img_as_height

def large_image_translate(source:str,output:str):
  # 소스를 PIL형으로 변환
  large_source = Image.open(source)
  # 작은 이미지로 나눔
  print("Slicing image...")
  small_imgs = devide_img_as_height(limit=1960, large_img=large_source)
  # 작은 이미지들을 번역
  print("Translating images...")
  
  for i in range(len(small_imgs)):
    print(i+1, '/',len(small_imgs))
    translated_small_img = translate_PILimg(small_imgs[i])
    small_imgs[i] = translated_small_img
    translated_small_img.save(f'temp/translated{i}.png', 'png')
    
  # 작은 이미지들을 합침
  print("Combine images...")
  large_output = combine_img(small_imgs=small_imgs)
  # PIL형 큰 이미지를 save
  print("Save at ", output)
  if output.split('.')[-1] == 'jpg':
      output = output.replace('jpg', 'jpeg')

  large_output.save(output, output.split('.')[-1])



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
  # print('Remove temp files...')
  # os.remove(temp_file_path)
  # os.remove(translated_file_path)
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
    if res.status_code == 200:
        resObj = json.loads(res.text)
        imageStr = resObj.get("data").get("renderedImage")
        imgdata = base64.b64decode(imageStr)
        # Save as image file
        filename = output
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print('Translate succeed.')

    elif res.status_code == 500:
      # 이미지에 글자가 발견되지 않은 경우
        import shutil
        shutil.copy(source, output)
        print(res.status_code, 'Error.')
        print(source,' is coped to ', output)
    else:
        print('Status code Error.')
        print(res.status_code)
        print(res.text)





if __name__ == '__main__':
    large_image_translate('source/텀블러 상세3.jpg', 'output/텀블러 상세3_translated.jpg')