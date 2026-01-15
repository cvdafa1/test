import importlib.util
import os
from __runner__ import Context
import asyncio
from typing import Any, Dict, Optional, Callable

def load_module(module_path: str, module_name: Optional[str] = None):
    """
    根据文件路径加载Python模块
    
    Args:
        module_path: Python文件的路径，可以是相对路径(.runtime/tools/目录下)或绝对路径
        module_name: 模块名称，默认根据路径自动生成
        
    Returns:
        加载的模块对象
    """
    # 处理相对路径，转为绝对路径
    if not os.path.isabs(module_path):
        # 转换路径分隔符为系统适用的格式
        module_path = module_path.replace("/", os.path.sep)
        base_dir = os.path.dirname(__file__)
        module_path = os.path.join(base_dir, module_path)
    
    # 如果未提供module_name，则根据路径自动生成
    if module_name is None:
        # 从路径中提取不带扩展名的文件名作为默认module_name
        file_name = os.path.basename(module_path)
        module_name = os.path.splitext(file_name)[0]
        
        # 如果路径包含版本信息等，可以将路径转换为带点的模块名
        # 例如: demo/1.0.0/echo.py -> demo.v1_0_0.echo
        rel_path = os.path.relpath(module_path, os.path.dirname(__file__))
        dir_parts = os.path.dirname(rel_path).split(os.path.sep)
        if dir_parts and dir_parts[0]:
            # 将版本号中的点替换为下划线
            dir_parts = [p.replace(".", "_") for p in dir_parts]
            # 组合成module_name，如demo.v1_0_0.echo
            module_name = ".".join(dir_parts + [module_name])
        
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {module_path}")
        
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

async def run_async(func: Callable, 
             context: Optional[Context] = None, 
             params: Optional[Dict[str, Any]] = None) -> Any:
    """
    异步执行函数
    
    Args:
        func: 要执行的函数对象
        context: 执行上下文
        params: 执行参数
        
    Returns:
        函数的执行结果
    """
    if context is None:
        context = Context()
        context.config = {}
        
    if params is None:
        params = {}
    
    if not callable(func):
        raise TypeError(f"对象不可调用: {func}")
    
    # 执行函数
    if asyncio.iscoroutinefunction(func):
        return await func(context, params)
    else:
        return await asyncio.to_thread(func, context, params)

def run(func: Callable, 
       context: Optional[Context] = None, 
       params: Optional[Dict[str, Any]] = None) -> Any:
    """
    同步执行函数
    
    Args:
        func: 要执行的函数对象
        context: 执行上下文
        params: 执行参数
        
    Returns:
        函数的执行结果
    """
    return asyncio.run(run_async(func, context, params))
