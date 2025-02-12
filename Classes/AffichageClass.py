import tkinter as tk
import pandas as pd
import math
import numpy as np

RAYON = 20
LARGEUR = 800
HAUTEUR = 600
NB_MEILLEURES_ROUTES = 5


class Affichage:
    def __init__(self, path_csv, matrice_od):
        info_csv = pd.read_csv(path_csv)
        self.x = info_csv["x"].tolist()
        self.y = info_csv["y"].tolist()
        self.root = tk.Tk()
        self.root.title("Groupe 6 - Affichage du Graphe")
        self.matrice_od = matrice_od
        self.canvas = tk.Canvas(self.root, width=LARGEUR, height=HAUTEUR, bg="white")
        self.canvas.pack()
        self.info_zone = tk.Text(self.root, height=2, width=100, bg="lightgrey")
        self.info_zone.pack()
        self.text_zone = tk.Text(self.root, height=10, width=100)
        self.text_zone.pack()
        self.nb_ite = 0
        self.meilleures_routes = {}
        self.info_zone.insert(tk.END, "Nombre d'itération: " + str(self.nb_ite))
        self.root.bind("<Escape>", lambda event: self.root.quit())
        self.dessiner_lieux()
        self.distance_min = 0
        self.best_route = []
        self.matrice_pheromone = []
        self.liste_de_route = []

    def dessiner_lieux(self):
        """Dessine les lieux sous forme de cercles avec leurs numéros."""
        for i in range(len(self.x)):
            x, y = float(self.x[i]), float(self.y[i])
            self.canvas.create_oval(
                x - RAYON,
                y - RAYON,
                x + RAYON,
                y + RAYON,
                fill="lightblue",
                outline="black",
            )
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))

    def afficher_matrice(self, event, matrice_pheromones):
        """Affiche la matrice des coûts dans la zone de texte."""
        self.text_zone.delete(1.0, tk.END)
        self.text_zone.insert(tk.END, "Matrice des coûts:\n")
        for row in matrice_pheromones:
            self.text_zone.insert(tk.END, "\t".join(map(str, row)) + "\n")

    def mettre_a_jour(self):
        """Met à jour l'affichage avec une nouvelle matrice."""
        self.distance_min = 0
        self.canvas.delete("all")
        self.dessiner_lieux()
        min_value = np.min(self.matrice_pheromone)
        max_value = np.max(self.matrice_pheromone)
        self.matrice_pheromone = (
            (self.matrice_pheromone - min_value) / (max_value - min_value)
        ) * 2
        # Convertir best_route en ensemble de tuples pour une recherche rapide
        best_route_set = {
            (self.best_route[i], self.best_route[i + 1])
            for i in range(len(self.best_route) - 1)
        }
        # Dessiner les routes en noir sauf si elles sont dans best_route
        for elt in self.liste_de_route:
            longueur_par_route = 0
            for i in range(len(elt) - 2):
                x1, y1 = float(self.x[elt[i]]), float(self.y[elt[i]])
                x2, y2 = float(self.x[elt[i + 1]]), float(self.y[elt[i + 1]])
                longueur_par_route += self.matrice_od[elt[i]][elt[i + 1]]
                if (elt[i], elt[i + 1]) not in best_route_set and (
                    elt[i + 1],
                    elt[i],
                ) not in best_route_set:
                    cout = self.matrice_pheromone[elt[i]][elt[i + 1]]
                    if cout > 0:
                        self.canvas.create_line(
                            x1, y1, x2, y2, fill="black", width=cout
                        )
            self.meilleures_routes[str(longueur_par_route)] = elt
        longueur_par_route = 0
        # Dessiner la route principale en bleu
        for i in range(len(self.best_route) - 1):
            longueur_par_route += self.matrice_od[self.best_route[i]][
                self.best_route[i + 1]
            ]
            cout = self.matrice_pheromone[self.best_route[i]][self.best_route[i + 1]]
            if cout > 0:
                x1, y1 = float(self.x[self.best_route[i]]), float(
                    self.y[self.best_route[i]]
                )
                x2, y2 = float(self.x[self.best_route[i + 1]]), float(
                    self.y[self.best_route[i + 1]]
                )
                self.canvas.create_line(
                    x1, y1, x2, y2, fill="blue", width=1, dash=(4, 2)
                )
                self.canvas.create_text(
                    x1,
                    y1 - 25,
                    text=str(i + 1),
                    font=("Arial", 10, "bold"),
                    fill="black",
                )
                self.distance_min += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.meilleures_routes[str(longueur_par_route)] = self.best_route
        self.nb_ite += 1
        print(self.nb_ite)
        self.info_zone.delete(1.0, tk.END)
        self.info_zone.insert(
            tk.END,
            "Nombre d'itération: "
            + str(self.nb_ite)
            + " meilleure distance trouvée: "
            + str(self.distance_min),
        )

    def afficher_meilleures_routes(self, event, best_route):
        """Affiche les 5 meilleures routes enregistrées."""
        self.text_zone.delete(1.0, tk.END)
        self.text_zone.insert(
            tk.END, "Affichage des ", str(NB_MEILLEURES_ROUTES), " meilleures routes:\n"
        )
        meilleures_routes_triees = sorted(
            self.meilleures_routes.items(), key=lambda x: float(x[0])
        )[:NB_MEILLEURES_ROUTES]

        # Afficher les 4 meilleures routes
        for i, (distance, route) in enumerate(meilleures_routes_triees):
            self.text_zone.insert(
                tk.END, f"Route {i + 1}: Distance: {distance} - {route}\n"
            )

    def update_graph(self, matrice, liste_de_route, best_route):
        """Met à jour l'affichage avec une nouvelle matrice."""
        if matrice is not None:
            best_route_noms = [lieu.nom for lieu in best_route]
            liste_de_route_noms = [
                [lieu.nom for lieu in route] for route in liste_de_route
            ]

            self.matrice_pheromone, self.liste_de_route, self.best_route = (
                matrice,
                liste_de_route_noms,
                best_route_noms,
            )
            self.mettre_a_jour()
            self.root.update_idletasks()
            self.root.bind(
                "<m>",
                lambda event: self.afficher_matrice(event, self.matrice_pheromone),
            )
            self.root.bind(
                "<n>",
                lambda event: self.afficher_meilleures_routes(event, self.best_route),
            )
            self.root.update()
