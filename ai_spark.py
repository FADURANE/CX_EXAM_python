# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : ai_spark.py
# Github : https://github.com/SJYssr
# 用途：封装讯飞星火大模型的WebSocket API调用、参数生成、消息处理等。

import base64
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import websocket
import ssl

class Ws_Param(object):
    """
    讯飞星火WebSocket参数生成类。
    用于生成带鉴权的WebSocket连接URL。
    """
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    def create_url(self):
        """生成带鉴权的WebSocket连接URL"""
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        v = {"authorization": authorization, "date": date, "host": self.host}
        url = self.gpt_url + '?' + urlencode(v)
        return url

def gen_params(appid, query, domain):
    """
    生成星火API请求参数。
    :param appid: 应用ID
    :param query: 用户问题
    :param domain: 领域
    :return: dict
    """
    data = {
        "header": {"app_id": appid, "uid": "1234"},
        "parameter": {"chat": {"domain": domain, "temperature": 0.5, "max_tokens": 4096, "auditing": "default"}},
        "payload": {"message": {"text": [{"role": "user", "content": query}]}}
    }
    return data

def on_error(ws, error, *args, **kwargs):
    """WebSocket错误回调"""
    update_ai_text = kwargs.get('update_ai_text')
    if update_ai_text:
        update_ai_text(f"WebSocket错误: {error}")

def on_close(ws, *args, **kwargs):
    """WebSocket关闭回调（正常关闭不覆盖内容）"""
    pass  # 只保留空实现，不再打印日志

def on_open(ws, run_func):
    """WebSocket连接建立回调，启动AI请求"""
    run_func(ws)

def run(ws, appid, query, domain):
    """WebSocket发送AI请求数据"""
    data = json.dumps(gen_params(appid=appid, query=query, domain=domain))
    ws.send(data)

def on_message(ws, message, ai_text_box, update_ai_text, root):
    """
    WebSocket消息回调，处理AI返回内容。
    :param ws: WebSocket对象
    :param message: 消息内容
    :param ai_text_box: Tkinter文本框控件
    :param update_ai_text: 更新文本框的回调
    :param root: Tk主窗口
    """
    data = json.loads(message)
    ai_text_box.config(state='normal')
    if data['header']['code'] != 0:
        root.after(0, update_ai_text, f"请求错误: {data['header']['code']} {data['header'].get('message', '')}")
        ws.close()
    else:
        content = data["payload"]["choices"]["text"][0]["content"]
        root.after(0, ai_text_box.insert, 'end', content)
        if data["payload"]["choices"]["status"] == 2:
            ws.close()
    ai_text_box.config(state='disabled') 