from typing import Any

import openai
import base64
import io
import os
import json
import datetime

# print(os.getenv("OPENAI_API_URL"))
# print(os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI(
    base_url=os.getenv("OPENAI_API_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
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


def get_object_location(image_base64: str, mime_type: str, object_description: str) -> tuple[str, None] | tuple[
    int, int]:
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
                    {"type": "text",
                     "text": f"请从图片中找到如下对象的位置: {object_description}. 请定位到对象的中心位置. 请返回包含'x','y'两个key的json格式结果. 比如: {{\"x\": 100, \"y\": 200}} . 如果有任何异常情况，比如找不到对象，或描述有歧义，无法定位到唯一结果，请返回包含'error' key的json结果, 例如: {{\"error\":\"你的反馈\"}}"},
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
        # print("req")
        # 调用 OpenAI API
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=messages,
            # max_tokens=100,  # 限制响应长度
        )
        # print(response)
        # 提取响应内容
        response_content = response.choices[0].message.content
        # print(response_content)

        # 记录请求和响应
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "response": response_content,
        }
        log_to_file(log_data)

        # 解析响应中的坐标
        try:
            data = json.loads(response_content)
            if "error" in data:
                return data["error"], None
            x = int(data['x'])
            y = int(data['y'])
            return x, y
        except (json.JSONDecodeError, KeyError, ValueError):
            print("Error: Could not parse coordinates from the response.")
            log_to_file({
                "error": "Error: Could not parse coordinates from the response."
            })
            return json.dumps(response_content), None

    except Exception as e:
        print(f"Error: {e}")
        log_to_file({
            "Exception": f"Error: {e}"
        })
        return "call api error", None


if __name__ == '__main__':
    get_object_location("",
                        "image/jpeg", "任务栏上的 Firefox 浏览器图标")
