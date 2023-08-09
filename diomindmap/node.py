class Node:
    """
    A node in a tree. The level of a node is determined by the indentation of the line that created the node.
    This was inspired by: https://stackoverflow.com/a/53346240
    """

    def __init__(self, indented_line, data: {} = {}, node_id: str | None = None, root: bool = False) -> None:
        """
        Args:
            indented_line: A space or tab indented line (indentation determines the level of the node)
            data: Any arbitrary data to store on the node.
            node_id: A ID to uniquely identify the node.
            root: Whether this node is the root node of the tree.
        """
        self.id = node_id
        self.root = root
        self.parent = None
        self.children = []
        self.text = indented_line.strip()
        self.data = data
        self.level = len(indented_line) - len(indented_line.lstrip())
        self.sibling_number = None

    def add_children(self, nodes) -> None:
        """
        Add one or more children to this node.

        Args:
            nodes: a list of Node objects
        """
        child_level = nodes[0].level
        while nodes:
            node = nodes.pop(0)
            if node.level == child_level:  # add node as a child
                node.parent = self
                node.sibling_number = len(self.children)
                self.children.append(node)
            elif node.level > child_level:  # add nodes as grandchildren of the last child
                nodes.insert(0, node)
                self.children[-1].add_children(nodes)
            elif node.level <= self.level:  # this node is a sibling, no more children
                nodes.insert(0, node)
                return

    def traverse(self) -> None:
        """
        Traverse the tree rooted at this node in depth-first order.
        """
        yield self
        for child in self.children:
            yield from child.traverse()

    def depth(self) -> int:
        """
        Return the depth of the tree rooted at this node.
        """
        if not self.children:
            return 1
        else:
            return max(child.depth() for child in self.children) + 1

    def normalize_levels(self, start_level: int = 0) -> None:
        """
        Normalize the levels of this node and its children so that this node is level X, and its children are level X+1,
            and so on.

        Args:
            start_level: the level of this node after normalization
        """

        self.level = start_level
        for child in self.children:
            child.normalize_levels(start_level + 1)

    #
    def __str__(self):
        """
        Return a string representation of this node. This should be used for debugging only.
        """
        label = ''
        if self.parent:
            label += f'{self.parent.text} -> '

        label += f'({self.text})'
        label += f' -> {len(self.children)} children'

        return label
