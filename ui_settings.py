# _*_coding : UTF_8 _*_
# author : SJYssr (extended)
# Date : 2025/09/10
# ClassName : ui_settings.py
# 用途：设置界面（Deepseek配置），遵循主界面风格，保存到config.yaml。

import tkinter as tk
from tkinter import ttk

def create_settings_ui(root, on_save, text_size=10, default_api_key='', default_model='deepseek-chat'):
    """
    创建设置界面（作为顶层窗口），允许输入Deepseek APIKey与模型并保存。
    :param root: Tk主窗口
    :param on_save: 保存回调函数，签名 on_save(api_key: str, model: str)
    :param text_size: 初始字体大小
    :param default_api_key: 默认显示的Deepseek API Key（从配置/运行时传入）
    :param default_model: 默认显示的模型（"deepseek-chat"/"deepseek-reasoner"）
    :return: dict - 窗口与控件引用字典
    """
    win = tk.Toplevel(root)
    win.title("设置")
    win.geometry("300x220")
    win.configure(bg='white')
    win.transient(root)
    win.grab_set()

    # 顶部区域
    top_frame = tk.Frame(win)
    top_frame.pack(side="top", fill="x")

    title_label = tk.Label(top_frame, text="Deepseek 设置", font=("Arial", text_size))
    title_label.pack(side="left", padx=5, pady=5)
    title_label.configure(foreground='gray')

    # 表单区域
    form_frame = tk.Frame(win)
    form_frame.pack(fill="both", expand=True)

    api_label = tk.Label(form_frame, text="API Key:")
    api_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
    api_label.configure(foreground='gray')
    api_entry = tk.Entry(form_frame)
    api_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)
    api_entry.configure(foreground='gray')
    if default_api_key:
        api_entry.insert(0, default_api_key)

    model_label = tk.Label(form_frame, text="模型:")
    model_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
    model_label.configure(foreground='gray')
    model_values = [
        "deepseek-chat",
        "deepseek-reasoner"
    ]
    model_entry = ttk.Combobox(form_frame, values=model_values, state='readonly')
    model_entry.grid(row=1, column=1, sticky='we', padx=5, pady=5)
    model_entry.set(default_model if default_model in model_values else "deepseek-chat")

    form_frame.columnconfigure(1, weight=1)

    # 底部按钮
    bottom_frame = tk.Frame(win)
    bottom_frame.pack(side="bottom", fill="x")

    def do_save():
        on_save(api_entry.get().strip(), model_entry.get().strip())
        win.destroy()

    save_btn = tk.Button(bottom_frame, text="保存", command=do_save)
    save_btn.pack(side="right", padx=5, pady=5)
    save_btn.configure(foreground='gray')

    cancel_btn = tk.Button(bottom_frame, text="取消", command=win.destroy)
    cancel_btn.pack(side="right", padx=5, pady=5)
    cancel_btn.configure(foreground='gray')

    return {
        'window': win,
        'api_entry': api_entry,
        'model_entry': model_entry,
        'save_btn': save_btn,
        'cancel_btn': cancel_btn
    }

def create_settings_embedded(root, on_save, on_back, text_size=10, default_api_key='', default_model='deepseek-chat'):
    """
    创建嵌入式设置界面（Frame），与主界面/AI界面一致风格，可在同一窗口切换。
    :param root: Tk主窗口
    :param on_save: 保存回调函数，签名 on_save(api_key: str, model: str)
    :param on_back: 返回回调，用于切回主界面
    :param text_size: 初始字体大小
    :param default_api_key: 默认显示的Deepseek API Key（从配置/运行时传入）
    :param default_model: 默认显示的模型（"deepseek-chat"/"deepseek-reasoner"）
    :return: dict - 设置界面控件引用字典
    """
    settings_frame = tk.Frame(root)

    # 顶部栏
    top_frame = tk.Frame(settings_frame)
    top_frame.pack(side="top", fill="x")

    title_label = tk.Label(top_frame, text="Deepseek 设置", font=("Arial", text_size))
    title_label.pack(side="left", padx=5, pady=5)
    title_label.configure(foreground='gray')

    back_button = tk.Button(top_frame, text="返回", command=on_back)
    back_button.pack(side="right", padx=5, pady=5)
    back_button.configure(foreground='gray')

    # 表单区域
    form_frame = tk.Frame(settings_frame)
    form_frame.pack(fill="both", expand=True)

    api_label = tk.Label(form_frame, text="API Key:")
    api_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
    api_label.configure(foreground='gray')
    api_entry = tk.Entry(form_frame)
    api_entry.grid(row=0, column=1, sticky='we', padx=5, pady=5)
    api_entry.configure(foreground='gray')
    if default_api_key:
        api_entry.insert(0, default_api_key)

    model_label = tk.Label(form_frame, text="模型:")
    model_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
    model_label.configure(foreground='gray')
    model_values = [
        "deepseek-chat",
        "deepseek-reasoner"
    ]
    model_entry = ttk.Combobox(form_frame, values=model_values, state='readonly')
    model_entry.grid(row=1, column=1, sticky='we', padx=5, pady=5)
    model_entry.set(default_model if default_model in model_values else "deepseek-chat")

    form_frame.columnconfigure(1, weight=1)

    # 底部按钮
    bottom_frame = tk.Frame(settings_frame)
    bottom_frame.pack(side="bottom", fill="x")

    def do_save():
        on_save(api_entry.get().strip(), model_entry.get().strip())

    save_btn = tk.Button(bottom_frame, text="保存", command=do_save)
    save_btn.pack(side="right", padx=5, pady=5)
    save_btn.configure(foreground='gray')

    return {
        'settings_frame': settings_frame,
        'api_entry': api_entry,
        'model_entry': model_entry,
        'save_btn': save_btn,
        'top_frame': top_frame,
        'form_frame': form_frame,
        'bottom_frame': bottom_frame,
        'back_button': back_button
    }



