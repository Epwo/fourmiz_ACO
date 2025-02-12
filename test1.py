from Classes import AffichageClass
import time


# Définition des matrices de phéromones
matrice_pheromones1 = [
    [0, 0.8, 0, 0, 0],
    [0, 0, 0.4, 0, 0],
    [0, 0, 0, 0.6, 0],
    [0, 0, 0, 0, 0.9],
    [4.0, 0, 0, 0, 0],
]

matrice_pheromones2 = [
    [0, 0.8, 2, 2, 2],
    [2.5, 0, 0.4, 3, 0],
    [3.1, 1.8, 0, 0.6, 0],
    [4.0, 2.2, 2.8, 0, 0.9],
    [4.0, 2.2, 2.8, 3.7, 0],
]
matrice_od = [
    [0, 0.8, 2, 2, 2],
    [2.5, 0, 0.4, 3, 0],
    [3.1, 1.8, 0, 0.6, 0],
    [4.0, 2.2, 2.8, 0, 0.9],
    [4.0, 2.2, 2.8, 3.7, 0],
]
# Création de l'affichage
affi = AffichageClass.Affichage("src/graph_5.csv", matrice_od)
route_main = [0, 1, 2, 3, 4]

affi.update_graph(None, None, None)
time.sleep(1)
affi.update_graph(matrice_pheromones1, [[0, 2, 3], [1, 2, 4], [2, 3, 4]], route_main)
time.sleep(1)
affi.update_graph(matrice_pheromones2, [[0, 2, 3], [1, 2, 4], [2, 3, 4]], route_main)
time.leep(1)

affi.root.mainloop()
