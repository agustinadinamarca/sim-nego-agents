
import numpy as np

# Obtengo contenido por filas
F = open("configurations.txt", "r")
content = F.readlines()
F.close()

# Particiono el contenido en 3 files config_1, config_2 y config_3 (1 por cada server)

# número de configuraciones totales
N = len(content) - 1
# número de servers
n = 3

# cantidad de configuraciones por particion
k = int(np.trunc(N / n))
# resto para agregar a la última partición
r = N % n

F1 = open("config_srv_103.txt", "w")
for i in range(1, k+1):
    F1.write(content[i])
F1.close()
    
F2 = open("config_srv_104.txt", "w")
for i in range(k+1, 2*k+1):
    F2.write(content[i])
F2.close()
    
F3 = open("config_srv_106.txt", "w")
for i in range(2*k+1, 3*k+1+r):
    F3.write(content[i])
F3.close()

