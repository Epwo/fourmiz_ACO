from math import dist


class Lieu:
    def __init__(self, x, y, nom):
        self.x = x
        self.y = y
        self.nom = nom

    def get_coords(self):
        coords = (self.x, self.y)
        return coords

    def calc_dist_eucl(self, LieuDest):
        return dist(self.get_coords(), LieuDest.get_coords())
