# py-folin

## 请先看这里！
## 项目简介
py-folin是一个使用 Python 实现的茯苓语音客户端


## 环境要求
- Python 3.9.13+（推荐 3.12）最大支持版本3.12
- Windows/Linux/macOS

## 相关分支
- main 主分支
- feature/v1 第一个版本
- feature/visual 视觉分支

## 功能特点
- **语音交互**：支持语音输入与识别，实现智能人机交互。  
- **图形化界面**：提供直观易用的 GUI，方便用户操作。  
- **音量控制**：支持音量调节，适应不同环境需求。  
- **会话管理**：有效管理多轮对话，保持交互的连续性。  
- **加密音频传输**：保障音频数据的安全性，防止信息泄露。  
- **CLI 模式**：支持命令行运行，适用于嵌入式设备或无 GUI 环境。  
- **自动验证码处理**：首次使用时，程序自动复制验证码并打开浏览器，简化用户操作。  
- **唤醒词**：支持语音唤醒，免去手动操作的烦恼。  
- **键盘按键**：监听可以最小化视口

## 状态流转图

```
                        +----------------+
                        |                |
                        v                |
+------+  唤醒词/按钮  +------------+   |   +------------+
| IDLE | -----------> | CONNECTING | --+-> | LISTENING  |
+------+              +------------+       +------------+
   ^                                            |
   |                                            | 语音识别完成
   |          +------------+                    v
   +--------- |  SPEAKING  | <-----------------+
     完成播放 +------------+
```

## 项目结构

```
├── .github                          # GitHub 相关配置
│   └── ISSUE_TEMPLATE               # Issue 模板目录
│       ├── bug_report.md            # Bug 报告模板
│       ├── code_improvement.md      # 代码改进建议模板
│       ├── documentation_improvement.md  # 文档改进建议模板
│       └── feature_request.md       # 功能请求模板
├── config                           # 配置文件目录
│   └── config.json                  # 应用程序配置文件
├── docs                             # 文档目录
│   ├── 使用文档.md                  # 用户使用指南
│   └── 异常汇总.md                  # 常见错误及解决方案
├── libs                             # 依赖库目录
│   └── windows                      # Windows 平台特定库
│       └── opus.dll                 # Opus 音频编解码库
├── models                           # 语音模型目录（用于语音唤醒）
├── src                              # 源代码目录
│   ├── audio_codecs                 # 音频编解码模块
│   │   └── audio_codec.py           # 音频编解码器实现
│   ├── audio_processing             # 音频处理模块
│   │   └── wake_word_detect.py      # 语音唤醒词检测实现
│   ├── constants                    # 常量定义
│   │   └── constants.py             # 应用程序常量（状态、事件类型等）
│   ├── display                      # 显示界面模块
│   │   ├── base_display.py          # 显示界面基类
│   │   ├── cli_display.py           # 命令行界面实现
│   │   └── gui_display.py           # 图形用户界面实现
│   ├── iot                          # IoT设备相关模块
│   │   ├── things                   # 具体设备实现目录
│   │   │   ├── lamp.py              # 智能灯具控制实现
│   │   │   ├── music_player.py      # 音乐播放器实现
│   │   │   └── speaker.py           # 智能音箱控制实现
│   │   ├── thing.py                 # IoT设备基类定义
│   │   └── thing_manager.py         # IoT设备管理器（统一管理各类设备）
│   ├── protocols                    # 通信协议模块
│   │   ├── mqtt_protocol.py         # MQTT 协议实现（用于设备通信）
│   │   ├── protocol.py              # 协议基类
│   │   └── websocket_protocol.py    # WebSocket 协议实现
│   ├── utils                        # 工具类模块
│   │   ├── config_manager.py        # 配置管理器（单例模式）
│   │   ├── logging_config.py        # 日志配置
│   │   └── system_info.py           # 系统信息工具（处理 opus.dll 加载等）
│   └── application.py               # 应用程序主类（核心业务逻辑）
├── .gitignore                       # Git 忽略文件配置
├── LICENSE                          # 项目许可证
├── README.md                        # 项目说明文档
├── main.py                          # 程序入口点
├── requirements.txt                 # Python 依赖包列表（通用）
├── requirements_mac.txt             # macOS 特定依赖包列表
└── xiaozhi.spec                     # PyInstaller 打包配置文件
```




## Star History
