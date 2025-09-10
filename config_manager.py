# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : config_manager.py
# Github : https://github.com/SJYssr
# 用途：负责加载和校验配置文件config.yaml，提供全局配置访问接口。

import os
import yaml
from tkinter import messagebox

class FileNotFoundError(Exception):
    """自定义异常：配置文件未找到（保留但不再强制触发）"""
    pass

def config_file_exists():
    """返回当前目录下是否存在config.yaml文件"""
    config_name = "config.yaml"
    current_dir = os.getcwd()
    return config_name in os.listdir(current_dir)

def load_config_if_exists():
    """若存在config.yaml则加载返回配置字典，否则返回None"""
    if not config_file_exists():
        return None
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    return config

def save_deepseek_config(api_key, model):
    """仅保存Deepseek相关配置到config.yaml，不包含讯飞星火或选择项"""
    data = {
        'deepseek': {
            'api_key': api_key,
            'model': model
        }
    }
    with open('config.yaml', 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)