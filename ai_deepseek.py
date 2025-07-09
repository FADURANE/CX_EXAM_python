# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : ai_deepseek.py
# Github : https://github.com/SJYssr
# 用途：封装DeepseekAI的HTTP API调用，负责AI问答请求与异常处理。

import requests

def call_deepseek_api(deepseek_api_key, prompt, deepseek_model):
    """
    调用DeepseekAI的API进行问答。
    :param deepseek_api_key: Deepseek API密钥
    :param prompt: 用户输入内容
    :param deepseek_model: 使用的模型名称
    :return: AI回复内容或异常信息
    """
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": f"{deepseek_model}",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return e
    except KeyError as e:
        return e
    except Exception as e:
        return e 