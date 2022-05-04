#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from itertools import product
from json import loads 

def create_configurations(header, parameters):

	file_name = "configurations.txt"

	F = open(file_name, "w")

	F.write(header + "\n")

	to_replace = ["(", ")", " "]

	id_label = 0

	for i in product(*parameters):
		# modificación para satisfacer que en la configuración
		# el número de alternativas sea igual o menor al número
		# de argumentos prácticos
		i = list(i)
		
		if i[1] <= i[2]:
			i = tuple(i)
			
			label_configuration = str(i)

			for j in to_replace:
				label_configuration = label_configuration.replace(j, "")

			label_configuration = "0," + str(id_label) + "," + label_configuration
			id_label += 1
			F.write(label_configuration + "\n")
	   
	F.close()


def extract_json_parameters(file_name):

	f = open(file_name, "r") 
	
	data = loads(f.read()) 

	f.close()

	parameters = list(data["parameters"].values())
	parameters_names = list(data["parameters"].keys())

	header = "status,id,"

	for i in range(len(parameters_names)):

		if i != len(parameters_names) - 1:
			header += parameters_names[i] + ","
		else:
			header += parameters_names[i]

	return parameters, header


def get_configurations(parameters_json_file_name):
	parameters, header = extract_json_parameters(parameters_json_file_name)
	create_configurations(header, parameters)
	return "Complete."

###########################################################

parameters_json_file_name = "parameters.json"
get_configurations(parameters_json_file_name)
