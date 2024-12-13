import pyautogui
import keyboard
import tkinter as tk
from tkinter import ttk
import time
import threading
import win32api
import win32con
import json
import os
from PIL import ImageGrab

class ColorPicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("颜色检测自动点击器")
        self.root.geometry("400x500")
        
        # 性能优化变量
        self.is_mouse_down = False
        self.last_screenshot = None
        self.screenshot_interval = 0.02
        self.last_screenshot_time = 0
        
        # 默认快捷键设置
        self.default_hotkeys = {
            "pick_color": "space",
            "set_target": "insert",
            "start_click": "home",
            "stop_click": "end"
        }
        
        # 加载保存的快捷键设置
        self.hotkeys = self.load_hotkeys()
        
        # 快捷键设置区域
        self.shortcut_frame = tk.LabelFrame(self.root, text="快捷键设置", padx=10, pady=5)
        self.shortcut_frame.pack(fill="x", padx=10, pady=5)
        
        # 创建快捷键按钮
        self.shortcut_buttons = {}
        self.shortcut_labels = {
            "pick_color": "实时取色",
            "set_target": "设置目标颜色",
            "start_click": "开始自动点击",
            "stop_click": "停止自动点击"
        }
        
        for key, label in self.shortcut_labels.items():
            frame = tk.Frame(self.shortcut_frame)
            frame.pack(fill="x", pady=2)
            
            tk.Label(frame, text=f"{label}:", width=12, anchor="w").pack(side="left")
            
            button = tk.Button(
                frame,
                text=self.hotkeys[key].upper(),
                width=10,
                command=lambda k=key: self.start_key_detection(k)
            )
            button.pack(side="left", padx=5)
            self.shortcut_buttons[key] = button
        
        # 创建界面元素
        self.color_frame = tk.Frame(self.root, width=100, height=100, relief="solid", borderwidth=1)
        self.color_frame.pack(pady=10)
        
        self.color_label = tk.Label(
            self.root, 
            text="当前颜色\nRGB: ---, ---, ---\nHEX: #------",
            font=("Arial", 10)
        )
        self.color_label.pack(pady=5)
        
        # 目标颜色显示区域
        self.target_frame = tk.LabelFrame(self.root, text="目标颜色", padx=10, pady=5)
        self.target_frame.pack(fill="x", padx=10, pady=5)
        
        self.target_color_label = tk.Label(
            self.target_frame, 
            text="目标颜色: 未设置",
            font=("Arial", 10)
        )
        self.target_color_label.pack()
        
        # 容差设置
        self.tolerance_frame = tk.Frame(self.target_frame)
        self.tolerance_frame.pack(fill="x", pady=5)
        
        self.tolerance_label = tk.Label(
            self.tolerance_frame, 
            text="颜色容差值(0-255):",
            font=("Arial", 10)
        )
        self.tolerance_label.pack(side="left")
        
        self.tolerance_var = tk.StringVar(value="10")
        self.tolerance_entry = tk.Entry(
            self.tolerance_frame, 
            textvariable=self.tolerance_var,
            width=10
        )
        self.tolerance_entry.pack(side="left", padx=5)
        
        # 状态显示
        self.status_label = tk.Label(
            self.root,
            text="等待操作...",
            font=("Arial", 10, "bold"),
            fg="blue"
        )
        self.status_label.pack(pady=10)
        
        # 初始化变量
        self.is_picking = False
        self.is_clicking = False
        self.running = True
        self.target_color = None
        self.detecting_key = False
        self.current_key_setting = None
        
        # 启动颜色检测线程
        self.color_thread = threading.Thread(target=self.color_picker_loop)
        self.color_thread.daemon = True
        self.color_thread.start()
        
        # 绑定键盘事件
        self.bind_hotkeys()
    
    def load_hotkeys(self):
        try:
            if os.path.exists('hotkeys.json'):
                with open('hotkeys.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return self.default_hotkeys.copy()
    
    def save_hotkeys(self):
        with open('hotkeys.json', 'w') as f:
            json.dump(self.hotkeys, f)
    
    def start_key_detection(self, key_type):
        if self.detecting_key:
            return
            
        self.detecting_key = True
        self.current_key_setting = key_type
        self.shortcut_buttons[key_type].configure(text="按下按键...")
        
        # 启动按键检测线程
        threading.Thread(target=self.detect_key, daemon=True).start()
    
    def detect_key(self):
        # 等待按键
        event = keyboard.read_event(suppress=True)
        if event.event_type == 'down':
            new_key = event.name
            
            # 解除旧的绑定
            try:
                keyboard.remove_hotkey(self.hotkeys[self.current_key_setting])
            except:
                pass
            
            # 更新快捷键
            self.hotkeys[self.current_key_setting] = new_key
            self.shortcut_buttons[self.current_key_setting].configure(text=new_key.upper())
            
            # 重新绑定快捷键
            self.bind_hotkeys()
            
            # 保存设置
            self.save_hotkeys()
        
        self.detecting_key = False
    
    def bind_hotkeys(self):
        # 清除所有现有的热键绑定
        keyboard.unhook_all()
        
        # 重新绑定所有热键
        keyboard.on_press_key(self.hotkeys["pick_color"], self.start_picking)
        keyboard.on_release_key(self.hotkeys["pick_color"], self.stop_picking)
        keyboard.on_press_key(self.hotkeys["set_target"], self.set_target_color)
        keyboard.on_press_key(self.hotkeys["start_click"], self.start_auto_click)
        keyboard.on_press_key(self.hotkeys["stop_click"], self.stop_auto_click)
    
    def color_matches(self, color1, color2, tolerance):
        if not color1 or not color2:
            return False
        return all(abs(a - b) <= tolerance for a, b in zip(color1, color2))
    
    def set_target_color(self, e=None):
        if hasattr(self, 'current_color'):
            self.target_color = self.current_color
            hex_color = '#{:02x}{:02x}{:02x}'.format(*self.target_color)
            self.target_color_label.configure(
                text=f"目标颜色: RGB{self.target_color} / {hex_color}"
            )
            self.status_label.configure(
                text="✅ 目标颜色已设置！",
                fg="green"
            )
    
    def mouse_down(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    
    def mouse_up(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def get_screen_pixel(self, x, y):
        current_time = time.time()
        
        # 控制截图频率
        if current_time - self.last_screenshot_time >= self.screenshot_interval:
            try:
                # 使用PIL的ImageGrab代替pyautogui的screenshot
                # 只截取鼠标位置附近的小区域
                bbox = (x-1, y-1, x+2, y+2)
                self.last_screenshot = ImageGrab.grab(bbox=bbox)
                self.last_screenshot_time = current_time
            except:
                return None
        
        try:
            # 获取中心点的颜色
            return self.last_screenshot.getpixel((1, 1))
        except:
            return None
    
    def color_picker_loop(self):
        while self.running:
            if not self.detecting_key:  # 只在不检测按键时更新颜色
                try:
                    x, y = win32api.GetCursorPos()  # 使用win32api代替pyautogui
                    pixel = self.get_screen_pixel(x, y)
                    
                    if pixel:
                        self.current_color = pixel
                        hex_color = '#{:02x}{:02x}{:02x}'.format(*pixel)
                        
                        # 使用after方法更新GUI，避免线程冲突
                        self.root.after(0, self.update_color_display, hex_color, pixel)
                        
                        if self.is_clicking and self.target_color:
                            tolerance = int(self.tolerance_var.get())
                            if self.color_matches(pixel, self.target_color, tolerance):
                                if not self.is_mouse_down:
                                    self.mouse_down()
                                    self.is_mouse_down = True
                            elif self.is_mouse_down:
                                self.mouse_up()
                                self.is_mouse_down = False
                                
                except Exception as e:
                    print(f"Error: {e}")
                
            time.sleep(0.001)  # 减少睡眠时间，提高响应速度
    
    def update_color_display(self, hex_color, pixel):
        """更新颜色显示（在主线程中执行）"""
        self.color_frame.configure(bg=hex_color)
        self.color_label.configure(
            text=f"当前颜色\nRGB: {pixel[0]}, {pixel[1]}, {pixel[2]}\nHEX: {hex_color}"
        )
    
    def start_picking(self, e):
        self.is_picking = True
        self.status_label.configure(
            text="🔍 正在取色...",
            fg="blue"
        )
    
    def stop_picking(self, e):
        self.is_picking = False
        self.status_label.configure(
            text="等待操作...",
            fg="blue"
        )
    
    def start_auto_click(self, e):
        if self.target_color:
            self.is_clicking = True
            self.status_label.configure(
                text="🖱️ 自动点击已启动！",
                fg="green"
            )
        else:
            self.status_label.configure(
                text="❌ 请先设置目标颜色！",
                fg="red"
            )
    
    def stop_auto_click(self, e):
        self.is_clicking = False
        self.mouse_up()
        self.status_label.configure(
            text="⏹️ 自动点击已停止",
            fg="blue"
        )
    
    def run(self):
        self.root.mainloop()
        self.running = False

if __name__ == "__main__":
    app = ColorPicker()
    app.run() 