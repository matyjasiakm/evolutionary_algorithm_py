__author__ = "Mateusz Matyjasiak"

import random
import evolution_algorithm_Mateusz_Matyjasiak

POPULATION_SIZE = 200
MAX_FUN_CALL = 10_000
MUTATION_PROB = 0.1
DISTANCE = [[0, 345, 379, 327, 342, 429, 214, 295, 428, 237, 574],
            [345, 0, 268, 143, 159, 326, 366, 375, 181, 108, 287],
            [379, 268, 0, 395, 414, 62, 102, 246, 107, 233, 156],
            [327, 143, 395, 0, 20, 456, 486, 435, 294, 245, 369],
            [342, 159, 414, 20, 0, 475, 505, 454, 313, 258, 389],
            [429, 326, 62, 456, 475, 0, 69, 273, 169, 280, 196],
            [408, 366, 102, 486, 505, 69, 0, 227, 192, 335, 171],
            [214, 375, 246, 435, 454, 273, 227, 0, 223, 409, 100],
            [295, 181, 107, 294, 313, 169, 192, 223, 0, 188, 124],
            [428, 108, 233, 245, 258, 280, 335, 409, 188, 0, 311],
            [237, 287, 156, 369, 389, 196, 171, 100, 124, 311, 0]]

gasoline_price_per_km = 5


def mutation(individual):
    positions = random.sample(range(len(DISTANCE)), k=2)
    individual[positions[0]], individual[positions[1]] = individual[positions[1]], individual[positions[0]]
    return individual


def generate_random_individual():
    individual = list(range(len(DISTANCE)-1))
    random.shuffle(individual)
    return individual


def fit_fun(individual):
    dist_sum = 0
    dist_sum += DISTANCE[len(DISTANCE) - 1][individual[0]]
    dist_sum += DISTANCE[individual[len(individual) - 1]][len(DISTANCE) - 1]
    for i in range(len(individual) - 1):
        dist_sum += DISTANCE[individual[i]][individual[i + 1]]
    return dist_sum * gasoline_price_per_km


start_population = [generate_random_individual() for _ in range(POPULATION_SIZE)]
for _ in range(3):
    result = evolution_algorithm_Mateusz_Matyjasiak.do_evolutionary_algorithm(start_population, MAX_FUN_CALL, fit_fun,
                                                                              mutation, 0.1, selection_type=2,
                                                                              threshold=0.25)
    print(result[1], "zł", result[0])
