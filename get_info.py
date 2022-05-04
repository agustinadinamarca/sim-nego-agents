#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# se ejecuta al final del file .sh
# en la carpeta results, en la carpeta del experimento
# toma cada csv metric y genera uno solo con toda la información
# borra archivos metric

cwd = os.getcwd()
cwd = cwd + "/results/"
#print(cwd)
if os.path.exists(cwd):
	
	lstFiles = []
	
	lstDir = os.walk(cwd)
	F=open("terminados.txt", "w")
	for root, dirs, files in lstDir:
		for fichero in files:
			(nombreFichero, extension) = os.path.splitext(fichero)
			if(extension == ".txt"):
				lstFiles.append(cwd+nombreFichero+extension)
				F.write(nombreFichero.replace("__metrics_f", "")+"\n")
	F.close()

else:
	print("None")
