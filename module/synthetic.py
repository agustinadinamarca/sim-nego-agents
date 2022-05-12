#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from random import choice, randint, sample, shuffle, uniform
import numpy.random as npr

from agent import *

def num_total_arguments(args_bases):
    cumsum = 0
    for bs in args_bases:
        cumsum = cumsum + len(bs[0]) + len(bs[1])
    return cumsum

def num_redundant_args(num_total_args, redundancy):
    return int(num_total_args * redundancy)

def get_all_labels(args):
    labels = []
    for bs in args:
        for i in bs[0]:
            labels.append(i[0])
        for j in bs[1]:
            labels.append(j[0])
    return labels

def redundant_args(l, num):
    return npr.choice(l, num, replace=False)


def get_arg(args, label):
    for k in range(len(args)):
        for i in args[k][0]:
            if label == i[0]:
                return i, k, 0
        for j in args[k][1]:
            if label == j[0]:
                return j, k, 1

def add_arg_redundant(args, arg_to_add, m, avoid, typee):
    c = 0
    for k in range(len(args)):
        if k != avoid and c <= m:
            if typee == 0:
                args[k][0].append(arg_to_add)
                c+=1
            else:
                args[k][1].append(arg_to_add)
                c+=1
    return args

def generate_redundancy(args, p):
    res = args.deepcopy()
    for a in res:
        #localizo el arg
        arg = get_arg(args, a)
        #y lo repito en otras bases m veces random
        m = npr.randint(1, high=num_ag, size=1)[0]
        #print(arg, m)
        if arg[2] == 0: #practicao
            arg[0][4] * npr.random()
        res = add_arg_redundant(res, arg[0], m, arg[1], arg[2])
    return res

def get_major_agent_from_agents(agents):

	name = "MajorAgent"

	alternatives = set()
	practical_arguments, epistemic_arguments = [], []
	count = 0

	for agent in agents:
		if count == 0:
			alternatives = agent.get_alternatives()
		count = count + 1
		practical_arguments = practical_arguments + [argument for argument in agent.get_practical_base_structures()]
		epistemic_arguments = epistemic_arguments + [argument for argument in agent.get_epistemic_base_structures()]

	# remuevo argumentos duplicados
	my_args_p = []
	to_rem_p = []
	for a in practical_arguments:
		if a[0] not in my_args_p:
			my_args_p.append(a[0])
		else:
			to_rem_p.append(a)
	for i in to_rem_p:
		practical_arguments.remove(i)

	my_args_e = []
	to_rem_e = []
	for a in epistemic_arguments:
		if a[0] not in my_args_e:
			my_args_e.append(a[0])
		else:
			to_rem_e.append(a)
	for i in to_rem_e:
		epistemic_arguments.remove(i)

	return Agent("MajorAgent", alternatives, epistemic_arguments, practical_arguments, semantic_r=True)

def create_agents(number_agents, alternatives_number, maximum_number_practical_arguments,
 maximum_number_epistemic_arguments, maximum_attacks_density_value, redundancy):
	
	if number_agents >= 1 and alternatives_number >= 2 and isinstance(alternatives_number, int) and maximum_attacks_density_value >= 0 and maximum_attacks_density_value <= 1 and maximum_number_epistemic_arguments >= 1 and maximum_number_practical_arguments >= alternatives_number:

		agents = set()
	
		#goals_bases = create_goals_bases(number_agents, maximum_number_goals)

		alternatives = create_alternatives(alternatives_number)
		
		arguments, ext = create_arguments(number_agents,
										 maximum_number_practical_arguments,
										 maximum_number_epistemic_arguments,
										 maximum_attacks_density_value,
										 alternatives)
		
		# los args ext pueden estar mal (no se para que servian)
		#n = num_total_arguments(arguments)
		#r = num_redundant_args(num_total_args=n, redundancy=redundancy)
		#labels = get_all_labels(arguments)
		#selected_args = redundant_args(labels, r)
		#arguments = generate_redundancy(arguments, red_args=selected_args, num_ag=number_agents)


		add = agents.add
		for i in range(number_agents):
			agent = Agent("".join(["Ag", str(i + 1)]), alternatives, arguments[i][1], arguments[i][0], semantic_r=True)
			args_epistemic_number, args_practical_number = len(arguments[i][1]), len(arguments[i][0])

			number_internal = args_practical_number * args_epistemic_number + args_epistemic_number * (args_epistemic_number - 1) / 2
			agent.maximum_attacks_number = ext[i] + number_internal
			add(agent)
		
		return agents

	else:
		return -1	 

