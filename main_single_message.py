from Network import Network
from Node import Node
import random

NB_NODES = 10

# En moyenne, les noeuds du graph sont espacés de NB_NODES / 2 unités de distance
# On va volontairement mettre une valeur plus faible pour que certains message ne puissent pas transiter entre deux noeuds
DISTANCE_THRESHOLD = NB_NODES / 2.2

network = Network(nb_nodes=NB_NODES, distance_threshold=DISTANCE_THRESHOLD)

network.pretty_print()

shortest_path = network.custom_dijkstra()
print(shortest_path)
network.plot_print(shortest_path["path"])
