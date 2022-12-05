import time
def getTimestamp(size = 1000):
    t = time.time()
    return int(round(t * size))

def needCaptcha(session, headers, uid):
    tmp = headers.copy()
    tmp.update({
        "Accept": "text/plain, */*; q=0.01",
        })
    res = session.get(f'https://uis.fudan.edu.cn/authserver/needCaptcha.html?username={uid}&_={getTimestamp()}',
                      headers=tmp)
    if res.status_code != 200:
        raise Exception('res.status_code != 200')
    return not res.text.startswith('false')

def captcha(session, headers):
    tmp = headers.copy()
    tmp.update({
        "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        })
    res = session.get(r'https://uis.fudan.edu.cn/authserver/captcha.html',
                      headers=tmp)
    if res.status_code != 200:
        raise Exception('res.status_code != 200')
    time.sleep(1)
    return res.content

if __name__ == '__main__':
    from dailyFudan import Fudan
    tmp = Fudan('21301050114', '')
    tmp._page_init()
    if needCaptcha(tmp.session, tmp.headers, tmp.uid):
        tmp_res = captcha(tmp.session, tmp.headers)
        from captcha_break_dddd import dddd_3
        result = dddd_3(tmp_res)
