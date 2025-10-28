# _*_coding : UTF_8 _*_
# author : SJYssr
# Date : 2024/12/26 下午10:17
# ClassName : utils.py
# Github : https://github.com/SJYssr
# 用途：通用窗口操作工具函数，如置顶、透明度调整、窗口拖动、关闭等。

import tkinter as tk
from ctypes import windll, wintypes

def set_window_on_top(root):
    """
    将窗口始终保持在最上层。
    :param root: Tk主窗口
    """
    SetWindowDisplayAffinity = windll.user32.SetWindowDisplayAffinity
    SetWindowDisplayAffinity.argtypes = [wintypes.HWND, wintypes.DWORD]
    SetWindowDisplayAffinity.restype = wintypes.BOOL
    root.attributes("-topmost", True)
    hwnd = windll.user32.GetForegroundWindow()
    dwAffinity =0x00000001
    SetWindowDisplayAffinity(hwnd, dwAffinity)
    root.after(1000, lambda: set_window_on_top(root))

def change_opacity(event, root, current_opacity, is_small):
    """
    Ctrl+滚轮调整窗口透明度。
    :return: 新的透明度
    """
    if is_small != False:
        return current_opacity
    if event.delta > 0:
        current_opacity += 0.1
    else:
        current_opacity -= 0.1
    current_opacity = max(0.1, min(current_opacity, 1.0))
    root.attributes("-alpha", current_opacity)
    return current_opacity

def change_opacity0(event, root, current_opacity, is_small):
    """
    右键切换窗口透明度0.2/0.5。
    :return: 新的透明度
    """
    if is_small != False:
        return current_opacity
    if current_opacity == 0.2:
        current_opacity = 0.5
    else:
        current_opacity = 0.2
    root.attributes("-alpha", current_opacity)
    return current_opacity

def close_window(event, root):
    """关闭窗口"""
    root.destroy()

def change_weight(event, root, is_small, current_opacity):
    """
    F3切换窗口大小。
    :return: (新的is_small, 新的current_opacity)
    """
    if is_small:
        root.geometry("300x533+0+380")
        root.attributes("-alpha", current_opacity)
    else:
        root.geometry("5x910+0+0")
        current_opacity = root.attributes("-alpha")
        root.attributes("-alpha", 0.1)
    return not is_small, current_opacity 