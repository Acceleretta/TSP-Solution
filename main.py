from read_tsp import *

# Uso del método para leer el archivo

nombre_archivo = "a280.tsp"

nodes = read_tsp(nombre_archivo)

individuals = create_blocks(nodes, 50, .20, len(nodes))

print("Patrones de orden repetidos entre los mejores individuos:")

for order, count in individuals.items():
    print("Orden:", order, "Repetido en:", count, "individuos")
