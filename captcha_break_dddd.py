try:
    import ddddocr
except ModuleNotFoundError:
    from os import system
    from platform import platform
    if 'Windows' in platform():
        system(r'pip3 install ddddocr -i https://pypi.tuna.tsinghua.edu.cn/simple')
    else:
        system(r'pip3 install ddddocr')
    import ddddocr

ocr = ddddocr.DdddOcr()

def dddd_2(ss):
    print(f'dddd_2 {ss}')
    ss = ss.lower()
    s_set = {'0':'o', '1':'i', '2':'z', '3':'b', '4':'a', '5':'s', '6':'b', '7':'t', '8':'s', '9':'q'}
    res = ''
    for s in ss:
        s = s_set.get(s,s)
        if 'a' <= s <='z':
             res += s
    return res

def dddd(image):
    res = ocr.classification(image)
    res = dddd_2(res)
    print(f'dddd {res}')
    return res

if __name__ == "__main__":
    with open("01.jpg", 'rb') as f:
        image = f.read()
    print(dddd(image))
