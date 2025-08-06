class LayoutNode:
    parent: "LayoutNode"

    def find_all(self) -> list["LayoutNode"]:
        raise NotImplementedError()

    def find(self) -> "LayoutNode":
        raise NotImplementedError()

    def next_sibling(self) -> "LayoutNode":
        raise NotImplementedError()

    def prev_sibling(self) -> "LayoutNode":
        raise NotImplementedError()

    @property
    def children(self) -> list["LayoutNode"]:
        raise NotImplementedError()
