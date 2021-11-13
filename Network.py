import json
from Node import Node
import random
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Network:
    """
    La classe réseau, comme nous avons pu le voir dans le rapport, représente la classe qui gère la simulation.
    On y retrouve les méthodes permettant de créer le graphe aléatoire, déterminer le chemin ou envoyer les messages
    """

    def __init__(self, nb_nodes: int = 20, distance_threshold: int = 10) -> None:
        """
        Pour créer un objet Network, il est recommendé de renseigner 2 paramètres :
            - le nombre de noeuds
            - le seuil de distance

        Néanmoins, ces deux paramètres ont une valeur par défaut donc, si l'on ne renseigne pas de valeur pour ces deux paramètres,
        celles-ci auront les valeurs suivantes : 20 et 10.

        Ce constructeur permet également de, après avoir initialisé l'ensemble de nos attributs, générer un graphe aléatoire.
        """
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
        """
        Cette méthode permet de générer de manière aléatoire un noeud de départ et d'arrivé.
        Les valeurs retournées représentes les indexes des noeuds de départ et d'arrivé.
        """
        start = random.randint(0, self.nb_nodes - 1)
        end = random.randint(0, self.nb_nodes - 1)

        while end == start:
            end = random.randint(0, self.nb_nodes - 1)

        return {"start": start, "end": end}

    def _generate_random_coords(self) -> list:
        """
        Cette méthode permet de générer des coordonnées aléatoire dans la grille n*n
        avec n qui correspond au nombre de noeuds que l'on souhaite.
        """
        return [
            random.randint(0, self.nb_nodes - 1),
            random.randint(0, self.nb_nodes - 1),
        ]

    def _calculate_distance(self, A: Node, B: Node) -> float:
        """
        Cette méthode permet de calculer la distance euclidienne entre deux points de la grille.
        En d'autres termes, on calcule la distance entre deux noeuds du graphe.
        """
        return math.sqrt(
            (A.coords.x - B.coords.x) ** 2 + (A.coords.y - B.coords.y) ** 2
        )

    def _add_link_between_nodes(self, A: Node, B: Node) -> None:
        """
        Cette méthode permet de lier deux noeuds entre-eux. Le noeud A va devenir le voisin du noeud B et inversement.
        Nous allons également calculer et stocker la distance entre ces deux noeuds.
        """
        distance = self._calculate_distance(A, B)
        B.neighbors[A.index] = distance
        A.neighbors[B.index] = distance

    def _add_neightbors(self, node: Node) -> None:
        """
        Cette méthode permet d'ajouter un nombre aléatoire de voisins à un noeud placé en paramètre.
        """
        # Pour éviter de shuffle la liste de nodes elle-même
        # Nous prenons un échantillon de n noeuds avec n, une valeur aléatoire entre 1 et le minimum entre 10 et la taille du graphe
        random_nodes_link = random.sample(
            self.nodes, random.randint(1, min(10, len(self.nodes)))
        )
        # Pour chaque voisin que nous avons déterminés, nous le lions au noeud courant
        for other_node in random_nodes_link:
            self._add_link_between_nodes(other_node, node)

    def _add_node(self, node: Node) -> None:
        """
        Cette méthode permet d'ajouter un noeud dans la liste des noeuds.
        """
        # Si la liste n'est pas vide, c'est-à-dire que le graphe existe déjà, alors nous ajoutons un certain nombre de voisins au noeud courant
        if len(self.nodes) > 0:
            self._add_neightbors(node)

        # Ensuite nous ajoutons le noeud dans la liste des noeuds du graphe
        self.nodes.append(node)

    def _generate_random_graph(self) -> None:
        """
        Cette méthode permet de générer un graphe aléatoire avec la méthode que nous avons détaillée dans le rapport
        """
        assigned = []

        for i in range(self.nb_nodes):
            [y, x] = self._generate_random_coords()

            # Tant que les coordonnées existent déjà
            while [y, x] in assigned:
                # On en génère de nouveaux
                [y, x] = self._generate_random_coords()

            assigned.append([y, x])
            node = Node(index=i, coords=[y, x])
            self._add_node(node)

    def remove_random_node(self):
        """
        Cette méthode permet de supprimer de manière aléatoire un noeud du graphe.
        Cela permet de simuler l'inaccessibilité d'un noeud. Il n'est donc plus accessible lorsque le message essaye de transiter.
        """
        # S'il n'y a que 2 noeuds dans le graphe (noeuds de départ et d'arrivé)
        if self.nb_nodes == 2:
            # Alors on ne supprime aucun noeud
            return

        # On sélectionne un noeud du graphe
        node_to_remove = random.sample(self.nodes, 1)[0]

        # Si l'index du noeud à supprimer correspond à celui du noeud de départ ou d'arrivé
        while node_to_remove.index == self.start or node_to_remove.index == self.end:
            # On en génère un nouveau
            node_to_remove = random.sample(self.nodes, 1)[0]

        # On supprime le noeud dans la liste des voisins de chaque noeud du graphe
        for node in self.nodes:
            node.remove_neighbor(node_to_remove.index)

        self.nodes_index_removed.append(node_to_remove.index)
        self.nodes_index_in_list_removed.append(
            self._get_node_index_in_nodes_list(node_to_remove.index)
        )
        self.nodes.pop(self._get_node_index_in_nodes_list(node_to_remove.index))
        self.nb_nodes -= 1
        print(f"Node with index : {node_to_remove.index} has been removed")

    def pretty_print(self):
        """
        Cette méthode permet d'afficher des informations sur le graphe et les noeuds qui le constitu à un instant donné
        """
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
        """
        Cette méthode permet d'afficher dynamiquement le graphe généré.
        Pour ce faire, nous générons la matrice d'adjacence de notre graphe puis nous l'affichons grâce aux librairies networkx et matplotlib.
        """
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

    def _get_node_by_index(self, index: int):
        """
        Cette méthode permet de récupérer un noeud du graphe en fonction de son index
        """
        for node in self.nodes:
            if node.index == index:
                return node

        return None

    def _get_node_index_in_nodes_list(self, node_index: int):
        """
        Cette méthode permet de récupérer la position du noeuds en fonction de son index dans la liste des noeuds du graphe.
        """
        for i in range(self.nb_nodes):
            if self.nodes[i].index == node_index:
                return i

        return None

    def custom_depth_first_search(self, start_index: int, path: list = []):
        """
        Cette méthode correspond à la prémière implémentation de l'algorithme permettant de déterminer le chemin le plus court.
        En effet, avant d'implémenter l'algorithme de Dijkstra, nous nous sommes penché sur un algorithme de recherche classique : DFS
        """
        start_node = self._get_node_by_index(start_index)
        path = path + [start_index]

        if start_index == self.end:
            return path

        shortest_path = None

        # Pour chaque voisin du noeud actuel placé en paramètre
        for neighbors_index, distance in start_node.neighbors.items():

            # On vérifie si le noeud est dans la liste des éléments déjà visités et que la distance est inférieure au seuil
            if neighbors_index not in path and distance < self.distance_threshold:

                # On appelle de manière récurssive l'algorithme DFS avec en paramètre, un noeud de départ et la liste des index déjà parcourus
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
        """
        Cette méthode est une implémentation de l'algorithme Dijkstra.
        Cet algorithme permet de déterminer le chemin le plus court entre deux noeuds d'un graphe.
        """

        unvisited = {}
        visited = []
        process = {}

        # On crée les variables process et unvisited que l'on utilisera plus tard
        for node in self.nodes:
            unvisited[node.index] = node

            # La variable process est un dictionnaire avec en clé, l'index du noeud courant et en valeur,
            # un objet contenant la distance entre le noeud courant et le noeud de départ et son prédécésseur
            # par lequel nous sommes passés pour atteindre ce noeud en passant par le chemin le plus court
            process[node.index] = {"distance": float("inf"), "predecessor": None}

        # On initialise la distance entre le noeud de départ et le noeud de départ à 0
        process[self.start]["distance"] = 0

        # Tant qu'il existe un noeud dans la liste des noeuds non-visités
        while len(unvisited) != 0:

            # On récupère le noeuds avec la plus petite distance entre celui-ci et le noeud de départ
            current_index = self._get_node_by_min_distance(process, visited)

            # Pour chaque voisin de ce noeud
            for neighbor_index, neighbor_distance in unvisited[
                current_index
            ].neighbors.items():
                # On calcule la distance entre le voisin et le point de départ
                dist_from_start = process[current_index]["distance"] + neighbor_distance

                # Si la distance calculée est inférieure à la distance précédente
                if dist_from_start < process[neighbor_index]["distance"]:
                    # On remplace les valeurs
                    process[neighbor_index]["distance"] = dist_from_start
                    process[neighbor_index]["predecessor"] = current_index
            visited.append(current_index)
            unvisited.pop(current_index, None)

        # On parcourt le chemin en partant du noeud d'arrivé afin de remonter le chemin et ainsi déterminer le chemin le plus court
        path = []
        tmp_index = self.end
        distance = round(process[self.end]["distance"], 2)
        while tmp_index != self.start:
            if process[tmp_index]["predecessor"] != None:
                path.append(tmp_index)
                tmp_index = process[tmp_index]["predecessor"]
            else:
                return None

        path.append(self.start)

        # Puisque l'on parcourt le chemin dans le sens inverse, il faut retourner le chemin
        path.reverse()

        # On retourner le chemin et la longueur de ce chemin
        return {"path": path, "distance": distance}

    def _get_node_by_min_distance(self, process: dict, visited: list) -> list:
        """
        Cette méthode permet de retourner l'index du noeud ayant la plus petite distance avec le noeud de départ
        Nous déterminons ce noeud à l'aide de la variable process qui a été créée et modifiée dans la méthode précédente : custom_dijkstra
        """
        # On récupère le noeud avec la distance la plus faible avec le noeud de départ
        _min_distance = float("inf")
        _min_index = None
        for node_index, process in process.items():
            if process["distance"] <= _min_distance and node_index not in visited:
                _min_distance = process["distance"]
                _min_index = node_index

        return _min_index

    def get_average_distance(self):
        """
        Cette méthode permet de calculer la distance moyenne entre chaque noeud du graphe
        Elle a été utilisée afin d'avoir un ordre d'idée du seuil de distance à renseigner en fonction du nombre de noeuds
        """
        total_distance = 0
        nb_nodes = 0

        for node in self.nodes:
            for neighbor, distance in node.neighbors.items():
                total_distance += distance
                nb_nodes += 1

        return total_distance / nb_nodes

    def is_path_reachable(self, path: dict):
        """
        Cette méthode permet de déterminer si un chemin est valide ou non.
        """

        # Si aucun chemin n'a été trouvé
        if not path:
            return {"valid": False, "reason": "path_missing"}

        # On va récupérer l'élément i et i+1 donc ne prend le dernier élément
        for i in range(len(path["path"]) - 2):
            current_node = self._get_node_by_index(path["path"][i])
            # Si le prochain noeud du chemin existe dans la liste des voisins du noeud courant
            if current_node and path["path"][i + 1] in current_node.neighbors:
                distance = current_node.neighbors[path["path"][i + 1]]

                # Si la distance entre le noeud courant et le prochain élément du chemin est inférieure au seuil de distance
                if distance > self.distance_threshold:
                    return {"valid": False, "reason": "distance"}
            else:
                return {"valid": False, "reason": "missing"}

        return {"valid": True, "reason": "ok"}

    def send_message(self, path: dict, message_num: int):
        """
        Cette méthode permet de simuler l'envoie d'un message à travers le réseau.
        A chaque envoie d'un message, les noeuds contenus dans le chemin le plus court verront leur score incrémenté
        """
        for node_index in path["path"]:
            node = self._get_node_by_index(node_index)
            node.score += 1

        # La distance est exprimé en Km
        print(
            f"Path for message {message_num} : {path['path']} -> {path['distance']} Km"
        )

    def display_error_message(self, path_validity: dict, message_num: int):
        """
        Cette méthode permet d'afficher un message en fonction de la raison de l'invalidité déterminée avec la méthode is_path_reachable
        """
        if path_validity["reason"] == "distance":
            print(f"Error on messgae {message_num} : Distance between 2 nodes too high")
        elif path_validity["reason"] == "missing":
            print(f"Error on message {message_num} : Unknown node")
        elif path_validity["reason"] == "path_missing":
            print(f"Error on message {message_num} : No path found")

    def get_nodes_with_highest_score(self):
        """
        Cette méthode permet de détermier le ou les noeuds ayant le score le plus élevé
        """
        # On commence par déterminer le score le plus élevé
        _max_index = None
        _max_score = 0
        for i in range(self.nb_nodes):
            if self.nodes[i].score > _max_score:
                _max_score = self.nodes[i].score
                _max_index = i

        # Puis on parcourt la liste des noeuds du graphe afin de retourner l'ensemble des noeuds ayant le score le plus élevé
        highest_score_nodes = []
        for node in self.nodes:
            if node.score == _max_score:
                highest_score_nodes.append(node.index)

        return {"nodes": highest_score_nodes, "score": _max_score}
