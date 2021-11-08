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
        self.neighbors = {}

    def increment_score() -> None:
        self.score += 1

    def remove_neighbor(self, node_index: int) -> None:
        if node_index in self.neighbors:
            self.neighbors.pop(node_index, None)
