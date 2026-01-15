from __runner__ import tool, Context

@tool(version="*")
async def greet(context: Context, params: any):
    name = params.get("name", "world")

    return {
        "output": "hello, " + name
    }
