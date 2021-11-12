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



## Description des classes

### Node.py

### Coordinates.py

### Network.py

## Installation et exécution
