from typing import Callable, ContextManager


DbSession = Callable[..., ContextManager]
