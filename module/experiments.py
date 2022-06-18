
#from synthetic import *
from synthetic_new import *
from negotiation import *
from metrics import *

import numpy as np
import time
from time import perf_counter

import copy

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


def set_synthetic_experiment_taf_agents(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, redundancy):
	taf_agents, all_ep, all_pr, attacks = create_agents(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, redundancy)
	return taf_agents, all_ep, all_pr, attacks

def get_taf_plus_agent(taf_agents_initial):
	taf_plus = get_major_agent_from_agents(taf_agents_initial)
	return taf_plus

def execute_negotiations_with_taf_agents(N, taf_agents, all_ep, all_pr, attacks):
	#tafp = get_taf_plus_agent(copy.deepcopy(taf_agents))
	taf_agents_original = copy.deepcopy(taf_agents) # BORRAR
	X = -1
	for agent in taf_agents:
		X = agent.get_alternatives()
		break
	system_aguments = all_ep + all_pr
	lst = set() # almacena las alternativas ganadoras de cada agreement
	times = []
	red_i_m, red_i_s = metric_redundancy(taf_agents, len(taf_agents), attacks, system_aguments)
	red_m = []
	red_s = []
	#bullshit_m = []
	#bullshit_std = []
	print("Start", N, "negotiations with", len(taf_agents), "TAFs agents...")
	
	for i in range(N):
		t0 = perf_counter() # tiempo inicial
		#if are_equal_agents_sets(taf_agents, taf_agents_original):
		#	print("OK11")
		#print(len(taf_agents))
		result, taf_agents_final = negotiation(taf_agents, X) # [option, taf_agents_final]
		#print(len(taf_agents_final))
		#if are_equal_agents_sets(taf_agents, taf_agents_final) == False:
		#	print("OK22, intercambio")
		tf = perf_counter() # tiempo final

		rm, rs = metric_redundancy(taf_agents_final, len(taf_agents_final), attacks, system_aguments)
		red_m.append(rm)
		red_s.append(rs)

		#bm, bs = metric_bullshit(taf_agents_final, tafp)
		#bullshit_m.append(bm)
		#bullshit_std.append(bs)
		#for ag in taf_agents:
		#	init = ag.get_all_arguments_structures()
		#	print(init, "\n")
		#	print(len(init))
		#print("taf_final")
		#for ag in taf_agents_final:
		#	f = ag.get_all_arguments_structures()
		#	print(f, "\n")
		#	print(len(f))
		if result not in lst:
			lst.add(result)
			
		times.append(tf - t0) # duración de la negociación
		
		print("----- Progress:", int((i + 1) * 100 / N), "%" )
		
		if len(lst) > 1:
			return -1
	
	print("End", N, "negotiations with", len(taf_agents), "TAFs agents...")
	mean_time_by_negotiation = np.mean(times, dtype=np.float32)
	print("Average time by negotiation:", round(mean_time_by_negotiation, 3), "s")
	print("Total time", N, "negotiations:", round(sum(times), 3), "s") 
	#print("Redundancy init:", red_i_m, red_i_s)
	#print("Redundancy final:", np.mean(red_m), np.mean(red_s))
	#print("Bullshit?", np.mean(bullshit_m), np.mean(bullshit_std), np.std(bullshit_std)) 
	agreements_number = len(lst) # cantidad de agreements
	optimal_agreements = lst # set de soluciones óptimas

	return N, agreements_number, optimal_agreements, mean_time_by_negotiation, taf_agents_final
	
	
	
def save_taf_negotiation_results(name, N, agreements_number, optimal_agreements, mean_time_by_negotiation): 
	
	file_to_save = open(name, "w")
	file_to_save.write("TAFs Negotiations\n")
	file_to_save.write("Number of executions: "+ str(N) + "\n")
	file_to_save.write("Number of agreements: "+ str(agreements_number) + "\n")
	file_to_save.write("Optimal agreement: "+ str(optimal_agreements) + "\n")
	file_to_save.write("Average Time (1 execution):" + str(np.mean(mean_time_by_negotiation, dtype=np.float32)) + "\n")
	
	file_to_save.close()
	
	
