from time import sleep

from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
import mcp.types as types

from linuxserver import linux_automation

app = Server("linux-agent")


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
            name="ping",
            description="ping",
            inputSchema={"type": "object"}
        ),
        types.Tool(
            name="wait",
            description="等待一段时间",
            inputSchema={
                "type": "object",
                "properties": {
                    "duration": {"type": "integer", "description": "等待的时间（秒）"},
                },
                "required": ["duration"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[
    types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "capture_screen":
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        )]
    elif name == "move_mouse_to":
        x = arguments["x"]
        y = arguments["y"]
        linux_automation.move_mouse_to(x, y)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认鼠标指针（黄色圆点）位置是否符合预期，否则请继续调整",
        )]
    elif name == "mouse_click":
        linux_automation.mouse_click()
        sleep(1)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认是否点击成功，是否需要等待",
        )]
    elif name == "mouse_leftClick":
        linux_automation.mouse_leftClick()
        sleep(1)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认是否点击成功，是否需要等待",
        )]
    elif name == "mouse_doubleClick":
        linux_automation.mouse_doubleClick()
        sleep(1)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认是否点击成功，是否需要等待",
        )]
    elif name == "keyboard_input_key":
        key = arguments["key"]
        linux_automation.keyboard_input_key(key)
        sleep(1)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认是否输入成功，是否需要等待",
        )]
    elif name == "keyboard_input_hotkey":
        keys = arguments["keys"]
        linux_automation.keyboard_input_hotkey(keys)
        sleep(1)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认是否输入成功，是否需要等待",
        )]
    elif name == "keyboard_input_string":
        text = arguments["text"]
        linux_automation.keyboard_input_string(text)
        sleep(1)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认是否输入成功",
        )]
    elif name == "ping":
        return [types.TextContent(
            type="text",
            text="pong",
        )]
    elif name == "wait":
        duration = arguments["duration"]
        sleep(duration)
        base64_str, mime_type, (mouse_x, mouse_y) = linux_automation.capture_fullscreen_jpg_base64()
        return [types.ImageContent(
            type="image",
            mimeType=mime_type,
            data=base64_str
        ),types.TextContent(
            type="text",
            text="当前鼠标指针（黄色圆点）位置({},{})".format(mouse_x, mouse_y),
        ),types.TextContent(
            type="text",
            text="请确认等待的资源是否正确加载，是否加载完成",
        )]
    else:
        raise ValueError(f"Tool not found: {name}")



if __name__ == "__main__":
    sse = SseServerTransport("/messages/")


    async def handle_sse(request):
        async with sse.connect_sse(
                request.scope, request.receive, request._send
        ) as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )


    # Create Starlette routes for SSE and message handling
    routes = [
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]


    # # Define handler functions
    # async def handle_sse(request):
    #     async with sse.connect_sse(
    #             request.scope, request.receive, request._send
    #     ) as streams:
    #         await app.run(
    #             streams[0], streams[1], app.create_initialization_options()
    #         )


    starlette_app = Starlette(routes=routes)
    from starlette.middleware.cors import CORSMiddleware

    origins = [
        "http://localhost",  # 允许来自 localhost 的跨域请求
        "http://localhost:1420",  # 允许来自 localhost 的跨域请求
        "http://127.0.0.1",  # 允许来自 127.0.0.1 的跨域请求
        "http://127.0.0.1:1420",  # 允许来自 yourdomain.com 的跨域请求
    ]

    starlette_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  # 允许携带 cookie
        allow_methods=["*"],  # 允许所有 HTTP 方法
        allow_headers=["*"],  # 允许所有 HTTP header
    )
    # Create and run Starlette app

    import uvicorn

    uvicorn.run(starlette_app, host="0.0.0.0", port=54321)
