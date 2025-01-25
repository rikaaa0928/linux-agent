import pyautogui
import base64
from io import BytesIO
from PIL import ImageDraw

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
        draw.ellipse((mouse_x - 15, mouse_y - 15, mouse_x + 15, mouse_y + 15), fill='red')
        img_byte_arr = BytesIO()
        screenshot.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_str = base64.b64encode(img_byte_arr).decode('utf-8')
        mime_type = "image/jpeg"
        return base64_str, mime_type

    def move_mouse_to(self, x, y):
        """
        模拟移动鼠标到指定位置
        """
        pyautogui.moveTo(x, y)

    def mouse_click(self):
        """
        模拟鼠标点击
        """
        pyautogui.click()
    
    def mouse_leftClick(self):
        """
        模拟鼠标点击
        """
        pyautogui.leftClick()
        
    def mouse_doubleClick(self):
        """
        模拟鼠标点击
        """
        pyautogui.doubleClick()

    def keyboard_input_key(self, key):
        """
        模拟键盘输入一个key
        """
        pyautogui.press(key)

    def keyboard_input_hotkey(self, keys):
        """
        模拟键盘输入一个组合key
        """
        pyautogui.hotkey(*keys)

    def keyboard_input_string(self, text):
        """
        模拟键盘输入一个字符串
        """
        pyautogui.typewrite(text)

if __name__ == '__main__':
    automation = LinuxAutomation()

    # 示例：全屏截图
    base64_str, mime_type = automation.capture_fullscreen_jpg_base64()
    print(f"截图 mimeType: {mime_type}")
    print(f"截图 base64 (前100字符): {base64_str[:100]}...")

    # 示例：移动鼠标并点击
    automation.move_mouse_to(500, 500)
    automation.mouse_click()

    # 示例：键盘输入
    automation.keyboard_input_string("Hello, Linux!")
    automation.keyboard_input_key('enter')
    automation.keyboard_input_hotkey(['ctrl', 'shift', 'esc']) # 打开任务管理器 (示例组合键)
