# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : main.py
# Github : https://github.com/SJYssr
# 用途：程序主入口，负责加载配置、初始化界面、事件绑定、AI调用与主流程调度。

import tkinter as tk
from tkinter import messagebox
import _thread as thread
import time
from pynput.keyboard import Controller
from config_manager import load_config_if_exists, save_deepseek_config
from file_manager import load_tiku_file
from ai_spark import Ws_Param, on_error, on_close, on_open, run, on_message
from ai_deepseek import call_deepseek_api
from utils import set_window_on_top, change_opacity, change_opacity0, close_window, change_weight
from ui_main import create_main_ui, highlight_search, next_search_result
from ui_ai import create_ai_ui
from ui_settings import create_settings_ui, create_settings_embedded
import ssl
import websocket
import functools

# 全局状态变量
current_opacity = 0.5  # 窗口透明度
text_size = 10         # 字体大小
is_small = False       # 窗口大小状态
x = 0                  # 拖动窗口时的x坐标
y = 0                  # 拖动窗口时的y坐标
deepseek_api_key = ''  # Deepseek API Key（运行时可热切换）
deepseek_model = 'deepseek-chat'  # Deepseek 模型（运行时可热切换）

# 事件处理函数

def start_move(event):
    """鼠标按下，记录窗口当前位置"""
    global x, y
    x = event.x
    y = event.y

def stop_move(event):
    """鼠标拖动，移动窗口"""
    root.geometry(f"+{event.x_root - x}+{event.y_root - y}")

def change_text_size(event):
    """Ctrl+滚轮调整字体大小"""
    global text_size
    text_size = max(10, min(text_size, 12))
    if main_ui['main_frame'].winfo_ismapped():
        if event.delta > 0:
            text_size += 1
        else:
            text_size -= 1
        main_ui['text_box'].config(font=("Arial", text_size))
    elif ai_ui['ai_frame'].winfo_ismapped():
        if event.delta > 0:
            text_size += 1
        else:
            text_size -= 1
        ai_ui['ai_text_box'].config(font=("Arial", text_size))

def on_change_weight(event):
    """F3切换窗口大小"""
    global is_small, current_opacity
    is_small, current_opacity = change_weight(event, root, is_small, current_opacity)

def on_change_opacity(event):
    """Ctrl+滚轮调整窗口透明度"""
    global current_opacity
    current_opacity = change_opacity(event, root, current_opacity, is_small)

def on_change_opacity0(event):
    """右键切换窗口透明度"""
    global current_opacity
    current_opacity = change_opacity0(event, root, current_opacity, is_small)

def on_ai_button():
    """切换到AI界面"""
    main_ui['search_frame'].pack_forget()
    main_ui['main_frame'].pack_forget()
    ai_ui['ai_frame'].pack(fill="both", expand=True)

def on_back():
    """切换回主界面"""
    # 隐藏AI或设置界面
    if ai_ui['ai_frame'].winfo_ismapped():
        ai_ui['ai_frame'].pack_forget()
    if 'settings_ui' in globals() and settings_ui['settings_frame'].winfo_ismapped():
        settings_ui['settings_frame'].pack_forget()
    # 显示主界面
    main_ui['search_frame'].pack(side="top", fill="x")
    main_ui['main_frame'].pack(fill="both", expand=True)

def on_search():
    """主界面搜索高亮"""
    highlight_search(main_ui['text_box'], main_ui['search_entry'])

def on_input(entry):
    """主界面输入自动打字"""
    input_text = entry.get()
    if not input_text:
        return
    def input_thread():
        keyboard = Controller()
        time.sleep(1)
        keyboard.type(input_text)
        time.sleep(0.5)
        entry.delete(0, 'end')
    thread.start_new_thread(input_thread, ())

