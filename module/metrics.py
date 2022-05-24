#!/usr/bin/env python
# -*- coding: utf-8 -*-

# semantica r
#TP = R / (Re + Ne) --> R = [0, Re] --> TP = R / Re
#TN = N + I \int N+ = Ne / (Re + Ne) --> Ne = [0, Ne] --> TN = Ne / Ne
#FP = \emptyset = FP = 0
#FN = I \int Re / (Re + Ne) --> I int Re = [0, Re] --> FN = (I int Re) / Re
			
# semantica ri
#TP = Re / (Re + Ne) = 1
#TN = N / (Re + Ne)
#FP = In / (Re + Ne)
#FN = 0

from numpy import mean, std

def get_re_taf(agent_taf):
	return set(agent_taf.get_all_attacks())

def collect_attacks(label, lista, otra_lista):
	return [(i, label) for i in lista if i in otra_lista]

def get_i_paf(agent_paf):
	practical = agent_paf.get_practical_base_structures()
	epistemic = agent_paf.get_epistemic_base_structures()
	epistemic_labels = agent_paf.get_ep_labels()

	possible_attacks = []
	for argument in practical:
		label = argument[0]
		if len(argument[5]) > 0:
			possible_attacks = possible_attacks + collect_attacks(label, argument[5], epistemic_labels)
	
	for argument in epistemic:
		label = argument[0]
		if len(argument[2]) > 0:
			possible_attacks = possible_attacks + collect_attacks(label, argument[2], epistemic_labels)

	return set(possible_attacks)

def get_r_paf(agent_paf):
	practical = agent_paf.get_practical_base_structures()
	epistemic = agent_paf.get_epistemic_base_structures()

	epistemic_labels = agent_paf.get_epistemic_base_labels()

	attacks = set()
	for argument in practical:
		if len(argument[3]) > 0:
			label = argument[0]
			for i in argument[3]:
				if i in epistemic_labels:
					attacks.add((i, label))
	
	for argument in epistemic:
		if len(argument[1]) > 0:
			label = argument[0]
			for i in argument[1]:
				if i in epistemic_labels:
					attacks.add((i, label))

	return attacks

# metric 1: FP, FN, TP, TN
def metric1(agent_taf, agent_paf):

	tp, tn, fp, fn = 0, 0, 0, 0

	r = get_r_paf(agent_paf)
	re = get_re_taf(agent_taf)
	i = get_i_paf(agent_paf)

	len_r = len(r)
	len_re = len(re)
	len_i = len(i)
	len_total = agent_taf.get_maximum_attacks_number()
	len_ne = len_total - len_re
	len_n = len_ne - (len_i - len(i.intersection(re)))


	if agent_paf.semantic_r == True:
		if len_re > 0:
			tp = float(len_r / len_re)
			tn = 1
			fp = 0
			fn = float(len(re.intersection(i)) / len_re)
		else:
			tp = 1
			tn = 1
			fp = 0
			fn = 0

	else:
		if len_ne > 0:
			tp = 1
			tn = len_n / len_ne
			fp = (len_i - len(i.intersection(re))) / len_ne
			fn = 0
		else:
			tp = 1
			tn = 1
			fp = 0
			fn = 0

	return tp, tn, fp, fn

def get_agent_from_agents(name, agents):
	for agent in agents:
		if agent.get_agent_name() == name:
			return agent
	return -1
	
def metric(agents_taf, agents_paf):
	TP, TN, FP, FN = [], [], [], []
	
	append_TP, append_TN, append_FP, append_FN = TP.append, TN.append, FP.append, FN.append

	for agent in agents_taf:
		agent_p = get_agent_from_agents(agent.get_agent_name(), agents_paf)
		tp, tn, fp, fn = metric1(agent, agent_p)
		append_TP(tp)
		append_TN(tn)
		append_FP(fp)
		append_FN(fn)
	
	return mean(TP), mean(TN), mean(FP), mean(FN)
	
"""	
def metric_bullshit(agents_paf, taf_plus):
	taf_plus_acceptable_arguments_labels = taf_plus.get_acceptable_arguments()

	bullshit = []

	append = bullshit.append

	for agent_paf in agents_paf:
		agent_paf_acceptable_arguments_labels = agent_paf.get_acceptable_arguments()
		if len(agent_paf_acceptable_arguments_labels) > 0:
			normalization_factor = len(agent_paf_acceptable_arguments_labels)
			acc_in_paf_but_not_in_taf_plus = len(agent_paf_acceptable_arguments_labels.difference(taf_plus_acceptable_arguments_labels))
			len_bullshit = float(acc_in_paf_but_not_in_taf_plus / normalization_factor)
		else:
			len_bullshit = 0

		append(len_bullshit)

	mean_bullshit, std_bullshit = mean(bullshit), std(bullshit)

	return mean_bullshit, std_bullshit

def metric_global_wrongfully_cautious(agents_paf, taf_plus):
	taf_plus_acceptable_arguments_labels = taf_plus.get_acceptable_arguments()

	global_wrongfully_cautious = []

	append = global_wrongfully_cautious.append

	for agent_paf in agents_paf:
		agent_paf_acceptable_arguments_labels = agent_paf.get_acceptable_arguments()
		normalization_factor = len(taf_plus_acceptable_arguments_labels)
		taf_plus_self = set()
		for element in taf_plus_acceptable_arguments_labels:
			if agent_paf.name in element:
				taf_plus_self.add(element)
		acc_in_taf_plus_but_not_in_paf = len(taf_plus_self.difference(agent_paf_acceptable_arguments_labels))
		if normalization_factor > 0:
			len_gwc = float(acc_in_taf_plus_but_not_in_paf / normalization_factor)
		else:
			len_gwc = 0
		
		append(len_gwc)

	mean_gwc, std_gwc = mean(global_wrongfully_cautious), std(global_wrongfully_cautious)

	return mean_gwc , std_gwc

def metric_local_wrongfully_cautious(agents_paf, agents_taf):
	agents_paf, agents_taf = list(agents_paf), list(agents_taf)
	
	agents_number = len(agents_paf)

	local_wrongfully_cautious = []

	append = local_wrongfully_cautious.append

	for i in range(agents_number):
		agent_paf_acceptable_arguments = agents_paf[i].get_acceptable_arguments()
		agent_taf_acceptable_arguments = agents_taf[i].get_acceptable_arguments()
		if len(agent_taf_acceptable_arguments) > 0:
			normalization_factor = len(agent_taf_acceptable_arguments)
			acc_in_taf_but_not_in_paf = len(agent_taf_acceptable_arguments.difference(agent_paf_acceptable_arguments))
			len_lwc = float(acc_in_taf_but_not_in_paf / normalization_factor)
		else:
			len_lwc = 0

		append(len_lwc)
	
	mean_lwc, std_lwc = mean(local_wrongfully_cautious), std(local_wrongfully_cautious)

	return mean_lwc , std_lwc
"""

