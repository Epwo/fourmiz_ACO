import math
import random


class Route:

    def __init__(self, matrice_od, ordre_init=None):

        N = len(matrice_od.shape[0])

        if ordre_init is None:
            ordre_init = list(range(1, N))
            random.shuffle(ordre_init)
            ordre_init.insert(0, 0)
            ordre_init.append(0)

        if ordre_init[-1] != ordre_init[0]:
            raise ValueError(
                "Le point de départ doit être le même que le point d'arrivée"
            )

        self.ordre = ordre_init[:]
        self.matrice_od = matrice_od

    def calcul_distance_route(self):

        distance_totale = 0.0

        for i in range(len(self.ordre) - 1):

            lieu_depart = self.ordre[i]
            lieu_arrivee = self.ordre[i + 1]
            distance_totale += self.matrice_od[lieu_depart][lieu_arrivee]

        return distance_totale
