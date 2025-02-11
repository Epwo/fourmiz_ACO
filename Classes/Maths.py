import numpy as np


# memoire contient les villes pas encore visitées, à changer ?
def choix_ville(ville_actuelle, visibilite, pheromone, memoire, alpha, beta):

    probabilites = np.zeros(len(memoire))

    for i, ville in enumerate(memoire):
        probabilites[i] = (pheromone[ville] ** alpha) * (visibilite[ville] ** beta)

    return None


def mise_a_jour_pheromone(matrice_pheromone):

    for i in range(self.nb_lieux):
        for j in range(self.nb_lieux):
            matrice_pheromone[i][j] = self.rho * matrice_pheromone[i][
                j
            ] + self.depose_de_pheromone(self.calcul_distance_route(), Q)

    return matrice_pheromone

    
def depose_de_pheromone(distance_cycle, Q):

    fourmi.memoire

    delta_pheromone = Q / distance_cycle if 

    return None