def metric_d(optimal, other):
    if other == optimal:
        return 0
    elif other == -1:
        return 2
    elif other != optimal and other != -1:
        return 1


def metric_redundancy(agents, num_ag, system_attacks, system_aguments):
	obj=[]
	# arguments
	ta=len(system_aguments)
	for ag in agents:
		count=0
		for arg in system_aguments:
			if arg in ag.all_arguments_labels:
				count += 1
		obj.append(float(count/ta))

	# attacks
	tg=len(system_attacks)
	for ag in agents:
		count=0
		for at in system_attacks:
			if at in ag.get_all_attacks():
				count+= 1
		obj.append(float(count/tg))

	return mean(obj), std(obj)

"""
def metric_signal(agents, num_all_attacks):
	signal = []
	for i in range(len(agents)):
		ud = agents[i].get_undercuts(semantic_r=True)
		at = agents[i].get_attacks(semantic_r=True)
		tot = len(ud) + len(at)
		signal.append(tot / num_all_attacks)
	return mean(signal), std(signal)

def metric_noise(agents, num_all_attacks):
	noise = []
	for i in range(len(agents)):
		tot = agents[i].get_num_I()
		noise.append(tot / num_all_attacks)
	return mean(noise), std(noise)

"""

# metric signal true... (acc in paf y acc in taf_plus)
def metric_signal(agents_paf, acc_args_taf_plus):
	bullshit = []

	append = bullshit.append

	for agent_paf in agents_paf:
		agent_paf_acceptable_arguments_labels = agent_paf.get_acceptable_arguments()
		if len(agent_paf_acceptable_arguments_labels) > 0:
			normalization_factor = len(agent_paf_acceptable_arguments_labels)

			acc_in_paf_and_in_taf_plus = len(agent_paf_acceptable_arguments_labels.intersection(acc_args_taf_plus))
			
			len_bullshit = float(acc_in_paf_and_in_taf_plus / normalization_factor)
		else:
			len_bullshit = 0

		append(len_bullshit)

	mean_bullshit, std_bullshit = mean(bullshit), std(bullshit)

	return mean_bullshit, std_bullshit

# metric noise true (acc in paf but not in taf_plus)
def metric_noise(agents_paf, acc_args_taf_plus):
	bullshit = []

	append = bullshit.append

	for agent_paf in agents_paf:
		agent_paf_acceptable_arguments_labels = agent_paf.get_acceptable_arguments()
		if len(agent_paf_acceptable_arguments_labels) > 0:
			normalization_factor = len(agent_paf_acceptable_arguments_labels)

			acc_in_paf_and_not_taf_plus = len(agent_paf_acceptable_arguments_labels.difference(acc_args_taf_plus))
			
			len_bullshit = float(acc_in_paf_and_not_taf_plus / normalization_factor)
		else:
			len_bullshit = 0

		append(len_bullshit)

	mean_bullshit, std_bullshit = mean(bullshit), std(bullshit)

	return mean_bullshit, std_bullshit


def metric_signal_and_noise(agents_paf, acc_args_taf_plus, num_args):
	#print("DEBUG. Number of arguments taf plus: ", num_args)
	#print("DEBUG. List of all arguments: ", len(acc_args_taf_plus))
	signal = []
	noise = []
	for agent in agents_paf:
		signal_ag=0
		noise_ag=0
		ag_acc_args_labels = agent.get_acceptable_arguments()

		if len(ag_acc_args_labels) > 0:
			if len(acc_args_taf_plus) > 0:
				nn = len(ag_acc_args_labels.difference(acc_args_taf_plus))
				noise_ag = float(nn/len(ag_acc_args_labels))

				ss = len(ag_acc_args_labels.intersection(acc_args_taf_plus))
				signal_ag = float(ss/len(ag_acc_args_labels))
				
			else:
				signal_ag = 0
				noise_ag = 1
		else:
			signal_ag=1
			noise_ag=0

		#print("***", signal_ag, noise_ag, signal_ag+noise_ag)
		signal.append(signal_ag)
		noise.append(noise_ag)

	#print("final:", mean(signal), mean(noise))
	return mean(signal), std(signal), mean(noise), std(noise)


def metric_bis_1(agents_paf):
	"""
	promedio y desviacion estandar de la cantidad de 
	argumentos aceptables que tienen los agentes
	"""
	num = []
	for agent in agents_paf:
		n_ag_acc_args = len(agent.get_acceptable_arguments())
		num.append(n_ag_acc_args)
	return mean(num)


