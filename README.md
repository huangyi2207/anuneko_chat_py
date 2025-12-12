# [anuneko_chat_py]
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
这是一个与 [Anuneko.ai](https://anuneko.ai/) 网站进行交互的 Python 项目。它封装了必要的 API 调用，让你能够通过脚本实现聊天功能。
## 📋 要求
- Python 3.10 或更高版本
- pip (Python 包管理器)
## 🚀 安装与配置
### 1. 克隆项目
```bash
git clone https://github.com/huangyi2207/anuneko_chat_py.git
cd anuneko_chat_py
```
### 2. 安装依赖
建议使用虚拟环境来隔离项目依赖。
```bash
pip install -r requirements.txt
```
### 3. 配置 `x-token`
为了与 Anuneko.ai 的 API 进行交互，你需要提供你的个人 `x-token`。
1.  运行main.py按照提示填写即可
---
## 🔑 如何获取 `x-token`
`x-token` 是你登录 Anununeko.ai 网站后，浏览器用于身份验证的凭证。请按照以下步骤操作获取：
1.  **访问 [https://anuneko.ai/](https://anuneko.ai/) 完成登录**
2.  **在页面任意位置按下 `F12` 键（或在 Mac 上按 `Cmd + Option + I`）打开开发者工具** 
3.  **网络→标头→请求标头→x-token**
## 📁 项目结构
```
.
├── main.py                           # 主程序入口
├── requirements.txt                  # 项目依赖列表
└── README.md                         # 项目说明文档
```
## 📜 免责声明
本项目是一个非官方的工具，与 Anuneko.ai 官方没有任何关联。
- 本项目仅供学习和研究使用，请勿用于任何商业或非法用途。
- 使用本项目所产生的任何后果由使用者自行承担。
- Anuneko.ai 官方可能会随时更改其 API 或网站结构，导致本项目失效。
- 请务必遵守 Anuneko.ai 的服务条款。
---
