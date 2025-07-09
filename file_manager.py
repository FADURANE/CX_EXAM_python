# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : file_manager.py
# Github : https://github.com/SJYssr
# 用途：负责题库文件（tiku.txt）的读取，供主界面加载题库内容。

def load_tiku_file(text_box):
    """
    读取 tiku.txt 文件内容到传入的文本框控件。
    :param text_box: Tkinter Text控件，用于显示题库内容。
    """
    try:
        with open('tiku.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            text_box.insert('1.0', content)
            text_box.config(state='disabled')
    except FileNotFoundError:
        text_box.insert('1.0', "未找到tiku.txt，请确保文件夹中有此文件")
        text_box.config(state='disabled') 