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

    best_individuals = [(individuals[index], distance) for index, distance in indexes_best_individuals]
    #falta obtener el nombre del nodo
    nodeName = best_individuals[0][:, 0]

    repeated_orders = find_order_patterns(best_individuals)

    return repeated_orders


def find_order_patterns(best_individuals):
    order_counts = {}

    for individual, _ in best_individuals:
        order = tuple(node[0] for node in individual)  # Tomamos solo los índices de los nodos
        if order in order_counts:
            order_counts[order] += 1
        else:
            order_counts[order] = 1

    # Filtrar los órdenes que se repiten en al menos dos individuos
    repeated_orders = {order: count for order, count in order_counts.items() if count >= 2}

    return repeated_orders


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
        distances.Append(fitness(individual))

    return indivuals, distances
