
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from my_experiment import my_function

def save_configuration_ended(conf):
    F = open("end.txt", "a")
    F.write(conf+"\n")
    F.close()
def get_parameters_from_string(string_parameters):
    return string_parameters.split(",")

def f_ini(parameters):
    to_change = "i" + parameters[1:]
    f = open("configurations.csv", "r")
    content = f.readlines()
    f.close()

    for i in range(len(content)):
        if content[i] == parameters + "\n":
            content[i] = to_change + "\n" 
    
    f = open("configurations.csv", "w")
    f.writelines(content)
    f.close()

def f_fin(parameters):
    to_change = "f" + parameters[1:]
    f = open("configurations.csv", "r")
    content = f.readlines()
    f.close()

    for i in range(len(content)):
        if content[i] == "i" + parameters[1:] + "\n":
            content[i] = to_change + "\n" 
    
    f = open("configurations.csv", "w")
    f.writelines(content)
    f.close()

def function_experiment(idn, parameters):
    my_function(idn, *parameters)
    print("Completed!")

def experiment(parameters):
    list_p = get_parameters_from_string(parameters)
    function_experiment(list_p[1], list_p[2:]) #id
    cwd = os.getcwd()
    archivo = cwd +"/results/"+str(list_p[1])+"__metrics.txt"
    nombre_nuevo = cwd+"/results/"+str(list_p[1])+"__metrics_f.txt"
    os.rename(archivo, nombre_nuevo)


experiment(sys.argv[1])



