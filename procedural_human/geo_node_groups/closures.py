def create_float_curve_closure(nodes, links, label, location):
    """
    Creates a Closure Zone wrapping a Float Curve.
    Returns the Closure Output socket (Yellow Diamond) to be linked.
    """
    x, y = location

    c_in = nodes.new("NodeClosureInput")
    c_in.location = (x, y)
    c_in.label = f"{label} (Start)"

    c_out = nodes.new("NodeClosureOutput")
    c_out.location = (x + 400, y)
    c_out.label = f"{label} (End)"

    c_in.pair_with_output(c_out)

    c_out.input_items.new("FLOAT", "Value")

    c_out.output_items.new("FLOAT", "Value")

    curve = nodes.new("ShaderNodeFloatCurve")
    curve.location = (x + 200, y)
    curve.label = label

    links.new(c_in.outputs["Value"], curve.inputs["Value"])
    links.new(curve.outputs["Value"], c_out.inputs["Value"])

    return c_out.outputs["Closure"]
