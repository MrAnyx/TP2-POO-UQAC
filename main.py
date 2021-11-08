# On indique la valeur de m correspondant au nombre de message à envoyer

# from Node import Node
from Network import Network
from Node import Node

NB_MESSAGES = 10
NB_NODES = 10

network = Network(nb_nodes=NB_NODES, distance_threshold=20)
# network.pretty_print()

# print(f"network length : {len(network.nodes)}")
network.remove_random_node()
network.remove_random_node()
network.remove_random_node()
network.remove_random_node()
# network.remove_random_node()
# print(f"network length : {len(network.nodes)}")

# network.pretty_print()

# best_path = network.custom_depth_first_search(network.start)
# print("Best path = ", best_path)
# print("Starting at index : ", network.start)
# print("Ending at index : ", network.end)


# network.pretty_print()
# network.plot_print()