def create_arguments(number_agents, maximum_number_practical_arguments, maximum_number_epistemic_arguments,
		 maximum_attacks_density_value, alternatives):

	arguments_bases = []

	alternatives_number = len(alternatives)

	for i in range(number_agents):
		practical_arguments_number = randint(alternatives_number, maximum_number_practical_arguments)
		epistemic_arguments_number = randint(1, maximum_number_epistemic_arguments)
		
		maximum_attacks_number = practical_arguments_number * epistemic_arguments_number + epistemic_arguments_number * (epistemic_arguments_number - 1) / 2
		
		#attacks_density_value = uniform(0.1, maximum_attacks_density_value)
		attacks_density_value = maximum_attacks_density_value

		attacks_number = round(maximum_attacks_number * attacks_density_value, 0)
		
		ide = str(i + 1)

		practical_arguments_base = ["".join(["ap", str(j + 1), "Ag", ide]) for j in range(practical_arguments_number)]

		epistemic_arguments_base = ["".join(["ae", str(j + 1), "Ag", ide]) for j in range(epistemic_arguments_number)]
		
		#for j in range(practical_arguments_number):
		#	practical_arguments_base.append("ap" + str(j + 1) + "Ag" + str(i + 1))

		#for j in range(epistemic_arguments_number):
		#	epistemic_arguments_base.append("ae" + str(j + 1) + "Ag" + str(i + 1))

		all_arguments = [practical_argument for practical_argument in practical_arguments_base]

		#for practical_argument in practical_arguments_base:
		#	all_arguments.append(practical_argument)
		all_arguments = all_arguments + [epistemic_argument for epistemic_argument in epistemic_arguments_base]
		#for epistemic_argument in epistemic_arguments_base:
		#	all_arguments.append(epistemic_argument)

		########################
		
		#all_attacks = []
			
		# EPISTEMIC_INT, PRACTICAL_INT
		all_attacks = [(ep, pr) for ep in epistemic_arguments_base for pr in practical_arguments_base]
		#for ep in epistemic_arguments_base:
		#	for pr in practical_arguments_base:
		#		all_attacks.append((ep, pr))
			
		# arreglar pra que no haya 12 o 21, solo una posibilidad
		# EPISTEMIC_INT, EPISTEMIC_INT
		le = len(epistemic_arguments_base)
		for i in range(le):
			for j in range(le):
				if j < i:
					l = [epistemic_arguments_base[i], epistemic_arguments_base[j]]
					shuffle(l)
					l = tuple(l)
					all_attacks.append(l)
		#print(len(practical_arguments_base), len(epistemic_arguments_base), len(all_attacks))	
		#print(all_attacks)
		# selecciono un porcentaje de ellos
		#list_indices = []
		#for i in range(len(all_attacks)):
		#	list_indices.append(i)
		list_indices = [i for i in range(len(all_attacks))]
		#print(list_indices)
		#print(attacks_number, len(list_indices))
		selection = sample(list_indices, int(attacks_number))
		#print(len(selection))
		#attacks = set()
		#for index in selection:
		#	attacks.add(all_attacks[index])
		attacks = {all_attacks[index] for index in selection}
		
		################################################################
		alternatives_list_variable = list(alternatives)
		alternatives_list = list(alternatives)

		if alternatives_number < practical_arguments_number:
			alternatives_list_variable = alternatives_list_variable + [choice(alternatives_list) for j in range(practical_arguments_number - alternatives_number)]	
		
		practical_base = []
		index = 0

		for practical_argument_label in practical_arguments_base:

			type_label = choice(["P", "C"])
			certainty_value = uniform(0, 1)

			practical_argument_structure = (practical_argument_label, type_label, alternatives_list_variable[index], [], certainty_value, [], [])

			for attack in attacks:
				if practical_argument_label == attack[1]:
					practical_argument_structure[3].append(attack[0])
				if practical_argument_label == attack[0]:
					practical_argument_structure[6].append(attack[1]) # agrego argumento que es atacado por el argumento

			practical_base.append(practical_argument_structure)

			index = index + 1
			
		epistemic_base = []

		for epistemic_argument_label in epistemic_arguments_base:

			epistemic_argument_structure = (epistemic_argument_label, [], [], [])

			for attack in attacks:
				if epistemic_argument_label == attack[1]:
					epistemic_argument_structure[1].append(attack[0])
				if epistemic_argument_label == attack[0]:
					epistemic_argument_structure[3].append(attack[1])

			epistemic_base.append(epistemic_argument_structure)
			
		arguments_bases.append([practical_base, epistemic_base])

	#print(arguments_bases, "OKONO")
	#return -11
	arguments_bases, ext = create_external_attacks(arguments_bases, maximum_attacks_density_value)

	return arguments_bases, ext

