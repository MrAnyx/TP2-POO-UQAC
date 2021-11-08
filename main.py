# On indique la valeur de m correspondant au nombre de message à envoyer

# from Node import Node
from Network import Network
from Node import Node

NB_MESSAGES = 10
NB_NODES = 30

network = Network(nb_nodes=NB_NODES, distance_threshold=50)
# network.pretty_print()
# network.remove_random_node()
network.pretty_print()

# network.plot_print()
