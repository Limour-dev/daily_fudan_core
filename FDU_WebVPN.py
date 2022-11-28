from aes_cfb import getCiphertext, getPlaintext
from binascii import hexlify, unhexlify
from urllib.parse import quote
from time import sleep
from os import environ
print(environ['OPENSSL_CONF'])

key_ = b'wrdvpnisthebest!'
iv_  = b'wrdvpnisthebest!'
institution = 'webvpn.fudan.edu.cn'

def getVPNUrl(url):
    '''From ordinary url to webVPN url'''

    parts = url.split('://')
    pro = parts[0]
    add = parts[1]
    
    hosts = add.split('/')
    cph = getCiphertext(hosts[0], key=key_, cfb_iv=iv_)
    fold = '/'.join(hosts[1:])

    key = hexlify(iv_).decode('utf-8')
    
    return 'https://' + institution + '/' + pro + '/' + key + cph + '/' + fold

def getOrdinaryUrl(url):
    '''From webVPN url to ordinary url'''

    parts = url.split('/')
    pro = parts[3]
    key_cph = parts[4]
    
    if key_cph[:16] == hexlify(iv_).decode('utf-8'):
        print(key_cph[:32])
        return None
    else:
        hostname = getPlaintext(key_cph[32:], key=key_, cfb_iv=iv_)
        fold = '/'.join(parts[5:])

        return pro + "://" + hostname + '/' + fold

import time
def getTimestamp(size = 1000):
    t = time.time()
    return int(round(t * size))

from lxml import etree
from requests import session

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

UA_Firefox = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
UA_WeChat_PC = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
UA_Chrome = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

import http.cookies as Cookie

class WebVPN:
    refresh = '0'
    login_url = 'https://webvpn.fudan.edu.cn/login?cas_login=true'
    logout_url = 'https://webvpn.fudan.edu.cn/logout'
    logout_uis = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
    api_ip = 'http://ip-api.com/json/?fields=258047&lang=en'
    def setProxy(self, proxy_url):
        '''
            格式为 http://user:password@host:port
        '''
        proxies = {
            'http': proxy_url,
            'https': proxy_url,
        }
        self.session.proxies.update(proxies)

    def setUA(self, UA=UA_Chrome):
        self.UA = UA

    def update_headers(self, headers):
        if 'User-Agent' not in headers:
            headers['User-Agent'] = self.UA
        if headers['User-Agent'] == UA_Chrome:
            headers['sec-ch-ua'] = r'" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'
            headers['sec-ch-ua-mobile'] = r'?0'
            headers['sec-ch-ua-platform'] = r'"Windows"'
            headers['DNT'] = '1'
            
        cookie_key = 'Cookie' if 'Cookie' in headers else 'cookie'
        ck = Cookie.SimpleCookie()
        if cookie_key in headers:
            ck.load(headers[cookie_key])
        co = self.session.cookies.get_dict()
        co['refresh'] = self.refresh
