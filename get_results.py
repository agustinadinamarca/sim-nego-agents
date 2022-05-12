#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
# se ejecuta al final del file .sh
# en la carpeta results, en la carpeta del experimento
# toma cada csv metric y genera uno solo con toda la información
# borra archivos metric

# server num 103, 104 0 106
num = sys.argv[1]


cwd = os.getcwd()
cwd1 = cwd + "/results/"
#print(cwd)
if os.path.exists(cwd1):
	
	lstFiles = []
	
	lstDir = os.walk(cwd1)
	#F=open("terminados.txt", "w")
	for root, dirs, files in lstDir:
		for fichero in files:
			(nombreFichero, extension) = os.path.splitext(fichero)
			if(extension == ".txt"):
				lstFiles.append(cwd1+nombreFichero+extension)
				#F.write(nombreFichero.replace("__metrics_f", "")+"\n")
	#F.close()
	name = cwd+"/results-srv-"+num+".csv"
	file_to_save = open(name, "a+")
	
	titles = [
		"id",
		"number_agents",
		"alternatives_number",
		"maximum_number_practical_arguments",
		"maximum_number_epistemic_arguments",
		"maximum_attacks_density_value",
		"N",
		"bullshiters_density",
		"overcautios_density",
		"resource_boundness_density",
		"redundancy_init_theory",
		"num_agents_R",
		"num_agents_RI",
		"bullshiters_density",
		"overcautios_density",
		"metric_d",
		"std_metric_d",
		"resource_boundness_density",
		"time_neg_mean",
		"time_neg_std",
		"FP_mean",
		"FP_std",
		"FN_mean",
		"FN_std",
		"TP_mean",
		"TP_std",
		"TN_mean",
		"TN_std",
		"redundancy_init_theory",
	    "redundancy_final_mean",
	    "redundancy_final_std",
	    "signal_mean",
	    "signal_std",
	    "noise_mean",
	    "noise_std",
	    "redundancy_init_mean",
	    "redundancy_init_std"
	]

	main_title = " ".join(s for s in titles) + "\n"
	file_to_save.write(main_title)
	
	for filename in lstFiles:
		#copio contenido y lo pego en results (salto primera linea de titulo)
		file_new = open(filename, "r")
		content = file_new.read()
		file_new.close()
		for line in content:
			file_to_save.write(line)
		#os.remove(filename)
	file_to_save.close()
	
	

else:
	print("None")



