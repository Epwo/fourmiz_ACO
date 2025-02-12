import csv
import time
from logic import TSP_ACO

nb_fourmis = 5
nb_iter = 15
# TODO: change values of alpha, beta, q, rho (find optimal values)
alpha = 1
beta = 1
q = 1
rho = 0.5

# Définir les paramètres à tester
parametres = {
    "alpha": [0.1, 0.5, 1, 2],
    "beta": [0.1, 0.5, 1, 2],
    "rho": [0.1, 0.5, 0.9],
    "q": [0.5, 1, 2],
    "nb_fourmis": [5, 10, 25, 75, 150],
    "nb_iter": [10, 50, 100, 200, 500],
}

# Liste des fichiers CSV
fichiers_csv = [
    "fichier_200_lignes_1.csv",
    "fichier_200_lignes_3.csv",
    "fichier_200_lignes_2.csv",
    "fichier_200_lignes_4.csv",
    "fichier_200_lignes_5.csv",
    "fichier_500_lignes_1.csv",
    "fichier_500_lignes_2.csv",
    "fichier_500_lignes_3.csv",
    "fichier_500_lignes_4.csv",
    "fichier_500_lignes_5.csv",
]


# Fonction pour charger les données à partir d'un fichier CSV
def charger_fichier_csv(nom_fichier):
    list_lieux = []
    with open(nom_fichier, "r") as f:
        next(f)  # Ignore la première ligne d'entête
        for i, line in enumerate(f):
            x = float(line.split(",")[0])
            y = float(line.split(",")[-1].strip())
            list_lieux.append([x, y, i])
    return list_lieux


# Fonction de grid search
def grid_search(fichiers_csv, parametres, i=0):
    resultats = []

    # Essayer toutes les combinaisons de paramètres
    for alpha in parametres["alpha"]:
        for beta in parametres["beta"]:
            for rho in parametres["rho"]:
                for q in parametres["q"]:
                    for q0 in parametres["nb_fourmis"]:
                        for nb_iter in parametres["nb_iter"]:
                            for fichier_csv in fichiers_csv:
                                # Charger le fichier CSV
                                list_lieux = charger_fichier_csv(fichier_csv)

                                # Créer l'instance de l'ACO
                                aco = TSP_ACO(
                                    list_lieux,
                                    nb_fourmis=q0,
                                    nb_iter=nb_iter,
                                    alpha=alpha,
                                    beta=beta,
                                    rho=rho,
                                    q=q,
                                )
                                aco.init_fourmis()

                                # Mesurer le temps d'exécution et exécuter l'algorithme
                                start_time = time.time()
                                aco.run()
                                end_time = time.time()

                                # Mesurer la performance, ici on pourrait utiliser la meilleure distance, temps d'exécution, etc.
                                temps_execution = end_time - start_time
                                # On suppose que la méthode aco.get_solution() donne la qualité de la solution obtenue
                                solution = aco.shortest_route["distance"]

                                # Sauvegarder les résultats pour cette configuration
                                resultats.append(
                                    {
                                        "fichier": fichier_csv,
                                        "alpha": alpha,
                                        "beta": beta,
                                        "rho": rho,
                                        "q": q,
                                        "nb_fourmis": q0,
                                        "nb_iter": nb_iter,
                                        "temps_execution": temps_execution,
                                        "distance": solution,
                                    }
                                )
                                i += 1
                                print(i, temps_execution)

    return resultats


# Exécuter le grid search
resultats = grid_search(fichiers_csv, parametres)

# Sauvegarder les résultats dans un fichier CSV
with open("resultats_grid_search.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "fichier",
            "alpha",
            "beta",
            "rho",
            "q",
            "nb_fourmis",
            "nb_iter",
            "temps_execution",
            "distance",
        ],
    )
    writer.writeheader()
    for resultat in resultats:
        writer.writerow(resultat)

print("Grid search terminé et résultats enregistrés dans 'resultats_grid_search.csv'.")
