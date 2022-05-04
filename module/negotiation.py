#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from random import random, shuffle

from moves import *


class Move:
	def __init__(self, creator, content, label):
		self.creator = creator
		self.content = content
		self.label = label
	
def create_move(creator, content, label):
	new_move = Move(creator, content, label)
	return new_move

# Dados los agentes y alternativas, genara un listado 
#de los agentes que empezarán cada ronda de diálogo Di en la negociación N
def first_turn_per_dialogue(agents_list, number_offers):

	turns = []

	number_agents = len(agents_list)

	fraction = number_offers / number_agents
	remainder = number_offers % number_agents

	shuffle(agents_list)
	
	if fraction == 1: # num(X) == num(agents)
		return agents_list

	elif fraction > 1: # num(X) > num(agents)
		count = 0
		fraction = number_offers // number_agents

		while count < fraction:
			turns = turns + [agent for agent in agents_list]
			count = count + 1
		
		turns = turns + [agents_list[i] for i in range(remainder)]

		return turns

	else: # fraction < 1, num(X) < num(agents)
		turns = [agents_list[i] for i in range(number_offers)]

		return turns

######################################################################

def first_move_dialogue(first_speaker, remaining_alternatives):
	offer_proposed = first_speaker.negotiation.offer_x.preconditions(remaining_alternatives) # pongo True si quiero info de los agentes
	move_created = create_move(first_speaker, offer_proposed, "Offer")
	first_speaker.negotiation.offer_x.postconditions(offer_proposed)
	return move_created
	

def new_move(creator, current_offer, agents, move_index): # index es un número entre 2 y más

	if move_index == 2:
		reply_chosen = reply_offer_preconditions(creator, current_offer) # 1, 2, 3 o -1
		reply_label = reply_offer_postconditions(creator, current_offer, reply_chosen) # label

		move_created = create_move(creator, current_offer, reply_label)
		
	elif move_index == 3:
		reply_chosen = reply_argue_accept_challenge_preconditions(creator, current_offer) # 1, arg, 3 o -1
		reply_label = reply_argue_accept_challenge_postconditions(creator, current_offer, reply_chosen)

		if reply_label == "SayNothing":
			move_created = create_move(creator, "SayNothing", reply_label)

		elif reply_label == "AcceptX" or reply_label == "ChallengeX":
			move_created = create_move(creator, current_offer, reply_label)

		else:
			move_created = create_move(creator, reply_label, "Argue")
			# AÑADO ARGUMENTO A LOS DEMÁS AGENTES
			agents = add_argument(agents, creator, reply_label)
	
	else:
		reply_chosen = reply_all_preconditions(creator, current_offer) # -1, 1, arg, 3, [arg]
		reply_label = reply_all_postconditions(creator, current_offer, reply_chosen)

		if reply_label == "SayNothing":
			move_created = create_move(creator, "SayNothing", reply_label)

		elif reply_label == "AcceptX" or reply_label == "ChallengeX":
			move_created = create_move(creator, current_offer, reply_label)

		elif isinstance(reply_label, list):
			move_created = create_move(creator, reply_label[0], "AcceptS")
		
		else:
			move_created = create_move(creator, reply_label, "Argue")
			# AÑADO ARGUMENTOS A OTROS AGENTES
			agents = add_argument(agents, creator, reply_label)

			
	#for agent in agents:
	#	if agent.name == creator.name:
	#		agent = creator

	count = 0
	status = True
	while status:
		if agents[count].name == creator.name:
			agents[count] = creator
			status = False
		count = count + 1

	return [move_created, agents]

#####################################################
def add_argument(agents, creator_agent, argument_structure):
	for agent in agents:
		if agent.name != creator_agent.name:
			if agent.is_label_in_arguments_base(argument_structure[0]) == False:
				if len(argument_structure)==7:
					argument_structure = list(argument_structure)
					argument_structure[4] = random() # si es práctico, le pongo un nuevo peso
					argument_structure = tuple(argument_structure)

				# para que el agente no argumentente un arg presentado por otro (NO ESTÁ FUNCIONANDO)
				agent.commitment_store.add_argument_presented(argument_structure)
				agent.commitment_store.add_external_argument(argument_structure)
				agent.add_argument_structure_to_base(argument_structure)
				agent.practical_labels.add(argument_structure[0])

	return agents


