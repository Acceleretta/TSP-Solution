import numpy as np
from tsplib95.distances import euclidean


def read_tsp(archive):
    nodes = []

    with open(archive, 'r') as archivo:
        lines = archivo.readlines()
        select_nodes = False

        for line in lines:
            if line.strip() == "NODE_COORD_SECTION":
                select_nodes = True
                continue
            elif line.strip() == "EOF":
                break

            if select_nodes:
                data_node = line.strip().split()
                nodes.append((int(data_node[0]), float(data_node[1]), float(data_node[2])))

    nodos_array = np.array(nodes)
    return nodos_array


def create_blocks(nodes, population_size, selected_population, individual_size, selection_threshold=3,
                  number_generations=30):
    for i in range(number_generations):
        if i == 0:
            individuals, distances = create_individual(population_size, nodes, individual_size)
        else:
            individuals, distances = create_best_generation(population_size, nodes, individual_size, patterns,
                                                            patterns_index)

        number_select_nodes = int(len(distances) * selected_population)
        indexes_best_individuals = sorted(enumerate(distances), key=lambda x: x[1])[:number_select_nodes]
        solutions_matrix = best_solutions_matrix(individuals, indexes_best_individuals, individual_size)

        patterns, patterns_index = find_most_frecuent(solutions_matrix, number_select_nodes, selection_threshold,
                                                      individual_size)

    return solutions_matrix[0]


def best_solutions_matrix(individuals, indexes_best_individuals, individual_size):
    best_individuals = np.zeros((len(indexes_best_individuals), individual_size))

    for i, (row, _) in enumerate(indexes_best_individuals):
        best_individuals[i] = individuals[row]

    return best_individuals


def find_most_frecuent(solutions_matrix, number_select_nodes, selection_threshold, individual_size):
    max_freq_per_column = np.zeros(individual_size)

    # Calcular las frecuencias del valor más repetido por columna
    for i in range(individual_size):
        _, counts = np.unique(solutions_matrix[:, i], return_counts=True)
        max_freq_per_column[i] = np.max(counts)

    # Crear una máscara para identificar los patrones que cumplen con el threshold
    patterns_mask = max_freq_per_column >= selection_threshold

    # Obtener los índices de las columnas que cumplen con el threshold
    patterns_index = np.where(patterns_mask)[0]

    # Crear la lista de patrones con las columnas que cumplen con el threshold y el valor más repetido en cada una
    patterns = [np.unique(solutions_matrix[:, i])[np.argmax(np.unique(solutions_matrix[:, i], return_counts=True)[1])]
                for i in patterns_index]

    return patterns, patterns_index


def choose_random_nodes(nodos_array, individual_size):
    index = np.random.choice(nodos_array.shape[0], size=individual_size, replace=False)
    random_nodes = nodos_array[index]
    return random_nodes


def fitness(individual, nodes):
    distances = []
    for i in range(len(individual) - 1):
        node1 = nodes[int(individual[i] - 1)]
        node2 = nodes[int(individual[i + 1] - 1)]
        distance = euclidean(node1[1:], node2[1:])
        distances.append(distance)
    return sum(distances)


def create_individual(population_size, nodes, individual_size):
    distances = []
    individuals = np.zeros((population_size, individual_size))

    for i in range(population_size):
        for j in range(individual_size):
            available_numbers = np.setdiff1d(nodes[:, 0], individuals[i, :individual_size])
            available_numbers = np.setdiff1d(available_numbers, individuals[i, j + 1:])
            individuals[i, j] = np.random.choice(available_numbers)

        distances.append(fitness(individuals[i], nodes))

    return individuals, distances


def create_best_generation(population_size, nodes, individual_size, patterns, patterns_index):
    individuals = np.zeros((population_size, individual_size))
    distances = []

    for i in range(population_size):
        # Copiar los patrones en los individuos
        individuals[i, patterns_index] = patterns

        # Verificar y llenar los números faltantes
        for j in range(individual_size):
            if individuals[i, j] == 0:
                available_numbers = np.setdiff1d(nodes[:, 0], individuals[i, :individual_size])
                available_numbers = np.setdiff1d(available_numbers, individuals[i, j + 1:])
                individuals[i, j] = np.random.choice(available_numbers)

        distances.append(fitness(individuals[i], nodes))

    return individuals, distances
