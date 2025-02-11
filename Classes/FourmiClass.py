class Fourmi:
    def __init__(self, start_point, nb):
        self.start_point = start_point
        self.current_point = start_point
        self.visited_points = [start_point]
        self.nom = "micheline " + str(nb)

    def get_attributes(self):
        return f"""
        Fourmi {self.nom}
        Start point: {self.start_point.x, self.start_point.y}, Point n°{self.start_point.nom}
        Current point: {self.start_point.x, self.start_point.y}, Point n°{self.start_point.nom}
        Visited points: {[(point.x, point.y,point.nom) for point in self.visited_points]}
        """
