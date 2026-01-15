import base64
import json
import aiohttp
from __runner__ import tool, Context


@tool(private=True)
async def screenshot(context: Context, params: any):
    """
    网页截图工具

    参数格式：
    {
        "html": "要截图的网页HTML内容", # 可选，如果html不为空，则url参数无效
        "url": "要截图的网页URL（支持绝对URL或相对URL）", # 可选，如果html不为空，则url参数无效
        "timeout": 30,  # 可选，超时时间（秒），默认30
        "width": 1920,  # 可选，浏览器窗口宽度，默认1920
        "height": 1080, # 可选，浏览器窗口高度，默认1080
        "full_page": false, # 可选，是否截取完整页面，默认false
        "wait_for": "networkidle", # 可选，等待条件，默认networkidle
        "delay": 0  # 可选，截图前延迟时间（秒），用于等待动画或动态内容加载完成，默认0
    }

    说明：
    - 如果html不为空，则使用html参数，否则使用url参数
    - 如果url是相对地址（不以http://或https://开头），会自动拼接context.config中的web_base
    - 例如：url为"/page1"，web_base为"https://example.com"，最终URL为"https://example.com/page1"
    - delay参数可以在页面加载完成后额外等待一段时间，适用于有开场动画或动态内容的网页

    返回格式：
    {
        "image": "<base64编码的图片数据>"
    }
    """
    # 截图服务API地址
    screenshot_api_url = context.config["screenshot_api"]

    # 验证必需参数
    if not isinstance(params, dict) or "url" not in params and "html" not in params:
        raise ValueError("参数必须包含 'url' 或 'html' 字段")

    # 处理URL：如果是相对地址，拼接web_base
    url = params.get("url", None)
    if url and not url.startswith(('http://', 'https://')):
        # 相对地址，需要拼接web_base
        if not hasattr(context, 'config') or 'web_base' not in context.config:
            raise ValueError("相对URL需要配置web_base，但未找到web_base配置")
        web_base = context.config["web_base"]
        # 确保web_base以/结尾，url不以/开头
        if web_base.endswith('/') and url.startswith('/'):
            url = web_base + url[1:]
        elif not web_base.endswith('/') and not url.startswith('/'):
            url = web_base + '/' + url
        else:
            url = web_base + url

    # 构建请求参数
    request_data = {
        "html": params.get("html", None),
        "url": url,
        "timeout": params.get("timeout", 30),
        "width": params.get("width", 1920),
        "height": params.get("height", 1080),
        "full_page": params.get("full_page", False),
        "wait_for": params.get("wait_for", "networkidle"),
        "delay": params.get("delay", 0)
    }

    try:
        # 调用截图服务API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                screenshot_api_url,
                json=request_data,
                timeout=aiohttp.ClientTimeout(
                    total=request_data["timeout"] + 10)
            ) as response:
                if response.status == 200:
                    # 获取图片二进制数据
                    image_bytes = await response.read()
                    # 转换为base64编码
                    image_base64 = base64.b64encode(
                        image_bytes).decode('utf-8')

                    return {
                        "image": image_base64
                    }
                else:
                    error_text = await response.text()
                    raise Exception(
                        f"截图服务返回错误: {response.status} - {error_text}")

    except aiohttp.ClientError as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"截图失败: {str(e)}")


@tool(private=True)
async def template_screenshot(context: Context, params: any):
    """
    模板截图工具

    参数格式：
    {
        "template": "模板名称",
        "data": {},  # 动态类型，传递给模板的数据
        "width": 800,  # 可选，浏览器窗口宽度，默认800
        "height": 600  # 可选，浏览器窗口高度，默认600
    }

    说明：
    - template: 模板名称，用于指定要使用的截图模板
    - data: 动态类型的数据，会传递给模板进行渲染
    - width: 浏览器窗口宽度，默认800
    - height: 浏览器窗口高度，默认600

    返回格式：
    {
        "image": "<base64编码的图片数据>"
    }
    """
    # 模板截图服务API地址
    template_screenshot_api_url = context.config["template_screenshot_api"]

    # 验证必需参数
    if not isinstance(params, dict) or "template" not in params:
        raise ValueError("参数必须包含 'template' 字段")

    # 构建请求参数
    request_data = {
        "template": params["template"],
        "data": params.get("data", {}),
        "width": params.get("width", 1920),
        "height": params.get("height", 1080)
    }

    try:
        # 调用模板截图服务API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                template_screenshot_api_url,
                json=request_data,
                timeout=aiohttp.ClientTimeout(total=60)  # 设置60秒超时
            ) as response:
                if response.status == 200:
                    # 获取图片二进制数据
                    image_bytes = await response.read()
                    # 转换为base64编码
                    image_base64 = base64.b64encode(
                        image_bytes).decode('utf-8')

                    return {
                        "image": image_base64
                    }
                else:
                    error_text = await response.text()
                    raise Exception(
                        f"模板截图服务返回错误: {response.status} - {error_text}")

    except aiohttp.ClientError as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"模板截图失败: {str(e)}")
