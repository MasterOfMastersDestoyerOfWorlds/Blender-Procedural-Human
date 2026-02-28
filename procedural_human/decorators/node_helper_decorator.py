import inspect
from dataclasses import dataclass, field


@dataclass
class NodeHelperMeta:
    """Metadata describing how a node helper replaces a raw Blender node."""

    bl_idname: str
    func_name: str
    func_module: str
    prop_args: list = field(default_factory=list)
    inputs: object = field(default_factory=dict)
    optional_inputs: object = field(default_factory=set)
    outputs: object = field(default_factory=dict)
    custom_emit: object = None
    arg_order: list = field(default_factory=list)

    def resolve_inputs(self, node):
        return self.inputs(node) if callable(self.inputs) else self.inputs

    def resolve_optional_inputs(self, node):
        return self.optional_inputs(node) if callable(self.optional_inputs) else self.optional_inputs

    def resolve_outputs(self, node):
        return self.outputs(node) if callable(self.outputs) else self.outputs


class node_helper:
    """Decorator that registers a node helper with export metadata.

    Usage::

        @node_helper(
            bl_idname="ShaderNodeMath",
            prop_args=["operation"],
            inputs={0: "a", 1: "b"},
            optional_inputs={1},
            outputs={0: None},
        )
        def math_op(group, op, a, b=None):
            ...

    :param bl_idname: Blender node type this helper replaces.
    :param prop_args: Node properties to extract as positional arguments.
    :param inputs: Dict mapping input_idx (int) or input_name (str) to argument names.
        Can be a callable(node) -> dict for operation-dependent routing.
    :param optional_inputs: Set of input indices that may be omitted when not linked.
        Can be a callable(node) -> set.
    :param outputs: Dict mapping output_idx (int) or output_name (str) to variable suffix.
        None means the bare variable name; a string like "_x" becomes var_x.
        Can be a callable(node) -> dict.
    :param custom_emit: Optional callable(node, var_name, resolve_input) for complex cases.
        Should return (lines: list[str], output_map: dict[int, str]).
    """

    registry: dict[str, NodeHelperMeta] = {}

    def __init__(self, bl_idname, prop_args=None, inputs=None, optional_inputs=None,
                 outputs=None, custom_emit=None):
        self._bl_idname = bl_idname
        self._prop_args = prop_args or []
        self._inputs = inputs if inputs is not None else {}
        self._optional_inputs = optional_inputs if optional_inputs is not None else set()
        self._outputs = outputs if outputs is not None else {}
        self._custom_emit = custom_emit

    def __call__(self, func):
        params = list(inspect.signature(func).parameters.keys())
        skip = 1 + len(self._prop_args)
        arg_order = params[skip:]

        meta = NodeHelperMeta(
            bl_idname=self._bl_idname,
            func_name=func.__name__,
            func_module=func.__module__,
            prop_args=self._prop_args,
            inputs=self._inputs,
            optional_inputs=self._optional_inputs,
            outputs=self._outputs,
            custom_emit=self._custom_emit,
            arg_order=arg_order,
        )
        func._node_helper_meta = meta
        node_helper.registry[self._bl_idname] = meta
        return func
