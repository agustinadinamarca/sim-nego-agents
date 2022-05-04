#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from agentCython import get_argument_structure_from_label, get_certain_attacked_set
#import networkx as nx
#import random

#import itertools 
from functools import lru_cache
from networkx.algorithms.approximation import max_clique
from networkx import Graph, find_cliques
##################################################################################
### DM ARGUMENTATION FRAMEWORK - Amgoud and Prade (2004)
##################################################################################

#def powerset(iterable):
#	s = list(iterable)
#	return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))
	
class CommitmentStore:
	
	def __init__(self):
		self.offers_proposed = []
		self.arguments_presented = []
		self.challenges_made = []

		self.say_nothing = []
		self.external_arguments_added = []
		#self.R = []
		#self.AS = [] # AGUMENTOS QUE SE EMITIO UNA ACEPTABILIDAD O NO
		
	def __eq__(self, other):
		if isinstance(other, CommitmentStore):
			return self.offers_proposed == other.offers_proposed and self.arguments_presented == other.arguments_presented and self.challenges_made == other.challenges_made and self.say_nothing == other.say_nothing and self.external_arguments_added == other.external_arguments_added
		else:
			return False

	def reset(self):
		self.offers_proposed = []
		self.arguments_presented = []
		self.challenges_made = []
		self.say_nothing = []
		self.external_arguments_added = []

	def is_offer_accepted(self, current_offer):
		if current_offer in self.offers_proposed:
			return True
		else:
			return False
			
	def is_no_arguments_to_share(self):
		if True in self.say_nothing:
			return True
		else:
			return False

	def add_proposed_or_accepted_offer(self, offer):
		self.offers_proposed.append(offer)

	def add_argument_presented(self, argument):
		self.arguments_presented.append(argument)

	def get_argument_presented_from_index(self, index):
		if index >= 0 and index < len(self.arguments_presented):
			return self.arguments_presented[index]
		else:
			return -1

	def get_arguments_presented_number(self):
		return len(self.arguments_presented)

	def add_challenge_presented(self, challenge):
		self.challenges_made.append(challenge)
	#def add_Refuse(self, ref):
	#	self.R.append(ref)
	def add_no_arguments(self):
		self.say_nothing.append(True)
		
	def add_external_argument(self, argument_structure):
		status = False
		for i in self.external_arguments_added:
			if argument_structure[0] == i[0]:
				status = True
				break
		if status == False:
			self.external_arguments_added.append(argument_structure)

# Case: inconsistence bases y criterio bipolar de Amgoud and Prade 2009
# The framework computes the ‘best’ decision (if it exists)

def filter_external_attacks(arguments, agent_name):
	#filtered = set()
	#for arg in arguments:
	#	if agent_name in arg:
	#		filtered.add(arg)
	#return filtered
	return {arg for arg in arguments if agent_name in arg}
		
