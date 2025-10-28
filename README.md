# 超星考试客户端工具  

<div align="center">

![license](https://img.shields.io/github/license/SJYssr/CX_EXAM_python?style=flat-square)
![stars](https://img.shields.io/github/stars/SJYssr/CX_EXAM_python?style=flat-square)
![release](https://img.shields.io/github/v/release/SJYssr/CX_EXAM_python?style=flat-square)
![python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square)
![platform](https://img.shields.io/badge/platform-windows-lightgrey?style=flat-square)

</div>

---

> **因不可抗拒因素，暂停更新，如有需要请留[issues](https://github.com/SJYssr/CX_EXAM_python/issues)**

> **或者访问作者网站[SJYssr](http://sjyssr.net/)留言，作者会尽量回复**

> **留[issues](https://github.com/SJYssr/CX_EXAM_python/issues)后可以赞赏作者指明具体的issues号，作者会优先处理** 

---
## 赞赏
<p align="center">
  <img src="https://github.com/SJYssr/img/raw/main/1/zanshang.jpg" width="250" />
</p>

---

- **窗口置顶与防录屏/截屏**：调用`SetWindowDisplayAffinity`，窗口始终置顶且无法被录屏/截屏工具捕获。
- **窗口透明度调节**：右键一键切换（0.2/0.5），Ctrl+滚轮精细调节（0.1~1.0）。
- **字体大小调节**：Alt+滚轮随时调整题库/AI答案字体大小。
- **窗口快速隐藏/显示**：F3一键隐藏到屏幕边缘，再次按下恢复。
- **窗口自由拖动**：Ctrl+鼠标左键拖动窗口到任意位置。
- **ESC/F1-F12快捷退出**：ESC或任意F1-F12键可快速关闭程序（可自定义）。

### 其他实用功能
- **多线程处理**：AI问答、输入等操作均采用多线程，保证界面流畅不卡顿。
- **详细注释与易用配置**：所有代码文件均有详细头部说明和函数注释；`config.yaml`仅存放 Deepseek 配置，简单明了，便于二次开发。

---

## 代码结构与模块说明

本项目已重构为模块化结构，主入口为`main.py`，各功能分为独立模块，便于维护和扩展。

```
├── main.py            # 程序主入口，负责加载配置、初始化界面、事件绑定、AI调用与主流程调度
├── config_manager.py  # 配置加载与校验，提供全局配置访问接口
├── file_manager.py    # 题库文件读取，供主界面加载题库内容
├── ai_spark.py        # 讯飞星火AI WebSocket API调用、参数生成、消息处理
├── ai_deepseek.py     # DeepseekAI HTTP API调用，AI问答请求与异常处理
├── ui_main.py         # 主界面控件的创建、布局、搜索高亮、输入等事件处理
├── ui_ai.py           # AI界面控件的创建、布局、AI搜索与输入事件处理
├── ui_settings.py     # 设置界面（嵌入式）Deepseek 配置读写与保存
├── utils.py           # 通用窗口操作工具函数，如置顶、透明度调整、窗口拖动、关闭等
├── config.yaml        # 配置文件，仅包含 Deepseek 配置（可选）
├── tiku.txt           # 本地题库文件
└── README.md          # 项目说明文档
```
---
### 启动程序
1. **运行程序**：在命令行中运行`python main.py`。
2. **主界面功能**：
   - 题库搜索：输入关键词，回车跳转下一个结果。
   - 设置/AI：顶部右侧“设置”按钮与“AI”按钮（已对调位置）。
   - 快捷输入：在输入框中输入内容，点击"输入"按钮自动输入。

### 常用快捷键与操作
- **F3**：窗口隐藏/恢复
- **Ctrl+鼠标左键**：拖动窗口
- **右键**：切换透明度
- **Ctrl+滚轮**：调整透明度
- **Alt+滚轮**：调整字体大小
- **ESC/F1-F12**：快速退出
- **回车**：题库搜索下一个
---

## 时间日历
| 日期         | 事件                                           |
|------------|----------------------------------------------|
| 2024.12.26 | 项目开始，创建代码仓库                                  |
| 2024.12.27 | 创建README和GPL-3.0 License，demo1.py实现透明度、快捷退出等 |
| 2024.12.28 | 解决截屏/录屏，题库导入与高亮搜索                            |
| 2024.12.29 | 添加一键输入功能                                     |
| 2024.12.30 | 完成AI功能（讯飞星火），项目基本完成                          |
| 2025.1.1   | 添加Alt+滚轮调整字体大小                               |
| 2025.1.6   | 添加窗口可移动（Ctrl+鼠标左键）                           |
| 2025.1.7   | 添加config文件，AI功能更易配置                          |
| 2025.2.13  | 添加Deepseek AI                                |
| 2025.2.25  | 添加前置文件查找、详细注释                                |
| 2025.2.27  | 多线程处理防止堵塞                                    |
| 2025.4.22  | 查找下一个功能                                          |
| 2025.7.9   | 终于把屎山重构了，更加便于修改                              |
| 2025.9.10  | 更新架构                            |
---


## 贡献与反馈
欢迎提交 [Issues](https://github.com/SJYssr/CX_EXAM_python/issues) 反馈问题或建议，或直接 Fork/PR 参与开发。

---

## 免责声明
> **本代码仅用于学习讨论，禁止用于盈利或违法用途。**

- 遵循 [GPL-3.0 License](https://github.com/SJYssr/CX_EXAM_python/blob/main/LICENSE) 协议：
  - 允许开源/免费使用、引用、修改、衍生
  - 禁止闭源商业发布、销售及盈利
  - 基于本代码的程序**必须**同样遵守GPL-3.0协议
- 他人或组织使用本代码进行的任何违法行为与本人无关

---