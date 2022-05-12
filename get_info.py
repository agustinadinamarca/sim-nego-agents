#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Genera informacion del estado de las simulaciones
# numero de configuraciones totales
# numero de configuraciones sin ejecutar
# numero de simulaciones ejecutadas
# informacion de las simulaciones no ejecutadas al momento

import os
import sys

# server num 103, 104 0 106
num = sys.argv[1]
num_sim_tot = 0
# num de configuraciones to execute
with open("config_srv_"+num+".txt", "r") as myfile:
    num_sim_tot = sum(1 for line in myfile)

#print(num_sim_tot)


cwd = os.getcwd() + "/results/"
num_exe = 0
if os.path.exists(cwd):
	#lstFiles = []
	lstDir = os.walk(cwd)
	F = open("info.txt", "w")
	for root, dirs, files in lstDir:
		for fichero in files:
			(nombreFichero, extension) = os.path.splitext(fichero)
			if(extension == ".txt") and "__metrics_f" in nombreFichero:
				num_exe += 1
				#lstFiles.append(cwd+nombreFichero+extension)
				#F.write(nombreFichero.replace("__metrics_f", "")+"\n")

	F.write("Number of total configurations in server "+num+": "+str(num_sim_tot)+"\n")
	F.write("Number of configurations executed and finished: "+str(num_exe)+"\n")
	F.write("Number of configurations NOT finished: "+str(num_sim_tot - num_exe)+"\n")
	F.write("Percentage of progress: "+str(100*round(float(num_exe / num_sim_tot),2))+"%")
	F.close()
	print("Number of total configurations in server "+num+": "+str(num_sim_tot))
	print("Number of configurations executed and finished: "+str(num_exe))
	print("Number of configurations NOT finished: "+str(num_sim_tot - num_exe))
	print("Percentage of progress: "+str(100*round(float(num_exe / num_sim_tot),2))+"%")


else:
	print("None")
