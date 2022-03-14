__author__ = "Mateusz Matyjasiak"

import random
from statistics import stdev, mean
from optproblems.cec2005 import F1, F2, F3, F6, F14

import evolution_algorithm_Mateusz_Matyjasiak

# Wymiar zadania
D = 10
# Maks wywołań funkcji ewaluacji
MAX_FUNC_CALL = D * 10_000
# Rozmiar populacji
pop_size = 500
# Prawdopodobieństwo mutacji
mutation_prob = 0.1
# Prawdopodobienstwo krzyżowania
cross_prob = 0.8
# Wszystkie funkcje musza miec zmienne w zakresie [-100, 100]
func_list = [F1(D), F2(D), F3(D), F6(D), F14(D)]


def get_random_individual(cec2005_func):
    return [random.uniform(cec2005_func.min_bounds[index], cec2005_func.max_bounds[index]) for index in range(D)]


def generate_start_population(population_size, individual_generator_func, func):
    return [individual_generator_func(func) for _ in range(population_size)]


def mutation(individual):
    r = random.randint(0, len(individual) - 1)
    gen = individual[r]
    gen += random.normalvariate(0, 1)
    if gen < -100:
        gen = -100
    elif gen > 100:
        gen = 100
    individual[r] = gen
    return individual


def cross(parent1, parent2):
    r = random.randint(1, len(parent1) - 1)
    return parent1[0:r] + parent2[r:], parent2[0:r] + parent1[r:]


def testing(fit_fun, population):
    general_result = []
    threshold = 0.75
    selection_type = 0
    for selection_number in range(5):
        if selection_number == 0:
            selection_type = 0
        elif selection_number == 1:
            selection_type = 1
        elif selection_number == 2:
            selection_type = 2
            threshold = 0.75
        elif selection_number == 3:
            selection_type = 2
            threshold = 0.5
        elif selection_number == 4:
            selection_type = 2
            threshold = 0.25

        results = []
        for _ in range(25):
            results.append(
                evolution_algorithm_Mateusz_Matyjasiak.do_evolutionary_algorithm(population,
                                                                                 MAX_FUNC_CALL,
                                                                                 fit_fun,
                                                                                 mutation,
                                                                                 mutation_prob, cross,
                                                                                 cross_prob,
                                                                                 selection_type,
                                                                                 threshold)[1] - fit_fun.bias)
        result_sorted = sorted(results)
        general_result.append(
            [result_sorted[0], result_sorted[6], result_sorted[12],
             result_sorted[18], result_sorted[24],
             mean(result_sorted), stdev(result_sorted)])
    return general_result


start_population = generate_start_population(pop_size, get_random_individual, func_list[0])

for i in range(len(func_list)):
    result_for_one_func = testing(func_list[i], start_population)
    print(result_for_one_func)
