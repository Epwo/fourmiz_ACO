from math import dist

class Lieu:
    def __init__(self, x, y, nom):
        self.x = x
        self.y = y
        self.nom = nom

    def getcoordonnee(self):
        coordonnee = (self.x, self.y)
        return coordonnee

    def euclidienne(self, coord_other):
        return dist(self.getcoordonnee(), coord_other)