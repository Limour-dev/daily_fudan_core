import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# https://sct.ftqq.com/
def ftqq(FTQQ_TOKEN):
    url = f"https://sctapi.ftqq.com/{FTQQ_TOKEN}.send"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    def send(text, desp=""):
        Form = {'text': text, 'desp': desp}
        return requests.post(url, data=Form, headers=headers, verify=False)
    return send
