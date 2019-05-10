# William Kavanagh, May 2019
# Extended CSG - strategy updater

def choice_available(state_desc):
    # Takes a state_description as <str>
    # returns true if more than 1 non-skip action can be taken from that state.

    # from input update if p2x is a valid actor and p1y is a valid target..
    p2K = 1 if state_desc[6] > "0" and state_desc[9] != "1" else 0
    p2A = 1 if state_desc[7] > "0" and state_desc[9] != "2" else 0
    p2W = 1 if state_desc[8] > "0" and state_desc[9] != "3" else 0
    p1K = 1 if state_desc[2] > "0" else 0
    p1A = 1 if state_desc[3] > "0" else 0
    p1W = 1 if state_desc[4] > "0" else 0
    p1sum = p1K+p1A+p1W         # Used to show only one opponent is alive
    possible_actions = []
    if p2K and p1K: possible_actions += [13]
    if p2K and p1A: possible_actions += [14]
    if p2K and p1W: possible_actions += [15]
    if p2A and p1K and p1sum == 1: possible_actions += [16]
    if p2A and p1A and p1sum == 1: possible_actions += [17]
    if p2A and p1W and p1sum == 1: possible_actions += [18]
    if p2A and p1K and p1A: possible_actions += [19]
    if p2A and p1K and p1W: possible_actions += [20]
    if p2A and p1A and p1W: possible_actions += [21]
    if p2W and p1K: possible_actions += [22]
    if p2W and p1A: possible_actions += [23]
    if p2W and p1W: possible_actions += [24]
    return len(possible_actions) > 1

def run(file_prefix, pair, i):
    # Updates the best strategy for a pair with any new transitions when played optimally against 'the meta'
    # also returns the number of transitions changed and the total number of transitions
    new_actions = 0

    old_transitions = {}
    transitions = {} # intermediary used for reading tra/sta files
    new_transitions = {}

    action_list = ['K_K', 'K_A', 'K_W', 'A_K', 'A_A', 'A_W', 'A_KA', 'A_KW', 'A_AW', 'W_K', 'W_A', 'W_W']
    f = open(file_prefix + "/" + pair + "_strategy_" + str(i) + ".txt", "w")    # file to write to
    f.write("// Generated strategy for " + pair + " at a later iteration \n")
    f.write(open("forced_p2_moves.txt","r").read())     # print forced actions
    # read in the previous strategy as a dictionary
    old_strategy = open(file_prefix + "/" + pair + "_strategy_" + str(i-1) + ".txt", "r").readlines()[39:]
    for i in range(len(old_strategy)):
        if "[p2" in old_strategy[i]:    # if the line begins a guard
            state_desc = "0,2,"
            state_desc += old_strategy[i].strip().split(" ")[10]+","    # add p1K
            state_desc += old_strategy[i].strip().split(" ")[14]+","   # add p1A
            state_desc += old_strategy[i].strip().split(" ")[18]+","   # add p1W
            state_desc += old_strategy[i].strip().split(" ")[22]+","   # add p1_stun
            state_desc += old_strategy[i+1].strip().split(" ")[2]+","  # add p2K
            state_desc += old_strategy[i+1].strip().split(" ")[6]+","  # add p2A
            state_desc += old_strategy[i+1].strip().split(" ")[10]+","  # add p2W
            state_desc += old_strategy[i+1].strip().split(" ")[14]  # add p2_stun
            old_transitions[state_desc] = int(old_strategy[i+2].split(" ")[2][:-1])
    # read in the adversary as a dictionary and translate it
    for line in open(file_prefix+"/tmp.tra","r").readlines()[1:]:   # for every transition
        if line.split(" ")[4][:2] == "p1":     # if the line is relevant
            transitions[line.split(" ")[0]] = line.split(" ")[4][3:-1]
    # Transitions = {state, action_string} for every relevant action.
    var_descriptors = ["attack","turn","p1K","p1A","p1W","p1_stun","p2K","p2A","p2W","p2_stun"]
    for line in open(file_prefix+"/tmp.sta","r").readlines()[1:]:   # for every state
        if line.split(":(")[0] in transitions.keys():           # if it's relevant
            single_s = line.split(":(")[0]                      # the state is
            state_desc_string = line.split(":(")[1][:-2].split(",")
            state_desc = state_desc_string[:1] + ["2"] + state_desc_string[6:] + state_desc_string[2:6]  # translate P1 > P2
            if choice_available(state_desc):
                single_t = transitions[line.split(":(")[0]]         # the transition string is
                single_a = 13                                       # the value for 'attack' is
                if single_t[0] == "A": single_a += 3                # silly numerisation...
                if single_t[0] == "W": single_a += 9
                if single_t[2] == "A": single_a += 1
                if single_t[2] == "W": single_a += 2
                if len(single_t) > 3 and "KA" in single_t: single_a += 3
                elif len(single_t) > 3: single_a += 4               # .. done. single_a is correct.
                new_transitions[str(state_desc)[2:-2].replace("', '",",")] = single_a
                #print(str(state_desc)[2:-2].replace("', '",","))
    # write out strategy for translations (if any) onto old strategy
    for elem in old_transitions.keys():
        if elem in new_transitions:
            if new_transitions[elem] != old_transitions[elem]:
                old_transitions[elem] = new_transitions[elem]   # Update for adversarial transition
                new_actions += 1
        if old_transitions[elem] != 0:              # if the action is non-skip
            label = "\t[p2_" + action_list[old_transitions[elem]-13] + "]\t"
            command = "\t\t\t\t(attack' = " + str(old_transitions[elem]) + ") & (p2_stun' = 0);\n"
        else:
            label = "\t[p2_skip]\t"
            command = "\t\t\t\t(attack' = 0) & (turn' = 1) & (p2_stun' = 0);\n"
        elem = elem.split(",")
        guard = label + "attack = 0 & turn = 2 & p1K = "
        guard += elem[2] + " & p1A = " + elem[3] + " & p1W = " + elem[4]
        guard += " & p1_stun = " + elem[5] + " &\n\t\t\tp2K = " + elem[6]
        guard += " & p2A = " + elem[7] + " & p2W = " + elem[8] + " & p2_stun"
        guard += " = " + elem[9] + " ->\n"
        f.write(guard + command)
    f.write("// There are " + str(len(old_transitions)) + " actions in total, " + str(new_actions) \
    + " have been updated\n")

    return(len(old_transitions), len(new_transitions), new_actions)

#run("output", "KW", 1)
