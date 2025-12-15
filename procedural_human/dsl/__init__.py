"""
DSL (Domain Specific Language) module for procedural generation.

This module provides a Python-based DSL for defining procedural structures
like fingers, limbs, and other segmented objects using classes with __init__ methods.

The operators and panels are registered via the decorator system when this module
is discovered during addon initialization.

Usage:
    # In a DSL file (e.g., procedural_human/dsl/finger.py):

    class Finger:
        def __init__(self, segment_lengths=[], radius_taper=0.85, curl_axis='Y'):
            Segment = DualRadial(ik=IKLimits(x=(-10, 150)))
            segments = []
            for i in range(len(segment_lengths)):
                seg = Segment(length=segment_lengths[i], radius=radius, profile_lookup=i)
                segments.append(seg)
            Knuckle = Joint(type=QuadRadial, overlap=0.2)
            Extend(segments, axis='Z')
            Join(segments, Knuckle)

    Index = Finger([39.78, 22.38, 15.82])
"""


# Lazy imports - these are only loaded when accessed
def __getattr__(name):
    """Lazy import of DSL components."""
    if name in (
        "DualRadial",
        "QuadRadial",
        "IKLimits",
        "RadialAttachment",
        "Joint",
        "SegmentChain",
        "JoinedStructure",
        "AttachedStructure",
        "normalize",
        "last",
        "Extend",
        "Join",
        "AttachRaycast",
    ):
        from procedural_human.dsl import primitives

        return getattr(primitives, name)

    if name in ("NamingEnvironment", "NamingContext", "build_naming_environment"):
        from procedural_human.dsl import naming

        return getattr(naming, name)

    if name in (
        "DSLExecutor",
        "DSLExecutionResult",
        "DSLInstance",
        "execute_dsl_file",
        "get_dsl_instances",
        "get_dsl_definitions",
    ):
        from procedural_human.dsl import executor

        return getattr(executor, name)

    if name in (
        "DSLGenerator",
        "GeneratedObject",
        "generate_from_dsl_file",
        "regenerate_dsl_object",
    ):
        from procedural_human.dsl import generator

        return getattr(generator, name)

    if name in ("DSLFileWatcher", "start_watching", "stop_watching"):
        from procedural_human.dsl import watcher

        return getattr(watcher, name)

    raise AttributeError(f"module 'procedural_human.dsl' has no attribute '{name}'")


__all__ = [
    # Primitives
    "DualRadial",
    "QuadRadial",
    "IKLimits",
    "RadialAttachment",
    "Joint",
    "SegmentChain",
    "JoinedStructure",
    "AttachedStructure",
    "normalize",
    "last",
    "Extend",
    "Join",
    "AttachRaycast",
    # Naming
    "NamingEnvironment",
    "NamingContext",
    "build_naming_environment",
    # Executor
    "DSLExecutor",
    "DSLExecutionResult",
    "DSLInstance",
    "execute_dsl_file",
    "get_dsl_instances",
    "get_dsl_definitions",
    # Generator
    "DSLGenerator",
    "GeneratedObject",
    "generate_from_dsl_file",
    "regenerate_dsl_object",
    # Watcher
    "DSLFileWatcher",
    "start_watching",
    "stop_watching",
]
