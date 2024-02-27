# Разработать генетический алгоритм решения задачи коммивояжера
import numpy as np
import random

# Функция для создания матрицы расстояний между городами
def create_distance_matrix(n):
    # Создаем матрицу n x n со случайными значениями расстояний
    return np.random.randint(1, 100, size=(n, n))

# Функция для расчета длины маршрута
def calculate_route_length(route, distance_matrix):
    # Считаем сумму расстояний между последовательными городами в маршруте
    # и возвращаемся в начальный город
    return sum([distance_matrix[route[i], route[i+1]] for i in range(len(route)-1)]) + distance_matrix[route[-1], route[0]]

# Создание начальной популяции
def create_initial_population(size, n_cities):
    # Генерация списка уникальных маршрутов
    return [random.sample(range(n_cities), n_cities) for _ in range(size)]

# Отбор родителей для скрещивания
def select_parents(population, distance_matrix, k=5):
    # Выбираем k случайных индивидов и отбираем из них 2 с наилучшей пригодностью
    selection = random.sample(population, k)
    selection.sort(key=lambda x: calculate_route_length(x, distance_matrix))
    return selection[0], selection[1]

# Функция скрещивания (кроссовера)
def crossover(parent1, parent2):
    size = len(parent1)
    child = [-1]*size
    # Выбираем случайный сегмент от одного родителя
    start, end = sorted(random.sample(range(size), 2))
    child[start:end] = parent1[start:end]
    # Заполняем оставшиеся позиции генами второго родителя
    pointer = end
    for gene in parent2:
        if gene not in child:
            if pointer >= size:
                pointer = 0
            child[pointer] = gene
            pointer += 1
    return child

# Функция мутации
def mutate(route, mutation_rate=0.01):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route)-1)
            route[i], route[j] = route[j], route[i]
    return route

# Основная функция генетического алгоритма
def genetic_algorithm(n_cities, population_size, n_generations):
    # Создаем матрицу расстояний и начальную популяцию
    distance_matrix = create_distance_matrix(n_cities)
    population = create_initial_population(population_size, n_cities)

    # Повторяем для заданного количества поколений
    for _ in range(n_generations):
        new_population = []
        for _ in range(population_size):
            # Отбор родителей и создание потомства
            parent1, parent2 = select_parents(population, distance_matrix)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        population = new_population

    # Находим лучший маршрут в финальной популяции
    best_route = min(population, key=lambda x: calculate_route_length(x, distance_matrix))
    best_length = calculate_route_length(best_route, distance_matrix)
    return best_route, best_length

# Запуск алгоритма
n_cities = 10  # Количество городов
population_size = 100  # Размер популяции
n_generations = 1000  # Количество поколений
best_route, best_length = genetic_algorithm(n_cities, population_size, n_generations)
print(f"Best route: {best_route}\nLength: {best_length}")