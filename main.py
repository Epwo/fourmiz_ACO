from logic import TSP_ACO

nb_fourmis = 5
nb_iter = 15
# TODO: change values of alpha, beta, q, rho (find optimal values)
alpha = 1
beta = 1
q = 1
rho = 0.5

list_lieux = []

with open("src/graph_20.csv", "r") as f:
    next(f)  # Skip header line
    for i, line in enumerate(f):
        x = float(line.split(",")[0])
        y = float(line.split(",")[-1].strip())
        list_lieux.append([x, y, i])

aco = TSP_ACO(list_lieux, nb_fourmis, nb_iter, alpha, beta, rho, q)
aco.init_fourmis()


aco.run()
print(aco.shortest_route)

# for e in aco.fourmis:
#     print(e.get_attributes())
# print("coo")