def save_synthetic_experiment_taf_agents(name, taf_agents):
	file_to_save = open(name, "w")
	file_to_save.write(str(len(taf_agents)) + "\n")
	file_to_save.write("Name\n")
	
	for ag in taf_agents:
		file_to_save.write(str(ag.name) + "\n")
		#file_to_save.write("Goals\n ")
		#for g in ag._Agent__G: 
		#	file_to_save.write(str(g[0])+" "+str(g[1])+"\n")

		file_to_save.write("Alternatives\n")
		X = ag.get_alternatives()
		
		for x in X:
			file_to_save.write(str(x) + " ")

		file_to_save.write("\nCandidates decisions preferred order\n")
		file_to_save.write(str(ag.candidate_decisions_descending_order_of_preference())+"\n")
		
		file_to_save.write("Practical Arguments\n")
		pab = ag.get_practical_base_structures()
		
		for e in pab:
			file_to_save.write(e[0]+" "+e[1]+" "+e[2]+" "+str(round(e[4], 2))+" ")
			for k in e[3]:
				file_to_save.write(k)
				file_to_save.write(" ")
			file_to_save.write("\n")
									
		file_to_save.write("Epistemic Arguments\n")
		eab = ag.get_epistemic_base_structures()
		
		for e in eab:
			file_to_save.write(e[0]+" ")
			for k in e[1]:
				file_to_save.write(k)
				file_to_save.write(" ")
			file_to_save.write("\n")

		file_to_save.write("Name\n")
	 
	file_to_save.close()
	

def get_number_semantics_r(semantics_list):
	count = 0
	for i in semantics_list:
		if i == True:
			count += 1
	return count

def get_alternatives_from_agents(agents):
	for ag in agents:
		return ag.get_alternatives()

