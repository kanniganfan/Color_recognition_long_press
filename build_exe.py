import PyInstaller.__main__
import os

# 确保在正确的目录中
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

PyInstaller.__main__.run([
    'color_picker.py',
    '--name=MinecraftAutoMiner',
    '--windowed',
    '--onefile',
    '--clean',
    '--add-data=README.md;.',
    '--add-data=LICENSE;.',
    # '--icon=icon.ico',  # 如果您想添加图标，取消这行的注释
]) 