def get_remaining_bases(current_bases, arguments_bases):
	return [agent_bases for agent_bases in arguments_bases if current_bases != agent_bases]

def get_epistemic_labels_from_remaining_bases(remaining_bases):
	return [argument_structure[0] for bases in remaining_bases for argument_structure in bases[1]]

def get_arguments_number(agent_arguments_bases):
	return len(agent_arguments_bases[0]) + len(agent_arguments_bases[1])

def is_already_attacked(argument_structure_seggested, external_epictemic_label):
	if len(argument_structure_seggested) == 4:
		if external_epictemic_label in argument_structure_seggested[1]:
			return True
		else:
			return False
	else:
		if external_epictemic_label in argument_structure_seggested[3]:
			return True
		else:
			return False

def get_all_arguments_from_agent_bases(agent_bases):
	arguments = [practical_argument for practical_argument in agent_bases[0]]
	arguments = arguments + [epistemic_argument for epistemic_argument in agent_bases[1]]
	return arguments

def select_possible_argument_to_be_attacked(agent_bases):

	arguments = get_all_arguments_from_agent_bases(agent_bases)
	arguments_number = len(arguments)

	if arguments_number > 0:
		index = randint(0, arguments_number - 1) 
		return arguments[index]
	else:
		return -1

def is_mutual_attack(label_argument_to_be_attacked, argument_structure_that_wants_to_attack):
	if len(argument_structure_that_wants_to_attack) != 4:
		return False
	else:
		if label_argument_to_be_attacked in argument_structure_that_wants_to_attack[1]:
			return True
		else:
			return False

def get_argument_structure_from_label(remaining_bases, argument_label):
	for bases in remaining_bases:
		for argument in bases[0]:
			if argument_label == argument[0]:
				return argument

		for argument in bases[1]:
			if argument_label == argument[0]:
				return argument

	return -1

def add_attacked_by(attack_label, argument_structure, agent_bases):
	if isinstance(attack_label, str):
		#print(attack_label, argument_structure, "ver")
		if len(argument_structure) == 4:
			argument_label = argument_structure[0]
			l = len(agent_bases[1])
			for i in range(l):
				if agent_bases[1][i][0] == argument_label:
					r = list(agent_bases[1][i])
					r[4].append(attack_label)
					agent_bases[1][i] = tuple(r)
					return agent_bases
			#print("D")
			return -1

		elif len(argument_structure) == 7:
			argument_label = argument_structure[0]
			l = len(agent_bases[0])
			for i in range(l):
				if agent_bases[0][i][0] == argument_label:
					r = list(agent_bases[0][i])
					r[6].append(attack_label)
					agent_bases[0][i] = tuple(r)
					return agent_bases
			#print("C")
			return -1

		else:
			#print("B")
			return -1

	else:
		#print("A")
		return -1

def add_effective_attack(argument_structure, attack_label, agent_bases):

	if isinstance(attack_label, str):
		#print(attack_label, argument_structure, "ver-addefectiveatack")
		if len(argument_structure) == 4:
			argument_label = argument_structure[0]
			l = len(agent_bases[1])
			for i in range(l):
				if agent_bases[1][i][0] == argument_label:
					r = list(agent_bases[1][i])
					r[1].append(attack_label)
					agent_bases[1][i] = tuple(r)
					return agent_bases

			return -1

		elif len(argument_structure) == 7:
			argument_label = argument_structure[0]
			l = len(agent_bases[0])
			for i in range(l):
				if agent_bases[0][i][0] == argument_label:
					r = list(agent_bases[0][i])
					r[3].append(attack_label)
					agent_bases[0][i]= tuple(r)
					return agent_bases
			return -1

		else:
			return -1

	else:
		return -1

