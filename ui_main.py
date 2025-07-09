# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : ui_main.py
# Github : https://github.com/SJYssr
# 用途：主界面控件的创建、布局、搜索高亮、输入等事件处理。

import tkinter as tk
from file_manager import load_tiku_file

# 全局搜索状态
current_search_index = 0  # 当前高亮搜索结果索引
search_results = []       # 所有搜索结果位置

def highlight_search(text_box, search_entry):
    """
    高亮显示文本框中匹配搜索框内容项，并支持单个跳转。
    :param text_box: Tkinter Text控件
    :param search_entry: Tkinter Entry控件
    """
    global current_search_index, search_results
    search_term = search_entry.get()
    if not search_term:
        return
    text_box.tag_remove('highlight', '1.0', 'end')
    text_box.tag_remove('current_highlight', '1.0', 'end')
    search_results = []
    start = '1.0'
    while True:
        start = text_box.search(search_term, start, stopindex='end')
        if not start:
            break
        end = f"{start}+{len(search_term)}c"
        search_results.append((start, end))
        start = end
    if not search_results:
        return
    current_search_index = 0
    start, end = search_results[current_search_index]
    text_box.tag_add('current_highlight', start, end)
    text_box.tag_config('current_highlight', background='yellow')
    text_box.see(start)

def next_search_result(text_box):
    """
    跳转到下一个搜索结果。
    :param text_box: Tkinter Text控件
    """
    global current_search_index, search_results
    if not search_results:
        return
    text_box.tag_remove('current_highlight', '1.0', 'end')
    current_search_index = (current_search_index + 1) % len(search_results)
    start, end = search_results[current_search_index]
    text_box.tag_add('current_highlight', start, end)
    text_box.see(start)

def create_main_ui(root, on_ai_button, on_search, on_input, text_size=10):
    """
    创建主界面控件并布局，返回控件引用字典。
    :param root: Tk主窗口
    :param on_ai_button: AI按钮回调
    :param on_search: 搜索按钮回调
    :param on_input: 输入按钮回调
    :param text_size: 初始字体大小
    :return: dict
    """
    # 顶部搜索框和AI按钮
    search_frame = tk.Frame(root)
    search_frame.pack(side="top", fill="x")
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    search_entry.configure(foreground='gray')
    ai_button = tk.Button(search_frame, text="AI", command=on_ai_button)
    ai_button.pack(side="right", padx=5, pady=5)
    ai_button.configure(foreground='gray')
    search_button = tk.Button(search_frame, text="搜索", command=lambda: on_search())
    search_button.pack(side="right", padx=5, pady=5)
    search_button.configure(foreground='gray')
    # 主界面文本框
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)
    text_frame = tk.Frame(main_frame)
    text_frame.pack(fill="both", expand=True)
    text_box = tk.Text(text_frame, wrap='word', font=("Arial", text_size))
    text_box.pack(side="left", fill="both", expand=True)
    text_box.configure(foreground='gray')
    load_tiku_file(text_box)
    # 底部输入框
    bottom_frame = tk.Frame(main_frame)
    bottom_frame.pack(side="bottom", fill="x")
    input_entry = tk.Entry(bottom_frame)
    input_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
    input_entry.configure(foreground='gray')
    submit_button = tk.Button(bottom_frame, text="输入", command=lambda: on_input(input_entry))
    submit_button.pack(side="right", padx=5, pady=5)
    submit_button.configure(foreground='gray')
    return {
        'search_frame': search_frame,
        'search_entry': search_entry,
        'ai_button': ai_button,
        'search_button': search_button,
        'main_frame': main_frame,
        'text_box': text_box,
        'input_entry': input_entry,
        'submit_button': submit_button
    } 