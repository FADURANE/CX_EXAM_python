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
    """自定义异常：配置文件未找到"""
    pass

def check_config_file():
    """检查当前目录下是否存在config.yaml文件"""
    config_name = "config.yaml"
    current_dir = os.getcwd()
    if config_name not in os.listdir(current_dir):
        raise FileNotFoundError("缺少config.yaml文件，请检查")

def load_config():
    """加载config.yaml配置文件并返回配置字典"""
    check_config_file()
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config 