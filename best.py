from logic import TSP_ACO
import json
import random

iters = 0

alpha = 5
beta = 10
q = 5
rho = 0.5

while iters < 10000:
    print(">> Iteration", iters)
    alpha = random.uniform(0, 10)
    beta = random.uniform(0, 10)
    q = random.uniform(0, 10)
    rho = random.uniform(0, 1)

    nb_fourmis = 5
    nb_iter = 15
    # TODO: change values of alpha, beta, q, rho (find optimal values)

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
    # print("shortest route:")
    score = aco.shortest_route["distance"]
    # print(score)

    with open("currentHighScore.json", "r+") as f:
        currHighScore = json.load(f)
        if currHighScore["dist"] > score:
            print("New high score!")
            currHighScore["dist"] = score
            currHighScore["alpha"] = alpha
            currHighScore["beta"] = beta
            currHighScore["q"] = q
            currHighScore["rho"] = rho
            print(">>", currHighScore)
            f.seek(0)
            json.dump(currHighScore, f)
            f.truncate()

    iters += 1
