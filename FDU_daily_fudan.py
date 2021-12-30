import time
from json import loads as json_loads
from FDU_WebVPN import WebVPN
from geo_disturbance import geoDisturbance
from captcha_break import DailyFDCaptcha

gl_info = "快去手动填写！"
url_login = r'https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Fzlapp.fudan.edu.cn%2Fa_fudanzlapp%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fzlapp.fudan.edu.cn%252Fsite%252Fncov%252FfudanDaily%26from%3Dwap'
url_info = r'https://zlapp.fudan.edu.cn/ncov/wap/fudan/get-info?vpn-12-o2-zlapp.fudan.edu.cn'

def set_q(iterO):
    res = list()
    for item in iterO:
        if item not in res:
            res.append(item)
    return res

def check():
##    test_info = {'sfzx':0}
##    print(s_sfzx(test_info))
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        'referer': 'https://webvpn.fudan.edu.cn/https/77726476706e69737468656265737421eafb408c377e6e457a0987e29d51367bff35/site/ncov/fudanDaily'
    }
    get_info = vpn.get(url_info, headers=headers)
    last_info = get_info.json()
    position = last_info["d"]["info"]['geo_api_info']
    position = json_loads(position)
    print(f'上一次提交日期为(WebVPN): {last_info["d"]["info"]["date"]}')
    print(f'上一次提交地址为(WebVPN): {position["formattedAddress"]}')
    
    today = time.strftime("%Y%m%d", time.localtime())
    if last_info["d"]["info"]["date"] == today:
        print("今日已提交(WebVPN)")
        global gl_info
        gl_info = f'{last_info["d"]["info"]["date"]}:{position["formattedAddress"]}'
        return True
    else:
        print("未提交(WebVPN)")
        global _last_info, _old_info
        _last_info = last_info["d"]["info"]
        _old_info = last_info["d"]["oldInfo"]
        return False

def checkin(captcha):
    headers = {
        "Referer"   : "https://zlapp.fudan.edu.cn/site/ncov/fudanDaily?from=history",
        "TE"        : "Trailers",
    }
    geo_api_info = json_loads(_last_info["geo_api_info"])
    province = geo_api_info["addressComponent"].get("province", "")
    city = geo_api_info["addressComponent"].get("city", "") or province
    district = geo_api_info["addressComponent"].get("district", "")
    _last_info.update(
        {
            "tw"      : "13",
            "province": province,
            "city"    : city,
            "area"    : " ".join(set_q((province, city, district))),
            "ismoved" : 0,
            "geo_api_info" : geoDisturbance(_last_info["geo_api_info"])
        }
    )
    for i in range(3):
        captcha_text = captcha()
        #captcha_text = 'abcd'
        _last_info.update({
            'sfzx': s_sfzx(_old_info),
            'code': captcha_text
        })
        save = vpn.post(
                'https://zlapp.fudan.edu.cn/ncov/wap/fudan/save',
                data=_last_info,
                headers=headers,
                allow_redirects=False)
        print(save.text)
        save_msg = json_loads(save.text)["m"]
        if save_msg != '验证码错误':
            break
        else:
            captcha.reportError()
            print('captcha.reportError')

def dailyFudan(uid, psw, uname, pwd, info, lc_s_sfzx=None):
    global vpn, s_sfzx
    if lc_s_sfzx:
        s_sfzx = lc_s_sfzx
    else:
        s_sfzx = lambda x: "1"
    vpn = WebVPN()
    try:
        if 'token-login' not in vpn.login(uid, psw):
            return False
        print('FDU_daily_fudan by WebVPN')
        if vpn.get(url_login).status_code != 200:
            print('FDU_daily_fudan 登录失败')
            return False
        if check():
            info("平安复旦：今日已提交(WebVPN)", gl_info)
            return True
        
        def captcha_info(message):
            info(message, gl_info)
        captcha = DailyFDCaptcha(uname, pwd, vpn, captcha_info)
        checkin(captcha)

        # 再检查一遍
        if check():
            info("平安复旦：今日已提交(WebVPN)", gl_info)
            return True
        else:
            info("平安复旦：本次提交失败(WebVPN)", gl_info)
            return False
    finally:
        vpn.close()

