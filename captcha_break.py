import base64
import json
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from time import sleep

def base64_api(uname, pwd, img, typeid):
    base64_data = base64.b64encode(img)
    b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    try:
        result = json.loads(requests.post("https://api.ttshitu.com/predict", json=data).text)
    except:
        import traceback
        print(traceback.format_exc())
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    return result

def reportError(id):
    data = {"id": id}
    result = json.loads(requests.post("http://api.kuaishibie.cn/reporterror.json", json=data).text)
    if result['success']:
        return "报错成功"
    else:
        return result["message"]

from sys import exit as sys_exit
def getCaptchaData(zlapp):
    url = 'https://zlapp.fudan.edu.cn/backend/default/code'
    headers = {'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'dnt': '1',
    'referer': 'https://zlapp.fudan.edu.cn/site/ncov/fudanDaily',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    "User-Agent": zlapp.UA}
    if hasattr(zlapp, 'get'):
        res = zlapp.get(url, headers=headers)
    else:
        res = zlapp.session.get(url, headers=headers)
    sleep(1)
    return res.content

class DailyFDCaptcha:
    zlapp = None
    uname = ''
    pwd = ''
    typeid = 2 # 纯英文
    info = lambda x: x
    id = 0
    def __init__(self,
                 uname, pwd,
                 zlapp,
                 info_callback):
        self.zlapp = zlapp
        self.uname = uname
        self.pwd = pwd
        self.info = info_callback
    def __call__(self):
        if(self.id == 0 or not (queryAccountInfo(self.uname, self.pwd))):
            self.id = 'local'
            print('captcha_break by dddd_ocr')
            try:
                from captcha_break_dddd import dddd
                for i in range(3):
                    img = getCaptchaData(self.zlapp)
                    result = dddd(img)
                    if len(result) == 4:
                        return result
            except:
                import traceback
                print(traceback.format_exc())
                
        print('captcha_break by ttshitu')
        img = getCaptchaData(self.zlapp)
        result = base64_api(self.uname,self.pwd,img,self.typeid)
        print(result)
        if result['success']:
            self.id = result["data"]["id"]
            return result["data"]["result"]
        else:
            self.info(result["message"])
    def reportError(self):
        try:
            if (self.id != 0) and (self.id != 'local'):
                self.info(reportError(self.id))
        except:
            import traceback
            print(traceback.format_exc())

def queryAccountInfo(uname, pwd):
    try:
        result = json.loads(requests.get(f'https://api.ttshitu.com/queryAccountInfo.json?username={uname}&password={pwd}').text)
        print(result)
        if result['success']:
            successNum = int(result['data']['successNum'])
            if successNum <= 1:
                successNum = 1
            failNum = int(result['data']['failNum'])
            print(f'ttshitu 识别准确率：{successNum / (successNum + failNum) * 100:.2f}%')
            return float(result['data']['balance']) > 0.01
        else:
            return False
    except:
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    from captcha_break_dddd import dddd