def pafs_negotiations(fname, number_agents, bullshiters_density, overcautios_density, M, taf_agents, resource_boundness_density, taf_agents_final, optimal_agreements, configuration_string, id_label, all_ep, all_pr, attacks):
	
	#data_to_save = open(fname, "w")
	
	taf_plus = get_taf_plus_agent(taf_agents)
	acc_args_taf_plus = taf_plus.get_acceptable_arguments()
	
	#sc = get_semantics_configurations(number_agents)
	
	#ssc = get_sample_semantics_configurations(number_agents, step, sc)
	
	#taf_agents_original = copy.deepcopy(taf_agents) # borrar
	X = get_alternatives_from_agents(taf_agents)
	
	#print("\nStart", len(ssc) * M, "negotiations with", number_agents, "PAFs agents...")
	print("\nStart", M, "negotiations with", number_agents, "PAFs agents...")
	
	# CREO SEMANTIC LIST (modificar)
	# Porcentaje puro Bullshiters y resto taf
	semantics_list = [] # tener tantos elementos como agentes paf de alguna semantica
	if bullshiters_density > 0:
		num_bullshiters = int(number_agents * bullshiters_density)
		if num_bullshiters < 1:
			num_bullshiters = 1
		for k in range(num_bullshiters):
			semantics_list.append(True)
	# Porcentaje puro Overcautios y resto taf
	if overcautios_density > 0:
		num_overcautios = int(number_agents * overcautios_density)
		if num_overcautios < 1:
			num_overcautios = 1
		for k in range(num_overcautios):
			semantics_list.append(False)
	#count = 0
	#for semantics_list in ssc: # ARREGLAR V
		#count += 1
		
	D = []
		
	FP = []
	FN = []
	TP = []
	TN = []
		
	#Bullshit = []
	#GWC = []
	#LWC = []
	RED_M = []
	RED_S = []

	SIGNAL_MEAN = []
	SIGNAL_STD = []
	NOISE_MEAN = []
	NOISE_STD = []
		
	time = []

	rmi_mean = []
	rsi_std = []

	bis1 = []
	
	#print(type(taf_agents))
	#print("overcautios_density:", overcautios_density)
	#print("bullshiters_density:", bullshiters_density)
	#print("semantics_list:", semantics_list)
	
	# transformo a lista
	taf_agents = list(taf_agents)
	# lista de indices taf
	taf_indices = [i for i in range(len(taf_agents))]
	system_aguments = all_ep + all_pr
	for i in range(M):
		print("iteration", i+1)
		# INDICES
		paf_i = set(np.random.choice(a=taf_indices, size=len(semantics_list), replace=False))
		ind = set(taf_indices)
		taf_i = list(ind.difference(paf_i))
		
		# SPLITEO CONJUNTOS
		taf = [taf_agents[w] for w in taf_i]
		paf = [taf_agents[j] for j in paf_i]
	
		#np.random.shuffle(semantics_list)
			# comparar siempre taf_agents con su original
			#if are_equal_agents_sets(taf_agents_original, taf_agents) == True:
			#	print("OK1")
		# NECESITO CREAR AGENTES PAF Y TAF
		# splitear taf_agents en dos conjuntos
		# CREO PAF AGENTS
		#paf_agents = create_paf_agents(taf_agents, resource_boundness_density, semantics_list)
		paf_agents = create_paf_agents(paf, resource_boundness_density, semantics_list)
			#if are_equal_agents_sets(paf_agents, taf_agents) != True:
			#	print("OK2, modificacion")
			# paf y taf distintos

		rmi, rsi = metric_redundancy(paf_agents, len(paf_agents), attacks, system_aguments)
		rmi_mean.append(rmi)
		rsi_std.append(rsi)

		t0 = perf_counter() # tiempo inicial
		# MEZCLO CONJUNTOS TAF Y PAF
		all_agents = taf+paf_agents
		#result, paf_agents_final = negotiation(set(paf_agents), X)
		result, paf_agents_final = negotiation(set(all_agents), X)
			#if are_equal_agents_sets(paf_agents_final, paf_agents) != True:
			#	print("OK3, intercambio", len(paf_agents_final), len(paf_agents))
			#print(len(paf_agents_final), len(paf_agents))
			# paf con paf final
		tf = perf_counter() # tiempo final
				  
		time.append(tf - t0)
			
		d = metric_d(optimal_agreements, result)
		D.append(d)
			
		#mean_bullshit, std_bullshit = metric_bullshit(paf_agents_final, taf_plus)
		#mean_gwc, std_gwc = metric_global_wrongfully_cautious(paf_agents_final, taf_plus)
		#mean_lwc, std_lwc = metric_local_wrongfully_cautious(paf_agents_final, taf_agents_final)
		tp, tn, fp, fn = metric(taf_agents_final, paf_agents_final)

		rm, rs = metric_redundancy(paf_agents_final, len(taf_agents_final), attacks, system_aguments)
		RED_M.append(rm)
		RED_S.append(rs)

		#sigm, sigs = metric_signal(paf_agents_final, len(attacks))
		#noim, nois = metric_noise(paf_agents_final, len(attacks))

		#sigm, sigs = metric_signal(paf_agents_final, acc_args_taf_plus)
		#noim, nois = metric_noise(paf_agents_final, acc_args_taf_plus)

		sigm, sigs, noim, nois = metric_signal_and_noise(paf_agents_final, acc_args_taf_plus, len(system_aguments))

		b1 = metric_bis_1(paf_agents_final)
		bis1.append(b1)




		SIGNAL_MEAN.append(sigm)
		SIGNAL_STD.append(sigs)
		NOISE_MEAN.append(noim)
		NOISE_STD.append(nois)

		FP.append(fp)
		FN.append(fn)
		TP.append(tp)
		TN.append(tn)
		#Bullshit.append(mean_bullshit)
		#GWC.append(mean_gwc)
		#LWC.append(mean_lwc)
		#print("----- Progress:", count, "of", len(ssc), ": ", int((i + 1) * 100 / M), "%" )
		
	# info a guardar
	if bullshiters_density > 0:
		num_agents_R = len(semantics_list)
		num_agents_RI = 0
	if overcautios_density > 0:
		num_agents_R = 0
		num_agents_RI = len(semantics_list)
		

	signal_mean = np.mean(SIGNAL_MEAN, dtype=np.float32)
	signal_std = np.std(SIGNAL_MEAN, dtype=np.float32)
	noise_mean = np.mean(NOISE_MEAN, dtype=np.float32)
	noise_std = np.std(NOISE_MEAN, dtype=np.float32)
	redund_mean = np.mean(RED_M, dtype=np.float32)
	redund_std = np.mean(RED_S, dtype=np.float32)
	D_mean = np.mean(D, dtype=np.float32)
	D_std = np.std(D, dtype=np.float32)
		
	time_neg_mean = np.mean(time, dtype=np.float32)
	time_neg_std = np.std(time, dtype=np.float32)
	FP_mean = np.mean(FP, dtype=np.float32)
	FP_std = np.std(FP, dtype=np.float32)
	FN_mean = np.mean(FN, dtype=np.float32)
	FN_std = np.std(FN, dtype=np.float32)
	TP_mean = np.mean(TP, dtype=np.float32)
	TP_std = np.std(TP, dtype=np.float32)
	TN_mean = np.mean(TN, dtype=np.float32)
	TN_std = np.std(TN, dtype=np.float32)

	red_init_mean = np.mean(rmi_mean, dtype=np.float32)
	red_init_std = np.std(rmi_mean, dtype=np.float32)

	meb1mean = np.mean(bis1, dtype=np.float32)
	#bullshit_mean = np.mean(Bullshit)
	#bullshit_std = np.std(Bullshit)
	#gwc_mean = np.mean(GWC)
	#gwc_std = np.std(GWC)
	#lwc_mean = np.mean(LWC)
	#lwc_std = np.std(LWC)
	"""
	data_to_save.write(id_label + " ")
	data_to_save.write(configuration_string + " ")
	data_to_save.write(str(num_agents_R) + " ")
	data_to_save.write(str(num_agents_RI) + " ")
	data_to_save.write(str(D_mean) + " ")
	data_to_save.write(str(D_std) + " ")
	data_to_save.write(str(resource_boundness_density) + " ")
	data_to_save.write(str(time_neg_mean) + " ")
	data_to_save.write(str(time_neg_std) + " ")
	data_to_save.write(str(FP_mean) + " ")
	data_to_save.write(str(FP_std) + " ")
	data_to_save.write(str(FN_mean) + " ")
	data_to_save.write(str(FN_std) + " ")
	data_to_save.write(str(TP_mean) + " ")
	data_to_save.write(str(TP_std) + " ")
	data_to_save.write(str(TN_mean) + " ")
	data_to_save.write(str(TN_std) + " ")
		
	data_to_save.write(str(bullshit_mean) + " ")
	data_to_save.write(str(bullshit_std) + " ")
	data_to_save.write(str(gwc_mean) + " ")
	data_to_save.write(str(gwc_std) + " ")
	data_to_save.write(str(lwc_mean) + " ")
	data_to_save.write(str(lwc_std) + "\n")
	"""
	#data_to_save.close()
	
	#print("End", len(ssc) *M, "negotiations with", number_agents, "PAFs agents...")
	print("End", M, "negotiations with", number_agents, "PAFs agents...")
	return id_label, configuration_string, num_agents_R, num_agents_RI, D_mean, D_std, resource_boundness_density, time_neg_mean,time_neg_std, FP_mean, FP_std, FN_mean, FN_std, TP_mean, TP_std, TN_mean, TN_std, redund_mean, redund_std, signal_mean, signal_std, noise_mean, noise_std, red_init_mean, red_init_std, meb1mean
	
""" 
def get_semantics_configurations(number_agents):
	semantics_set = []
	
	for i in range(0, number_agents + 1):
		S = []
		if i == 0:
			for j in range(number_agents):
				S.append(False)
			semantics_set.append(S)
		else:
			for w in range(i):
				S.append(True)
				
			for k in range(i, number_agents):
				S.append(False)
				
			semantics_set.append(S)
	
	return semantics_set

def get_sample_semantics_configurations(number_agents, step, semantics_configurations):
	sample = []
	for i in range(0, len(semantics_configurations), step):
		sample.append(semantics_configurations[i])
		
	if semantics_configurations[len(semantics_configurations) - 1] not in sample:
		sample.append(semantics_configurations[len(semantics_configurations) - 1])
	
	return sample
"""