def create_external_attacks(arguments_bases, maximum_attacks_density_value):

	max_ext_attacks_number = []
	lab = len(arguments_bases)
	all_new_attacks = set() # guardo todos los ataques que voy a agregar al sistema
	for i in range(lab):
		remaining_bases = get_remaining_bases(arguments_bases[i], arguments_bases)
		epistemic_labels_from_remaining_bases = get_epistemic_labels_from_remaining_bases(remaining_bases)
		argument_number_current_bases = get_arguments_number(arguments_bases[i])
		external_arguments_number = len(epistemic_labels_from_remaining_bases)
		maximum_attacks_number_from_external_arguments = argument_number_current_bases * external_arguments_number
		attacks_density_value = uniform(0, 1) * maximum_attacks_density_value
		attacks_to_add_number = round(attacks_density_value * maximum_attacks_number_from_external_arguments, 0)

		max_ext_attacks_number.append(maximum_attacks_number_from_external_arguments)

		effective_attacks_added_number = 0

		while effective_attacks_added_number < attacks_to_add_number:
			# tomo un argumento al azar de los restantes
			external_argument_label_selected = choice(epistemic_labels_from_remaining_bases)
			
			possible_argument_structure_to_be_attacked = select_possible_argument_to_be_attacked(arguments_bases[i])
			possible_argument_label_to_be_attacked = possible_argument_structure_to_be_attacked[0]
			# checkeo que no repita ese mismo ataque
			attack_status = is_already_attacked(possible_argument_structure_to_be_attacked, external_argument_label_selected)
			#checkeo que si se agraga a un epistemic, no exista el ataue mutuo
			external_argument_structure_selected = get_argument_structure_from_label(remaining_bases, external_argument_label_selected)
			mutual_status = is_mutual_attack(possible_argument_label_to_be_attacked, external_argument_structure_selected)
			# lo incorporo como ataque a un practico o epistemico en la base corriente
			if attack_status == False and mutual_status == False:
				# añado ataque
				#print(arguments_bases[i], "1")
				arguments_bases[i] = add_effective_attack(possible_argument_structure_to_be_attacked, external_argument_label_selected, arguments_bases[i])
				#print(arguments_bases[i], "2")
				#print(possible_argument_label_to_be_attacked, external_argument_structure_selected, "OK???")
				# problema con argument_bases...
				#arguments_bases[i] = add_attacked_by(possible_argument_label_to_be_attacked, external_argument_structure_selected, arguments_bases[i])
				#print(arguments_bases[i], "3")
				effective_attacks_added_number = effective_attacks_added_number + 1
				all_new_attacks.add((external_argument_label_selected, possible_argument_structure_to_be_attacked[0]))

	for attack in all_new_attacks:
		name = from_label_extract_agent_name(attack[0])
		arguments_bases = from_agent_name_return_base(arguments_bases, name, attack)
	return arguments_bases, max_ext_attacks_number


def last_function(bases, attacks):
	for attack in attacks:
		name = from_label_extract_agent_name(attack[0])
		bases = from_agent_name_return_base(bases, name)
	
	
def from_label_extract_agent_name(label):
	return label[-3::]

def from_agent_name_return_base(bases, name, attack):
	for base in bases:
		if name in base[0][0][0]:
			#print("ok")
			for arg in base[1]:
				if arg[0] == attack[0]:
					arg1 = list(arg)
					arg1[3].append(attack[1])
					arg = arg1
					return bases

	return -1
	
def create_alternatives(number_alternatives):

	if number_alternatives >= 0 and isinstance(number_alternatives, int):

		#alternatives = set()

		#for i in range(number_alternatives):
		#	alternatives.add("X" + str(i + 1)) 
		
		#return alternatives
		return {"".join(["X", str(i + 1)]) for i in range(number_alternatives)}

	else:
		return -1

def create_paf_agent(agent, resource_boundness_density, semantic_r, external_epistemic_arguments_list):
	practical_base = agent.get_practical_base_structures()
	epistemic_base = agent.get_epistemic_base_structures()
	#goals_base = agent.get_goals_base()
	agent_name = agent.get_agent_name()
	alternatives = agent.get_alternatives()


	# modifico bases segun kinit y kturn
	new_practical_base, new_epistemic_base = modify_agent_arguments_bases(practical_base, epistemic_base, external_epistemic_arguments_list, resource_boundness_density)
	#print("okkk??", new_practical_base, new_epistemic_base)
	return Agent(agent_name, alternatives, new_epistemic_base, new_practical_base, semantic_r)