def on_ai_search():
    """AI界面AI搜索，支持讯飞星火和Deepseek"""
    ai_ui['ai_search_button'].config(state='disabled')
    # 仅在Deepseek时展示占位提示；讯飞星火不显示
    if type == 2:
        ai_ui['ai_text_box'].config(state='normal')
        ai_ui['ai_text_box'].delete('1.0', tk.END)
        ai_ui['ai_text_box'].insert(tk.END, "正在思考中，请稍候...")
        ai_ui['ai_text_box'].config(state='disabled')
    def update_ai_text(content):
        ai_ui['ai_text_box'].config(state='normal')
        ai_ui['ai_text_box'].delete('1.0', tk.END)  # 回答前先清空
        ai_ui['ai_text_box'].insert(tk.END, content)
        ai_ui['ai_text_box'].config(state='disabled')
    def run_ai():
        try:
            if type == 1:
                wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
                websocket.enableTrace(False)
                wsUrl = wsParam.create_url()
                query = ai_ui['ai_search_entry'].get()
                ws = websocket.WebSocketApp(wsUrl,
                    on_message=functools.partial(on_message, ai_text_box=ai_ui['ai_text_box'], update_ai_text=update_ai_text, root=root),
                    on_error=functools.partial(on_error, update_ai_text=update_ai_text),
                    on_close=functools.partial(on_close, update_ai_text=update_ai_text),
                    on_open=lambda ws: on_open(ws, lambda ws: run(ws, appid, query, domain))
                )
                ws.appid = appid
                ws.query = query
                ws.domain = domain
                ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            elif type == 2:
                response = call_deepseek_api(deepseek_api_key, ai_ui['ai_search_entry'].get(), deepseek_model)
                root.after(0, lambda: update_ai_text(response))
        except Exception as e:
            root.after(0, lambda: update_ai_text(f"发生错误: {str(e)}"))
        finally:
            root.after(0, lambda: ai_ui['ai_search_button'].config(state='normal'))
    thread.start_new_thread(run_ai, ())

def on_ai_input(entry):
    """AI界面输入自动打字"""
    input_text = entry.get()
    if not input_text:
        return
    def input_thread():
        keyboard = Controller()
        time.sleep(1)
        keyboard.type(input_text)
        time.sleep(0.5)
        entry.delete(0, 'end')
    thread.start_new_thread(input_thread, ())

# 加载配置（若无则使用写死的讯飞星火默认配置，不创建文件）
config = load_config_if_exists()

# 启动验证与版本检测已移除，直接进入主程序

deepseek_config = (config or {}).get('deepseek', {})
deepseek_api_key = deepseek_config.get('api_key', deepseek_api_key)
deepseek_model = deepseek_config.get('model', deepseek_model)

if deepseek_api_key:
    # 使用Deepseek
    type = 2
else:
    # 使用写死的讯飞星火
    type = 1
    appid = "1b69309b"
    api_secret = "YWY0MWJhNTM4MGU3NTJkZDJiMDM0ZjZl"
    api_key = "5b2302f3ac2295e56bd13f587d7ffa6e"
    Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"
    domain = "lite"

# 初始化主窗口和界面
root = tk.Tk()
root.geometry("300x533+0+380")
root.attributes("-alpha", current_opacity)
root.configure(bg='white')
root.overrideredirect(True)

def open_settings():
    def on_save(api_key_value, model_value):
        try:
            if not api_key_value.strip():
                return
            save_deepseek_config(api_key_value.strip(), (model_value or 'deepseek-chat').strip())
            # 热切换到Deepseek
            global type, deepseek_api_key, deepseek_model
            deepseek_api_key = api_key_value.strip()
            deepseek_model = (model_value or 'deepseek-chat').strip()
            type = 2
        except Exception:
            return
    global settings_ui
    # 如果尚未创建，先创建嵌入式设置界面
    if 'settings_ui' not in globals():
        settings_ui = create_settings_embedded(
            root,
            on_save,
            on_back,
            text_size,
            default_api_key=deepseek_api_key,
            default_model=deepseek_model
        )
    else:
        # 已创建则更新默认显示（覆盖原值）
        try:
            settings_ui['api_entry'].delete(0, tk.END)
            if deepseek_api_key:
                settings_ui['api_entry'].insert(0, deepseek_api_key)
            settings_ui['model_entry'].set(deepseek_model)
        except Exception:
            pass
    # 切换显示
    if main_ui['search_frame'].winfo_ismapped():
        main_ui['search_frame'].pack_forget()
    if main_ui['main_frame'].winfo_ismapped():
        main_ui['main_frame'].pack_forget()
    if ai_ui['ai_frame'].winfo_ismapped():
        ai_ui['ai_frame'].pack_forget()
    settings_ui['settings_frame'].pack(fill="both", expand=True)

# 创建主界面、AI界面与（懒加载）设置界面
main_ui = create_main_ui(root, on_ai_button, on_search, on_input, text_size, on_settings=open_settings)
ai_ui = create_ai_ui(root, on_back, on_ai_search, on_ai_input, text_size)
ai_ui['ai_frame'].pack_forget()

# 启动窗口置顶
set_window_on_top(root)

# 事件绑定
root.bind("<Control-Button-1>", start_move)
root.bind("<Control-B1-Motion>", stop_move)
root.bind("<F3>", on_change_weight)
root.bind("<Button-3>", on_change_opacity0)
root.bind("<Control-MouseWheel>", on_change_opacity)
root.bind("<Alt-MouseWheel>", change_text_size)
root.bind("<Escape>", lambda e: close_window(e, root))
root.bind("<Return>", lambda e: next_search_result(main_ui['text_box']))

# 启动主循环
root.mainloop()