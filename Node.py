from Coordinates import Coordinates


class Node:
    def __init__(
        self,
        index: int,
        coords: list,
    ) -> None:
        [y, x] = coords
        self.index = index
        self.coords = Coordinates(x, y)
        self.score = 0
        self.neighboors = {}

    def increment_score() -> None:
        self.score += 1

    def remove_neighboor(self, node: Node) -> None:
        if node.index in self.neighboors:
            self.neighboors.pop(node.index, None)
