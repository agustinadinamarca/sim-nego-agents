# IMPORTAR Y ENCAPSULAR EN ESTA FUNCIÓN EL EXPERIMENTO DE INTERÉS
# Coloque tantos parámetros como fueron declarados en parameters.json respetando el orden
from experiments_to_run import exp

def my_function(idn, number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, N, bullshiters_density, overcautios_density, resource_boundness_density, redundancy):
    # función me mi experimento que quiero encapsular
    # pasar de string a valores numéricos
    number_agents = int(number_agents)
    alternatives_number = int(alternatives_number)
    maximum_number_practical_arguments = int(maximum_number_practical_arguments)
    maximum_number_epistemic_arguments = int(maximum_number_epistemic_arguments)
    maximum_attacks_density_value = float(maximum_attacks_density_value)
    N = int(N)
    bullshiters_density = float(bullshiters_density)
    overcautios_density = float(overcautios_density)
    resource_boundness_density = float(resource_boundness_density)
    redundancy = float(redundancy)
    
    exp(idn, number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, N, bullshiters_density, overcautios_density, resource_boundness_density, redundancy)

