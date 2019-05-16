
# William Kavanagh, May 2019
# Extended CSG - strategy generator for 5c RPGLite

action_d = {'p1_K_K': 1, 'p1_K_A': 2, 'p1_K_W': 3, 'p1_K_R': 4, 'p1_K_H': 5, 'p1_A_K': 6, 'p1_A_KA': 7, 'p1_A_KW': 8, 'p1_A_KR': 9, 'p1_A_KH': 10,
'p1_A_A': 11, 'p1_A_AW': 12, 'p1_A_AR': 13, 'p1_A_AH': 14, 'p1_A_W': 15, 'p1_A_WR': 16, 'p1_A_WH': 17, 'p1_A_R': 18, 'p1_A_RH': 19, 'p1_A_H': 20,
'p1_W_K': 21, 'p1_W_A': 22, 'p1_W_W': 23, 'p1_W_R': 24, 'p1_W_H': 25, 'p1_R_K': 26, 'p1_R_A': 27, 'p1_R_W': 28, 'p1_R_R': 29, 'p1_R_H': 30, 'p1_H_KK': 31,
'p1_H_KA': 32, 'p1_H_KW': 33, 'p1_H_KR': 34, 'p1_H_KH': 35, 'p1_H_AK': 36, 'p1_H_AA': 37, 'p1_H_AW': 38, 'p1_H_AR': 39, 'p1_H_AH': 40, 'p1_H_WK': 41,
'p1_H_WA': 42, 'p1_H_WW': 43, 'p1_H_WR': 44, 'p1_H_WH': 45, 'p1_H_RK': 46, 'p1_H_RA': 47, 'p1_H_RW': 48, 'p1_H_RR': 49, 'p1_H_RH': 50, 'p1_H_HK': 51,
'p1_H_HA': 52, 'p1_H_HW': 53, 'p1_H_HR': 54, 'p1_H_HH': 55, 'p2_K_K': 56, 'p2_K_A': 57, 'p2_K_W': 58, 'p2_K_R': 59, 'p2_K_H': 60, 'p2_A_K': 61,
'p2_A_KA': 62, 'p2_A_KW': 63, 'p2_A_KR': 64, 'p2_A_KH': 65, 'p2_A_A': 66, 'p2_A_AW': 67, 'p2_A_AR': 68, 'p2_A_AH': 69, 'p2_A_W': 70, 'p2_A_WR': 71,
'p2_A_WH': 72, 'p2_A_R': 73, 'p2_A_RH': 74, 'p2_A_H': 75, 'p2_W_K': 76, 'p2_W_A': 77, 'p2_W_W': 78, 'p2_W_R': 79, 'p2_W_H': 80, 'p2_R_K': 81, 'p2_R_A': 82,
'p2_R_W': 83, 'p2_R_R': 84, 'p2_R_H': 85, 'p2_H_KK': 86, 'p2_H_KA': 87, 'p2_H_KW': 88, 'p2_H_KR': 89, 'p2_H_KH': 90, 'p2_H_AK': 91, 'p2_H_AA': 92,
'p2_H_AW': 93, 'p2_H_AR': 94, 'p2_H_AH': 95, 'p2_H_WK': 96, 'p2_H_WA': 97, 'p2_H_WW': 98, 'p2_H_WR': 99, 'p2_H_WH': 100, 'p2_H_RK': 101, 'p2_H_RA': 102,
'p2_H_RW': 103, 'p2_H_RR': 104, 'p2_H_RH': 105, 'p2_H_HK': 106, 'p2_H_HA': 107, 'p2_H_HW': 108, 'p2_H_HR': 109, 'p2_H_HH': 110}


def choice_available(state_desc):
    # if there is more than one viable action: return True, else return False.

    p1_sum = int(state_desc[8])+int(state_desc[9])+int(state_desc[10])+int(state_desc[11])+int(state_desc[12])
    p1_max = max(int(state_desc[8]),int(state_desc[9]),int(state_desc[10]),int(state_desc[11]),int(state_desc[12]))
    p2_sum = int(state_desc[2])+int(state_desc[3])+int(state_desc[4])+int(state_desc[5])+int(state_desc[6])
    # if more than one actor is available:
    non_zero = 0
    for i in range(2,7):
        if state_desc[i] != "0" and state_desc[7] != str(i-1): non_zero += 1
    if non_zero > 1: return True
    # forced skip -> one action.
    elif non_zero == 0: return False
    # if one actor is available but multiple targets are available
    if p1_sum > p1_max: return True
    # Healers might have a second heal target who is stunned...
    if state_desc[6] > "0" and int(state_desc[6]) < p2_sum and state_desc[7] != "5":
        return True
    # one actor, one target, no special cases -> one action.
    return False

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
            #print(line.split(" ")[0], line.split(" ")[4][3:-1])
            transitions[line.split(" ")[0]] = line.split(" ")[4][3:-1]
    # Transitions = {state, action_string} for every relevant action.
    var_descriptors = ["attack","turn","p1K","p1A","p1W","p1R","p1H","p1_stun","p2K","p2A","p2W","p2R","p2H","p2_stun"]
    for line in open(file_prefix+"/tmp.sta","r").readlines()[1:]:   # for every state
        if line.split(":(")[0] in transitions.keys():               # if it's relevant
            single_s = line.split(":(")[0]                          # the state is
            state_desc = line.split(":(")[1][:-2].split(",")
            if choice_available(state_desc):                        # if a choice is needed.
                single_t = transitions[line.split(":(")[0]]         # the transition string is
                single_a = 0                                        # the value for 'attack' is skip by default
                for act in action_d.keys():
                    if act == "p2_" + single_t:
                        #print("woa")
                        single_a = action_d[act]                    # set attack int.
                guard = "\t[p2_" + single_t + "]\tattack = 0 & turn = 2 & p1K = "
                guard += state_desc[8] + " & p1A = " + state_desc[9] + " & p1W = " + state_desc[10]
                guard += " & p1R = " + state_desc[11] + " & p1H = " + state_desc[12]
                guard += " & p1_stun = " + state_desc[13] + " &\n\t\t\tp2K = " + state_desc[2]
                guard += " & p2A = " + state_desc[3] + " & p2W = " + state_desc[4] + " & p2R = " + state_desc[5]
                guard += " & p2H = " + state_desc[6] + " & p2_stun = " + state_desc[7] + " ->\n"
                if single_a != 0:
                    command = "\t\t\t\t(attack' = " + str(single_a) + ") & (p2_stun' = 0);\n"
                else:
                    command = "\t\t\t\t(attack' = 0) & (turn' = 1) & (p2_stun' = 0);\n"
                f.write(guard + command)      # print the guard
            else: voided_actions += 1

    f.write("// There are " + str(total_actions) + " actions in total, " + str(voided_actions) + " were invalid.\n" )
    return(total_actions)


# states: (attack,turn,p1K,p1A,p1W,p1R,p1H,p1_stun,p2K,p2A,p2W,p2R,p2H,p2_stun)
# sta_e.g. 1740:(0,1,0,2,5,2,0,6,1,0)
# tra_e.g. 1740 0 11901 1 p1_W_W
# 13 K2>K1, 14 K2>A1, 15 K2>W1, 16 A2>K1, 17 A2>A1, 18 A2>W1, 19 A2>K1A1, 20 A2>K1W1, 21 A2>A1W1, 22 W2>K1, 23 W2>A1, 24 W2>W1

#run("output/test", "WR", 0)
