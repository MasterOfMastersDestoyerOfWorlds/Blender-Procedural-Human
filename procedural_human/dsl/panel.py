"""
DSL Browser panel UI.
"""

import os
import bpy
from bpy.types import Panel

from procedural_human.decorators.panel_decorator import procedural_panel


def _get_dsl_instances_cache():
    """Lazy import to avoid circular dependencies."""
    from procedural_human.dsl.operators import _dsl_instances_cache, scan_dsl_files

    if not _dsl_instances_cache:
        scan_dsl_files()
    return _dsl_instances_cache


def _get_watcher():
    """Lazy import to avoid circular dependencies."""
    from procedural_human.dsl.watcher import DSLFileWatcher

    return DSLFileWatcher.get_instance()


@procedural_panel
class DSLBrowserPanel(Panel):
    """DSL Browser panel for creating procedural objects from DSL definitions"""

    bl_label = "DSL Browser"

    def draw(self, context):
        layout = self.layout

        watcher = _get_watcher()
        watched_count = len(watcher.get_watched_files())

        row = layout.row(align=True)
        row.operator(
            "mesh.procedural_dsl_scan_files", text="Refresh", icon="FILE_REFRESH"
        )
        if watched_count > 0:
            row.operator(
                "mesh.procedural_dsl_stop_watcher", text="Stop Watch", icon="PAUSE"
            )
        else:
            row.operator(
                "mesh.procedural_dsl_start_watcher", text="Auto-Update", icon="PLAY"
            )

        layout.separator()

        cache = _get_dsl_instances_cache()
        if cache:
            for file_path, instance_names in cache.items():
                file_name = os.path.basename(file_path).replace(".py", "").title()

                box = layout.box()
                box.label(text=file_name, icon="FILE_SCRIPT")

                if instance_names:
                    for name in instance_names:
                        row = box.row(align=True)
                        row.label(text=name, icon="OBJECT_DATA")

                        op = row.operator(
                            "mesh.procedural_dsl_create_instance",
                            text="Create",
                            icon="ADD",
                        )
                        op.file_path = file_path
                        op.instance_name = name
                else:
                    box.label(text="(No instances found)", icon="ERROR")
        else:
            layout.label(text="No DSL definitions found", icon="INFO")
            layout.label(text="Click Refresh to scan")


@procedural_panel
class DSLObjectInfoPanel(Panel):
    """Panel showing DSL info for selected object"""

    bl_label = "DSL Object Info"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.get("dsl_source_file", "") != ""

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        source_file = obj.get("dsl_source_file", "")
        instance_name = obj.get("dsl_instance_name", "")
        definition_name = obj.get("dsl_definition_name", "")

        box = layout.box()
        box.label(text="DSL Source", icon="FILE_SCRIPT")

        col = box.column(align=True)
        col.label(text=f"Instance: {instance_name}")
        col.label(text=f"Definition: {definition_name}")
        col.label(text=f"File: {os.path.basename(source_file)}")

        row = layout.row(align=True)
        row.operator("mesh.procedural_dsl_refresh_from_source", icon="FILE_REFRESH")
        row.operator("mesh.procedural_dsl_open_source_file", icon="TEXT")

        layout.separator()

        box2 = layout.box()
        box2.label(text="Animation", icon="ARMATURE_DATA")

        col2 = box2.column(align=True)
        col2.operator(
            "mesh.procedural_dsl_realize_and_animate",
            text="Realize & Animate",
            icon="POSE_HLT",
        )

        row2 = box2.row(align=True)
        row2.operator(
            "mesh.procedural_dsl_realize_geometry",
            text="Realize Only",
            icon="MESH_DATA",
        )
        row2.operator(
            "mesh.procedural_dsl_add_armature", text="Add Armature", icon="BONE_DATA"
        )
