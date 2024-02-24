import datetime
import requests
import os
import json


appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
openId = os.environ.get("OPEN_ID")
template_id = os.environ.get("TV_TEMPLATE_ID")


def get_access_token():
    global appID, appSecret
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token


name_y = {}
with open("直播源.txt", "r", encoding="utf-8") as file:
    for line in file.readlines():
        i = line.split(",")
        name_y[i[0]] = i[1].strip()
n = 1
error = []
for key, value in name_y.items():
    # print(f"正在测试第{n}个")
    try:
        r = requests.get(value, timeout=3)
        if r.status_code != 200:
            error.append(key)
    except requests.exceptions.RequestException:
        error.append(key)
    n += 1

today = datetime.date.today()
today_str = today.strftime("%Y年%m月%d日 %H点%M分%S秒")
if error == []:
    err = f"截至 {today_str} 电视直播源全部可用！"
else:
    err = f"截至 {today_str} 以下频道在3秒内无法返回结果，请检查：\n"
    n = 1
    for e in error:
        err = err + str(n) + '.' + e + "\n"
        n += 1

# print(err)

access_token = get_access_token()
body = {
    "touser": openId.strip(),
    "template_id": template_id.strip(),
    "url": "",
    "data": {
        "msg": {
            "value": err
        }
    }
}
url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
print(requests.post(url, json.dumps(body)).text)
