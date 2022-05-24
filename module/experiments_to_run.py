#!/usr/bin/env python
# -*- coding: utf-8 -*-

from experiments import *
from datetime import datetime
import os
import random
from numpy import mean, std

def get_agent_from_name(name, agents):
	for agent in agents:
		if agent.name == name:
			return agent
	return -1
	
def are_equal_arguments_set(args1, args2):
	if len(args1) != len(args2):
		return False
	else:	
		for arg in args1:
			if arg not in args2:
				return False
	return True
	
# si dos conjuntos de agents son iguales
def are_equal_agents_sets(agent_set_1, agent_set_2):
	for agent1 in agent_set_1:
		agent2 = get_agent_from_name(agent1.name, agent_set_2)
		args_1 = agent1.get_all_arguments_structures()
		args_2 = agent2.get_all_arguments_structures()
		status = are_equal_arguments_set(args_1, args_2)
		if status == False:
			return False
	return True

def exp(idn, number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, N, bullshiters_density, overcautios_density, resource_boundness_density, redundancy):
	configuration_string = str(number_agents)+" "+str(alternatives_number)+" "+str(maximum_number_practical_arguments)+" "+ str(maximum_number_epistemic_arguments)+" "+str(maximum_attacks_density_value)+" "+str(N)+" "+str(bullshiters_density)+" "+str(overcautios_density)+ " "+str(resource_boundness_density) + " " + str(redundancy)
	# Returns a datetime object containing the local date and time
	dto = datetime.now()
	num_random = round(random.random(), 3)
	if not os.path.exists('results'):
		os.makedirs('results')
		
	cwd = os.getcwd()
	cwd = cwd + "/results/"
	name1 = str(cwd)+str(dto.day)+"-"+str(dto.month)+"-"+str(dto.year)+"-"+str(dto.hour)+"-"+str(dto.minute)+"-"+str(dto.second)+"-"+str(num_random)+"__synthetic.csv"
	name2 = str(cwd)+str(dto.day)+"-"+str(dto.month)+"-"+str(dto.year)+"-"+str(dto.hour)+"-"+str(dto.minute)+"-"+str(dto.second)+"-"+str(num_random)+"__negotiation_taf_optimal.csv"
	fname = str(cwd) + str(idn) + "__metrics.txt"
	id_label = str(dto.day)+"-"+str(dto.month)+"-"+str(dto.year)+"-"+str(dto.hour)+"-"+str(dto.minute)+"-"+str(dto.second)+"-"+str(num_random)
	id_label=str(idn)
	##################################
	data_to_save = open(fname, "w")
	
	
	D_mean_l = []
	D_std_l = []

	time_neg_mean_l = []	
	time_neg_std_l = []

	FP_mean_l = []
	FP_std_l = []
	FN_mean_l = []
	FN_std_l = []
	TP_mean_l = []
	TP_std_l = []
	TN_mean_l = []
	TN_std_l = []

	red_mean_l = []
	red_std_l = []

	signal_mean_l = []
	signal_std_l = []

	noise_mean_l = []
	noise_std_l = []

	#bullshit_mean_l = [] 
	#bullshit_std_l = []
	#gwc_mean_l = []
	#gwc_std_l = []
	#lwc_mean_l = []
	#lwc_std_l = []
		
	num_agents_R = 0
	num_agents_RI = 0
	
	D_mean=0
	D_std=0

	time_neg_mean=0
	time_neg_std=0

	FP_mean=0
	FP_std=0
	FN_mean=0
	FN_std=0
	TP_mean=0
	TP_std=0
	TN_mean=0
	TN_std=0

	red_mean=0
	red_std=0

	noise_mean = 0
	noise_std=0
	signal_mean = 0
	signal_std=0

	#bullshit_mean=0
	#bullshit_std=0
	#gwc_mean=0
	#gwc_std=0
	#lwc_mean=0
	#lwc_std=0
	red_init_m = []
	red_init_s = []
		
	m_bis_1 = []

	for f in range(N):
		
		status = False
		
		while status == False:
			taf_agents, all_ep, all_pr, attacks = set_synthetic_experiment_taf_agents(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, redundancy)
			#taf_plus = get_taf_plus_agent(taf_agents)
			R = execute_negotiations_with_taf_agents(N, taf_agents,  all_ep, all_pr, attacks)
			
			if R != -1:
				N, agreements_number, optimal_agreements, mean_time_by_negotiation, taf_agents_final = R
				optimal_agreements = list(optimal_agreements)[0]
				status = True	
		
		id_label, configuration_string, num_agents_R, num_agents_RI, D_mean, D_std, resource_boundness_density, time_neg_mean,time_neg_std,FP_mean, FP_std, FN_mean, FN_std, TP_mean, TP_std, TN_mean, TN_std, red_mean, red_std, signal_mean, signal_std, noise_mean, noise_std, redmi, redsi, mb1 = pafs_negotiations(fname, number_agents, bullshiters_density, overcautios_density, N, taf_agents, resource_boundness_density, taf_agents_final, optimal_agreements, configuration_string, id_label, all_ep, all_pr, attacks)
		
		D_mean_l.append(D_mean)
		D_std_l.append(D_std)
		time_neg_mean_l.append(time_neg_mean)	
		time_neg_std_l.append(time_neg_std)
		FP_mean_l.append(FP_mean)
		FP_std_l.append(FP_std)
		FN_mean_l.append(FN_mean)
		FN_std_l.append(FN_std)
		TP_mean_l.append(TP_mean)
		TP_std_l.append(TP_std)
		TN_mean_l.append(TN_mean)
		TN_std_l.append(TN_std)
		#bullshit_mean_l.append(bullshit_mean)
		#bullshit_std_l.append(bullshit_std)
		#gwc_mean_l.append(gwc_mean)
		#gwc_std_l.append(gwc_std)
		#lwc_mean_l.append(lwc_mean)
		#lwc_std_l.append(lwc_std)
		red_mean_l.append(red_mean)
		red_std_l.append(red_std)
		signal_mean_l.append(signal_mean)
		noise_mean_l.append(noise_mean)
		signal_std_l.append(signal_std)
		noise_std_l.append(noise_std)
		red_init_m.append(redmi)
		red_init_s.append(redsi)
		m_bis_1.append(mb1)
		

	data_to_save.write(id_label + " ")
	data_to_save.write(configuration_string + " ")
	data_to_save.write(str(num_agents_R) + " ")
	data_to_save.write(str(num_agents_RI) + " ")
	#data_to_save.write(str(bullshiters_density) + " ")  REPETIDO
	#data_to_save.write(str(overcautios_density) + " ")  REPETIDO
	data_to_save.write(str(mean(D_mean_l)) + " ")
	data_to_save.write(str(std(D_mean_l)) + " ")
	#data_to_save.write(str(resource_boundness_density) + " ")  REPETIDO
	data_to_save.write(str(mean(time_neg_mean_l)) + " ")
	data_to_save.write(str(std(time_neg_mean_l)) + " ")
	data_to_save.write(str(mean(FP_mean_l)) + " ")
	data_to_save.write(str(std(FP_mean_l)) + " ")
	data_to_save.write(str(mean(FN_mean_l)) + " ")
	data_to_save.write(str(std(FN_mean_l)) + " ")
	data_to_save.write(str(mean(TP_mean_l)) + " ")
	data_to_save.write(str(std(TP_mean_l)) + " ")
	data_to_save.write(str(mean(TN_mean_l)) + " ")
	data_to_save.write(str(std(TN_mean_l)) + " ")
	#data_to_save.write(str(mean(bullshit_mean_l)) + " ")
	#data_to_save.write(str(mean(bullshit_std_l)) + " ")
	#data_to_save.write(str(mean(gwc_mean_l)) + " ")
	#data_to_save.write(str(mean(gwc_std_l)) + " ")
	#data_to_save.write(str(mean(lwc_mean_l)) + " ")
	#data_to_save.write(str(mean(lwc_std_l)) + " ")
	#data_to_save.write(str(redundancy) + " ")   REPETIDO
	#data_to_save.write(str(mean(red_init_m)) + " ")
	#data_to_save.write(str(mean(red_init_s)) + " ")
	data_to_save.write(str(mean(red_mean_l)) + " ")
	data_to_save.write(str(std(red_mean_l)) + " ")

	data_to_save.write(str(mean(signal_mean_l)) + " ")
	data_to_save.write(str(std(signal_mean_l)) + " ")
	data_to_save.write(str(mean(noise_mean_l)) + " ")
	data_to_save.write(str(std(noise_mean_l)) + " ")
	snm = mean(signal_mean_l) + mean(noise_mean_l)
	data_to_save.write(str(snm) + " ")

	data_to_save.write(str(mean(m_bis_1)) + " ")
	data_to_save.write(str(std(m_bis_1)) + "\n")




	data_to_save.close()

