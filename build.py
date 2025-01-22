import os
import platform
import shutil
import subprocess
import sys
import time

def install_requirements():
    """安装必要的依赖"""
    print("检查并安装依赖...")
    requirements = ['pygame', 'pyinstaller', 'tqdm']
    for req in requirements:
        try:
            print(f"正在安装 {req}...")
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--upgrade', req],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ {req} 已安装")
        except subprocess.CalledProcessError as e:
            print(f"安装 {req} 失败: {e.stderr}")
            raise

def clean_install_dir(install_dir):
    """清理安装目录"""
    if os.path.exists(install_dir):
        print("\n清理旧的安装文件...")
        try:
            for item in os.listdir(install_dir):
                item_path = os.path.join(install_dir, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            print("✓ 清理完成")
        except Exception as e:
            print(f"清理过程中出现错误: {e}")
            raise

def get_system_specific_config():
    """获取系统特定的配置"""
    system = platform.system()
    
    # 获取 pygame 安装路径
    import pygame
    pygame_path = os.path.dirname(pygame.__file__)
    
    config = {
        'extra_args': [
            '--noupx',  # 禁用 UPX 压缩以提高启动速度
            '--clean'
        ],
        'hidden_imports': [
            'pygame',
            'numpy',
            'json',
            'random',
            'sys',
            'os',
            'time'
        ],
        'binary_paths': [],
        'data_paths': []
    }

    if system == 'Darwin':  # macOS
        # 检测是否是 Apple Silicon
        is_arm = platform.machine() == 'arm64'
        
        config['extra_args'].extend([
            '--codesign-identity', '-',
            '--osx-bundle-identifier', 'com.barrysen.gamecollection',
            '--noconsole',
            '--name', '经典游戏合集',
            '--hidden-import', 'pkg_resources.py2_warn'
        ])
        
        # 如果是 Apple Silicon，不使用 universal2
        if not is_arm:
            config['extra_args'].extend(['--target-architecture', 'universal2'])
        
        # 使用实际的 pygame 路径
        config['binary_paths'].append(f'{pygame_path}:pygame')
        
        # 添加 SDL2 相关文件
        sdl_paths = [
            '/opt/homebrew/lib/libSDL2-2.0.0.dylib',
            '/opt/homebrew/lib/libSDL2_image-2.0.0.dylib',
            '/opt/homebrew/lib/libSDL2_mixer-2.0.0.dylib',
            '/opt/homebrew/lib/libSDL2_ttf-2.0.0.dylib'
        ]
        
        for sdl_path in sdl_paths:
            if os.path.exists(sdl_path):
                config['binary_paths'].append(f'{sdl_path}:.')
        
    elif system == 'Windows':
        config['extra_args'].extend([
            '--noconsole',
            '--uac-admin',
            '--win-private-assemblies',
            '--win-no-prefer-redirects',
            '--name', '经典游戏合集'
        ])
        # Windows 上使用分号作为分隔符
        config['binary_paths'].append(f'{pygame_path};pygame')
        config['hidden_imports'].extend([
            'win32api',
            'win32con'
        ])
        
    elif system == 'Linux':
        config['extra_args'].extend([
            '--noconsole',
            '--runtime-tmpdir', '.',
            '--name', '经典游戏合集'
        ])
        # Linux 上使用冒号作为分隔符
        config['binary_paths'].append(f'{pygame_path}:pygame')
        config['hidden_imports'].extend([
            'cairo',
            'gi'
        ])

    # 添加 pygame 相关的数据文件
    pygame_data = os.path.join(pygame_path, 'pygame_sdl2_data')
    if os.path.exists(pygame_data):
        separator = ';' if system == 'Windows' else ':'
        config['data_paths'].append(f'{pygame_data}{separator}pygame_sdl2_data')

    return config

def main():
    # 首先安装依赖
    install_requirements()
    
    # 现在可以安全地导入 tqdm
    from tqdm import tqdm
    
    def show_progress_bar(description, total_seconds):
        """显示进度条"""
        with tqdm(total=100, 
                  desc=description, 
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            for _ in range(100):
                time.sleep(total_seconds/100)
                pbar.update(1)

    def build():
        try:
            # 确定系统类型
            system = platform.system()
            print(f"当前操作系统: {system}")
            
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 创建 Install 目录
            install_dir = os.path.join(current_dir, "Install")
            if not os.path.exists(install_dir):
                os.makedirs(install_dir)
            
            # 在打包前清理安装目录
            clean_install_dir(install_dir)
            
            # 准备打包命令
            print("\n准备打包环境...")
            show_progress_bar("环境准备", 2)
            
            # 获取系统特定配置
            config = get_system_specific_config()
            
            # 基本命令
            cmd = [
                sys.executable,
                '-m',
                'PyInstaller',
                '--noconfirm',
                '--onefile',
                '--clean',
                '--distpath', install_dir,
                '--workpath', os.path.join(current_dir, 'build', 'temp'),
                '--specpath', os.path.join(current_dir, 'build')
            ]
            
            # 在 macOS 上添加额外的链接器参数
            if system == 'Darwin':
                os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
                if platform.machine() == 'arm64':
                    os.environ['ARCHFLAGS'] = '-arch arm64'
            
            # 添加系统特定参数
            cmd.extend(config['extra_args'])
            
            # 添加隐藏导入
            for hidden_import in config['hidden_imports']:
                cmd.extend(['--hidden-import', hidden_import])
            
            # 添加二进制文件
            for binary_path in config['binary_paths']:
                cmd.extend(['--add-binary', binary_path])
            
            # 添加数据文件
            for data_path in config['data_paths']:
                cmd.extend(['--add-data', data_path])
            
            # 添加图标
            if system == 'Windows' and os.path.exists('icon.ico'):
                cmd.extend(['--icon', os.path.join(current_dir, 'icon.ico')])
            elif system == 'Darwin' and os.path.exists('icon.icns'):
                cmd.extend(['--icon', os.path.join(current_dir, 'icon.icns')])
            
            # 添加所有必需的文件
            separator = ';' if system == 'Windows' else ':'
            scores_path = os.path.join(current_dir, 'scores.py')
            cmd.extend(['--add-data', f'{scores_path}{separator}.'])
            
            # 添加其他Python文件
            for py_file in ['snake_game.py', 'tetris_game.py']:
                py_path = os.path.join(current_dir, py_file)
                if os.path.exists(py_path):
                    cmd.extend(['--add-data', f'{py_path}{separator}.'])
            
            # 添加字体文件
            font_paths = {
                'Darwin': [
                    "/System/Library/Fonts/Hiragino Sans GB.ttc",
                    "/System/Library/Fonts/STHeiti Light.ttc"
                ],
                'Windows': [
                    "C:\\Windows\\Fonts\\msyh.ttc",
                    "C:\\Windows\\Fonts\\simhei.ttf"
                ],
                'Linux': [
                    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
                ]
            }
            
            for font_path in font_paths.get(system, []):
                if os.path.exists(font_path):
                    cmd.extend(['--add-data', f'{font_path}{separator}.'])
                    break
            
            # 主程序文件
            game_menu_path = os.path.join(current_dir, 'game_menu.py')
            cmd.append(game_menu_path)
            
            # 执行打包命令
            print("\n开始打包...")
            print(f"执行命令: {' '.join(cmd)}")
            
            # 显示打包进度条
            with tqdm(total=100, 
                     desc="打包进度", 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # 模拟打包进度
                while process.poll() is None:
                    if pbar.n < 90:  # 保留最后10%给完成阶段
                        pbar.update(1)
                    time.sleep(0.5)
                
                # 完成最后的进度
                pbar.n = 100
                pbar.refresh()
            
            # 获取命令输出
            stdout, stderr = process.communicate()
            
            # 检查打包结果
            executable_name = '经典游戏合集.exe' if system == 'Windows' else '经典游戏合集'
            executable_path = os.path.join(install_dir, executable_name)
            
            if os.path.exists(executable_path):
                print("\n" + "="*50)
                print("打包完成！")
                print("="*50 + "\n")
                
                # 显示生成的文件信息
                print("生成的文件:")
                if system == 'Darwin':  # macOS
                    print(f"1. {executable_name}.app")
                    print("   - 这是 macOS 应用程序包，双击即可运行")
                    print(f"2. {executable_name}")
                    print("   - 这是命令行可执行文件，可以在终端中运行")
                elif system == 'Windows':
                    print(f"1. {executable_name}")
                    print("   - 这是 Windows 可执行文件，双击即可运行")
                
                print(f"\n文件位置: {install_dir}")
                
                # 清理临时文件
                print("\n清理临时文件...")
                show_progress_bar("清理临时文件", 1)
                
                build_dir = os.path.join(current_dir, 'build')
                if os.path.exists(build_dir):
                    shutil.rmtree(build_dir)
                spec_file = os.path.join(current_dir, '经典游戏合集.spec')
                if os.path.exists(spec_file):
                    os.remove(spec_file)
                
                # 显示文件大小
                size_mb = os.path.getsize(executable_path) / (1024 * 1024)
                print(f"\n可执行文件大小: {size_mb:.1f}MB")
                
                print("\n" + "="*50)
                print("打包过程全部完成！游戏已准备就绪！")
                print("="*50)
                
                # 根据系统显示不同的运行提示
                if system == 'Darwin':
                    print("\n运行方式：")
                    print("1. 直接双击 Install/经典游戏合集.app")
                    print("2. 或在终端中运行 Install/经典游戏合集")
                elif system == 'Windows':
                    print("\n运行方式：")
                    print("双击 Install/经典游戏合集.exe")

                # 在 macOS 上设置可执行权限
                if system == 'Darwin':
                    os.chmod(executable_path, 0o755)
                    # 如果存在 .app 文件，也设置其权限
                    app_path = os.path.join(install_dir, f"{executable_name}.app")
                    if os.path.exists(app_path):
                        os.system(f'chmod -R 755 "{app_path}"')
                        # 对 .app 包进行签名
                        os.system(f'codesign --force --deep --sign - "{app_path}"')
            else:
                print("\n打包失败！未找到生成的可执行文件")
                if stdout:
                    print("\nPyInstaller 输出:")
                    print(stdout)
                if stderr:
                    print("\n错误信息:")
                    print(stderr)
                raise Exception("打包失败")
                
        except subprocess.CalledProcessError as e:
            print(f"\n错误: 命令执行失败")
            if e.stdout:
                print("\n输出:")
                print(e.stdout)
            if e.stderr:
                print("\n错误信息:")
                print(e.stderr)
            raise
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            raise
        finally:
            # 确保清理临时文件
            build_dir = os.path.join(current_dir, 'build')
            if os.path.exists(build_dir):
                try:
                    shutil.rmtree(build_dir)
                except:
                    pass
            spec_file = os.path.join(current_dir, '经典游戏合集.spec')
            if os.path.exists(spec_file):
                try:
                    os.remove(spec_file)
                except:
                    pass

            if system == 'Darwin':
                # 创建 Info.plist
                info_plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>经典游戏合集</string>
    <key>CFBundleExecutable</key>
    <string>经典游戏合集</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.barrysen.gamecollection</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>经典游戏合集</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
'''
                info_plist_path = os.path.join(current_dir, 'Info.plist')
                with open(info_plist_path, 'w') as f:
                    f.write(info_plist_content)
                cmd.extend(['--osx-bundle-identifier', 'com.barrysen.gamecollection'])
                cmd.extend(['--plist', info_plist_path])

    return build()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("\n打包过程中断")
        sys.exit(1) 