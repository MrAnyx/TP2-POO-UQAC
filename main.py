# On indique la valeur de m correspondant au nombre de message à envoyer

# from Node import Node
from Network import Network
from Node import Node

network = Network(nb_nodes=20, distance_threshold=35)
network.pretty_print()
network.plot_print()
