import sys
import bpy


class FloatCurveClosure:
    """
    A Closure Zone wrapping a Float Curve.
    """

    def __init__(self, in_node, out_node, curve_node, output_socket):
        self.in_node: bpy.types.NodeClosureInput = in_node
        self.out_node: bpy.types.NodeClosureOutput = out_node
        self.curve_node: bpy.types.ShaderNodeFloatCurve = curve_node
        self.output_socket: bpy.types.NodeSocketClosure = output_socket
        self.list: list[bpy.types.Node] = [self.in_node, self.out_node, self.curve_node]

    def nodes(self) -> list[bpy.types.Node]:
        return [self.in_node, self.out_node, self.curve_node]

    def height(self) -> float:
        min_y = sys.float_info.max
        max_y = sys.float_info.min
        for node in self.list:
            if node.location[1] < min_y:
                min_y = node.location[1]
            if node.location[1] + node.height > max_y:
                max_y = node.location[1] + node.height
        return max_y - min_y

    def min_y(self) -> float:
        return min(node.location_absolute[1] - 3 * node.height for node in self.list)


def create_float_curve_closure(nodes, links, label, location) -> FloatCurveClosure:
    """
    Creates a Closure Zone wrapping a Float Curve.
    Returns the Closure Output socket (Yellow Diamond) to be linked.
    """
    x, y = location

    c_in = nodes.new("NodeClosureInput")
    c_in.location = (x, y)
    c_in.label = f"{label} (Start)"

    curve = nodes.new("ShaderNodeFloatCurve")
    curve.location = (c_in.location[0] + c_in.width + 100, y)
    curve.label = label

    c_out = nodes.new("NodeClosureOutput")
    c_out.location = (curve.location[0] + curve.width + 100, y)
    c_out.label = f"{label} (End)"

    c_in.pair_with_output(c_out)
    c_out.input_items.new("FLOAT", "Value")
    c_out.output_items.new("FLOAT", "Value")

    links.new(c_in.outputs["Value"], curve.inputs["Value"])
    links.new(curve.outputs["Value"], c_out.inputs["Value"])
    c_in.update()
    c_out.update()
    curve.update()

    return FloatCurveClosure(c_in, c_out, curve, c_out.outputs["Closure"])


def create_flat_float_curve_closure(nodes, links, label, location, value=0.5) -> FloatCurveClosure:
    """
    Creates a Closure Zone with a flat horizontal Float Curve at a specified value.
    """
    closure = create_float_curve_closure(nodes, links, label, location)
    curve = closure.curve_node.mapping.curves[0]
    for point in curve.points:
        point.location = (point.location[0], value)
    closure.curve_node.mapping.update()
    return closure