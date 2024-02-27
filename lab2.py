#Реализовать популяционный алгоритм
import numpy as np

# Функция приспособленности
def fitness(x):
    return x * np.sin(10 * np.pi * x) + 1

# Инициализация популяции
def initialize_population(size):
    # Добавляем второе измерение размером 1 для создания двумерного массива
    return np.random.uniform(-1, 2, (size, 1))

# Отбор
def select(population, fitness_scores, num_parents):
    parents_idx = np.argsort(fitness_scores)[-num_parents:]
    return population[parents_idx]

# Кроссовер
def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)
    crossover_point = np.uint8(offspring_size[1]/2)
    for k in range(offspring_size[0]):
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k+1) % parents.shape[0]
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

# Мутация
def mutate(offspring_crossover):
    for idx in range(offspring_crossover.shape[0]):
        random_value = np.random.uniform(-0.1, 0.1, 1)
        offspring_crossover[idx, :] += random_value
    return offspring_crossover

# Главная функция алгоритма
def genetic_algorithm(num_generations, population_size, num_parents, mutation_rate):
    population = initialize_population(population_size)
    for generation in range(num_generations):
        fitness_scores = np.array([fitness(x) for x in population[:, 0]])
        parents = select(population, fitness_scores, num_parents)
        offspring_crossover = crossover(parents, (population_size - parents.shape[0], 1))
        offspring_mutation = mutate(offspring_crossover)
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = offspring_mutation
        print(f"Поколение {generation + 1}, лучшая приспособленность {np.max(fitness_scores)}")
    best_fitness_idx = np.argmax(fitness_scores)
    return population[best_fitness_idx, :], fitness_scores[best_fitness_idx]

# Параметры алгоритма
num_generations = 10
population_size = 50
num_parents = 20
mutation_rate = 0.1

# Запуск алгоритма
best_solution, best_fitness = genetic_algorithm(num_generations, population_size, num_parents, mutation_rate)
print(f"Лучшее решение: {best_solution}, с приспособленностью: {best_fitness}")