from Network import Network
from Node import Node
import random


NB_MESSAGES = 100
NB_NODES = 200

# En moyenne, les noeuds du graph de NB_NODES / 2 unités de distance
# On va volontairement mettre une valeur plus faible pour que certains message ne puissent pas transiter entre deux noeuds
DISTANCE_THRESHOLD = NB_NODES / 3

network = Network(nb_nodes=NB_NODES, distance_threshold=DISTANCE_THRESHOLD)

# shortest_path = network.custom_depth_first_search(network.start)

print(f"Start : {network.start}")
print(f"End : {network.end}")


for i in range(NB_MESSAGES):

    # 1 chance sur 3 pour que un des noeuds du réseaux tombe en panne et ne soit plus accessible
    if random.randint(1, 2) == 1:
        network.remove_random_node()

    # Si aucun chemin n'a été n'existe pour le moment
    shortest_path = network.custom_dijkstra()

    # Si un chemin a été trouvé avec Dijkstra
    if shortest_path:
        # La distance est exprimé en Km
        print(
            f"Path for message {i} : {shortest_path['path']} -> {shortest_path['distance']} Km"
        )

    else:
        print(f"No path found for message {i}")
        # network.plot_print()
        # network.pretty_print()
