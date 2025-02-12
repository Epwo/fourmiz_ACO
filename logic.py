from Classes.LieuClass import Lieu
from Classes.GraphClass import Graph
from Classes.RouteClass import Route
from Classes.FourmiClass import Fourmi

import random


class TSP_ACO(Graph):
    def __init__(self, list_lieux, nb_fourmis, nb_iter, alpha, beta, rho, q):
        self.nb_fourmis = nb_fourmis
        self.nb_iter = nb_iter
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.fourmis: list[Fourmi] = []
        self.graph = Graph(list_lieux)
        self.graph.calcul_matrice_cout_od()
        self.shortest_route = {"route": [], "distance": float("inf")}

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

        remaining_points = [p.nom for p in points if p not in visited_points]
        list_eq1 = []
        for next_point in remaining_points:
            eq1 = ((mat_phero[current_point][next_point]) ** self.alpha) * (
                (1 / mat_od[current_point][next_point]) ** self.beta
            )
            list_eq1.append(eq1)
        probas = {
            remaining_points[i]: list_eq1[i] / sum(list_eq1)
            for i in range(len(remaining_points))
        }
        # we divide by the sum of the list to have a sum of 1 ( and probabilities between 0 & 1)
        print(probas)
        return probas

    def forward(
        self,
        fourmi: Fourmi,
        graph: Graph,
    ):

        # calculate the probability of going to each point
        probas = self.calc_next_point(
            mat_od=graph.matrice_cout_od,
            points=graph.liste_lieux,
            current_point=fourmi.current_point.nom,
            visited_points=fourmi.visited_points,
            mat_phero=graph.matrice_pheromones,
        )

        # choose the next point
        if probas == {}:
            # we are on the last point, lets go back on the first one
            next_point_name = fourmi.visited_points[0].nom
        else:
            choices = list(probas.keys())
            weights = list(probas.values())
            next_point_name = random.choices(choices, weights=weights)[0]

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
        print(f"olds pheromones: {self.graph.matrice_pheromones}")
        for fourmi in fourmis:
            visited_lieux = fourmi.visited_points
            route = Route(visited_lieux, self.graph.matrice_cout_od)
            dist_tot = route.calcul_distance_route()
            if dist_tot < self.shortest_route["distance"]:
                self.shortest_route["route"] = visited_lieux
                self.shortest_route["distance"] = dist_tot
            amount_pheromones = self.q / dist_tot

            for i in range(len(visited_lieux) - 1):
                x_value = visited_lieux[i].nom
                y_value = visited_lieux[i + 1].nom
                self.graph.matrice_pheromones[x_value][y_value] = (
                    self.rho * self.graph.matrice_pheromones[x_value][y_value]
                ) + amount_pheromones

        print(f"new pheromones: \n {self.graph.matrice_pheromones}")