def create_paf_agents(taf_agents, resource_boundness_density, semantics_r):
	paf_agents = []
	number_agents = len(taf_agents)
	taf_agents = deepcopy(list(taf_agents))
	arguments_bases = []
	for i in range(number_agents):
		arguments_bases.append([taf_agents[i].get_practical_base_structures(), taf_agents[i].get_epistemic_base_structures()])
		
	for i in range(number_agents):
		current_bases = [taf_agents[i].get_practical_base_structures(), taf_agents[i].get_epistemic_base_structures()]

		remaining_bases_list = get_remaining_bases(current_bases, arguments_bases)
		external_epistemic_arguments_labels_list = get_epistemic_labels_from_remaining_bases(remaining_bases_list)
		paf_agent = create_paf_agent(taf_agents[i], resource_boundness_density, semantics_r[i], external_epistemic_arguments_labels_list)
		paf_agents.append(paf_agent)
	
	# NUEVA PARTE
	final(paf_agents)
	
	return paf_agents


def get_certain_attacks_number_agent(practical_base, epistemic_base):
	certain_attacks_number = 0

	for practical_argument in practical_base:
		certain_attacks_number += len(practical_argument[3])

	for epistemic_argument in epistemic_base:
		certain_attacks_number += len(epistemic_argument[1])

	return certain_attacks_number

def get_labels_from_arguments_list(arguments_list):
	#labels = set()

	#for argument in arguments_list:
	#	labels.add(argument[0])

	#return labels
	return {argument[0] for argument in arguments_list}

def get_certain_attacks_from_bases(practical_base, epistemic_base):
	all_attacks = []
	
	for practical_argument in practical_base:
		if len(practical_argument[3]) > 0:
			for label in practical_argument[3]:
				all_attacks.append((label, practical_argument[0]))
	
	for epistemic_argument in epistemic_base:
		if len(epistemic_argument[1]) > 0:
			for label in epistemic_argument[1]:
				all_attacks.append((label, epistemic_argument[0]))
	
	return all_attacks
	
def get_attacks_to_remove_set(number, all_set):
	num_attacks_set = len(all_set)
	# selección del conjunto de ataques seguros para pasar a indeterminados
	indices_list = []
	for i in range(num_attacks_set):
		indices_list.append(i)
	
	select_attacks_indices = sample(population=indices_list, k=number) # sin reemplazo
	
	attacks_to_be_remove = []
	
	for i in select_attacks_indices:
		attacks_to_be_remove.append(all_set[i])
	
	return attacks_to_be_remove
	
def attacks_to_indeterminated_method(attacks, epistemic_base, practical_base):
	
	eps = deepcopy(epistemic_base)
	prs = deepcopy(practical_base)
	
	le = len(eps)
	lp = len(prs)
	
	for attack in attacks:
		label1, label2 = attack
		
		if "ae" in label2:
			for i in range(le):
				if eps[i][0] == label2:
					arg = list(eps[i])
					arg[1].remove(label1)
					arg[2].append(label1)
					arg = tuple(arg)
					eps[i] = arg
					break
		else:
			for i in range(lp):
				if prs[i][0] == label2:
					arg = list(prs[i])
					arg[3].remove(label1)
					arg[5].append(label1)
					arg = tuple(arg)
					prs[i] = arg
					break
	
	return eps, prs
	
def all_attacks_minus_certain_attacks(practical_base, epistemic_base, certain_attacks_initial, external_epistemic_arguments_labels):
	practical_base_labels = get_labels_from_arguments_list(practical_base) # set
	epistemic_base_labels = list(get_labels_from_arguments_list(epistemic_base))# set
	
	all_attacks = []
	
	# EPISTEMIC_INT, PRACTICAL_INT
	for ep in epistemic_base_labels:
		for pr in practical_base_labels:
			all_attacks.append((ep, pr))
	
	# arreglar pra que no haya 12 o 21, solo una posibilidad
	# EPISTEMIC_INT, EPISTEMIC_INT
	le = len(epistemic_base_labels)
	for i in range(le):
		for j in range(le):
			if j < i:
				l = [epistemic_base_labels[i], epistemic_base_labels[j]]
				shuffle(l)
				l = tuple(l)
				all_attacks.append(l)
	
	for ex in external_epistemic_arguments_labels:
		for ep in epistemic_base_labels:
			all_attacks.append((ex, ep))
		for pr in practical_base_labels:
			all_attacks.append((ex, pr))

	for element in certain_attacks_initial:
		if element in all_attacks:
			all_attacks.remove(element)
		
	return all_attacks

