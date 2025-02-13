import threading
from time import sleep
import pyautogui
import base64
from io import BytesIO
from PIL import ImageDraw, Image
import subprocess
import pyperclip
class LinuxAutomation:
    def __init__(self):
        pass

    def capture_fullscreen_jpg_base64(self):
        """
        全屏截图为jpg格式并返回图片的base64和mimeType
        """
        screenshot = pyautogui.screenshot()
        mouse_x, mouse_y = pyautogui.position()
        draw = ImageDraw.Draw(screenshot)
        # draw.ellipse((mouse_x - 7, mouse_y - 7, mouse_x + 7, mouse_y + 7), fill='red')
        draw.line((mouse_x - 5, mouse_y - 5, mouse_x + 5, mouse_y + 5), fill='red', width=2)
        draw.line((mouse_x - 5, mouse_y + 5, mouse_x + 5, mouse_y - 5), fill='red', width=2)

        # 绘制带白色边框的黄色三角形作为鼠标指针
        # pointer_size = 10
        # draw.polygon([
        #     (mouse_x, mouse_y),
        #     (mouse_x + pointer_size, mouse_y + pointer_size * 2),
        #     (mouse_x - pointer_size, mouse_y + pointer_size * 2),
        # ], fill='yellow', outline='white')

        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_str = base64.b64encode(img_byte_arr).decode('utf-8')
        mime_type = "image/jpeg"
        width, height = screenshot.size
        return base64_str, mime_type, width, height, mouse_x, mouse_y

    def _capture_and_get_info(self):
        """
        Helper function to capture screen and return relevant info.
        """
        base64_str, mime_type, width, height, mouse_x, mouse_y = self.capture_fullscreen_jpg_base64()
        description = f"截图分辨率: {width}x{height}, 鼠标指针坐标: ({mouse_x}, {mouse_y}), 鼠标指针为红色x的交叉点。"
        return base64_str, mime_type, description

    def move_mouse_to(self, x, y):
        """
        模拟移动鼠标到指定位置
        """
        pyautogui.moveTo(x, y)
        base64_str, mime_type, description = self._capture_and_get_info()
        return base64_str, mime_type, description, "通过返回的图片分析，鼠标指针指向的点是否在需要操作的对象上？"

    def mouse_click(self):
        """
        模拟鼠标点击
        """
        pyautogui.click()
        sleep(1)
        base64_str, mime_type, description = self._capture_and_get_info()
        return base64_str, mime_type, description, "鼠标是否点击成功？"
    
    def mouse_leftClick(self):
        """
        模拟鼠标点击
        """
        pyautogui.leftClick()
        sleep(1)
        base64_str, mime_type, description = self._capture_and_get_info()
        return base64_str, mime_type, description, "鼠标是否左键点击成功？"
        
    def mouse_doubleClick(self):
        """
        模拟鼠标点击
        """
        pyautogui.doubleClick()
        sleep(1)
        base64_str, mime_type, description = self._capture_and_get_info()
        return base64_str, mime_type, description, "鼠标是否双击成功？"

    def keyboard_input_key(self, key):
        """
        模拟键盘输入一个key
        """
        pyautogui.press(key)
        sleep(1)
        base64_str, mime_type, description = self._capture_and_get_info()
        return base64_str, mime_type, description, f"是否输入了键 {key}？"

    def keyboard_input_hotkey(self, keys):
        """
        模拟键盘输入一个组合key
        """
        pyautogui.hotkey(*keys)
        sleep(1)
        base64_str, mime_type, description = self._capture_and_get_info()
        return base64_str, mime_type, description, f"是否输入了组合键 {', '.join(keys)}？"

    def keyboard_input_string(self, text):
        """
        模拟键盘输入一个字符串
        """
        if has_unsupported_chars(text):
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
        else:
            pyautogui.typewrite(text)
        base64_str, mime_type, description = self._capture_and_get_info()
        return base64_str, mime_type, description, f"是否输入了字符串 '{text}'？"

    def execute_command(self, command):
        """
        执行控制台命令并返回所有标准输出和标准错误的输出
        """

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        output = stdout.decode() + stderr.decode()
        return output

    def execute_command_non_blocking(self, command):
        """
        执行控制台命令但不等待，并立即返回标准输出和标准错误的输出
        """

        thread = threading.Thread(target=run_command, args=(command,))
        thread.start()

        sleep(1)  # 例如，主线程可以执行 5 秒的其他任务
        return "done"

import re
def has_unsupported_chars(text):
  pattern = r'[^\x00-\x7F]+'  # 匹配非 ASCII 字符
  return bool(re.search(pattern, text))

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sleep(1)  # 等待 1 秒

    # 获取 stdout 和 stderr 的内容
    stdout_output = process.stdout.read().decode('utf-8')
    stderr_output = process.stderr.read().decode('utf-8')

    return stdout_output, stderr_output, process

if __name__ == '__main__':
    automation = LinuxAutomation()

    # 示例：全屏截图
    base64_str, mime_type = automation.capture_fullscreen_jpg_base64()
    print(f"截图 mimeType: {mime_type}")
    print(f"截图 base64 (前100字符): {base64_str[:100]}...")

    # 示例：移动鼠标并点击
    base64_str, mime_type, description, question = automation.move_mouse_to(500, 500)
    print(description, question)
    automation.mouse_click()

    # 示例：键盘输入
    base64_str, mime_type, description, question = automation.keyboard_input_string("Hello, Linux!")
    print(description, question)
    automation.keyboard_input_key('enter')
    automation.keyboard_input_hotkey(['ctrl', 'shift', 'esc']) # 打开任务管理器 (示例组合键)
