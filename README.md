# 经典游戏合集

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.6.1-green.svg)
![License](https://img.shields.io/github/license/barrysen/game_collection)
![Release](https://img.shields.io/github/v/release/barrysen/game_collection)

这是一个包含贪吃蛇和俄罗斯方块的经典游戏合集。

## 下载地址

- [最新版本下载](https://github.com/barrysen/game_collection/releases/latest)
- [历史版本](https://github.com/barrysen/game_collection/releases)

## 游戏说明

### 贪吃蛇
- 使用方向键控制蛇的移动
- 空格键暂停游戏
- 吃到食物可以增加长度和分数

### 俄罗斯方块
- 方向键左右移动方块
- 上方向键旋转方块
- 下方向键加速下落
- 空格键直接落下

## 安装说明

### 环境准备

1. 确保安装了 Python 3.8 或更高版本。
2. 克隆项目到本地：

   ```bash
   git clone https://github.com/barrysen/game_collection.git
   cd game_collection
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

### 打包游戏

1. 运行打包脚本：

   ```bash
   python build.py
   ```

   这将使用 PyInstaller 打包游戏，生成的可执行文件会在 `Install` 目录下。

### 运行游戏

- Windows 用户：双击 `Install/经典游戏合集.exe` 运行游戏。
- Mac 用户：双击 `Install/经典游戏合集.app` 运行游戏。

## 注意事项
- 游戏会自动保存最高分记录
- 如遇到字体显示问题，请确保系统安装了中文字体

## 贡献指南

欢迎为经典游戏合集做出贡献！请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 了解更多信息。 