def inteterminations_selection(set_non_attacks, number):
	indices = []
	for i in range(number):
		indices.append(i)
	
	selection = sample(population=indices, k=number) # sin reemplazo
	
	new_list = []
	for i in selection:
		new_list.append(set_non_attacks[i])
	return new_list


def get_strcuture_from_label_and_bases(epistemic_base, practical_base, label):
	if "ae" in label:
		for i in epistemic_base:
			if i[0] == label:
				return i
	else:
		for i in practical_base:
			if i[0] == label:
				return i

# agarro no ataques y los coloco como indeterminados
def make_indeterminations_in_bases(epistemic_base, practical_base, indeterminations_set):
	leb = len(epistemic_base)
	lpb = len(practical_base)
	for attack in indeterminations_set:
		label1, label2 = attack
		
		if "ae" in label2: # label2 epistémica
			for i in range(leb):
				if epistemic_base[i][0] == label2: # si la etiqueta de la estructura coincide con la etiqueta label2
					arg = list(epistemic_base[i]) # transformo en lista la estructura
					#la = arg[0] # guardo etiqueta ???
					arg[2].append(label1) # coloco el label1 en ataque indeterminado
					# hay que tomar label1, buscar su estructura, y añadir arg[0] a la lista de atacados
					arg = tuple(arg) # lo transformo a tupla
					epistemic_base[i] = arg # asigno modificacion
					break
					#other_arg_structure = get_strcuture_from_label_and_bases(epistemic_base, practical_base, label1)
					#other_arg_structure = list(other_arg_structure)
					#oa = other_arg_structure[0]
					#other_arg_structure[3].append(la)
					#other_arg_structure = tuple(other_arg_structure)
					#for j in range(leb):
					#	if epistemic_base[j][0] == oa:
					#		epistemic_base[j] = other_arg_structure
					#		break
					#break
		else:
			for i in range(lpb):
				if practical_base[i][0] == label2:
					arg = list(practical_base[i])
					#la = arg[0]
					arg[5].append(label1)
					arg = tuple(arg)
					practical_base[i] = arg
					break
					#other_arg_structure = get_strcuture_from_label_and_bases(epistemic_base, practical_base, label2)
					#other_arg_structure = list(other_arg_structure)
					#other_arg_structure[3].append(la)
					#oa = other_arg_structure[0]
					#other_arg_structure = tuple(other_arg_structure)
					#for j in range(leb):
					#	if epistemic_base[j][0] == oa:
					#		epistemic_base[j] = other_arg_structure
					#		break
					#		
					#break
	
	return epistemic_base, practical_base
				
def filter_attacks_by_agent_name(attacks_set, agent_name):
	filtered_set = set()
	if attacks_set != set():
		#for attack in attacks_set:
		#	if agent_name in attack[0]:
		#		filtered_set.add(attack)
		filtered_set = {attack for attack in attacks_set if agent_name in attack[0]}
	return filtered_set

def add_external_attacks_(filtered_attacks, paf_agent):
	if filtered_attacks != set():
		for attack in filtered_attacks:
			# añado en la parte epistemica
			paf_agent.set_attacked_by(attack)

def get_all_agents_attacks(agents):
	all_attacks = set()
	for agent in agents:
		to_add = get_all_agent_attacks_certain_and_uncertain(agent)
		all_attacks = all_attacks.union(to_add)
	return all_attacks

def final(agents):
	attacks_system = get_all_agents_attacks(agents)
	for agent in agents:
		filtered = filter_attacks_by_agent_name(attacks_system, agent.get_agent_name())
		attacks_system = attacks_system.difference(filtered) # CHECK
		add_external_attacks_(filtered, agent)

def get_all_agent_attacks_certain_and_uncertain(agent):
	practical_base = agent.get_practical_base_structures()
	epistemic_base = agent.get_epistemic_base_structures()
	attacks = set()
	for argument in practical_base:
		if len(argument[3]) > 0:
			for label in argument[3]:
				attacks.add((label, argument[0]))
		if len(argument[5]) > 0:
			for label in argument[5]:
				attacks.add((label, argument[0]))
	for argument in epistemic_base:
		if len(argument[1]) > 0:
			for label in argument[1]:
				attacks.add((label, argument[0]))
		if len(argument[2]) > 0:
			for label in argument[2]:
				attacks.add((label, argument[0]))
	return attacks
	

