import io
import math
import os

import requests
import pyautogui
import base64
from io import BytesIO
from PIL import ImageDraw, Image, ImageFont
from google.genai import types
from google.genai.types import Tool
from google import genai

client = genai.Client(
    http_options={
        "base_url": os.getenv("GEMINI_API_URL"),
    },
    api_key=os.getenv("GEMINI_API_KEY"))
grid_size = 100


def capture_fullscreen_jpg_base64(LINUX_SERVER_URL: str):
    response = requests.get(f"{LINUX_SERVER_URL}/capture_screen?grid=true")
    response.raise_for_status()
    data = response.json()
    base64_str = data["data"]
    mime_type = data["mime_type"]
    return base64_str, mime_type


def capture_grid_jpg_base64(LINUX_SERVER_URL: str, grid_number: int):
    response = requests.get(f"{LINUX_SERVER_URL}/capture_grid?grid={grid_number}")
    response.raise_for_status()
    data = response.json()
    base64_str = data["data"]
    mime_type = data["mime_type"]
    return base64_str, mime_type


def get_point(grid_number: int, width: int, height: int, select: int):
    x = (grid_number // (math.ceil(height / grid_size))) * grid_size
    y = (grid_number % (math.ceil(height / grid_size))) * grid_size
    fromx = x - grid_size
    fromy = y - grid_size
    tox = x + 2 * grid_size
    toy = y + 2 * grid_size
    if fromx < 0:
        fromx = 0
    if fromy < 0:
        fromy = 0
    if tox > width:
        tox = width
    if toy > height:
        toy = height

    offx = x
    offy = y

    # 定义九个点的坐标和编号
    points = [
        (offx + 0, offy + 0, "0"),  # 左上角
        (offx + grid_size // 2, offy + 0, "1"),  # 上边中点
        (offx + grid_size - 1, offy + 0, "2"),  # 右上角
        (offx + 0, offy + grid_size // 2, "3"),  # 左边中点
        (offx + grid_size // 2, offy + grid_size // 2, "4"),  # 中心
        (offx + grid_size - 1, offy + grid_size // 2, "5"),  # 右边中点
        (offx + 0, offy + grid_size - 1, "6"),  # 左下角
        (offx + grid_size // 2, offy + grid_size - 1, "7"),  # 下边中点
        (offx + grid_size - 1, offy + grid_size - 1, "8"),  # 右下角
    ]
    return points[select][0], points[select][1]


def get_object_location(LINUX_SERVER_URL: str, target: str) -> tuple[str, None] | tuple[
    int, int]:
    base64_str, mime_type = capture_fullscreen_jpg_base64(LINUX_SERVER_URL)
    img_data = base64.b64decode(base64_str)
    img_bytes = io.BytesIO(img_data)
    img = Image.open(img_bytes)
    width, height = img.size
    # target = input("请输入目标（例如 'firefox 图标'）: ")  # 让用户输入目标
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[f"请找出包含 '{target}' 的网格编号：", "当前截图：", img],  # 使用用户输入的目标
        config=types.GenerateContentConfig(
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode=types.FunctionCallingConfigMode.ANY)),
            tools=[types.Tool(function_declarations=[
                types.FunctionDeclaration(
                    name="set_grid_number",
                    description="包含目标的网格",
                    parameters=types.Schema(
                        properties={
                            'grid_number': types.Schema(type=types.Type.NUMBER, description="网格编号"),
                        },
                        type=types.Type.OBJECT,
                        required=["grid_number"]
                    ),
                )
            ])],
            system_instruction="找出包含目标的网格编号，然后调用set_grid_number函数指定网格。",
            # automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        )
    )
    for parts in response.candidates[0].content.parts:
        print(parts)
        if parts.function_call is None:
            continue
        fc = parts.function_call
        if fc.name != "set_grid_number":
            continue
        grid_number = fc.args["grid_number"]
        grid_img_base64, grid_img_mime_type = capture_grid_jpg_base64(LINUX_SERVER_URL, grid_number)
        grid_img_data = base64.b64decode(grid_img_base64)
        grid_img_bytes = io.BytesIO(grid_img_data)
        grid_img = Image.open(grid_img_bytes)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[[f"请定位出可以点击到 '{target}' 的点：", "局部截图：", grid_img]],  # 使用用户输入的目标
            config=types.GenerateContentConfig(
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode=types.FunctionCallingConfigMode.ANY)),
                tools=[types.Tool(function_declarations=[
                    types.FunctionDeclaration(
                        name="set_point_number",
                        description="以点击到目标的点",
                        parameters=types.Schema(
                            properties={
                                'point_number': types.Schema(type=types.Type.NUMBER, description="点编号"),
                            },
                            type=types.Type.OBJECT,
                            required=["point_number"]
                        ),
                    )
                ])],
                system_instruction="找出请找出可以点击到目标的点的编号，然后调用set_point_number函数指定该点。",
                # automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            )
        )
        for parts in response.candidates[0].content.parts:
            print(parts)
            if parts.function_call is None:
                continue
            fc = parts.function_call
            if fc.name != "set_point_number":
                continue
            point_number = fc.args["point_number"]
            x, y = get_point(grid_number=grid_number, width=width, height=height, select=point_number)
            return x, y
    return "error", None
