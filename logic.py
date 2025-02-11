from Classes.LieuClass import Lieu
from Classes.GraphClass import Graph
from Classes.RouteClass import Route
from Classes.FourmiClass import Fourmi

import random


class TSP_ACO(Graph):
    def __init__(self, list_lieux, nb_fourmis, nb_iter, alpha, beta, rho, q, q0):
        self.nb_fourmis = nb_fourmis
        self.nb_iter = nb_iter
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.q0 = q0
        self.fourmis: list[Fourmi] = []
        self.graph = Graph(list_lieux)
        self.graph.calcul_matrice_cout_od()

    def init_fourmis(self):
        for i in range(self.nb_fourmis):
            # set the start point
            start_point = self.graph.liste_lieux[i % self.graph.nb_lieux]
            self.fourmis.append(Fourmi(start_point, i))

    def wip(self):
        for i in range(self.nb_iter):
            # new fourmis generation
            for fourmi in self.fourmis:
                # for each fourmi, we calculate the next point
                self.forward(
                    fourmi,
                    self.graph,
                )
            # self.update_pheromones()

    def calc_next_point(
        self,
        mat_od,
        points: list[Lieu],
        current_point,
        visited_points,
        mat_phero,
    ):
        probas = {}

        for point in points:
            max_value = int(max(max(row) for row in mat_od))
            is_unvisited = 1 if point not in visited_points else 0
            eq = (
                -(mat_od[current_point][point.nom] * (1 / 3))
                + (mat_phero[current_point][point.nom] * (1 / 3))
                + (1 / 3) * random.randint(0, max_value)
            ) * is_unvisited
            probas[point.nom] = eq
        return probas

    def forward(
        self,
        fourmi: Fourmi,
        graph: Graph,
    ):
        # calculate the probability of going to each point
        proba = self.calc_next_point(
            mat_od=graph.matrice_cout_od,
            points=graph.liste_lieux,
            current_point=fourmi.current_point.nom,
            visited_points=fourmi.visited_points,
            mat_phero=graph.matrice_pheromones,
        )

        print(proba)
        # choose the next point
        next_point_name = max(proba, key=proba.get)
        next_point = next(
            point for point in graph.liste_lieux if point.nom == next_point_name
        )
        print(
            f"Next point: {next_point.nom}, {next_point.x, next_point.y} for dist {proba[next_point_name]}"
        )
        # next_point = fourmi.choose_next_point(proba, q, q0)
        # # update the current point
        # self.current_point = next_point
        # # add the point to the visited points
        # fourmi.visited_points.append(next_point)
