from N2G import drawio_diagram

from diomindmap.node import Node


class MindMap:
    def __init__(self, input_text: str, colors: list[str], max_brightness_offset: int) -> None:
        """
        Args:
            input_text: A multi-line string that represents the mind map
            colors: Base colors for children of the diagram root node
            max_brightness_offset: The maximum brightness offset between the base color and leaf nodes
        """

        tree = self._build_tree(input_text.splitlines())

        self.diagram = self._build_diagram(tree, colors=colors, max_brightness_offset=max_brightness_offset)

    @staticmethod
    def _build_tree(lines: list[str]) -> Node:
        """
        Build a tree from a list of lines. Each line is a node in the tree. The level of each node is determined by the
            indentation of the line.
        Args:
            lines: a list of string lines

        Returns: the root node of the tree
        """
        root_node = Node(indented_line='root', node_id='root', root=True)
        root_node.add_children([Node(line, node_id=f'node_{idx}') for idx, line in enumerate(lines) if line.strip()])
        root_node.normalize_levels()

        return root_node

    def _build_diagram(self, root_node: Node, colors: list[str], max_brightness_offset: int) -> drawio_diagram:
        """
        Build a N2G Draw.io diagram from a tree.
        Args:
            root_node: the root node of the tree
        Returns: a N2G Draw.io diagram
        """

        if not root_node.root:
            raise Exception("_build_diagram() requires a root node")

        diagram = drawio_diagram()
        tree_depth = root_node.depth()

        for node in root_node.traverse():
            if not node.root:
                if node.parent == root_node:
                    diagram.add_diagram(node.text)

                node_style = self._get_style(node, tree_depth, colors, max_brightness_offset)
                diagram.add_node(id=node.id, label=node.text, style=node_style)

                if node.level > 1:
                    diagram.add_link(source=node.parent.id, target=node.id)

        diagram.layout(algo="rt")

        return diagram

    def _get_style(self, node: Node, tree_depth: int, colors: list[str], max_brightness_offset: int) -> str:
        """
        Get the style of a node.

        Args:
            node: the Node object

        Returns: a Draw.io compliant style string
        """
        styles = {
            "rounded": "1",
            "whiteSpace": "wrap",
            "html": "1",
            "fillColor": "default",
            "strokeColor": "default",
        }

        # The diagram root node is the default style, but with bold text
        if node.level == 1:
            styles["fontStyle"] = "1"
        # Children of the diagram root node are colored according to their sibling number (each sibling has a different
        # color)
        elif node.level == 2:
            node.data["fillColor"] = styles["fillColor"] = colors[node.sibling_number % len(colors)]
        # All other nodes are progressively lighter than their parent
        else:
            parent_fill_color = node.parent.data["fillColor"]
            brightness_offset = int(max_brightness_offset / tree_depth * node.level)
            node.data["fillColor"] = styles["fillColor"] = self._adjust_brightness(hex_color=parent_fill_color,
                                                                                   brightness_offset=brightness_offset)

        return ";".join([f'{name}={value}' for name, value in styles.items()])

    @staticmethod
    def _adjust_brightness(hex_color: str, brightness_offset=1) -> str:
        """
        Lighten or darken a color in hexadecimal format.
        This method is from: https://chase-seibert.github.io/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html

        Args:
            brightness_offset:

        Returns: a hexadecimal color string
        """
        if len(hex_color) != 7:
            raise Exception("Passed %s into color_variant(), needs to be in #AAAAAA format." % hex_color)

        rgb_hex = [hex_color[x:x + 2] for x in [1, 3, 5]]
        new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
        # make sure new values are between 0 and 255
        new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
        # hex() produces "0x88", we want just "88"
        return "#" + "".join([hex(i)[2:] for i in new_rgb_int])

    def __str__(self):
        return self.diagram.dump_xml()
