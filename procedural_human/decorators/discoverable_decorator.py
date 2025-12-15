import re


class DiscoverableClassDecorator:

    registry: dict = {}
    """
    Base class for discoverable decorators.
    """

    def __new__(cls, target_cls=None, **kwargs):
        if target_cls is not None and isinstance(target_cls, type):
            cls.setup_decorator(target_cls, **kwargs)
            return target_cls
        instance = super().__new__(cls)
        return instance

    def __init__(self, target_cls=None, **kwargs):
        if target_cls is not None and isinstance(target_cls, type):
            return
        self._kwargs = kwargs

    def __call__(self, cls):
        self.setup_decorator(cls, **self._kwargs)
        return cls

    @staticmethod
    def setup_decorator(cls, **kwargs):
        raise NotImplementedError("Subclasses must implement setup_decorator()")

    def register(self):
        DiscoverableClassDecorator.registry[self.name] = self

    def unregister(self):
        del DiscoverableClassDecorator.registry[self.name]

    @classmethod
    def to_snake_case(cls, name: str) -> str:
        """
        Convert CamelCase to snake_case, handling acronyms properly.

        @param name: The name to convert to snake case.
        @return: The name converted to snake case.
        """
        result = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
        result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", result)
        return result.lower()

    @classmethod
    def to_title_with_spaces(cls, name: str) -> str:
        """
        Convert CamelCase to Title With Spaces, handling acronyms properly.

        @param name: The name to convert to title with spaces.
        @return: The name converted to title with spaces.
        """
        result = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
        result = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", result)
        return result
