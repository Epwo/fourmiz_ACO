from ..Classes.GraphClass import Graph
from ..Classes.LieuClass import Lieu

lieu1 = Lieu(0, 0, "lieu1")
lieu2 = Lieu(1, 1, "lieu2")
lieu3 = Lieu(2, 2, "lieu3")
lieu4 = Lieu(3, 3, "lieu4")

print(lieu1.calc_dist_eucl(lieu2))

graph = Graph([lieu1, lieu2, lieu3, lieu4])
graph.calcul_matrice_cout_od()
print(graph.matrice_cout_od)
