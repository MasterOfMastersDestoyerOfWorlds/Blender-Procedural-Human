from typing import Callable, Dict
from procedural_human.logger import logger


class geo_node_group:
    """
    Decorator for registering geometry node group creation functions.
    Usage:
        @geo_node_group
        def create_my_node_group():
            ...
    """

    registry: Dict[str, Callable] = {}

    def __new__(cls, func: Callable):
        cls.registry[func.__name__] = func
        logger.info(f"[Geo Node Registry] Registered node group: {func.__name__}")
        return func

    @classmethod
    def discover_and_register_all_decorators(cls):
        """
        Log the number of registered node groups.
        Actual registration happens at import time via the decorator.
        """
        logger.info(f"[Geo Node Registry] Registered {len(cls.registry)} node groups")

    @classmethod
    def unregister_all_decorators(cls):
        """
        Clear the registry.
        """
        cls.registry.clear()
