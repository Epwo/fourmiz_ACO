from Classes import GraphClass
import random

# Define your options
choices = ["0", "3", "2", "5"]

# Define weights (higher values mean higher probability)
weights = [0.1, 0.3, 0.5, 0.1]  # Probabilities sum to 1

# Select one item based on weights
selected = random.choices(choices, weights=weights, k=1)[0]
print(selected)

graph = GraphClass.Graph([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
