import json
from Node import Node
import random
import math


class Network:
    def __init__(self, nb_nodes: int = 30, distance_threshold: int = 35) -> None:
        self.nb_nodes = nb_nodes
        self.nodes = []
        self.distance_threshold = distance_threshold

        start_end = self._generate_start_and_end_nodes()
        self.start = start_end["start"]
        self.end = start_end["end"]

        self._generate_random_graph()

    def _generate_start_and_end_nodes(self):
        start = random.randint(0, self.nb_nodes - 1)
        end = random.randint(0, self.nb_nodes - 1)

        while end == start:
            end = random.randint(0, self.nb_nodes - 1)

        return {"start": start, "end": end}

    def _generate_random_coords(self) -> list:
        return [
            random.randint(0, self.nb_nodes - 1),
            random.randint(0, self.nb_nodes - 1),
        ]

    def _calculate_distance(self, A: Node, B: Node) -> float:
        return math.sqrt(
            (A.coords.x - B.coords.x) ** 2 + (A.coords.y - B.coords.y) ** 2
        )

    def _add_link_between_nodes(self, A: Node, B: Node) -> None:
        distance = self._calculate_distance(A, B)
        B.neighboors[A.index] = distance
        A.neighboors[B.index] = distance

    def _add_neightboors(self, node: Node) -> None:
        if len(self.nodes) == 1:
            # Dans tous les cas, on lie la nouvelle node à la précédente
            prev = self.nodes[0]  # Node précédente
            self._add_link_between_nodes(prev, node)

        else:
            # Pour éviter de shuffle la liste de nodes elle-même
            random_nodes_link = self.nodes
            random.shuffle(random_nodes_link)
            random_nodes_link = random_nodes_link[
                0 : random.randint(1, min(3, len(random_nodes_link) - 1))
            ]
            # On ajoute de manière aléatoire entre 0 et le minimum entre 3 et la taille du graph
            for other_node in random_nodes_link:
                self._add_link_between_nodes(other_node, node)

    def _add_node(self, node: Node) -> None:
        if len(self.nodes) == 0:
            self.nodes.append(node)

        else:
            self._add_neightboors(node)
            self.nodes.append(node)

    def _generate_random_graph(self) -> None:
        assigned = []

        for i in range(self.nb_nodes):
            [y, x] = self._generate_random_coords()

            while [y, x] in assigned:
                [y, x] = self._generate_random_coords()

            assigned.append([y, x])
            node = Node(index=i, coords=[y, x])
            self._add_node(node)

    def pretty_print(self):
        result = {"nodes": {}}
        for node in self.nodes:
            result["nodes"][node.index] = node.neighboors

        result["start"] = self.start
        result["end"] = self.end
        print(json.dumps(result, sort_keys=False, indent=3))
