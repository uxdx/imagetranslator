import cv2
import pytesseract

from math import comb
from typing import List, Tuple
from PIL import Image

def is_image_has_text(path):
    img = cv2.imread(path)   
    config = ('-l kor --oem 3 --psm 11')
    text = pytesseract.image_to_string(image=img, config=config)
    return text

def devide_img_as_height(limit:int, large_img:Image.Image) -> List[Image.Image]:
    (w,h) = large_img.size
    small_imgs = []
    for i in range(h//limit+1):
        upper = limit * i
        lower = limit * i + h%limit if (i == h//limit) else limit * (i+1)
        crop_box = (0, upper, w, lower)
        small_img = large_img.crop(crop_box)
        small_imgs.append(small_img)
    
    return small_imgs

def combine_img(small_imgs:List[Image.Image]) -> Image.Image:
    width, height = small_imgs[0].size[0], 0
    for img in small_imgs:
        height += img.size[1]
    print('large image size = ', width, height)
    large_img = Image.new('RGB',(width, height), (250,250,250))

    for idx in range(len(small_imgs)):
        limit = small_imgs[0].size[1]
        upper = limit * idx # 0, limit, 2limit, ...
        crop_box = (0, upper)
        large_img.paste(small_imgs[idx], crop_box)

    return large_img

if __name__ == '__main__':
    # large_img = Image.open('large_img.jpg')
    # print(large_img.size)
    # small_imgs = devide_img_as_height(limit=1960, large_img=large_img)
    # for img in small_imgs:
    #     print(img.size)
    
    # combined_img = combine_img(small_imgs=small_imgs)
    # combined_img.save('combined_img.jpeg', 'jpeg')
    # print(combined_img.size)
    # 파일에 한글 텍스트가 있는 지
    text = is_image_has_text('source/non_text_image.jpg')
    print(text)