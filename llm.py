import openai
import base64
import io
from PIL import Image, ImageDraw
import os
import json
import datetime

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_API_URL"), api_key=os.getenv("OPENAI_API_KEY")
)

# 从环境变量读取日志文件路径
LOG_FILE_PATH = os.getenv("LLM_LOG_FILE_PATH")

def log_to_file(log_data):
    """将日志数据写入文件"""
    if LOG_FILE_PATH:
        try:
            with open(LOG_FILE_PATH, "a") as log_file:
                log_file.write(json.dumps(log_data, ensure_ascii=False) + "\\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")
def get_object_location(image_base64: str, mime_type:str, object_description: str) -> tuple[int, int]:
    """
    使用 OpenAI SDK 确定图像中对象的位置。

    Args:
        image_base64: base64 编码的图像数据。
        mime_type: 图像的 MIME 类型 (例如 "image/jpeg", "image/png")。
        object_description: 图像中对象的描述。

    Returns:
        一个包含对象 x 和 y 坐标的元组。如果未找到对象或发生错误，则返回 None。
    """
    try:
        # 构建发送给 OpenAI API 的消息
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"请从图片中找到如下对象的位置: {object_description}。请定位到对象的中心位置，使用setPosition反馈给我。如果有任何异常情况，请使用error函数进行反馈",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_base64}"},
                    },
                ],
            }
        ]
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "request": messages,
        }
        log_to_file(log_data)
        # 调用 OpenAI API
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "setPosition",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "integer","description":"位置的x坐标值"},
                                "y": {"type": "integer","description":"位置的y坐标值"},
                                "thinking": {"type": "string"},
                            },
                            "required": ["x", "y"],
                        },
                        "description": "设置鼠标的位置",
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "error",
                        "parameters": {
                            "type": "object",
                            "properties": {"text": {"type": "string"}},
                            "required": ["text"],
                        },
                        "description": "返回错误信息",
                    }
                },
            ],
            tool_choice="required",
            # max_tokens=100,  # 限制响应长度
        )

        print(response)
        # 提取响应内容
        response_content = response.choices[0].message
        # print(response_content)

        # 记录请求和响应
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "response": response_content,
        }
        log_to_file(log_data)

       # 解析响应中的坐标
        try:
            if response_content.tool_calls:
                for tool_call in response_content.tool_calls:
                    function_name = tool_call.function.name
                    print(tool_call.function.arguments)
                    arguments = json.loads(tool_call.function.arguments)
                    print(arguments)
                    if function_name == "setPosition":
                        x = int(arguments['x'])
                        y = int(arguments['y'])
                        return x, y
                    elif function_name == "error":
                        return arguments['text'],None
                    else:
                        return "call api error",None # 未知function
            elif response_content.function_call:
                function_name = response_content.function_call.name
                arguments = json.loads(response_content.function_call.arguments)
                if function_name == "setPosition":
                    x = int(arguments['x'])
                    y = int(arguments['y'])
                    return x, y
                elif function_name == "error":
                    return arguments['text'],None
                else:
                    return "call api error",None # 未知function
            else: # 正常文本返回
                return response_content.content,None

        except (json.JSONDecodeError, KeyError, ValueError):
            print("Error: Could not parse coordinates from the response.")
            log_to_file({
                "error":"Error: Could not parse coordinates from the response."
            })
            return (response_content.content,None)

    except Exception as e:
        print(f"Error: {e}")
        log_to_file({"Exception": f"Error: {e}"})
        return ("call api error", None)


if __name__ == "__main__":
    # get_object_location("", "image/jpeg", "任务栏上的 Firefox 浏览器图标")
    # 从本地文件读取图像并转换为base64
    with open("/Users/rikaaa0928/Downloads/screenshot_20250212_155450.png", "rb") as image_file:  # 假设图片文件名为 image.jpg，且与 llm.py 在同一目录下
        image = Image.open(image_file)
        image = image.rotate(-90) # 顺时针旋转90度
        buffered = io.BytesIO()
        image.save(buffered, format="PNG") # 假设原图是PNG, 这里保存为PNG
        encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
    test_image_base64 = encoded_string
    # 测试对象描述
    test_object_description = "右上角搜索框"
    # 调用函数
    result = get_object_location(test_image_base64, "image/jpeg", test_object_description)
    # 输出结果
    print(result)
    image = Image.open(io.BytesIO(base64.b64decode(test_image_base64)))
    print(image.size)
    if result and isinstance(result, tuple) and len(result) == 2 and all(isinstance(coord, int) for coord in result):
        x, y = result
        # 将base64图像数据转换为PIL图像对象
        
        # 创建ImageDraw对象
        draw = ImageDraw.Draw(image)
        # 画一个小红点
        radius = 5  # 半径
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='red')
        # 保存图片
        image.save("save.png")
