from PIL import Image

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
def test_cutted_imgs(imgs:list):
    for img in imgs:
        print(img.size)

if __name__ == '__main__':
    cutted_imgs = make_better_image('large_img.jpg')
    print(cutted_imgs)
    test_cutted_imgs(cutted_imgs)
    # print(13000//1960)