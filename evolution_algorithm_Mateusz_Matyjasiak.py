__author__ = "Mateusz Matyjasiak"

import random
from typing import List, Tuple, Callable, Optional

Individual = List[float]
Population = List[Individual]
EvaluatedPopulation = List[Tuple[Individual, float]]
FitnessFun = Callable[[Individual], float]
CrossFun = Callable[[Individual, Individual], Tuple[Individual, Individual]]
MutationFun = Callable[[Individual], Individual]
StopFun = Callable[[Individual], bool]


def do_evolutionary_algorithm(start_population: Population,
                              max_fitness_function_call: int,
                              fitness_func: FitnessFun,
                              mutation_func: MutationFun,
                              mutation_prob: float,
                              cross_func: Optional[CrossFun] = None,
                              cross_prob: float = 0,
                              selection_type: int = 0,
                              threshold: float = 0.5) -> Tuple[Individual, float]:
    max_iteration = max_fitness_function_call / len(start_population)
    evaluated_population = evaluate_population(start_population, fitness_func)
    i = 1
    while i <= max_iteration:

        if selection_type == 0:
            selected = roulette_selection(evaluated_population)
        elif selection_type == 1:
            selected = tournament_selection(evaluated_population)
        else:
            selected = threshold_selection(evaluated_population, threshold)

        new_population = do_cross_and_mutation(selected, len(evaluated_population), mutation_func, mutation_prob,
                                               cross_func,
                                               cross_prob)
        evaluated_population = evaluate_population(new_population, fitness_func)
        temp = min(evaluated_population, key=lambda x: x[1])
        i += 1
        continue
    return temp


def evaluate_population(population: Population, fitness_func: FitnessFun) -> EvaluatedPopulation:
    return [(individual, fitness_func(individual)) for individual in population]


def roulette_selection(evaluated_population: EvaluatedPopulation) -> Population:
    fitness_max = max(evaluated_population, key=lambda x: x[1])[1]
    fitness_min = min(evaluated_population, key=lambda x: x[1])[1]
    fitness_values = [evaluated_individual[1] for evaluated_individual in evaluated_population]
    fitness_values_scaled = [(val - fitness_min) / (fitness_max - fitness_min) for val in fitness_values]
    fitness_values_scaled = [1 - fitness_val for fitness_val in fitness_values_scaled]
    fitness_scaled_sum = sum(fitness_values_scaled)
    individual_probabilities = [fitness_scaled_val / fitness_scaled_sum for fitness_scaled_val in fitness_values_scaled]
    probability_mass = [sum(individual_probabilities[:i + 1]) for i in range(len(individual_probabilities))]

    selected = []
    for _ in range(len(evaluated_population)):
        random_number = random.random()
        for i in range(len(probability_mass)):
            if random_number <= probability_mass[i]:
                selected.append(evaluated_population[i][0])
                break
    return selected


def tournament_selection(evaluated_population: EvaluatedPopulation, rivals_count: int = 2) -> Population:
    evaluated_population = sorted(evaluated_population, key=lambda x: x[1])
    selected = []
    for _ in range(len(evaluated_population)):
        rivals = random.sample(evaluated_population, k=rivals_count)
        rivals_sorted = sorted(rivals, key=lambda x: x[1])
        selected.append(rivals_sorted[0][0])
    return selected


def threshold_selection(evaluated_population: EvaluatedPopulation, threshold: int = 0.5) -> Population:
    evaluated_population = sorted(evaluated_population, key=lambda x: x[1])
    population_border = int(len(evaluated_population) * threshold)
    choosen = evaluated_population[:population_border]
    selected = []
    for _ in range(len(evaluated_population)):
        r = random.randint(0, len(choosen) - 1)
        selected.append(choosen[r][0])
    return selected


def do_cross_and_mutation(selected_generation: Population, generation_size: int, mutation_func: MutationFun,
                          mutation_prob: float, cross_func: CrossFun,
                          cross_prob: float) -> Population:
    new_generation = []
    while len(new_generation) != generation_size:
        if cross_func is not None:
            parents = random.sample(selected_generation, k=2)
            r = random.random()
            if r <= cross_prob:
                child1, child2 = cross_func(parents[0], parents[1])
            else:
                child1 = parents[0]
                child2 = parents[1]

            r = random.random()
            if r < mutation_prob:
                child1 = mutation_func(child1)
            r = random.random()
            if r < mutation_prob:
                child2 = mutation_func(child2)

            new_generation.append(child1)
            new_generation.append(child2)
        else:
            for gen in selected_generation:
                r = random.random()
                if r < mutation_prob:
                    gen = mutation_func(gen)
                new_generation.append(gen)
    return new_generation
