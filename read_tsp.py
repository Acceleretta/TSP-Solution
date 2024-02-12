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


def create_blocks(nodes, population_size, selected_population, individual_size):
    individuals, distances = create_individual(population_size, nodes, individual_size)
    n = int(len(distances) * selected_population)
    indexes_best_individuals = sorted(enumerate(distances), key=lambda x: x[1])[:n]
    solutions_matrix = best_solutions_matrix(individuals, indexes_best_individuals, n)

    find_order_patterns(solutions_matrix, n)

    return repeated_orders



def best_solutions_matrix(individuals, indexes_best_individuals, n):
    best_individuals = [(individuals[index], distance) for index, distance in indexes_best_individuals]
    solutions_matrix = []
    # falta obtener el nombre del nodo
    for i in range(n):
        nodes = best_individuals[i][:]  # Access the entire first element
        solutions_matrix.append(nodes[0][:, 0])

    return np.array(solutions_matrix)


def find_order_patterns(solutions_matrix, n):
    for i in range(n):
        valores, frecuencia = np.unique(solutions_matrix[:, i], return_counts=True)
        print(f"Posición {i}: {valores} - {frecuencia}")

    for i in range(len(solutions_matrix[0])):
        if solutions_matrix[0][i] == solutions_matrix[1][i] and solutions_matrix[1][i] == solutions_matrix[2][i]:
            print(f"Patrón encontrado en la posición {i}: {solutions_matrix[0][i]}")


def choose_random_nodes(nodos_array, n):
    index = np.random.choice(nodos_array.shape[0], size=n, replace=False)
    random_nodes = nodos_array[index]
    return random_nodes


def fitness(nodes):
    distances = []
    for i in range(len(nodes) - 1):
        distance = euclidean(nodes[i][1:], nodes[i + 1][1:])
        distances.append(distance)
        sum_distances = sum(distances)
    return sum_distances


def create_individual(population_size, nodes, individual_size):
    distances = []
    indivuals = []
    for _ in range(population_size):
        individual = choose_random_nodes(nodes, individual_size)
        indivuals.append(individual)
        distances.append(fitness(individual))

    return indivuals, distances
