# Minecraft Auto Stone Miner / 我的世界自动挖石机

[English](#english) | [中文](#中文)

## English

### Introduction
This is an automatic color detection and clicking tool specifically designed for AFK stone mining in Minecraft. It helps players automatically mine stones from stone generators without constant manual clicking.

### Features
- Real-time color detection
- Automatic clicking when target color is detected
- Customizable hotkeys
- Adjustable color tolerance
- User-friendly GUI interface

### How to Use
1. Run the program
2. Hold the hotkey (default: Space) to pick the color of the stone you want to mine
3. Press the set target hotkey (default: Insert) to set the target color
4. Press the start hotkey (default: Home) to begin auto-mining
5. Press the stop hotkey (default: End) to stop

### Requirements
- Python 3.x
- Required packages:
  ```
  pyautogui==0.9.54
  keyboard==0.13.5
  pywin32==308
  ```

### Installation
1. Clone this repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the program:
   ```
   python color_picker.py
   ```

---

## 中文

### 简介
这是一个专门为我的世界（Minecraft）自动挖石机设计的颜色检测和自动点击工具。它可以帮助玩家在使用刷石机时实现自动挖掘，无需手动持续点击。

### 功能特点
- 实时颜色检测
- 检测到目标颜色自动点击
- 可自定义快捷键
- 可调节颜色容差
- 友好的图形界面

### 使用方法
1. 运行程序
2. 按住快捷键（默认：空格键）选取要挖掘的石头颜色
3. 按设置目标快捷键（默认：Insert键）设置目标颜色
4. 按开始快捷键（默认：Home键）开始自动挖掘
5. 按停止快捷键（默认：End键）停止操作

### 环境要求
- Python 3.x
- 所需包：
  ```
  pyautogui==0.9.54
  keyboard==0.13.5
  pywin32==308
  ```

### 安装步骤
1. 克隆此仓库
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```
   python color_picker.py
   ```

## License
MIT License 