class Agent:
	def __init__(self, agent_name, alternatives, epistemic_base, practical_base, semantic_r=True):
		self.name = agent_name
		self.alternatives = alternatives
		self.epistemic_base = epistemic_base
		self.practical_base = practical_base
		self.commitment_store = CommitmentStore()
		self.negotiation = Agent.Negotiation(self)
		self.semantic_r = semantic_r
		# PRUEBA
		self.epistemic_labels = Agent.get_epistemic_base_labels(self)
		self.practical_labels = Agent.get_practical_base_labels(self)
		self.all_arguments_labels = Agent.get_all_arguments_labels(self)
	
	def set_attacked_by(self, attack):
		l = len(self.epistemic_base)
		for i in range(l):
			if self.epistemic_base[i][0] == attack[0]:
				arg = list(self.epistemic_base[i])
				if attack[1] not in arg[3]:
					arg[3].append(attack[1])
				arg = tuple(arg)
				self.epistemic_base[i] = arg

	def get_agent_name(self):
		return self.name

	def get_ep_labels(self):
		return self.epistemic_labels

	def get_pr_labels(self):
		return self.practical_labels

	def get_all_labels(self):
		return self.all_arguments_labels

	def get_alternatives(self):
		return self.alternatives

	def get_practical_base_structures(self):
		return self.practical_base
		
	def get_epistemic_base_structures(self):
		return self.epistemic_base

	def get_maximum_attacks_number(self):
		num_p = len(self.get_practical_base_structures())
		num_e = len(self.get_epistemic_base_structures())
		
		return int(num_p * num_e + num_e * (num_e - 1) / 2)
		
	def add_argument_structure_to_base(self, argument_structure):
		if len(argument_structure) > 4:
			self.practical_base.append(argument_structure)
		else:
			self.epistemic_base.append(argument_structure)

	def get_practical_base_labels(self):
		#practical_labels = set()

		#for argument in self.practical_base:
		#	practical_labels.add(argument[0])

		#return practical_labels
		return {argument[0] for argument in self.practical_base}

	def get_epistemic_base_labels(self):
		#epistemic_labels = set()

		#for argument in self.epistemic_base:
		#	epistemic_labels.add(argument[0])

		#return epistemic_labels
		return {argument[0] for argument in self.epistemic_base}

	def get_commitment_store(self):
		return self.commitment_store

	def get_all_arguments_structures(self):
		pb = self.practical_base
		eb = self.epistemic_base
		arguments = pb + eb
		return arguments

	def is_label_in_arguments_base(self, argument_label):
		arguments = self.all_arguments_labels
		if argument_label in arguments:
			return True
		else:
			return False

	def get_num_I(self):
		i = 0
		pb = self.practical_base
		eb = self.epistemic_base
		for ae in eb:
			i += len(ae[2])
		for ap in pb:
			i += len(ap[5])
		return i


	def get_all_arguments_labels(self):
		epistemic_labels = self.get_ep_labels()
		practical_labels = self.get_pr_labels()

		arguments_labels = epistemic_labels.union(practical_labels)

		return arguments_labels
	
	# MUY COSTOSA
	"""
	def get_argument_structure_from_label(self, argument_label):
		if "ap" in argument_label:
			practical_base = self.get_practical_base_structures()

			for practical_argument in practical_base:
				if practical_argument[0] == argument_label:
					return practical_argument

			return -1
		else:
			epistemic_base = self.get_epistemic_base_structures()

			for epistemic_argument in epistemic_base:
				if epistemic_argument[0] == argument_label:
					return epistemic_argument

			return -1
	"""
	def get_certain_attacked_labels_set_from_argument_label(self, argument_label):
		attacked_set = set()
		
		if self.is_label_in_arguments_base(argument_label) == True:
			epistemic_base = self.get_epistemic_base_structures()
			practical_base = self.get_practical_base_structures()
			
			for argument_structure in epistemic_base:
				if argument_label in argument_structure[1]:
					attacked_set.add(argument_structure[0])
	
			for argument_structure in practical_base:
				if argument_label in argument_structure[3]:
					attacked_set.add(argument_structure[0])
				
		return attacked_set

	def get_attackers_of_argument_label(self, argument_label):
		#argument_structure = self.get_argument_structure_from_label(argument_label)
		practical_base = self.get_practical_base_structures()
		epistemic_base = self.get_epistemic_base_structures()
		argument_structure = get_argument_structure_from_label(argument_label, practical_base, epistemic_base)
		if self.semantic_r:
			if len(argument_structure) == 4:
				#real_attackers = set()
				#for label in argument_structure[1]:
				#	if self.is_label_in_arguments_base(label):
				#		real_attackers.add(label)
				#return real_attackers
				return {label for label in argument_structure[1] if self.is_label_in_arguments_base(label)}
			else:
				#real_attackers = set()
				#for label in argument_structure[3]:
				#	if self.is_label_in_arguments_base(label):
				#		real_attackers.add(label)
				#return real_attackers
				return {label for label in argument_structure[3] if self.is_label_in_arguments_base(label)}

		else:
			if len(argument_structure) == 4:
				#real_attackers = set()
				#for label in argument_structure[1]:
				#	if self.is_label_in_arguments_base(label):
				#		real_attackers.add(label)
				#for label in argument_structure[2]:
				#	if self.is_label_in_arguments_base(label):
				#		real_attackers.add(label)
				#return real_attackers
				return set([label for label in argument_structure[1] if self.is_label_in_arguments_base(label)] + [label for label in argument_structure[2] if self.is_label_in_arguments_base(label)])

			else:
				#real_attackers = set()
				#for label in argument_structure[3]:
				#	if self.is_label_in_arguments_base(label):
				#		real_attackers.add(label)
				#for label in argument_structure[5]:
				#	if self.is_label_in_arguments_base(label):
				#		real_attackers.add(label)
				#return real_attackers
				return set([label for label in argument_structure[3] if self.is_label_in_arguments_base(label)] + [label for label in argument_structure[5] if self.is_label_in_arguments_base(label)])
	"""
	def get_certain_attacked_set(self, attacker_set):
		attacked_set = set()

		if attacker_set != set():
			for argument_label in attacker_set:
				attacked_set_of_argument = self.get_certain_attacked_labels_set_from_argument_label(argument_label)
				attacked_set = attacked_set.union(attacked_set_of_argument)
			return attacked_set

		else:
			return attacked_set 
	"""
	"""
	# MUY COSTOSA---
	def get_certain_attacked_set(self, attacker_set):
		attacked_set = set()

		practical_base = self.get_practical_base_structures()
		epistemic_base = self.get_epistemic_base_structures()
		
		if attacker_set != set():
			for argument_label in attacker_set:
				structure = list(get_argument_structure_from_label(argument_label, practical_base, epistemic_base))
				attacked_set = attacked_set.union(set(structure[3]))
			# tendria que filtrar todos los argumentos externos
			attacked_set = filter_external_attacks(attacked_set, self.get_agent_name())
			return attacked_set

		else:
			return attacked_set
	"""
	def get_undercuts(self, semantic_r):
		undercuts = set()
		epistemic_base = self.get_epistemic_base_structures()

		if semantic_r:
			for epistemic_argument in epistemic_base:
				if len(epistemic_argument[1]) > 0:
					for attacker_label in epistemic_argument[1]:
						if self.is_label_in_arguments_base(attacker_label):
							undercuts.add((attacker_label, epistemic_argument[0]))
		else:
			for epistemic_argument in epistemic_base:
				if len(epistemic_argument[1]) > 0:
					for attacker_label in epistemic_argument[1]:
						if self.is_label_in_arguments_base(attacker_label):
							undercuts.add((attacker_label, epistemic_argument[0]))

				if len(epistemic_argument[2]) > 0:
					for attacker_label in epistemic_argument[2]:
						if self.is_label_in_arguments_base(attacker_label):
							undercuts.add((attacker_label, epistemic_argument[0]))

		return undercuts

	def get_attacks(self, semantic_r):
		attacks = set()
		practical_base = self.get_practical_base_structures()

		if semantic_r:
			for practical_argument in practical_base:
				if len(practical_argument[3]) > 0:
					for attacker_label in practical_argument[3]:
						if self.is_label_in_arguments_base(attacker_label):
							attacks.add((attacker_label, practical_argument[0]))
		else:
			for practical_argument in practical_base:
				if len(practical_argument[3]) > 0:
					for attacker_label in practical_argument[3]:
						if self.is_label_in_arguments_base(attacker_label):
							attacks.add((attacker_label, practical_argument[0]))

				if len(practical_argument[5]) > 0:
					for attacker_label in practical_argument[5]:
						if self.is_label_in_arguments_base(attacker_label):
							attacks.add((attacker_label, practical_argument[0]))

		return attacks

	def get_all_attacks(self):
		undercuts = copy(self.get_undercuts(False))
		attacks = copy(self.get_attacks(False))

		all_attacks = copy(undercuts.union(attacks))

		return all_attacks



	def get_acceptable_arguments(self):
		#maximal_cfs = self.get_maximal_cfs()
		#maximal_admisibles_sets = self.maximal_admisible_cfs(maximal_cfs) #extensiones preferidas
		maximal_admisibles_sets = self.maximal_admisible_cfs()
		acceptable_arguments = set()

		for admisible_set in maximal_admisibles_sets:
			acceptable_arguments = acceptable_arguments.union(admisible_set)

		return acceptable_arguments


	def is_candidate_decision(self, decision):
		acceptable_arguments = self.get_acceptable_arguments()
		practical_base = self.get_practical_base_structures()
		epistemic_base = self.get_epistemic_base_structures()
		for acceptable_argument_label in acceptable_arguments:
			acceptable_argument_structure = get_argument_structure_from_label(acceptable_argument_label, practical_base, epistemic_base)
			if len(acceptable_argument_structure) == 7:
				if acceptable_argument_label == acceptable_argument_structure[0] and acceptable_argument_structure[2]== decision:
					return True

		return False

	def get_candidate_decisions(self):
		#candidates_decisions = []

		#for alternative in self.alternatives:
		#	if self.is_candidate_decision(alternative):
		#		candidates_decisions.append(alternative)

		#return candidates_decisions
		return [alternative for alternative in self.alternatives if self.is_candidate_decision(alternative)]

	def is_acceptable_argument(self, argument_structure):
		acceptable_arguments = self.get_acceptable_arguments()

		if argument_structure[0] in acceptable_arguments:
			return True

		else:
			return False
	
	def get_acceptable_pro_of_decision(self, decision):
		acceptable_arguments_pro_decision = []
		acceptable_arguments = self.get_acceptable_arguments()
		practical_base = self.get_practical_base_structures()
		epistemic_base = self.get_epistemic_base_structures()
		for argument_label in acceptable_arguments:
			#argument_structure = self.get_argument_structure_from_label(argument_label)
			argument_structure = get_argument_structure_from_label(argument_label, practical_base, epistemic_base)
			if len(argument_structure) == 7 and argument_structure[1] == "P" and argument_structure[2] == decision:
				acceptable_arguments_pro_decision.append(argument_structure)

		return acceptable_arguments_pro_decision

	def get_acceptable_con_of_decision(self, decision):
		acceptable_arguments_con_decision = []
		acceptable_arguments = self.get_acceptable_arguments()
		practical_base = self.get_practical_base_structures()
		epistemic_base = self.get_epistemic_base_structures()
		for argument_label in acceptable_arguments:
			#argument_structure = self.get_argument_structure_from_label(argument_label)
			argument_structure = get_argument_structure_from_label(argument_label, practical_base, epistemic_base)
			if len(argument_structure) == 7 and argument_structure[1] == "C" and argument_structure[2] == decision:
				acceptable_arguments_con_decision.append(argument_structure)

		return acceptable_arguments_con_decision
	
	def get_preferred_decision_from_arguments_pro(self, arguments_pro_decision1, arguments_pro_decision2):
		arguments_pro_decision1_number = len(arguments_pro_decision1)
		arguments_pro_decision2_number = len(arguments_pro_decision2)

		if arguments_pro_decision1_number > 0 and arguments_pro_decision2_number > 0:
			strengths_arguments_pro_decision1 = [argument_pro_decision1[4] for argument_pro_decision1 in arguments_pro_decision1]
			strengths_arguments_pro_decision2 = [argument_pro_decision2[4] for argument_pro_decision2 in arguments_pro_decision2]

			#for argument_pro_decision1 in arguments_pro_decision1:
			#	strengths_arguments_pro_decision1.append(argument_pro_decision1[4])
			
			#for argument_pro_decision2 in arguments_pro_decision2:
			#	strengths_arguments_pro_decision2.append(argument_pro_decision2[4])
			
			maximum_strength_decision1 = max(strengths_arguments_pro_decision1)
			maximum_strength_decision2 = max(strengths_arguments_pro_decision2)

			if maximum_strength_decision1 > maximum_strength_decision2:
				return "Primera"

			elif maximum_strength_decision2 > maximum_strength_decision1:
				return "Segunda"

			else:
				if arguments_pro_decision1_number > arguments_pro_decision2_number:
					return "Primera"

				elif arguments_pro_decision1_number < arguments_pro_decision2_number:
					return "Segunda"

				else:
					return "Equal"
		else:
			if arguments_pro_decision1_number > 0 and arguments_pro_decision2_number == 0:
				return "Primera"

			else:
				return "Segunda"

	def get_preferred_decision_from_arguments_con(self, arguments_con_decision1, arguments_con_decision2):
		arguments_con_decision1_number = len(arguments_con_decision1)
		arguments_con_decision2_number = len(arguments_con_decision2)

		if arguments_con_decision1_number > 0 and arguments_con_decision2_number > 0:

			weaknesses_arguments_con_decision1 = [argument_con_decision1[4] for argument_con_decision1 in arguments_con_decision1]
			weaknesses_arguments_con_decision2 = [argument_con_decision2[4] for argument_con_decision2 in arguments_con_decision2]
			
			#for argument_con_decision1 in arguments_con_decision1:
			#	weaknesses_arguments_con_decision1.append(argument_con_decision1[4])

			#for argument_con_decision2 in arguments_con_decision2:
			#	weaknesses_arguments_con_decision2.append(argument_con_decision2[4])


			maximum_weakness_decision1 = max(weaknesses_arguments_con_decision1)
			maximum_weakness_decision2 = max(weaknesses_arguments_con_decision2)

			if maximum_weakness_decision1 > maximum_weakness_decision2:
				return "Primera"

			elif maximum_weakness_decision2 > maximum_weakness_decision1:
				return "Segunda"

			else:
				if arguments_con_decision1_number > arguments_con_decision2_number:
					return "Segunda"

				elif arguments_con_decision1_number < arguments_con_decision2_number:
					return "Primera"

				else:
					return "Equal"

		else:
			if arguments_con_decision1_number > 0 and arguments_con_decision2_number == 0:
				return "Segunda"

			else:
				return "Primera"



	def get_preferred_decision(self, decision1, decision2):
		arguments_pro_decision1 = self.get_acceptable_pro_of_decision(decision1)
		arguments_con_decision1 = self.get_acceptable_con_of_decision(decision1)
		arguments_pro_decision2 = self.get_acceptable_pro_of_decision(decision2)
		arguments_con_decision2 = self.get_acceptable_con_of_decision(decision2)

		status_pro = 0
		status_con = 0

		arguments_pro_decision1_number = len(arguments_pro_decision1)
		arguments_pro_decision2_number = len(arguments_pro_decision2)
		arguments_con_decision1_number = len(arguments_con_decision1)
		arguments_con_decision2_number = len(arguments_con_decision2)

		if arguments_pro_decision1_number == 0 and arguments_pro_decision2_number == 0:
			status_pro = None
		elif arguments_pro_decision1_number == 0 and arguments_pro_decision2_number > 0:
			status_pro = "Segunda"
		elif arguments_pro_decision1_number > 0 and arguments_pro_decision2_number == 0:
			status_pro = "Primera"
		elif arguments_pro_decision1_number > 0 and arguments_pro_decision2_number > 0:
			status_pro = self.get_preferred_decision_from_arguments_pro(arguments_pro_decision1, arguments_pro_decision2)

		if arguments_con_decision1_number == 0 and arguments_con_decision2_number == 0:
			status_con = None
		elif arguments_con_decision1_number == 0 and arguments_con_decision2_number > 0:
			status_con = "Primera"
		elif arguments_con_decision1_number > 0 and arguments_con_decision2_number == 0:
			status_con = "Segunda"
		elif arguments_con_decision1_number > 0 and arguments_con_decision2_number > 0:
			status_con = self.get_preferred_decision_from_arguments_con(arguments_con_decision1, arguments_con_decision2)

		if status_pro == None and status_con == None:
			return None
		elif status_pro == None and status_con != None:
			if status_con == "Primera":
				return decision1
			elif status_con == "Segunda":
				return decision2
			elif status_con == "Equal":
				return None
		elif status_con == None and status_pro != None:
			if status_pro == "Primera":
				return decision1
			elif status_pro == "Segunda":
				return decision2
			elif status_pro == "Equal":
				return None
		elif status_pro == "Primera" and status_con == "Primera":
			return decision1
		elif status_pro == "Segunda" and status_con == "Segunda":
			return decision2
		elif status_pro == "Segunda" and status_con == "Primera":
			return None
		elif status_pro == "Primera" and status_con == "Segunda":
			return None
		elif status_pro == "Equal" and status_con == "Equal":
			return None
		elif status_pro == "Equal" and status_con == "Primera":
			return decision1
		elif status_pro == "Equal" and status_con == "Segunda":
			return decision2
		elif status_pro == "Primera" and status_con == "Equal":
			return decision1
		elif status_pro == "Segunda" and status_con == "Equal":
			return decision2


	def candidate_decisions_descending_order_of_preference(self):

		candidate_decisions = self.get_candidate_decisions()

		if len(candidate_decisions) == 0:
			return ["equallyPreferred", self.alternatives]

		else:
			preference_list = self.selection_sort(candidate_decisions) # lista de preferencias de mayor a menor, res None, [a,b]

			if preference_list == None:
				return ["equallyPreferred", self.alternatives]
			else:
				return ["prefOrder", preference_list]
			
	def selection_sort(self, list_to_order): # lista de alternativas candidatas
		list_to_order_len = len(list_to_order)

		if list_to_order_len > 0:
			for i in range(list_to_order_len):
				least = i # índice de alternativa
				for k in range(i + 1, list_to_order_len):
					a = self.get_preferred_decision(list_to_order[k], list_to_order[least]) 
					if a == list_to_order[k]:
						least = k

				swap(list_to_order, least, i)

			return list_to_order

		else:
			return None


	def is_now_acceptable_offer(self, current_offer):
		candidates_decisions = self.get_candidate_decisions()
		candidates_decisions_number = len(candidates_decisions)

		if candidates_decisions_number == 0:
			return True

		elif current_offer not in candidates_decisions:
			return False

		elif candidates_decisions_number == 1 and current_offer in candidates_decisions:
			return True

		else:
			for decision in candidates_decisions:
				if decision != current_offer:
					preferred = self.get_preferred_decision(decision, current_offer)

					if preferred != current_offer and preferred != None:
						return False
			return True


	def get_maximal_cfs(self, all_attacks):
		all_arguments_labels = list(self.all_arguments_labels)
		arguments_number = len(all_arguments_labels)
		#all_attacks = list(self.get_all_attacks())

		graph = Graph()
		graph.add_nodes_from(all_arguments_labels)
	
		links = []
		append = links.append
		for i in range(0, arguments_number):
			for j in range(i + 1, arguments_number):
				
				no_attack = True
				
				for attack in all_attacks:
					if (attack[0] == all_arguments_labels[i] and
					 attack[1] == all_arguments_labels[j]) or (attack[0] == all_arguments_labels[j] and
					  attack[1] == all_arguments_labels[i]):
						no_attack = False
						break
						
				if no_attack:
					append((all_arguments_labels[i], all_arguments_labels[j]))
		#print("links", links)
		graph.add_edges_from(links)
		
		maximum_cliques = find_cliques(graph)

		#cliques_list = []

		#for clique in maximum_cliques:
		#	cliques_list.append(set(clique))
			
		#return cliques_list
		return [set(clique) for clique in maximum_cliques]
		
	# Retorna conjuntos admisibles maximales dados los cfs maximales
	def maximal_admisible_cfs(self):
		attacks = self.get_all_attacks()
		#print(attacks)
		maximal_cfs = self.get_maximal_cfs(attacks)
		#return maximal_cfs ### boraaaaaaarrrrrrrrrr
		#print("cfs_max", maximal_cfs)
		maximal_admisible_sets = []

		practical_base = self.get_practical_base_structures()
		epistemic_base = self.get_epistemic_base_structures()
		name = self.get_agent_name()

		for cfs in maximal_cfs:

			cfs = set(cfs)
			admisible_set = copy(cfs)

			while len(admisible_set) >= 0:
				to_delete = set()
				#print("admisible?", admisible_set)
				for argument in admisible_set:
						#comp = args.difference(admis) # complemento del cfs --- admis no cfs
					#print("Soy:", argument)
					argument_attakers = self.get_attackers_of_argument_label(argument) # argumentos que atacan a el elemento "x" de "admis"

					admisible_set_without_argument = admisible_set.difference({argument}) # cfs sin "x" --- admis no cfs
					certain_attacked_set = get_certain_attacked_set(admisible_set_without_argument, practical_base, epistemic_base, name)
					#certain_attacked_set = self.get_certain_attacked_set(admisible_set_without_argument)# argumentos a los que ataca "cfs" sin "x"
					#print("me atacan:", argument_attakers)
					#print("los demás atacan a:", certain_attacked_set)
					if len(argument_attakers) > 0: # si hay al menos un argumento externo a cfs que ataca a x
						if argument_attakers.intersection(certain_attacked_set) != argument_attakers:
							#print("NO ES ADM")
							to_delete.add(argument)
						#else:
						#	print("ADM")

				if to_delete == set(): 
					break

				else:
					admisible_set = copy(admisible_set.difference(to_delete))
				
			if admisible_set not in maximal_admisible_sets and admisible_set != set():
				maximal_admisible_sets.append(admisible_set)
					
		#necesito quedarme con los qque satisfacen lema 10 (elimino subconjuntos de uqellos)
		to_remove = []
		
		for s1 in maximal_admisible_sets:
			for s2 in maximal_admisible_sets:
				if s1 != s2:
					if s1 == s2.intersection(s1):
						if s1 not in to_remove:
							to_remove.append(s1)

		remove = maximal_admisible_sets.remove

		for k in to_remove:
			remove(k)

		return maximal_admisible_sets

	class Negotiation:
		def __init__(self, af):
			self.af = af

			self.offer_x = Agent.Negotiation.OfferX(self)
			self.challenge_x = Agent.Negotiation.ChallengeX(self)
			self.challenge_y = Agent.Negotiation.ChallengeY(self)
			self.argue_s = Agent.Negotiation.ArgueS(self)
			self.accept_x = Agent.Negotiation.AcceptX(self)
			self.accept_s = Agent.Negotiation.AcceptS(self)
			self.refuse_x = Agent.Negotiation.RefuseX(self)
		
		class OfferX:
			def __init__(self, af):
				self.af = af
			def preconditions(self, remaining_alternatives):
				cd = self.af.af.candidate_decisions_descending_order_of_preference()
				
				for e in cd[1]:
					if e in remaining_alternatives:
						return e
				if len(remaining_alternatives) > 0:
					return remaining_alternatives[0]
				
				return None
				  
			def postconditions(self, offer):
				self.af.af.commitment_store.add_proposed_or_accepted_offer(offer) 

		class ChallengeX:
			def __init__(self, af):
				self.af = af

			def preconditions(self, current_offer):
				if current_offer not in self.af.af.commitment_store.offers_proposed:
					return True
				else:
					return False

			def postconditions(self, current_offer):
				self.af.af.commitment_store.add_challenge_presented(current_offer)

		class ChallengeY:
			def __init__(self, af):
				self.af = af

			def preconditions(self, argument_or_offer):
				if argument_or_offer not in self.af.af.commitment_store.challenges_made:
					return True
				else:
					return False

			def postconditions(self, argument_or_offer):
				self.af.af.commitment_store.add_challenge_presented(argument_or_offer)
				
		class ArgueS:
			def __init__(self, af):
				self.af = af

			def preconditions(self, current_offer):

				con_arguments = self.af.af.get_acceptable_con_of_decision(current_offer)
				pro_arguments = self.af.af.get_acceptable_pro_of_decision(current_offer)

				all_arguments_acceptable = con_arguments + pro_arguments
		
				arguments_presented = self.af.af.commitment_store.arguments_presented

				argument_to_present_label = search_argument_to_share(arguments_presented, all_arguments_acceptable)
				practical_base = self.af.af.get_practical_base_structures()
				epistemic_base = self.af.af.get_epistemic_base_structures()
				
				if argument_to_present_label != False:
					#return self.af.af.get_argument_structure_from_label(argument_to_present_label)
					return get_argument_structure_from_label(argument_to_present_label, practical_base, epistemic_base)

				else:
					return False

			def postconditions(self, argument_structure):
				self.af.af.commitment_store.add_argument_presented(argument_structure)

		class AcceptX:
			def __init__(self, af):
				self.af = af
			
			def preconditions(self, current_offer):
				if current_offer not in self.af.af.commitment_store.offers_proposed:

					if self.af.af.is_now_acceptable_offer(current_offer):
						return True

					else:
						return False
				else:
					return False
					
			def postconditions(self, current_offer):
				self.af.af.commitment_store.add_proposed_or_accepted_offer(current_offer)

		class AcceptS:
			def __init__(self, af):
				self.af = af

			def preconditions(self, argument_structure):
				if argument_structure not in self.af.af.commitment_store.external_arguments_added and self.af.af.name not in argument_structure[0]:
					if self.af.af.is_acceptable_argument(argument_structure):
						return True
					else:
						self.af.af.commitment_store.add_external_argument(argument_structure)
						return False
				else:
					return False

			def postconditions(self, argument_structure):
				self.af.af.commitment_store.add_external_argument(argument_structure)

		class RefuseX:
			def __init__(self, af):
				self.af = af

			def preconditions(self, current_offer):
					if current_offer in self.af.af.commitment_store.offers_proposed:
						return False

					else:
						arguments_con = self.af.af.get_acceptable_con_of_decision(current_offer)
						
						status = True

						for argument in arguments_con:
							if argument not in self.af.af.commitment_store.arguments_presented:
								status = False
								break

						if status:
							return False
						else:
							return True
						
			def postconditions(self):
				#self.af.af.commitment_store.add_Refuse(current_offer)
				return None


##########################
### Otras funciones
##########################

def get_arguments_labels_set_from_structures_list(arguments_structures_list):
	#labels = set()

	#if arguments_structures_list != []:
	#	for argument_structure in arguments_structures_list:
	#		labels.add(argument_structure[0])

	#return labels
	return {argument_structure[0] for argument_structure in arguments_structures_list if arguments_structures_list != []}

def search_argument_to_share(arguments_presented, acceptable_arguments):

	arguments_presented_labels_set = get_arguments_labels_set_from_structures_list(arguments_presented)
	arguments_acceptable_labels_set = get_arguments_labels_set_from_structures_list(acceptable_arguments)

	if len(arguments_acceptable_labels_set) > 0:
		for j in arguments_acceptable_labels_set:
			if len(arguments_presented_labels_set.intersection({j})) == 0:
				return j
		return False
	else:
		return False



def swap(A, x, y): # recibe una lista de alternativas candidatas, e índices de 2 de ellas distintas
	if 0 <= x < len(A) and 0 <= y < len(A):
		#temp = A[x]
		#A[x] = A[y]
		#A[y] = temp
		A[x], A[y] = A[y], A[x]

				

