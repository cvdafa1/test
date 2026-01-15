tools = list()


def tool(version: str = "*"):
    def decorator(func):
        tools.append({
            "name": func.__name__,
            "dependency_version": version,
            "function": func,
        })
        return func
    return decorator


validators = list()


def validator(version: str = "*"):
    def decorator(func):
        validators.append({
            "name": func.__name__,
            "dependency_version": version,
            "function": func,
        })
        return func
    return decorator


resources = list()

# DO NOT USE THIS, STILL IN EXPERIMENTAL STAGE


def resource(version: str = "*", scheme: str | None = None, mime: str | None = None):
    def decorator(func):
        resources.append({
            "name": func.__name__,
            "dependency_version": version,
            "function": func,
            "scheme": scheme,
            "mime": mime,
        })
        return func
    return decorator


class InteractionError(Exception):
    data: any

    def __init__(self, data: any):
        super().__init__(f"Interaction: {data}")
        self.data = data


class Context:
    config: dict | None = None

    session_id: str | None = None

    tenant_id: str | None = None

    user_id: str | None = None

    create_input_params_interaction: bool | None = None

    cache: dict = {}
    def call_tool(self, tool_name: str, context: any = None, params: any = None):
        print(params)
        for tool in tools:
            if tool["name"] == tool_name:
                func = tool["function"]
                if context is None:
                    context = self
                if params is None:
                    params = {}
                if not callable(func):
                    raise TypeError(f"对象不可调用: {func}")
                # 执行函数
                return func(context, params)
        raise ValueError(f"Tool {tool_name} not found")

    async def get_interaction(self, id: str):
        return self.cache.get(id, None)

    async def require_interaction(self, data: any):
        raise InteractionError(data)

    async def log(self, level: str, message: str):
        print(f"[{level}] {message}")

    async def log_info(self, message: str):
        await self.log("INFO", message)

    async def log_error(self, message: str):
        await self.log("ERROR", message)

    async def log_debug(self, message: str):
        await self.log("DEBUG", message)

    async def log_warn(self, message: str):
        await self.log("WARN", message)

    async def list_files(self, bucket: str, prefix: str | None = None, start_after: str | None = None):
        return []
