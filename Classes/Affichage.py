import tkinter as tk
from tkinter import messagebox
import math

# Constants
LARGEUR = 800
HAUTEUR = 600
NB_LIEUX = 10  # Exemple de nombre de lieux, cela peut varier


class Affichage:
    def __init__(self, root, graph, route=None):
        self.root = root
        self.graph = graph
        self.route = route
        self.canvas = tk.Canvas(root, width=LARGEUR, height=HAUTEUR)
        self.canvas.pack()

        self.text_area = tk.Text(root, height=10, width=80)
        self.text_area.pack()

        self.root.title("Colonie de fourmis - Groupe I")

        # Bind keys
        self.root.bind("<Key>", self.on_key_press)

        self.update_display()

    def update_display(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Dessiner les lieux comme des cercles
        for i, lieu in enumerate(self.graph.liste_lieux):
            x, y = lieu[0], lieu[1]
            self.canvas.create_oval(
                x - 10, y - 10, x + 10, y + 10, fill="blue", outline="black"
            )
            self.canvas.create_text(x, y, text=str(i), fill="white")

        if self.route:
            self.display_route(self.route)

    def display_route(self, route):
        # Afficher la meilleure route sous forme de ligne bleue pointillée
        for i in range(len(route) - 1):
            start_lieu = self.graph.liste_lieux[route[i]]
            end_lieu = self.graph.liste_lieux[route[i + 1]]
            x1, y1 = start_lieu[0], start_lieu[1]
            x2, y2 = end_lieu[0], end_lieu[1]
            self.canvas.create_line(
                x1, y1, x2, y2, fill="blue", dash=(4, 2)
            )  # Ligne pointillée

            # Afficher l'ordre de visite des lieux
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            self.canvas.create_text(
                mid_x, mid_y - 10, text=f"{route[i]}->{route[i + 1]}", fill="black"
            )

    def on_key_press(self, event):
        if event.keysym == "Escape":
            self.root.quit()
        elif (
            event.keysym == "Return"
        ):  # Appuyer sur "Entrée" pour afficher les meilleures routes
            self.display_best_routes()
        elif event.keysym == "m":  # Appuyer sur "m" pour afficher la matrice de coûts
            self.display_cost_matrix()

    def display_best_routes(self):
        # Afficher les N meilleures routes (exemple avec 5 routes)
        best_routes = self.graph.get_best_routes(
            N=5
        )  # Supposons que vous ayez une fonction qui donne les meilleures routes
        for route in best_routes:
            self.display_route(route)
        self.text_area.insert(tk.END, "Affichage des meilleures routes trouvées...\n")
        self.text_area.yview(tk.END)

    def display_cost_matrix(self):
        # Afficher la matrice de coûts (phéromones)
        matrix = (
            self.graph.matrice_od
        )  # Supposons que vous avez la matrice de coûts dans la classe Graph
        self.text_area.insert(tk.END, "Matrice de coûts entre les lieux :\n")
        for row in matrix:
            self.text_area.insert(tk.END, "\t".join(map(str, row)) + "\n")
        self.text_area.yview(tk.END)


# Classe Graph (extrait simplifié) pour interagir avec Affichage
class Graph:
    def __init__(self):
        # Simuler des lieux (exemple avec des coordonnées aléatoires)
        self.liste_lieux = [
            (random.randint(0, LARGEUR), random.randint(0, HAUTEUR))
            for _ in range(NB_LIEUX)
        ]
        self.matrice_od = self.calcul_matrice_cout_od()

    def calcul_matrice_cout_od(self):
        # Calculer la matrice de coûts (distance euclidienne)
        matrice = []
        for i in range(NB_LIEUX):
            row = []
            for j in range(NB_LIEUX):
                if i != j:
                    dist = math.sqrt(
                        (self.liste_lieux[i][0] - self.liste_lieux[j][0]) ** 2
                        + (self.liste_lieux[i][1] - self.liste_lieux[j][1]) ** 2
                    )
                else:
                    dist = 0
                row.append(dist)
            matrice.append(row)
        return matrice

    def get_best_routes(self, N=5):
        # Cette fonction renvoie les N meilleures routes (exemple aléatoire pour le moment)
        routes = [list(range(NB_LIEUX))]  # Simuler une route de base
        for _ in range(N - 1):
            random.shuffle(routes[0])  # Mélanger les lieux pour obtenir une autre route
            routes.append(routes[0][:])  # Ajouter la route mélangée
        return routes


# Code principal
if __name__ == "__main__":
    import random

    root = tk.Tk()
    graph = Graph()
    app = Affichage(root, graph)
    root.mainloop()
