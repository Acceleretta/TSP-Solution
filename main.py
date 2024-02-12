from read_tsp import *
import matplotlib.pyplot as plt

# Uso del método para leer el archivo

nombre_archivo = "kroA100.tsp"
archivo_optimo = "kroA100.opt.tour"

nodes = read_tsp(nombre_archivo)
optimo = read_tsp(archivo_optimo)
individuals = create_blocks(nodes, 200, .20, len(nodes), 5, 20)

print(individuals)


def plot_tsp(points, optimal_path, algorithm_path):
    x = points[:, 1]
    y = points[:, 2]

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', label='Puntos')

    # Dibujar el camino óptimo
    optimal_x = [x[i] for i in optimal_path]
    optimal_y = [y[i] for i in optimal_path]
    optimal_x.append(optimal_x[0])
    optimal_y.append(optimal_y[0])
    plt.plot(optimal_x, optimal_y, color='green', linestyle='-', linewidth=1, label='Camino óptimo')

    # Dibujar el camino generado por el algoritmo
    algorithm_x = [x[i] for i in algorithm_path]
    algorithm_y = [y[i] for i in algorithm_path]
    algorithm_x.append(algorithm_x[0])
    algorithm_y.append(algorithm_y[0])
    plt.plot(algorithm_x, algorithm_y, color='red', linestyle='-', linewidth=1, label='Camino generado')

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('TSP')
    plt.legend()
    plt.grid(True)
    plt.show()


plot_tsp(nodes[:, 0], optimo, individuals)

# Función para graficar los puntos y el camino
