# ReFile (自动重命名神器)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![PySide6](https://img.shields.io/badge/UI-PySide6-green)
![Nuitka](https://img.shields.io/badge/Build-Nuitka-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

ReFile 是一款基于 Python 与 PySide6 开发的现代化本地文件批量重命名工具。旨在帮助用户通过直观的图形界面，高效、安全地处理复杂的文件重命名需求。

## ✨ 核心特性

- **🚀 极致性能**：底层基于 Nuitka 编译为 C 语言级别的本地机器码，告别传统 Python 打包的臃肿与启动延迟。
- **💻 现代化 UI**：采用 PySide6 (Qt) 构建的直观图形界面，操作流畅，所见即所得。
- **🛡️ 纯净安全**：采用绿色文件夹架构（独立运行环境），无后台驻留，不写系统注册表，纯本地离线运行，绝不上传任何隐私数据。
- **🧩 灵活强大**：支持正则表达式切片、前后缀修改、序号递增等多种高级重命名逻辑。

---

## 📥 下载与使用说明 (面向普通用户)

1. 在 [Releases](https://github.com/dooth333/rename_file/releases) 页面下载最新版本的 `.zip` 压缩包。
2. 将压缩包解压到任意非系统关键目录（如 `D:\Tools\ReFile`）。
3. 进入文件夹，双击运行 `ReFile.exe` 即可开始使用。

### ⚠️ 杀毒软件拦截说明与解决方案 (必读)

由于本软件采用 Nuitka 深度编译技术，且作为独立开发者项目，**未购买每年数千元的商业 EV 代码签名证书**，初次运行时大概率会遇到以下情况，请勿惊慌：

> **现象：** Windows 弹出蓝色全屏警告（SmartScreen），提示“Windows 已保护你的电脑”，或者显示“未知发布者”。
>
> **原因分析：** > 微软的安全机制极度依赖昂贵的商业证书来判定软件的“声望”。本软件带有安全的 SHA-256 开发者自签名，行为极其规矩，**并非病毒**，系统绝对不会将其直接删除，仅仅是因为“缺乏全球知名度”而进行常规盘问。
>
> **✅ 完美解决方法：**
> 在弹出的蓝色警告窗口上，点击左侧的 **【更多信息】**，随后右下角会出现并点击 **【仍要运行】**。只需信任这一次，后续即可享受秒开的极致体验。

（如果您依然有所顾虑，本工具完全开源，欢迎审查源代码或将其上传至 VirusTotal 等在线引擎进行查杀验证。）

---

## 🛠️ 本地开发与编译 (面向开发者)

本项目的工程化管理采用了现代 Python 工具链。

### 环境准备
1. 安装 [uv](https://github.com/astral-sh/uv) (极速 Python 包与环境管理器)。
2. 克隆本项目代码到本地。

### 启动开发环境
无需手动配置虚拟环境，直接运行以下命令，`uv` 将自动在几秒内为你准备好完全一致的开发环境（锁定 Python 3.12）：

```powershell
uv sync
uv run main.py
```
### 编译打包
本项目摒弃了传统的 PyInstaller，采用 Nuitka + MinGW64 进行底层 C 语言级别编译，以获取最小的体积和最快的运行速度。

在项目根目录下执行：

```PowerShell
uv run nuitka main.py
```
(注：打包配置已全部硬编码在 main.py 顶部的 # nuitka-project: 注释中，包括去黑框、图标设置、版本号注入及免单文件解压策略。)

📜 许可协议
本项目采用 MIT License 开源协议。你可以自由地使用、修改和分发本代码，但请保留原作者版权声明。

Copyright (c) 2026 by Wenc. All rights reserved.