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
        self.fourmis = []
        for i in range(self.nb_fourmis):
            # set the start point
            start_point = self.graph.liste_lieux[i % self.graph.nb_lieux]
            self.fourmis.append(Fourmi(start_point, i))

    def run(self):
        for i in range(self.nb_iter):
            # new fourmis generation
            print(f"--- Iteration {i} ---")
            while len(self.fourmis[0].visited_points) <= self.graph.nb_lieux:
                for fourmi in self.fourmis:
                    # for each fourmi, we calculate the next point
                    self.forward(
                        fourmi,
                        self.graph,
                    )
                # finish the trajet, before updating pheromones
            print(f"finished  G{i} updating pheromones")
            self.update_pheromones(fourmis=self.fourmis)
            self.init_fourmis()

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
            print(f"current point {current_point} ; next point {point.nom}")
            is_unvisited = 1 if point not in visited_points else 0
            print(f"isUnvisited {is_unvisited == 1}")
            eq = (
                -(mat_od[current_point][point.nom] * (1 / 3))
                + (mat_phero[current_point][point.nom] * (1 / 3))
                + (1 / 3) * random.randint(0, max_value)
            ) * is_unvisited
            probas[point.nom] = eq
        print(probas)
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

        # choose the next point
        proba = {k: v for k, v in proba.items() if v != 0}
        # we remove all of the 0 values
        if proba == {}:
            # we are on the last point, lets go back on the first one
            next_point_name = graph.liste_lieux[0].nom
        else:
            next_point_name = max(proba, key=proba.get)
            print(">>", next_point_name)

        next_point = next(
            point for point in graph.liste_lieux if point.nom == next_point_name
        )
        print(
            f"  for {fourmi.nom} Next point: {next_point.nom}, {next_point.x, next_point.y}"
        )
        fourmi.current_point = next_point
        # add the point to the visited points
        fourmi.visited_points.append(next_point)
        print(fourmi.get_attributes())

    def update_pheromones(self, fourmis: list[Fourmi]):
        dist_routes = {}
        for i, fourmi in enumerate(fourmis):
            list_lieux = fourmi.visited_points
            route = Route(list_lieux, self.graph.matrice_cout_od)
            dist_routes[i] = route.calcul_distance_route()
        best_dist = min(dist_routes.values())
        best_route: list[Lieu] = fourmis[
            min(dist_routes, key=dist_routes.get)
        ].visited_points
        print(
            f"best route: {best_route} for fourmi {min(dist_routes, key=dist_routes.get)} for dist {best_dist}"
        )
        # update pheromones
        print(f"olds pheromones: {self.graph.matrice_pheromones}")
        for i in range(len(best_route) - 1):
            x_value = best_route[i].nom
            y_value = best_route[i + 1].nom
            self.graph.matrice_pheromones[x_value][y_value] = (
                (max(max(row) for row in self.graph.matrice_cout_od)) / 2
            ) + self.graph.matrice_pheromones[x_value][y_value]

        print(f"new pheromones: \n {self.graph.matrice_pheromones}")