def modify_agent_arguments_bases(practical_base, epistemic_base, external_epistemic_arguments_set, resource_boundness_density=0):
	
	internal_practical_arguments_number = len(practical_base)
	internal_epistemic_arguments_number = len(epistemic_base)
	external_epistemic_arguments_number = len(external_epistemic_arguments_set)
	internal_arguments_number = internal_practical_arguments_number + internal_epistemic_arguments_number
	internal_arguments = practical_base + epistemic_base
	internal_epistemic_arguments_labels = get_labels_from_arguments_list(epistemic_base)


	certain_attacks_number = get_certain_attacks_number_agent(practical_base, epistemic_base)
	maximum_relations_number = internal_practical_arguments_number * internal_epistemic_arguments_number + internal_epistemic_arguments_number * (internal_epistemic_arguments_number - 1) / 2 + internal_practical_arguments_number * external_epistemic_arguments_number + internal_epistemic_arguments_number * external_epistemic_arguments_number
	maximum_relations_number = int(maximum_relations_number)
	certain_non_attacks_number = int(maximum_relations_number - certain_attacks_number)
	#print("certain_non_attacks_number", certain_non_attacks_number)
	# cantidad de relaciones que no puedo procesar
	certain_non_deteminations_number = int(round(maximum_relations_number * resource_boundness_density, 0))

	#print(internal_practical_arguments_number)
	#print(internal_epistemic_arguments_number)
	#print(external_epistemic_arguments_number)
	#print(internal_arguments_number)
	#print(internal_arguments)
	#print(internal_epistemic_arguments_labels)
	#print(certain_attacks_number)
	#print(maximum_relations_number)
	#print(certain_non_attacks_number)
	#print(certain_non_deteminations_number)

	# ataques seguros a remover y colocar como indeterminados
	#NON_DETERMINATION_NUMBER = 5
	#ATTACKS_NUMBER = 5
	#NON_ATTACKS_NUMBER = 8
	
	count, attacks_to_indeterminated, non_attacks_to_indeterminated = 0, 0, 0
	
	while count < certain_non_deteminations_number:
		if uniform(0, 1) > 0.5:
			if attacks_to_indeterminated < certain_attacks_number:
				attacks_to_indeterminated = attacks_to_indeterminated + 1
			elif non_attacks_to_indeterminated < certain_non_attacks_number:
				non_attacks_to_indeterminated = non_attacks_to_indeterminated + 1
		else:
			if non_attacks_to_indeterminated < certain_non_attacks_number:
				non_attacks_to_indeterminated = non_attacks_to_indeterminated + 1
			elif attacks_to_indeterminated < certain_attacks_number:
				attacks_to_indeterminated = attacks_to_indeterminated + 1
		count = count + 1
	
	# VERRRRRRRR
	#print("maximum_relations_number", maximum_relations_number)
	#print("certain_attacks_number", certain_attacks_number)
	#print("certain_non_attacks_number", certain_non_attacks_number)
	#print("certain_non_deteminations_number", certain_non_deteminations_number)
	#print("attacks_to_indeterminated", attacks_to_indeterminated)
	
	
	
	#print("non_attacks_to_indeterminated", non_attacks_to_indeterminated)
	attacks_set = get_certain_attacks_from_bases(practical_base, epistemic_base)

	num_attacks_set = len(attacks_set)

	attacks_to_remove = get_attacks_to_remove_set(attacks_to_indeterminated, attacks_set)

	modify = all_attacks_minus_certain_attacks(practical_base, epistemic_base, attacks_set, external_epistemic_arguments_set)
	#print("attacks", attacks_set)
	epistemic_base_new, practical_base_new = attacks_to_indeterminated_method(attacks_to_remove, epistemic_base, practical_base)

	#print("len(modify)", len(modify), "debería ser igual o mayor a non_attacks_to_indeterminated", non_attacks_to_indeterminated)
	#print("nonatacks, modify", modify)
	to_modify = inteterminations_selection(modify, non_attacks_to_indeterminated)
	
	epistemic_base_final, practical_base_final = make_indeterminations_in_bases(epistemic_base_new, practical_base_new, to_modify)

	return practical_base_final, epistemic_base_final
