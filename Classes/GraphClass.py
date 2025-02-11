import numpy as np
from Classes.LieuClass import Lieu


class Graph(Lieu):
    def __init__(self, list_lieux):
        self.liste_lieux = []
        for e in list_lieux:
            self.liste_lieux.append(Lieu(e[0], e[1], e[2]))
        self.nb_lieux = len(list_lieux)

    def calcul_matrice_cout_od(self):
        self.matrice_cout_od = np.zeros((self.nb_lieux, self.nb_lieux))
        for i in range(self.nb_lieux):
            for j in range(self.nb_lieux):
                self.matrice_cout_od[i][j] = self.liste_lieux[i].calc_dist_eucl(
                    self.liste_lieux[j]
                )
