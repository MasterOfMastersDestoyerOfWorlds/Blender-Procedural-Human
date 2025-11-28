"""
DSL Executor for procedural generation.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from procedural_human.dsl.primitives import (
    DualRadial, QuadRadial, IKLimits, RadialAttachment, Joint,
    SegmentChain, JoinedStructure, AttachedStructure,
    normalize, last, Extend, Join, AttachRaycast,
)
from procedural_human.dsl.naming import NamingEnvironment, build_naming_environment
from procedural_human.decorators.curve_preset_decorator import resolve_profile_chain


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
        errors = []
        
        try:
            self.naming_env = build_naming_environment(file_path)
        except Exception as e:
            errors.append(f"Failed to parse DSL file: {e}")
            return DSLExecutionResult(
                file_path=file_path,
                naming_env=NamingEnvironment(),
                definitions={},
                instances={},
                errors=errors,
            )
        
        self.current_file = file_path
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
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
            exec(compile(source_code, file_path, 'exec'), namespace)
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
        """Create the sandboxed namespace with DSL primitives."""
        return {
            'DualRadial': DualRadial,
            'QuadRadial': QuadRadial,
            'IKLimits': IKLimits,
            'RadialAttachment': RadialAttachment,
            'Joint': Joint,
            'normalize': normalize,
            'last': last,
            'Extend': Extend,
            'Join': Join,
            'AttachRaycast': AttachRaycast,
            'range': range,
            'len': len,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'print': print,
            '__naming_env__': self.naming_env,
        }
    
    def _extract_results(self, namespace: Dict[str, Any]) -> None:
        """Extract definitions and instances from executed namespace."""
        self._definitions.clear()
        self._instances.clear()
        
        dsl_primitives = {'DualRadial', 'QuadRadial', 'IKLimits', 'RadialAttachment', 'Joint'}
        
        for name, value in namespace.items():
            if name.startswith('_'):
                continue
            if isinstance(value, type) and name not in dsl_primitives:
                self._definitions[name] = value
            elif not callable(value) and name not in dsl_primitives:
                if hasattr(value, '__class__') and value.__class__.__name__ in self._definitions:
                    self._instances[name] = value


def execute_dsl_file(file_path: str) -> DSLExecutionResult:
    """Execute a DSL file and return the results."""
    executor = DSLExecutor()
    return executor.execute_file(file_path)


def get_dsl_instances(file_path: str) -> List[str]:
    """Get list of instance names from a DSL file."""
    result = execute_dsl_file(file_path)
    return list(result.instances.keys())


def get_dsl_definitions(file_path: str) -> List[str]:
    """Get list of definition class names from a DSL file."""
    result = execute_dsl_file(file_path)
    return list(result.definitions.keys())

