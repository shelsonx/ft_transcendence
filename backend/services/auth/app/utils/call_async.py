from asgiref.sync import sync_to_async
from typing import Callable, Coroutine, Any, TypeVar, ParamSpec

_P = ParamSpec("_P")
_R = TypeVar("_R")

async def call_async(func: Callable[_P, _R], *args, **kwargs) -> _R:
    async_func = sync_to_async(func)
    return await async_func(*args, **kwargs)