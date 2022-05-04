
def get_argument_structure_from_label(str argument_label, list practical_base, list epistemic_base):
    if "ap" in argument_label:
        for practical_argument in practical_base:
            if practical_argument[0] == argument_label:
                return practical_argument
        return -1
    else:
        for epistemic_argument in epistemic_base:
            if epistemic_argument[0] == argument_label:
                return epistemic_argument
        return -1
  
def filter_external_attacks(set arguments, str agent_name):
    cdef str arg
    cdef set s = {arg for arg in arguments if agent_name in arg}
    return s
	
def get_certain_attacked_set(set attacker_set, list practical_base, list epistemic_base, str name):
    cdef set attacked_set = set()
    cdef str argument_label
    cdef structure = []

    if attacker_set != set():
        for argument_label in attacker_set:
            structure = list(get_argument_structure_from_label(argument_label, practical_base, epistemic_base))
            attacked_set = attacked_set.union(set(structure[3]))

        attacked_set = filter_external_attacks(attacked_set, name)
        return attacked_set
    else:
        return attacked_set
