import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import BoolProperty, PointerProperty

from procedural_human.decorators.operator_decorator import procedural_operator
from procedural_human.decorators.panel_decorator import procedural_panel
from procedural_human.utils.node_exporter.exporter import NodeGroupExporter, ExportOptions
from procedural_human.utils.node_exporter.utils import (
    clean_string, to_snake_case, get_next_temp_file_path, get_tmp_base_dir,
)


class NodeExportSettings(PropertyGroup):
    include_locations: BoolProperty(
        name="Locations",
        description="Include node .location = (x, y) in output",
        default=False,
    )
    include_labels: BoolProperty(
        name="Labels",
        description="Include node .label (blank labels always skipped)",
        default=True,
    )
    include_names: BoolProperty(
        name="Names",
        description="Include node .name in output",
        default=False,
    )
    use_helpers: BoolProperty(
        name="Node Helpers",
        description="Substitute node_helpers (math_op, separate_xyz, etc.) where patterns match",
        default=True,
    )
    split_frames: BoolProperty(
        name="Split Frames",
        description="Top-level frames become separate files in a folder",
        default=False,
    )


@procedural_operator
class NODE_OT_export_active_group_to_python(Operator):
    """Export the currently active node group to a Python script"""

    bl_idname = "node.export_active_group_to_python"
    bl_label = "Export Active Node Group to Python"

    def execute(self, context):
        node_group = None
        if context.space_data and context.space_data.type == "NODE_EDITOR":
            node_group = context.space_data.edit_tree
            if not node_group:
                node_group = context.space_data.node_tree
        if not node_group and context.active_object:
            for mod in context.active_object.modifiers:
                if mod.type == "NODES" and mod.node_group:
                    node_group = mod.node_group
                    break

        if not node_group:
            self.report({"ERROR"}, "No active node group found")
            return {"CANCELLED"}

        settings = context.scene.node_export_settings

        options = ExportOptions(
            include_locations=settings.include_locations,
            include_labels=settings.include_labels,
            include_names=settings.include_names,
            use_helpers=settings.use_helpers,
            split_frames=settings.split_frames,
        )

        exporter = NodeGroupExporter(options)
        exporter.process_group(node_group)

        base_dir = get_tmp_base_dir()

        if settings.split_frames:
            group_dir_name = to_snake_case(clean_string(node_group.name))
            group_dir = base_dir / group_dir_name
            group_dir.mkdir(parents=True, exist_ok=True)
            init_path = group_dir / "__init__.py"
            if not init_path.exists():
                init_path.touch()

            files = exporter.get_files(package_name=group_dir_name)
            for filename, code in files.items():
                file_path = group_dir / filename
                with open(file_path, "w") as f:
                    f.write(code)

            self.report({"INFO"}, f"Exported {len(files)} files to {group_dir}")
        else:
            code = exporter.get_full_code()
            file_path = get_next_temp_file_path(str(base_dir))
            with open(file_path, "w") as f:
                f.write(code)
            self.report({"INFO"}, f"Exported to {file_path}")

        return {"FINISHED"}


@procedural_panel
class NODE_PT_node_export(Panel):
    bl_label = "Node Export"
    bl_idname = "PROCEDURAL_PT_node_export"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Procedural"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.node_export_settings

        col = layout.column(align=True)
        col.prop(settings, "use_helpers")
        col.prop(settings, "split_frames")

        col.separator()
        col.prop(settings, "include_labels")
        col.prop(settings, "include_names")
        col.prop(settings, "include_locations")

        layout.separator()
        layout.operator("node.export_active_group_to_python", text="Export Node Group", icon="EXPORT")

        layout.separator()
        layout.operator("curve.export_curve_to_csv")


def register():
    bpy.utils.register_class(NodeExportSettings)
    bpy.types.Scene.node_export_settings = PointerProperty(type=NodeExportSettings)


def unregister():
    del bpy.types.Scene.node_export_settings
    bpy.utils.unregister_class(NodeExportSettings)
