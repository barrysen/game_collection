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

## 开发环境

### 基础环境
1. Python 3.8 或更高版本
2. pip 包管理工具
3. git 版本控制工具

### 获取代码
```bash
git clone https://github.com/barrysen/game_collection.git
cd game_collection
```

### 安装依赖
```bash
pip install -r requirements.txt
```

## 运行方式

### 开发模式
直接运行游戏菜单：
```bash
python game_menu.py
```

### 桌面版本
1. 运行打包脚本：
   ```bash
   python build.py
   ```
2. 运行方式：
   - Windows: 双击 `Install/经典游戏合集.exe`
   - macOS: 双击 `Install/经典游戏合集.app`

## 项目结构
```
game_collection/
├── game_menu.py     # 游戏菜单主程序
├── snake_game.py    # 贪吃蛇游戏
├── tetris_game.py   # 俄罗斯方块游戏
├── scores.py        # 分数管理
├── build.py         # 桌面版打包脚本
└── requirements.txt # 项目依赖
```

## 注意事项
- 游戏会自动保存最高分记录
- 如遇到字体显示问题，请确保系统安装了中文字体
- 打包功能需要额外的环境配置，详见打包脚本中的说明

## 贡献指南

欢迎为经典游戏合集做出贡献！请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 了解更多信息。

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。 