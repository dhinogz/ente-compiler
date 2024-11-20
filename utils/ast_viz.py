from graphviz import Digraph


def draw_ast(node, graph=None, parent_name=None, counter=[0]):
    """
    Draws the AST recursively using graphviz.

    :param node: The current node (tuple or string).
    :param graph: The graphviz Digraph object.
    :param parent_name: The name of the parent node for connecting edges.
    :param counter: A counter to give unique names to nodes.
    :return: The updated Digraph object.
    """
    if graph is None:
        graph = Digraph(format="png")
        graph.attr(rankdir="TB")  # Top-to-Bottom layout

    # Generate a unique name for the current node
    current_name = f"node_{counter[0]}"
    counter[0] += 1

    if isinstance(node, tuple):  # If the node is a tuple, treat it as a branch
        label = node[0]
        graph.node(current_name, label)

        if parent_name:
            graph.edge(parent_name, current_name)

        # Recursively add children
        for child in node[1:]:
            draw_ast(child, graph, current_name, counter)
    else:  # If the node is a leaf, treat it as a terminal
        graph.node(current_name, str(node))

        if parent_name:
            graph.edge(parent_name, current_name)

    return graph


def draw_ast_terminal(node, prefix="", is_last=True):
    """
    Recursively draws the AST in the terminal as ASCII art.

    :param node: The current node (tuple or string).
    :param prefix: The current prefix for indentation.
    :param is_last: Whether this is the last child of its parent.
    """
    if isinstance(node, tuple):
        # Draw the current node
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{node[0]}")

        # Update prefix for children
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node[1:]):
            draw_ast_terminal(child, new_prefix, i == len(node[1:]) - 1)
    else:
        # Draw the leaf node
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{node}")
