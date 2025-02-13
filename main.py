from logic import TSP_ACO
import json
import random

with open("currentHighScore.json", "r+") as f:
    HS = json.load(f)
    alpha = HS["alpha"]
    beta = HS["beta"]
    q = HS["q"]
    rho = HS["rho"]


nb_fourmis = 50
nb_iter = 25

list_lieux = []

file_path = "src/graph_20.csv"

with open(file_path, "r") as f:
    next(f)  # Skip header line
    for i, line in enumerate(f):
        x = float(line.split(",")[0])
        y = float(line.split(",")[-1].strip())
        list_lieux.append([x, y, i])

aco = TSP_ACO(list_lieux, nb_fourmis, nb_iter, alpha, beta, rho, q, file_path)
aco.enable_display = False
aco.init_fourmis()

aco.run()
print("shortest route:")
score = aco.shortest_route["distance"]
print(score)
