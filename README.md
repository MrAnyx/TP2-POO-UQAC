# Question 4

## Introduction

L'idée de cet exercice est de simuler l'envoie de plusieurs messages à travers un réseau lors d'une catastrophe naturelle. L'objectif est donc de transmettre plusieurs messages entre deux points d'un réseau. Le réseau sera représenté par un graphe de plusieurs noeuds qui représentent respectivement une région et les villes au sein de cette région.

Le noeud d'entré symbolise la ville dans laquelle la catastrophe naturelle a lieu. Le noeud de sortie symbolise la ville dans laquelle se trouve le bureau d'émergence de la région. Il faut donc trouver le chemin le plus court entre les deux villes afin que le bureau d'émergence soit tenu informé de ce qu'il se passe dans la zone dangereuse.

## Implémentation

Cette simulation a été réalisée en Python dans un environnement virtuel. De cette manière, les librairies nécessaires pour lancer le programme ne sont pas installées globalement sur le système mais seront uniquement accessible pour ce projet spécifiquement. La démarche pour installer l'environnement virtuel et exécuter le programme est disponible à la section [Installation et exécution](#installation-et-exécution).

### Création d'un noeud

Les noeuds d'un graphe représentent les points de passage par lesquels un message peut transiter afin que l'information soit transmise entre le noeud de départ et d'arrivé.

Pour que l'on puisse créer le graphe mais également pour pouvoir transiter d'un noeud à un autre, nous allons devoir stocker certains informations :

*   Les coordonnées afin de calculer la distances entre chaque noeud,

*   L'index, afin d'identifier un noeud dans la liste,

*   Le score du noeud courant pour, une fois l'ensemble des messages envoyés, pouvoir déterminer le noeud gagnant,

*   Les voisins du noeud sous la forme d'un dictionnaire avec comme clé, l'index du noeud voisin et en valeur, la distance.

### Création du réseau

La création du réseau a été faite de manière à ce que celui-ci soit aléatoire à chaque exécution du programme. Afin de créer un réseau aléatoire, nous avons décidé de nous baser sur une grille de n×n cases. Ainsi, nous pouvons facilement placer les noeuds du graphe de manière aléatoire sur la grille tout en ayant accès à la distance entre chacun d'entres-eux grâce à la formule de la distance euclidienne.

Ensuite, à chaque création d'un nouveau noeud dans le graphe, nous allons le lier à un certain nombre de noeuds déjà présentent dans le graphe. Ce nombre sera choisi aléatoirement entre 1 et 10.

Au sein de notre réseau, nous devons également sauvegarder certains paramètres afin de pouvoir facilement travailler avec :

*   Le nombre de noeuds à un instant précis,

*   Le nombre de noeuds lors de la création du graphe,

*   La liste des noeuds du graphe,

*   Le seuil de distance à partir duquel un message ne peut plus transiter d'un noeud à un autre,

*   Le noeud de départ,

*   Le noeud d'arrivé,

*   La liste des index des noeuds supprimés,

*   La liste des emplacements des noeuds supprimés dans la liste des noeuds du graphe.

### Logique principale de la simulation

Comme nous avons pu l'évoquer, le but est de transmettre *n* messages entre deux noeuds d'un graphe. Le chemin doit être le plus court possible et la distance entre chaque noeud du chemin doit être inférieure au seuil que nous allons définir.

```python
network = Network(nb_nodes=NB_NODES, distance_threshold=DISTANCE_THRESHOLD)
```

Dans un premier temps, nous commençons pas créer un graphe aléatoire en utilisant la méthode que nous avons décrite précédemment.

```python
shortest_path = None
```

Nous déclarons et initialisons ensuite notre variable `shortest_path` afin de pouvoir conserver le plus cours chemin d'un envoie d'un message à un autre.

Nos variables principales étant définies, nous allons maintenant pouvoir passer au coeur du programme : la logique de sélection du chemin et l'envoi des messages. Toute cette logique est implémentée dans une boucle for qui boucle *k* fois, *k* étant le nombre de message que l'on souhaite envoyer.

Pour rappel, l'idée de cet exercice est de simuler l'envoie de plusieurs message entre deux points pendant une catastrophe naturelle.

```python
if random.randint(1, 2) == 1:
   network.remove_random_node()
```

Nous avons donc décidé de, de manière aléatoire, supprimer un noeud du graphe afin de simuler l'inaccessibilité d'une ville de la région pendant l'envoie des messages. Ainsi, à chaque envoie d'un nouveau message, nous avons une probabilité de 0.5 qu'un noeud soit supprimé du graphe. Le noeud sélectionné et supprimé sera, bien évidemment, différent de ceux de départ et d'arrivé.

Ensuite, dans le cas ou il n'existe aucun chemin optimal entre les deux points, nous essayons d'en déterminer un. Pour ce faire, nous avons utilisé l'algorithme de **Dijkstra**. Cet algorithme est idéal dans ce cas de figure car il permet, précisement, de déterminer le chemin le plus court dans un graphe connexe.

L'algorithme de Dijkstra est relativement simple à comprendre. 

Après avoir déterminé notre chemin, deux cas de figures peuvent se présenter :

*   Après avoir supprimé un certain nombre de noeuds du graphe, il est possible que celui-ci devienne non-connexe et que les noeuds de départ et d'arrivé soient dans deux sous-graphe différent. Dans ce cas, aucun chemin n'existe.

*   L'algorithme de Dijkstra trouve un chemin optimal entre les deux points mais la distance entre deux noeuds est supérieur au seuil de distance. Dans ce cas, le message ne peut pas transiter entre les deux noeuds impliqué et donc, le chemin n'est pas valide.

Ainsi, si aucun chemin n'existe ou s'il n'est pas valide, alors le message est perdu. Il faudra alors attendre le prochain envoie d'un message pour réessayer de trouver un chemin optimal.

### Optimisation

Pour des raisons de performances, nous avons dû optimiser notre algorithme. En effet, plutôt que de re-calculer le chemin optimal à chaque envoie d'un message, nous avons opté pour une approche légerement différente.

En effet, nous re-calculons un nouveau chemin avec l'algorithme de Dijkstra dès que notre chemin n'est plus valide. Autrement-dit, tant que notre chemin existe et est valide, nous le concervons pour envoyer les messages du point de départ au point d'arrivé. Malheureusement, dès lors ou un chemin n'est pas valide, nous perdons un message. En d'autres termes, si nous avons déterminé un chemin valide lors de l'envoie du message 1, puis que, de manière aléatoire, lors de l'envoie du message 23, un noeud de ce chemin n'est plus accessible, alors ce même message 23 sera perdu. Toutefois, la perte de ce message donnera l'information au réseau afin de re-calculer un nouveau chemin lors de l'envoie du prochain message.

Ainsi, tant que les noeuds du chemin déterminé lors de l'envoie du premier message existent, alors nous n'aurons qu'à déterminer un seul chemin optimal ce augmente les performances générales de la simulation.

## Description des classes

### Node.py

### Coordinates.py

### Network.py

## Installation et
