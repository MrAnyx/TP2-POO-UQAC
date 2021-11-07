class Node:
    def __init__(
        self,
        index: int,
        coords: list,
        score: int = 0,
        neighboors: dict = {},
    ) -> None:
        self.index = index
        self.coords = coords
        self.score = score
        self.neighboors = neighboors
