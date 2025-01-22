import os
import platform

def build():
    # 确定系统类型
    system = platform.system()
    
    # 要打包的文件
    files = [
        'game_menu.py',
        'snake_game.py',
        'tetris_game.py',
        'scores.py'
    ]
    
    # 要包含的资源文件
    datas = []
    
    # 基本命令
    cmd = f'pyinstaller --noconfirm --onefile --windowed --name "经典游戏合集" '
    
    # 添加图标（如果有）
    if system == 'Windows':
        cmd += '--icon=icon.ico '
    elif system == 'Darwin':  # macOS
        cmd += '--icon=icon.icns '
    
    # 添加所有Python文件
    cmd += '--add-data "scores.py:." '
    cmd += 'game_menu.py'
    
    # 执行打包命令
    os.system(cmd)
    
    print("打包完成！")

if __name__ == '__main__':
    build() 