def negotiation(agents, X):
	remaining_alternatives = list(X)
	number_offers = len(X)
	number_agents = len(agents)
	agents_c = deepcopy(agents)
	agents_list = deepcopy(list(agents))
	agreement_status = False
	count = 0 # num_iteration
	global sn 
	sn = set()
	remove = remaining_alternatives.remove
	
	option = -1 # WTF

	initial_turn_per_dialogue = first_turn_per_dialogue(agents_list, number_offers)

	while len(remaining_alternatives) > 0 and agreement_status == False and count < number_agents: # en cada iteracion empieza un dialogo nuevo
		
		move_count = 0
		initiator_agent = initial_turn_per_dialogue[count] # este agente inicia el dialogo

		agent_list_dialogue = [initiator_agent]
		#print(len(agents_c), type(agents_c),"agent_c", initiator_agent.name)
		#if initiator_agent in agents_c:
		#	print("OK")

		#remaining_agents = set()
		#for ag in agents_c:
		#	if ag.name != initiator_agent.name:
		#		remaining_agents.add(ag)
		remaining_agents = [ag for ag in agents_c if ag.name != initiator_agent.name]
		#remaining_agents = agents_c.difference({initiator_agent})
		#for ag in remaining_agents:
		#	print(ag.name)
		shuffle(remaining_agents)

		#for agent in remaining_agents:
		#	agent_list_dialogue.append(agent)
		agent_list_dialogue = agent_list_dialogue + remaining_agents
		#print(len(agent_list_dialogue), "agent_ldial")
		move_index = 1
		first_move = first_move_dialogue(initiator_agent, remaining_alternatives) # primer move
		
		move_count = move_count + 1 # hay 1 move
		agent_list_dialogue[0] = first_move.creator
		current_alternative = first_move.content
		#print(current_alternative)
		initiator_name = first_move.creator.name
		dialogue_status = True
		index_next_agent = 1
		moves_labels_in_round = set()
		add_move_label = moves_labels_in_round.add
		while dialogue_status:
			
			if index_next_agent == 0:
				moves_labels_in_round = set() # la vacío al empezar una ronda nueva
			
			creator = agent_list_dialogue[index_next_agent]

			move_index = move_index + 1
			move_created_agents = new_move(creator, current_alternative, agent_list_dialogue, move_index)
			move_created = move_created_agents[0]
			#print("m ", move_created.label, creator.name, move_created.content)
			
			add_move_label(move_created.label) # añado movimientos depor ronda
			
			move_count = move_count + 1

			agent_list_dialogue = move_created_agents[1]

			result = 0

			if move_created.label == "AcceptX" and move_count >= number_agents:
				#count1 = 0
				#for agent in agent_list_dialogue:
				#	if agent.commitment_store.is_offer_accepted(current_alternative):
				#		count1 = count1 + 1
				count1 = sum([1 for agent in agent_list_dialogue if agent.commitment_store.is_offer_accepted(current_alternative)])
				if count1 == number_agents:
					result = "Success"
			# modificar
			#if move_created.label == "SayNothing":
			#	count2 = 0

			#	for agent in agent_list_dialogue: 
			#		if agent.commitment_store.is_no_arguments_to_share():
			#			count2 += 1

			#	if count2 == number_agents:
			#		result = "Failure"

			if index_next_agent == number_agents - 1:
				if "Argue" in moves_labels_in_round:
					sn = set()
			
			if move_created.label == "SayNothing":
				sn.add(creator.name)
				
			if len(sn) == number_agents:
				sn = set()
				result = "Failure"
			
			if move_created.label == "Argue":
				#count3 = 0

				#for agent in agent_list_dialogue:
				#	if agent.name != initiator_name:
				#		if agent.is_now_acceptable_offer(current_alternative):
				#			count3 = count3 + 1
				count3 = sum([1 for agent in agent_list_dialogue if agent.name != initiator_name and agent.is_now_acceptable_offer(current_alternative)])
				
				if count3 == number_agents - 1:
					result = "Success"
			
			
			if result == "Success" or result == "Failure":

				dialogue_status = False

				count = count + 1 # para que sea el turno de otro agente de empezar el siguiente dialogo D
					
				for agent in agent_list_dialogue:
					agent.commitment_store.reset()

				remove(current_alternative)
					
				if result == "Success":
					option = current_alternative # guardo alternativa "ganadora"
					agreement_status = True # cambio estado de agreement a True
					
			if index_next_agent == number_agents - 1:
				index_next_agent = 0
			else:
				index_next_agent = index_next_agent + 1
	
	return option, agent_list_dialogue				   
	
	
	