##        print(co)
        ck.update(co)
        headers[cookie_key] = "; ".join([str(x)+"="+str(y) for x,y in ck.items()])
        
        return headers
 
    def __init__(self):
        self.session = session()
        self.session.verify = False
        self.setUA()

    def get(self, url, *arg, headers={}, **kw):
        headers = self.update_headers(headers)
        if not url.startswith('https://webvpn.fudan.edu.cn'):
            url = getVPNUrl(url)
        return self.session.get(url, *arg, headers=headers, **kw)

    def post(self, url, *arg, headers={}, **kw):
        headers = self.update_headers(headers)
        if not url.startswith('https://webvpn.fudan.edu.cn'):
            url = getVPNUrl(url)
        return self.session.post(url, *arg, headers=headers, **kw)
    def login_uis(self, uid, psw):
        login_url = 'https://uis.fudan.edu.cn/authserver/login'
        page_login = self.session.get(login_url)
        if page_login.status_code != 200:
            return False
        html = etree.HTML(page_login.text, etree.HTMLParser())
        data = {
            "username": uid,
            "password": psw,
        }
        # 获取登录页上的令牌
        data.update(
                zip(
                        html.xpath("/html/body/form/input/@name"),
                        html.xpath("/html/body/form/input/@value")
                )
        )
        headers = {
            "Host"      : "uis.fudan.edu.cn",
            "Origin"    : "https://uis.fudan.edu.cn",
            "Referer"   : login_url,
            "User-Agent": self.UA
        }
        post = self.session.post(
                login_url,
                data=data,
                headers=headers,
                allow_redirects=False)
        return post
    def logout_uis(self):
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout'
        expire = self.session.get(exit_url).headers.get('Set-Cookie')
        return expire
    
    def login_webvpn(self):
        login_url = 'https://webvpn.fudan.edu.cn/login?cas_login=true'
        get = self.session.get(login_url, allow_redirects=True)
        return get
    def logout_webvpn(self):
        exit_url = 'https://webvpn.fudan.edu.cn/logout'
        return self.session.get(exit_url, allow_redirects=False)

    def login_uis_by_webvpn(self, uid, psw):
        login_url = 'https://uis.fudan.edu.cn/authserver/login'
        page_login = self.get(login_url)
        if page_login.status_code != 200:
            return False
        html = etree.HTML(page_login.text, etree.HTMLParser())
        data = {
            "username": uid,
            "password": psw,
        }
        # 获取登录页上的令牌
        data.update(
                zip(
                        html.xpath("/html/body/form/input/@name"),
                        html.xpath("/html/body/form/input/@value")
                )
        )
        headers = {
            "Origin"    : "https://uis.fudan.edu.cn",
            "Referer"   : login_url,
            "User-Agent": self.UA
        }
        post = self.post(
                login_url,
                data=data,
                headers=headers,
                allow_redirects=False)
        return post
        
    def logout_uis_by_webvpn(self):
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout'
        expire = self.get(exit_url)
        return self.cookie(exit_url)
    
    def login_old(self, uid, psw):
        page_login = self.get(self.login_url,allow_redirects=False)
        if not page_login.is_redirect:
            return False

        login_url = page_login.next.url
        page_login = self.session.send(page_login.next)
        
        if page_login.status_code != 200:
            return False
        
        html = etree.HTML(page_login.text, etree.HTMLParser())
        data = {
            "username": uid,
            "password": psw,
        }
        # 获取登录页上的令牌
        data.update(
                zip(
                        html.xpath("/html/body/form/input/@name"),
                        html.xpath("/html/body/form/input/@value")
                )
        )
        
        headers = {
            "referer"   : login_url,
            "origin": "https://webvpn.fudan.edu.cn"
        }
    
        post = self.post(
                login_url,
                data=data,
                headers=headers,
                allow_redirects=True)

        if post.history:
            if 'ticket=' in post.url:
                return self.ct_login(uid, post)
            else:
                return post.history[-1].url
        return post

    def ct_login(self, uid, rps):
        fix1 = 'https://webvpn.fudan.edu.cn/wengine-vpn/input'
        data = {
            'name': "username",
            'type': "text",
            'value': uid
            }
        headers = {
            'origin': 'https://webvpn.fudan.edu.cn',
            'referer': 'https://webvpn.fudan.edu.cn/https/77726476706e69737468656265737421e5fe52d221256c5170468ca88d1b203b/authserver/login?service=https%3A%2F%2Fwebvpn.fudan.edu.cn%2Flogin%3Fcas_login%3Dtrue'
            }
        self.post(fix1, headers=headers, data=data)
        for i in range(20): # ??? 为什么要多次尝试登录才能进 ???
            sleep(0.3)
            page_login = self.get(self.login_url,allow_redirects=True)
            if page_login.url == 'https://webvpn.fudan.edu.cn/':
                return 'token-login'
            html = etree.HTML(page_login.text, etree.HTMLParser())
            captcha = html.xpath("//img[@class='captcha-img']/@src")
            if len(captcha) != 1:
                return page_login
            captcha = captcha[0]
            captcha = self.get('https://webvpn.fudan.edu.cn'+captcha, allow_redirects=True)
        res = page_login
        return res

    def logout_old(self):
        """
        执行登出
        """
        expire = self.get(self.logout_uis).headers.get('Set-Cookie')
        expire += self.get(self.logout_url).headers.get('Set-Cookie')
        if '01-Jan-1970' in expire:
            return True
        return  expire

    def close(self):
        """
        执行登出并关闭会话
        """
        ret = self.logout()
        self.session.close()
        return ret    

    def cookie(self, url='',  method:['get','set']='get', host='', path='', scheme='https', ck_data=''):
        if url:
            parts = url.split('://')
            scheme = parts[0]
            add = parts[1]
            hosts = add.split('/')
            host = hosts[0]
            path = '/' + '/'.join(hosts[1:])
        qurl = r'https://webvpn.fudan.edu.cn/wengine-vpn/cookie?' + f'method={method}&host={host}&scheme={scheme}&path={path}' 
        if method == 'get':
            qurl += f'&vpn_timestamp={getTimestamp()}'
        else:
            qurl += f'&ck_data={quote(ck_data)}'
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
        }
        c = self.get(qurl, headers=headers)
        try:
            if c.ok and 'text' in c.headers.get('Content-Type'):
                return c.text
        except:
            pass
        return c

    def show(self, url):
        b = self.get(url)
        show(b)

    def getIP(self):
        ip = self.get(self.api_ip)
        if ip.ok and 'json' in ip.headers.get('Content-Type'):
            return ip.json()
        return ip
    def login(self, uid, psw):
        for i in range(3):
            st1 = self.login_uis(uid, psw)
            if st1.is_redirect and st1.next.url.endswith('index.do'):
                break
            sleep(0.3)
        else:
            return 'uis failed'
        
        for i in range(10):
            sleep(0.3)
            st2 = self.login_webvpn()
            if st2.history and (('ticket=' in st2.url) or ('ticket=' in st2.history[-1].url)):
                break
        else:
            return 'webvpn failed'
        
        for i in range(3):
            sleep(0.3)
            st3 = self.login_uis_by_webvpn(uid, psw)
            if st3.is_redirect and st3.next.url.endswith('index.do'):
                break
        else:
            return 'uis_by_webvpn failed'
        
        return 'token-login'
        return (st1, st2, st3)
        
    def logout(self):
        self.logout_uis_by_webvpn()
        sleep(0.3)
        self.logout_webvpn()
        sleep(0.3)
        self.logout_uis()
