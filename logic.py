from Classes.LieuClass import Lieu
from Classes.GraphClass import Graph
from Classes.RouteClass import Route
from Classes.FourmiClass import Fourmi


class TSP_ACO(Graph):
    def __init__(self, list_lieux, nb_fourmis, nb_iter, alpha, beta, rho, q, q0):
        self.nb_fourmis = nb_fourmis
        self.nb_iter = nb_iter
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.q0 = q0
        self.fourmis = []
        self.graph = Graph(list_lieux)
        self.graph.calcul_matrice_cout_od()

    def init_fourmis(self):
        for i in range(self.nb_fourmis):
            # set the start point
            start_point = self.graph.liste_lieux[i % self.graph.nb_lieux]
            self.fourmis.append(Fourmi(start_point, i))

    def forward(self):
        for i in range(self.nb_iter):
            for fourmi in self.fourmis:
                fourmi.forward(self.graph, self.alpha, self.beta, self.q, self.q0)
            self.update_pheromones()
