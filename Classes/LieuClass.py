from math import dist


class Lieu:
    def __init__(self, x, y, nom):
        self.x = x
        self.y = y
        self.nom = nom

    def get_coordonnee(self):
        coordonnee = (self.x, self.y)
        return coordonnee

    def calc_dist_eucl(self, coord1, coord2):
        return dist(coord1, coord2)
