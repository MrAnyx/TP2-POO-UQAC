from Network import Network
from Node import Node
import random


NB_MESSAGES = 20
NB_NODES = 6

# En moyenne, les noeuds du graph sont espacés de NB_NODES / 2 unités de distance
# On va volontairement mettre une valeur plus faible pour que certains message ne puissent pas transiter entre deux noeuds
DISTANCE_THRESHOLD = NB_NODES / 2.2

network = Network(nb_nodes=NB_NODES, distance_threshold=DISTANCE_THRESHOLD)

shortest_path = None

for i in range(NB_MESSAGES):

    """
    Pseudocode

    Si aucun chemin n'existe
        On trouve le chemin le plus court
    Si un chemin existe
        Si il est atteignable
            On envoie le message
            On affiche les infos du chemin et de la distance
        Si il n'est pas atteignable
            On set le chemin à None
            On affiche un message disant que le message n'est pas atteignable
            On affiche un message pour dire que le message a été perdu mais à donné l'information que le chemin n'était pas accessible
    """

    # 1 chance sur 2 pour que un des noeuds du réseaux tombe en panne et ne soit plus accessible
    if random.randint(1, 2) == 1:
        network.remove_random_node()

    # Si aucun chemin n'existe
    if not shortest_path:
        shortest_path = network.custom_dijkstra()

    # On vérifie la validité du chemin
    path_validity = network.is_path_reachable(path=shortest_path)

    # Si il est valide
    if path_validity["valid"]:
        # On envoie le message
        network.send_message(path=shortest_path, message_num=i)

    # S'il n'est pas valide
    else:
        shortest_path = None
        network.display_error_message(path_validity=path_validity, message_num=i)

# On affiche le ou les noeuds ayant le score le plus élevé
print(network.get_nodes_with_highest_score())
