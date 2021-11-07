import json
from Node import Node
import random


class Network:
    def __init__(self, start_node: int, end_node: int, nb_nodes: int = 30) -> None:
        self.nb_nodes = nb_nodes
        self.nodes = []
        self.start = start_node
        self.end = end_node
        self.generate_random_graph()

    def _generate_random_coords(self) -> list:
        return [
            random.randint(0, self.nb_nodes - 1),
            random.randint(0, self.nb_nodes - 1),
        ]

    def _add_random_neightboors(self, node: Node):
        if len(self.nodes) == 1:
            self._add_random_neightboors(node)
            # TODO Pas terminé

    def _add_node(self, node: Node):
        if len(self.nodes) == 0:
            self.nodes.append(node)

        elif len(self.nodes) == 1:
            self._add_random_neightboors(node)
            self.nodes.append(node)

        else:
            for i in range(random.randint(0, min(2, len(self.nodes)))):
                self._add_random_neightboors(node)
                self.nodes.append(node)
                # TODO pas terminé

    def generate_random_graph() -> None:
        assigned = []

        for i in range(self.nb_nodes):
            [y, x] = self._generate_random_coords()

            while [y, x] in assigned:
                [y, x] = self._generate_random_coords()

            node = Node(index=i, coords=[y, x], score=0)

            self._add_node(node)
            # TODO Pas terminé

        self.nodes = []

    def pretty_print():
        print(json.dumps(self.graph, sort_keys=False, indent=3))
