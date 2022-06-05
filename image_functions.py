from PIL import Image
from typing import List, Tuple
import os

from functions import get_dir_and_name_from_path
def make_better_image(path):
    """
    API의 최대 입력 허용 사이즈인 1960 X 1960 에 맞게
    이미지를 가공
    ex) 700 x 14000 => ((700*2) X 1960) x4 
    ex2) 
    """
    im = Image.open(path)
    (sw,sh) = im.size # source width & height
    print("sw, sh = "+str((sw,sh)))
    # 최적화수치; 이걸로 빈공간에 이미지를 더 우겨넣을 수 있음.
    optimize_row = 1960//sw # 가로방향 최대 최적화수치(정수) 0, 1, 2, ...
    optimize_col = 1960//sh
    # 초과수치; 이만큼 추가로 api요청이 필요함
    oversize_row = sw//1960
    oversize_col = sh//1960
    print('oversize_row : '+str(oversize_row))
    print('oversize_col : '+str(oversize_col))
    # 초과수치에 근거한 이미지 분할 
    rows = []
    results = []
    if oversize_row > 0:
        for i in range(oversize_row):
            # (left, upper, right, lower)
            box = (1960 * i, 0, 1960 * (i+1), sh)
            rows.append(im.crop(box))
    else:
        rows.append(im)
    if oversize_col > 0:
        for img in rows:
            for i in range(oversize_col+1):
                # (left, upper, right, lower)
                upper = 1960 * i
                lower = (1960 * i + sh%1960) if i is oversize_col else 1960 * (i+1)
                print(lower)
                box = (0, upper, sw, lower)
                results.append(img.crop(box))
    else:
        import copy
        results = copy.deepcopy(rows)
    
    return results

def save_imgs(path, name, extension, imgs:List[Image.Image]):
    # save_imgs('./', 'sample', 'png', imgs)
    # => sample0.png, sample1.png, ...
    i = 0
    for img in imgs:
        fullpath = path+name+str(i)+'.'+extension
        img.save(fullpath, extension)
        print("saved image at ", fullpath)
        i += 1
def test_cutted_imgs(imgs:List[Image.Image]):
    for img in imgs:
        print(img.size)

def merge_two_images(img1:Image.Image, img2:Image.Image, path:str)->Image.Image:
    img1_size = img1.size
    img2_size = img2.size
    new_img = Image.new('RGB',(img1_size[0]+img2_size[0], img1_size[1]), (250,250,250))
    new_img.paste(img1,(0,0))
    new_img.paste(img2,(img1_size[0],0))
    new_img.save(path, path.split('.')[-1])

def divide_image(img:Image.Image, path:str)->List[Image.Image]:
    (w,h) = img.size
    img1 = img.crop((0, 0, w//2, h//2))
    img2 = img.crop((w//2, h//2, w, h))
    print(path.split('.')[0]+'0'+path.split('.')[-1])
    img1.save(path.split('.')[0]+'0.'+path.split('.')[-1])
    img2.save(path.split('.')[0]+'1.'+path.split('.')[-1])

def translate_large_image(path:str):
    file_dir, file_name = get_dir_and_name_from_path(path) # /images
    img_extension = file_name[1].split('.')[1] # 이미지 확장자. ex) 'png'
    img_name = file_name[1].split('.')[0] # 이미지명 ex) large_image
    # 이미지 로드
    large_image = Image.open(path)
    # 큰 이미지를 작은 이미지들로 쪼갬
    small_imgs, shattered_shape = make_small_images(limit_size=(820, 1960), large_image=large_image)
    # 작은 이미지들끼리 결합할 수 있으면 결합 ;생략
    for idx in range(len(small_imgs)):
        img = small_imgs[idx]
        # 결합한 이미지들이 글자를 포함하고 있는 지 확인, 그렇다면 번역
        if is_contains_text(img):
            small_imgs[idx] = translate(img) #! 번역결과는 json데이터로 반환되는 문제
    # 결합된 이미지들을 다시 원상태로 분리 ;생략
    # 번역된 이미지, 번역이 필요없었던 이미지들을 합쳐서 원래 큰 이미지로 만듬
    large_image = make_large_images(small_imgs=small_imgs, shattered_shape=shattered_shape)
    
#! 아래는 구현이 필요한 메소드들
def make_small_images(limit_size:Tuple[int,int], large_image:Image.Image) -> Tuple[List[Image.Image], Tuple[int, int]]:
    """_summary_

    Args:
        limit_size (Tuple[int,int]): 이미지를 쪼갤 기준이 되는 사이즈
        large_image (Image.Image): _description_

    Returns:
        Tuple[List[Image.Image], Tuple[int, int]]: 이미지리스트는 작은 이미지들의 데이터를, 튜플은 쪼개진 모양을 표현함
        예를들어 (3,2)가 반환되었다면 
        0 1
        2 3
        4 5 
        모양으로 쪼개진 것.
    """
    
    pass
def is_contains_text(img:Image.Image) -> bool:
    pass
def translate(img:Image.Image) -> Image.Image:
    pass
def make_large_images(small_imgs:List[Image.Image], shattered_shape:Tuple[int, int]) -> Image.Image:
    pass
if __name__ == '__main__':
    # cutted_imgs = make_better_image('large_img.jpg')
    # print(cutted_imgs)
    # test_cutted_imgs(cutted_imgs)
    # save_imgs('images/','small_image','png',cutted_imgs)
    # print(13000//1960)
    # img1 = Image.open('images/small_image0.png')
    # img2 = Image.open('images/small_image1.png')
    # img3 = Image.open('images/merged_image.png')
    # print(img1.size)
    # print(img2.size)
    # print(img3.size)
    # divide_image(img3,'images/divided_image.png')
    # merge_two_images(img1, img2, 'images/merged_image.png')
    dir, name = get_dir_and_name_from_path("images/larget_img.jpg")
    print(dir, '  ', name)