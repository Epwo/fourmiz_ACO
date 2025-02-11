class Route:
    def __init__(self, ordre, matrice_od):
        self.ordre = ordre
        self.matrice_od = matrice_od

    def calcul_distance_route(self):

        distance_totale = 0.0

        for i in range(len(self.ordre) - 1):
            lieu_depart = self.ordre[i]
            lieu_arrivee = self.ordre[i + 1]
            distance_totale += self.matrice_od[lieu_depart][lieu_arrivee]

        return distance_totale
