# William Kavanagh, May 2019
# Extended CSG - metagenerator

def choice_available(state_desc):
    # Takes a state_description as <str>
    # returns true if more than 1 non-skip action can be taken from that state.
    # from input update if p2x is a valid actor and p1y is a valid target..
    p2K = 1 if state_desc[2] > "0" and state_desc[5] != "1" else 0
    p2A = 1 if state_desc[3] > "0" and state_desc[5] != "2" else 0
    p2W = 1 if state_desc[4] > "0" and state_desc[5] != "3" else 0
    p1K = 1 if state_desc[6] > "0" else 0
    p1A = 1 if state_desc[7] > "0" else 0
    p1W = 1 if state_desc[8] > "0" else 0
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
    # takes two files for .sta and .tra and generates a strategy, printed to <pair>_strategy_<i>.txt
    # also returns the total number of transitions
    transitions = {}
    total_actions = 0
    voided_actions = 0

    file_to_write = file_prefix + "/" + pair + "_strategy_" + str(i) + ".txt"
    f = open(file_to_write, "w")
    f.write("// Generated strategy for " + pair + " at a later iteration\n")
    f.write(open("forced_p2_moves.txt","r").read())     # print forced actions
    for line in open(file_prefix+"/tmp.tra","r").readlines()[1:]:   # for every transition
        if line.split(" ")[4][:2] == "p1":     # if the line is relevant
            total_actions +=1
            transitions[line.split(" ")[0]] = line.split(" ")[4][3:-1]
    # Transitions = {state, action_string} for every relevant action.
    var_descriptors = ["attack","turn","p1K","p1A","p1W","p1_stun","p2K","p2A","p2W","p2_stun"]
    for line in open(file_prefix+"/tmp.sta","r").readlines()[1:]:   # for every state
        if line.split(":(")[0] in transitions.keys():           # if it's relevant
            single_s = line.split(":(")[0]                      # the state is
            state_desc = line.split(":(")[1][:-2].split(",")
            if choice_available(state_desc):                        # if a choice is needed.
                single_t = transitions[line.split(":(")[0]]         # the transition string is
                single_a = 13                                       # the value for 'attack' is
                if single_t[0] == "A": single_a += 3                # silly numerisation...
                if single_t[0] == "W": single_a += 9
                if single_t[2] == "A": single_a += 1
                if single_t[2] == "W": single_a += 2
                if len(single_t) > 3 and "KA" in single_t: single_a += 3
                elif len(single_t) > 3 and "skip" not in single_t: single_a += 4
                elif "skip" in single_t: single_a = "0) & (turn' = 1" # must be skip. single_a is correct.
                guard = "\t[p2_" + single_t + "]\tattack = 0 & turn = 2 & p1K = "
                guard += state_desc[6] + " & p1A = " + state_desc[7] + " & p1W = " + state_desc[8]
                guard += " & p1_stun = " + state_desc[9] + " &\n\t\t\tp2K = " + state_desc[2]
                guard += " & p2A = " + state_desc[3] + " & p2W = " + state_desc[4] + " & p2_stun"
                guard += " = " + state_desc[5] + " ->\n"
                command = "\t\t\t\t(attack' = " + str(single_a) + ") & (p2_stun' = 0);\n"
                f.write(guard + command)      # print the guard
            else: voided_actions += 1
    f.write("// There are " + str(total_actions) + " actions in total, " + str(voided_actions) + " were invalid.\n" )
    return(total_actions)


# states: (attack,turn,p1K,p1A,p1W,p1_stun,p2K,p2A,p2W,p2_stun)
# sta_e.g. 1740:(0,1,0,2,5,2,0,6,1,0)
# tra_e.g. 1740 0 11901 1 p1_W_W
# 13 K2>K1, 14 K2>A1, 15 K2>W1, 16 A2>K1, 17 A2>A1, 18 A2>W1, 19 A2>K1A1, 20 A2>K1W1, 21 A2>A1W1, 22 W2>K1, 23 W2>A1, 24 W2>W1
