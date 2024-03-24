import tkinter as tk  # 导入tkinter模块用于创建GUI界面
import pyautogui  # 导入pyautogui模块用于模拟鼠标点击
import keyboard  # 导入keyboard模块用于检测按键
from PIL import Image  # 导入PIL库中的Image类
import os  # 导入os模块用于文件路径操作
import time  # 导入time模块用于时间操作

# 获取当前脚本所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))
image_folder = os.path.join(current_directory, "image")

# 图片路径字典，存储各图片名称及对应路径
image_paths = {
    "end2": os.path.join(image_folder, "end2.png"),
    "shibai": os.path.join(image_folder, "shibai.png"),
    "start": os.path.join(image_folder, "start.png"),
    "start1": os.path.join(image_folder, "start1.png"),
    "xuanzejiejie1": os.path.join(image_folder, "xuanzejiejie1.png"),
    "xuanzejiejie2": os.path.join(image_folder, "xuanzejiejie2.png"),
    "xuanshang": os.path.join(image_folder, "xuanshang.png")
}

# 加载图片文件到内存中，构建图片字典
images = {name: Image.open(path) for name, path in image_paths.items()}

is_running = False  # 标识是否正在运行自动点击程序
a = 0  # 计数器，记录成功点击次数

def simulate_click(x, y):
    """
    后台模拟鼠标点击操作
    """
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(x, y)
    time.sleep(0.5)  # 等待一段时间以确保稳定性
    pyautogui.click()
    pyautogui.moveTo(current_x, current_y)

def locate_and_click(image_name, confidence=0.8):
    """
    寻找指定图片并进行后台点击
    """
    try:
        result = pyautogui.locateCenterOnScreen(images[image_name], confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None
    
    if result:
        simulate_click(result.x, result.y)  # 后台模拟点击操作
        return True
    else:
        return False
    
def update_label():
    """
    更新标签内容显示
    """
    try:
        a_label.config(text=f"已成功突破寮突第 {a} 次")
    except Exception as e:
        print(f"Error updating label: {e}")
    root.after(100, update_label)

def check_and_handle_images():
    """
    检查和处理不同图片的情况
    """
    if locate_and_click("shibai"):  # 如果找到“失败”图片则停止
        return
    if locate_and_click("end2"):  # 如果找到“结束”图片增加计数
        global a
        a += 1
    elif locate_and_click("start") or locate_and_click("start1") or locate_and_click("xuanzejiejie1") or locate_and_click("xuanzejiejie2") or locate_and_click("xuanshang"):
        pass

def start_loop():
    """
    开始/停止循环函数
    """
    global is_running
    is_running = not is_running
    while is_running:  # 当程序处于运行状态时
        check_and_handle_images()  # 检查并处理图片
        if keyboard.is_pressed("1"):  # 按下数字1时退出程序
            print("退出成功")
            is_running = False
        root.update()

# 创建主窗口
root = tk.Tk()
root.title("自动寮突脚本")
root.geometry("250x120")

# 添加标签显示次数
a_label = tk.Label(root, text=f"已成功突破寮突第 {a} 次", font=("bold", 12))
a_label.pack(side="top", pady=10)

# 启动更新标签内容的函数
update_label()

# 添加按钮用于开始/停止循环
start_button = tk.Button(root, text="开始/停止寮突，或者按住数字1键结束", command=start_loop, width=31,height=2, font=("bold", 10))
start_button.pack(side="top", anchor="center")

# 运行Tkinter主循环
root.mainloop() 
