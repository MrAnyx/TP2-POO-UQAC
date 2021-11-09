import json
from Node import Node
import random
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Network:
    def __init__(self, nb_nodes: int = 30, distance_threshold: int = 35) -> None:
        self.nb_nodes = nb_nodes
        self.nb_nodes_initial = nb_nodes
        self.nodes = []
        self.distance_threshold = distance_threshold

        start_end = self._generate_start_and_end_nodes()
        self.start = start_end["start"]
        self.end = start_end["end"]

        self.nodes_index_removed = []
        self.nodes_index_in_list_removed = []

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
        B.neighbors[A.index] = distance
        A.neighbors[B.index] = distance

    def _add_neightbors(self, node: Node) -> None:
        # Pour éviter de shuffle la liste de nodes elle-même
        random_nodes_link = random.sample(
            self.nodes, random.randint(1, min(10, len(self.nodes)))
        )
        # On ajoute de manière aléatoire entre 0 et le minimum entre 3 et la taille du graph
        for other_node in random_nodes_link:
            self._add_link_between_nodes(other_node, node)

    def _add_node(self, node: Node) -> None:
        if len(self.nodes) > 0:
            self._add_neightbors(node)

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

    def remove_random_node(self):
        node_to_remove = random.sample(self.nodes, 1)[0]

        if self.nb_nodes == 2:
            return

        while node_to_remove.index == self.start or node_to_remove.index == self.end:
            node_to_remove = random.sample(self.nodes, 1)[0]

        for node in self.nodes:
            node.remove_neighbor(node_to_remove.index)

        self.nodes_index_removed.append(node_to_remove.index)
        self.nodes_index_in_list_removed.append(
            self.get_node_index_in_nodes_list(node_to_remove.index)
        )
        self.nodes.pop(self.get_node_index_in_nodes_list(node_to_remove.index))
        self.nb_nodes -= 1
        print("Node with index :", node_to_remove.index, "has been removed")

    def pretty_print(self):
        result = {"nodes": {}}
        for node in self.nodes:
            result["nodes"][node.index] = {
                "neighbors": node.neighbors,
                "coords": [node.coords.y, node.coords.x],
                "score": node.score,
            }

        result["start"] = self.start
        result["end"] = self.end
        print(json.dumps(result, sort_keys=False, indent=3))

    def plot_print(self, path: list = []):
        mat = []
        pos = []
        labels = {}
        color_map = []

        for node in self.nodes:
            pos.append([node.coords.x, node.coords.y])
            liste_adjacence = np.zeros(self.nb_nodes_initial)
            for neighbor, distance in node.neighbors.items():
                liste_adjacence[neighbor] = 1

            mat.append(liste_adjacence)

        A = np.matrix(mat)

        for k in self.nodes_index_in_list_removed:
            A = np.delete(A, k, 1)

        G = nx.from_numpy_matrix(A)

        for node in G.nodes():
            labels[node] = self.nodes[node].index
            if self.nodes[node].index == self.start:
                color_map.append("#008080")
            elif self.nodes[node].index == self.end:
                color_map.append("#f2353b")
            else:
                if self.nodes[node].index in path:
                    color_map.append("#ed5a2e")
                else:
                    color_map.append("#6a6a77")

        nx.draw_networkx(G, pos, node_color=color_map, with_labels=False)
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black")
        plt.show()

    def get_node_by_index(self, index: int):
        for node in self.nodes:
            if node.index == index:
                return node

    def get_node_index_in_nodes_list(self, node_index: int):
        for i in range(self.nb_nodes):
            if self.nodes[i].index == node_index:
                return i

    def custom_depth_first_search(self, start_index: int, path: list = []):
        start_node = self.get_node_by_index(start_index)
        path = path + [start_index]

        if start_index == self.end:
            return path

        shortest_path = None

        # Pour chaque voisin de la pièce actuelle placée en paramètre
        for neighbors_index, distance in start_node.neighbors.items():

            # On vérifie si la pièce est dans la liste des éléments déjà visités
            if neighbors_index not in path and distance < self.distance_threshold:

                # On appelle de manière récurssive l'algorithme DFS avec un pièce de départ, le premier voisin de la pièce actuelle
                _tmp_path = self.custom_depth_first_search(neighbors_index, path)

                # Si on chemin est retourné par la fonction
                if _tmp_path:

                    # On le compare avec le chemin le plus court précédemment sauvegardé
                    if not shortest_path or len(_tmp_path) < len(shortest_path):

                        # Si le nouveau chemin est plus court, on le conserve et un supprime l'ancien
                        shortest_path = _tmp_path

        # On retourne le chemin le plus court
        return shortest_path

    def custom_dijkstra(self):

        unvisited = {}
        visited = []
        process = {}

        for node in self.nodes:
            unvisited[node.index] = node
            process[node.index] = {"distance": float("inf"), "predecessor": None}

        process[self.start]["distance"] = 0

        while len(unvisited) != 0:
            current_index = self._get_node_by_min_distance(process, visited)

            for neighbor_index, neighbor_distance in unvisited[
                current_index
            ].neighbors.items():
                dist_from_start = process[current_index]["distance"] + neighbor_distance
                if dist_from_start < process[neighbor_index]["distance"]:
                    process[neighbor_index]["distance"] = dist_from_start
                    process[neighbor_index]["predecessor"] = current_index
            visited.append(current_index)
            unvisited.pop(current_index, None)

        path = []
        tmp_index = self.end
        distance = round(process[self.end]["distance"], 2)
        while tmp_index != self.start:
            if process[tmp_index]["predecessor"] != None:
                path.append(tmp_index)
                tmp_index = process[tmp_index]["predecessor"]
            else:
                return None

        # TODO Retourner la distance entre le départ et l'arrivée
        path.append(self.start)
        path.reverse()
        return {"path": path, "distance": distance}

    def _get_node_by_min_distance(self, process: dict, visited: list) -> list:
        # On récupère le noeud avec la distance la plus faible avec le noeud de départ
        _min_distance = float("inf")
        _min_index = None
        for node_index, process in process.items():
            if process["distance"] <= _min_distance and node_index not in visited:
                _min_distance = process["distance"]
                _min_index = node_index

        return _min_index

    def get_average_distance(self):
        total_distance = 0
        nb_nodes = 0

        for node in self.nodes:
            for neighbor, distance in node.neighbors.items():
                total_distance += distance
                nb_nodes += 1

        return total_distance / nb_nodes

    def send_message(self, path: list):
        # On va récupérer l'élément i et i+1 donc ne prend le dernier élément
        for i in range(len(path) - 2):
            current_node = self.get_node_by_index(path[i])
            # next_node = self.get_node_by_index(path[i+1])

            distance = current_node.neighbors[path[i + 1]]
            if distance > self.distance_threshold:
                return False

        return True
