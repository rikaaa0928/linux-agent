from time import sleep
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import asyncio
import requests

app = Server("linux-agent")
LINUX_SERVER_URL = "http://127.0.0.1:5001"

@app.list_tools()
async def handle_list_prompts() -> list[types.Tool]:
    return [
        types.Tool(
            name="capture_screen",
            description="全屏截图",
            inputSchema={"type": "object"}
        ),
        types.Tool(
            name="move_mouse_to",
            description="模拟移动鼠标到指定位置",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "integer", "description": "X 坐标"},
                    "y": {"type": "integer", "description": "Y 坐标"},
                },
                "required": ["x", "y"]
            }
        ),
        types.Tool(
            name="mouse_click",
            description="模拟鼠标点击",
            inputSchema={"type": "object"}
        ),
        types.Tool(
            name="mouse_leftClick",
            description="模拟鼠标左键点击",
            inputSchema={"type": "object"}
        ),
        types.Tool(
            name="mouse_doubleClick",
            description="模拟鼠标双击",
            inputSchema={"type": "object"}
        ),
        types.Tool(
            name="keyboard_input_key",
            description="模拟键盘输入一个key",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "按键名称"},
                },
                "required": ["key"]
            }
        ),
        types.Tool(
            name="keyboard_input_hotkey",
            description="模拟键盘输入一个组合key",
            inputSchema={
                "type": "object",
                "properties": {
                    "keys": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "组合键名称列表"
                    },
                },
                "required": ["keys"]
            }
        ),
        types.Tool(
            name="keyboard_input_string",
            description="模拟键盘输入一个字符串",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "要输入的字符串"},
                },
                "required": ["text"]
            }
        ),
         types.Tool(
                name="execute_command",
                description="执行控制台命令并返回所有标准输出和标准错误",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "要执行的命令"},
                    },
                    "required": ["command"]
                }
            ),
        types.Tool(
            name="execute_command_non_blocking",
            description="执行控制台命令但不等待并返回输出",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "要执行的命令"},
                },
                "required": ["command"]
            }
        ),
         types.Tool(
            name="wait",
            description="等待一段时间",
            inputSchema={
                "type": "object",
                "properties": {
                    "duration": {"type": "number", "description": "等待的时间(秒)"},
                },
                "required": ["duration"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "capture_screen":
        response = requests.get(f"{LINUX_SERVER_URL}/capture_screen")
        response.raise_for_status()
        data = response.json()
        base64_str = data["data"]
        mime_type = data["mime_type"]
        description = data["description"]
        return [
            types.TextContent(
                type="text",
                text=description
            ),
            types.ImageContent(
                type="image",
                mimeType=mime_type,
                data=base64_str
            )
        ]
    elif name == "move_mouse_to":
        x = arguments["x"]
        y = arguments["y"]
        response = requests.post(f"{LINUX_SERVER_URL}/move_mouse_to", json={"x": x, "y": y})
        response.raise_for_status()
        data = response.json()
        return [
                        types.TextContent(type="text", text=data["description"]),
            types.TextContent(type="text", text=data["question"]),
            types.ImageContent(type="image", mimeType=data["mime_type"], data=data["data"]),
        ]
    elif name == "mouse_click":
        response = requests.get(f"{LINUX_SERVER_URL}/mouse_click")
        response.raise_for_status()
        data = response.json()
        return [
            types.ImageContent(type="image", mimeType=data["mime_type"], data=data["data"]),
            types.TextContent(type="text", text=data["description"]),
            types.TextContent(type="text", text=data["question"]),
        ]
    elif name == "mouse_leftClick":
        response = requests.get(f"{LINUX_SERVER_URL}/mouse_leftClick")
        response.raise_for_status()
        data = response.json()
        return [
            types.ImageContent(type="image", mimeType=data["mime_type"], data=data["data"]),
            types.TextContent(type="text", text=data["description"]),
            types.TextContent(type="text", text=data["question"]),
        ]
    elif name == "mouse_doubleClick":
        response = requests.get(f"{LINUX_SERVER_URL}/mouse_doubleClick")
        response.raise_for_status()
        data = response.json()
        return [
            types.ImageContent(type="image", mimeType=data["mime_type"], data=data["data"]),
            types.TextContent(type="text", text=data["description"]),
            types.TextContent(type="text", text=data["question"]),
        ]
    elif name == "keyboard_input_key":
        key = arguments["key"]
        response = requests.post(f"{LINUX_SERVER_URL}/keyboard_input_key", json={"key": key})
        response.raise_for_status()
        data = response.json()
        return [
            types.ImageContent(type="image", mimeType=data["mime_type"], data=data["data"]),
            types.TextContent(type="text", text=data["description"]),
            types.TextContent(type="text", text=data["question"]),
        ]
    elif name == "keyboard_input_hotkey":
        keys = arguments["keys"]
        response = requests.post(f"{LINUX_SERVER_URL}/keyboard_input_hotkey", json={"keys": keys})
        response.raise_for_status()
        data = response.json()
        return [
            types.ImageContent(type="image", mimeType=data["mime_type"], data=data["data"]),
            types.TextContent(type="text", text=data["description"]),
            types.TextContent(type="text", text=data["question"]),
        ]
    elif name == "keyboard_input_string":
        text = arguments["text"]
        response = requests.post(f"{LINUX_SERVER_URL}/keyboard_input_string", json={"text": text})
        response.raise_for_status()
        data = response.json()
        return [
            types.ImageContent(type="image", mimeType=data["mime_type"], data=data["data"]),
            types.TextContent(type="text", text=data["description"]),
            types.TextContent(type="text", text=data["question"]),
        ]
    elif name == "execute_command":
        command = arguments["command"]
        response = requests.post(f"{LINUX_SERVER_URL}/execute_command", json={"command": command})
        response.raise_for_status()
        data = response.json()
        output = data["output"]
        return [
            types.TextContent(type="text", text=output),
        ]
    elif name == "execute_command_non_blocking":
        command = arguments["command"]
        response = requests.post(f"{LINUX_SERVER_URL}/execute_command_non_blocking", json={"command": command})
        response.raise_for_status()
        data = response.json()
        output = data["output"]
        return [
            types.TextContent(type="text", text=output),
        ]
    elif name == "wait":
        duration = arguments["duration"]
        sleep(duration)
        response = requests.get(f"{LINUX_SERVER_URL}/capture_screen")
        response.raise_for_status()
        data = response.json()
        base64_str = data["data"]
        mime_type = data["mime_type"]
        description = data["description"]
        return [
            types.TextContent(
                type="text",
                text=description
            ),
            types.ImageContent(
                type="image",
                mimeType=mime_type,
                data=base64_str
            )
        ]
    else:
        raise ValueError(f"Tool not found: {name}")

async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="linux-agent",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(run())
