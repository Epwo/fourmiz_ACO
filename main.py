from logic import TSP_ACO

nb_fourmis = 5
nb_iter = 15
# TODO: change values of alpha, beta, q, rho (find optimal values)
alpha = 1.67
beta = 6.34
q = 9.8
rho = 0.43

list_lieux = []

file_path = "src/graph_20.csv"

with open(file_path, "r") as f:
    next(f)  # Skip header line
    for i, line in enumerate(f):
        x = float(line.split(",")[0])
        y = float(line.split(",")[-1].strip())
        list_lieux.append([x, y, i])

aco = TSP_ACO(list_lieux, nb_fourmis, nb_iter, alpha, beta, rho, q, file_path)
aco.init_fourmis()


aco.run()
print(aco.shortest_route)
