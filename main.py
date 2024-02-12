from read_tsp import *

# Uso del método para leer el archivo
nombre_archivo = "a280.tsp"
nodes = read_tsp(nombre_archivo)


create_blocks(nodes, 50, .20, len(nodes))


