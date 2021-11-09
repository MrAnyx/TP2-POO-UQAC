# On indique la valeur de m correspondant au nombre de message à envoyer

# from Node import Node
from Network import Network
from Node import Node

NB_MESSAGES = 10
NB_NODES = 10

network = Network(nb_nodes=NB_NODES, distance_threshold=20)
# network.remove_random_node()
# network.pretty_print()

best_path = network.custom_depth_first_search(network.start)
print("Best path = ", best_path)

# network.pretty_print()
network.plot_print(best_path)
