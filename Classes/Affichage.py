import tkinter as tk
import pandas as pd
import math
RAYON = 20
LARGEUR = 800
HAUTEUR = 600
NB_MEILLEURES_ROUTES = 4


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
        self.text_zone.insert(tk.END, "Nombre d'itération: " + str(self.nb_ite))
        self.root.bind("<Escape>", lambda event: self.root.quit())
        self.dessiner_lieux()
        self.distance_min = 0
    def dessiner_lieux(self):
        """Dessine les lieux sous forme de cercles avec leurs numéros."""
        for i in range(len(self.x)):
            x, y = float(self.x[i]), float(self.y[i])
            self.canvas.create_oval(
                x - RAYON, y - RAYON, x + RAYON, y + RAYON,
                fill="lightblue", outline="black"
            )
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))


    def afficher_matrice(self, event, matrice_pheromones):
        """Affiche la matrice des coûts dans la zone de texte."""
        self.text_zone.delete(1.0, tk.END)
        self.text_zone.insert(tk.END, "Matrice des coûts:\n")
        for row in matrice_pheromones:
            self.text_zone.insert(tk.END, "\t".join(map(str, row)) + "\n")

    def mettre_a_jour(self, matrice_pheromones, liste_de_route, route_main):
        """Met à jour l'affichage avec une nouvelle matrice."""
        self.distance_min = 0
        self.canvas.delete("all")
        self.dessiner_lieux()
        # Convertir route_main en ensemble de tuples pour une recherche rapide
        route_main_set = {(route_main[i], route_main[i + 1]) for i in range(len(route_main) - 1)}
        # Dessiner les routes en noir sauf si elles sont dans route_main
        for elt in liste_de_route:
            longueur_par_route = 0
            for i in range(len(elt) - 1):
                x1, y1 = float(self.x[elt[i]]), float(self.y[elt[i]])
                x2, y2 = float(self.x[elt[i + 1]]), float(self.y[elt[i + 1]])
                longueur_par_route += self.matrice_od[elt[i]][elt[i+1]]
                if (elt[i], elt[i + 1]) not in route_main_set and (elt[i + 1], elt[i]) not in route_main_set:
                    cout = matrice_pheromones[elt[i]][elt[i + 1]]
                    if cout > 0:
                        self.canvas.create_line(x1, y1, x2, y2, fill="black", width=cout)
            self.meilleures_routes[str(longueur_par_route)] = elt




        # Dessiner la route principale en bleu
        for i in range(len(route_main) - 1):
            cout = matrice_pheromones[route_main[i]][route_main[i + 1]]
            if cout > 0:
                x1, y1 = float(self.x[route_main[i]]), float(self.y[route_main[i]])
                x2, y2 = float(self.x[route_main[i + 1]]), float(self.y[route_main[i + 1]])
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=cout, dash=(4, 2))
                self.canvas.create_text(x1, y1 - 25, text=str(i + 1), font=("Arial", 10, "bold"), fill="black")
                self.distance_min += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        self.nb_ite += 1
        print(self.nb_ite)
        self.info_zone.delete(1.0, tk.END)
        self.info_zone.insert(tk.END, "Nombre d'itération: " + str(self.nb_ite) + ' meilleure distance trouvée: ' + str(
            self.distance_min))

    def afficher_meilleures_routes(self, event, liste_de_route, route_main):
        """Affiche les 5 meilleures routes enregistrées."""
        self.text_zone.delete(1.0, tk.END)
        self.text_zone.insert(tk.END, "Affichage des 5 meilleures routes:\n")
        self.text_zone.insert(tk.END, f"Route {0}: {route_main}\n")
        meilleures_routes_triees = sorted(self.meilleures_routes.items(), key=lambda x: x[0])[:5]

        # Afficher les 4 meilleures routes
        for i, (distance, route) in enumerate(meilleures_routes_triees):
            self.text_zone.insert(tk.END, f"Route {i + 1}: Distance: {distance} - {route}\n")


    def lancer_affichage(self, matrice, liste_de_route, route_main):
        """Met à jour l'affichage avec une nouvelle matrice."""
        if matrice is not None:
            self.mettre_a_jour(matrice, liste_de_route, route_main)
            self.root.update_idletasks()
            self.root.bind("<m>", lambda event: self.afficher_matrice(event, matrice))
            self.root.bind("<n>", lambda event: self.afficher_meilleures_routes(event, liste_de_route, route_main))

            self.root.update()


# Définition des matrices de phéromones
matrice_pheromones1 = [
    [0, 0.8, 0, 0, 0],
    [0, 0, 0.4, 0, 0],
    [0, 0, 0, 0.6, 0],
    [0, 0, 0, 0, 0.9],
    [4.0, 0, 0, 0, 0]
]

matrice_pheromones2 = [
    [0, 0.8, 2, 2, 2],
    [2.5, 0, 0.4, 3, 0],
    [3.1, 1.8, 0, 0.6, 0],
    [4.0, 2.2, 2.8, 0, 0.9],
    [4.0, 2.2, 2.8, 3.7, 0]
]

matrice_od = [
    [0, 0.8, 2, 2, 2],
    [2.5, 0, 0.4, 3, 0],
    [3.1, 1.8, 0, 0.6, 0],
    [4.0, 2.2, 2.8, 0, 0.9],
    [4.0, 2.2, 2.8, 3.7, 0]
]
# Création de l'affichage
affi = Affichage("../src/graph_5.csv", matrice_od)
route_main = [0, 1, 2, 3, 4]
affi.lancer_affichage(None, None, None)
affi.lancer_affichage(matrice_pheromones1, [[0, 2, 3], [1, 2, 4], [2, 3, 4]], route_main)
affi.lancer_affichage(matrice_pheromones2, [[0, 2, 3], [1, 2, 4], [2, 3, 4]], route_main)
affi.root.after(2500, lambda: affi.lancer_affichage(matrice_pheromones1, [[0, 2, 3], [1, 2, 4], [2, 3, 4]], route_main))
affi.root.after(5000, lambda: affi.lancer_affichage(matrice_pheromones2, [[0, 2, 3], [1, 2, 4], [2, 3, 4]], route_main))
affi.root.mainloop()
