"""
DSL Executor for procedural generation.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from procedural_human.dsl.naming import NamingEnvironment, build_naming_environment
from procedural_human.decorators.dsl_primitive_decorator import (
    get_dsl_namespace,
    get_all_dsl_names,
)
from procedural_human.logger import *


@dataclass
class DSLExecutionResult:
    """Result of executing a DSL file."""

    file_path: str
    naming_env: NamingEnvironment
    definitions: Dict[str, type]
    instances: Dict[str, Any]
    errors: List[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


@dataclass
class DSLInstance:
    """A DSL instance created during execution."""

    name: str
    definition_name: str
    instance: Any
    source_file: str
    segments: List[Any] = field(default_factory=list)
    joints: List[Any] = field(default_factory=list)


class DSLExecutor:
    """Executes DSL files in a sandboxed environment."""

    def __init__(self):
        self.naming_env: Optional[NamingEnvironment] = None
        self.current_file: Optional[str] = None
        self._definitions: Dict[str, type] = {}
        self._instances: Dict[str, Any] = {}

    def execute_file(self, file_path: str) -> DSLExecutionResult:
        """Execute a DSL file and extract definitions and instances."""
        import traceback

        errors = []

        try:
            self.naming_env = build_naming_environment(file_path)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            error_lines = [f"Failed to parse DSL file: {type(e).__name__}: {e}"]
            for frame in tb:
                if "procedural_human" in frame.filename or file_path in frame.filename:
                    error_lines.append(
                        f"  at {frame.filename}:{frame.lineno} in {frame.name}()"
                    )
            errors.append("\n".join(error_lines))
            return DSLExecutionResult(
                file_path=file_path,
                naming_env=NamingEnvironment(),
                definitions={},
                instances={},
                errors=errors,
            )

        self.current_file = file_path

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
        except Exception as e:
            errors.append(f"Failed to read file: {e}")
            return DSLExecutionResult(
                file_path=file_path,
                naming_env=self.naming_env,
                definitions={},
                instances={},
                errors=errors,
            )

        namespace = self._create_namespace()

        try:
            exec(compile(source_code, file_path, "exec"), namespace)
        except Exception as e:
            errors.append(f"Failed to execute DSL: {e}")
            import traceback

            errors.append(traceback.format_exc())

        self._extract_results(namespace)

        return DSLExecutionResult(
            file_path=file_path,
            naming_env=self.naming_env,
            definitions=self._definitions,
            instances=self._instances,
            errors=errors,
        )

    def _create_namespace(self) -> Dict[str, Any]:
        """Create the sandboxed namespace with DSL primitives from registry."""
        return get_dsl_namespace({"__naming_env__": self.naming_env})

    def _extract_results(self, namespace: Dict[str, Any]) -> None:
        """Extract definitions and instances from executed namespace."""
        self._definitions.clear()
        self._instances.clear()

        skip_names = get_all_dsl_names()

        for name, value in namespace.items():
            if name.startswith("_"):
                continue
            if isinstance(value, type) and name not in skip_names:
                self._definitions[name] = value

        for name, value in namespace.items():
            if name.startswith("_"):
                continue
            if name in skip_names:
                continue
            if isinstance(value, type):
                continue
            if not callable(value):
                class_name = value.__class__.__name__
                if class_name in self._definitions:
                    self._instances[name] = value


def execute_dsl_file(file_path: str) -> DSLExecutionResult:
    """Execute a DSL file and return the results."""
    executor = DSLExecutor()
    return executor.execute_file(file_path)


def get_dsl_instances(file_path: str) -> List[str]:
    """Get list of instance names from a DSL file."""
    result = execute_dsl_file(file_path)
    logger.info(f"[DSL] File: {file_path}")
    logger.info(f"[DSL] Definitions found: {list(result.definitions.keys())}")
    logger.info(f"[DSL] Instances found: {list(result.instances.keys())}")
    if result.errors:
        logger.info(f"[DSL] Errors: {result.errors}")
    return list(result.instances.keys())
