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
    distances = []
    indivuals = []
    for _ in range(population_size):
        individual = choose_random_nodes(nodes, individual_size)
        indivuals.append(individual)
        distances.append(fitness(individual))

    n = int(len(distances) * selected_population)
    indexs_best_individuals = sorted(enumerate(distances), key=lambda x: x[1])[:n]

    for indice, valor in indexs_best_individuals:
        print("Índice:", indice, "Valor:", valor)


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
