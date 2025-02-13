import csv
import math
from itertools import permutations

progress_bar_length = 50


def load_points_from_csv(filename):
    points = []
    with open(filename, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            points.append((float(row["x"]), float(row["y"])))
    return points


def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def calculate_total_distance(route, points):
    total = 0
    for i in range(len(route) - 1):
        total += calculate_distance(points[route[i]], points[route[i + 1]])
    return total


def find_shortest_route(csv_file, total_routes):
    # Load points from CSV
    points = load_points_from_csv(csv_file)

    # Generate all possible routes
    possible_routes = permutations(range(len(points)))

    # Initialize best route and distance
    best_distance = float("inf")
    best_route = None
    count = 0
    # Try each route
    for route in possible_routes:
        distance = calculate_total_distance(route, points)
        if distance < best_distance:
            best_distance = distance
            best_route = route

        count += 1
        update_progress(count / total_routes)

    return best_route, best_distance


def update_progress(progress):
    filled = int(progress_bar_length * progress)
    bar = "=" * filled + "-" * (progress_bar_length - filled)
    print(f"\rProgress: [{bar}] {progress * 100:.1f}%", end="")


if __name__ == "__main__":

    update_progress(0)  # Initial progress
    csv_file = "src/graph_20.csv"
    total_routes = math.factorial(len(load_points_from_csv(csv_file)))
    print(f"Calculating {total_routes} possible routes...")

    count = 0

    best_route, best_distance = find_shortest_route(csv_file, total_routes)
    # Create a complete loop by adding the first point again
    complete_route = tuple(list(best_route) + [best_route[0]])
    best_distance = calculate_total_distance(
        complete_route, load_points_from_csv(csv_file)
    )
    print(f"Best route: {best_route}")
    print(f"Total distance: {best_distance:.2f}")
