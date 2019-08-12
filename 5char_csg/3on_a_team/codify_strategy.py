
# William Kavanagh, August 2019
# Extended CSG - strategy generator for 5c-3at RPGLite

full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
chars = ["K","A","W","R","H"]


def choice_available(state_desc):
    # if there is more than one viable action: return True, else return False.
    if state_desc[7:12].count("0") == 5: return(False) # Are all opponents dead?
    if state_desc[1:6].count("0") == 5: return(False) # Are all actors dead?
    if state_desc[1:6].count("0") == 4 and state_desc[7:12].count("0") == 4: return(False) # Is there only 1 actor and 1 target alive?
    if state_desc[1:6].count("0") == 3 and state_desc[7:12].count("0") == 4 and int(state_desc[6]) > 0:  # If 2 actors are alive and there is only 1 opponent alive ...
        if int(state_desc[int(state_desc[6])]) > 0: return(False)  # ... but one of those actors is stunned?
    return(True)

def run(output, trip):
    # takes two files for .sta and .tra and generates a strategy, printed to <pair>_strategy_<i>.txt
    # also returns the total number of transitions

    transitions = {}
    total_actions = 0
    voided_actions = 0
    file_to_write = output + "/" + trip + "_base_strategy.txt"
    f = open(file_to_write, "w")
    f.write(open("forced_p2_moves.txt","r").read())     # print forced actions
    f.write("// Generated strategy for " + trip + "\n")
    for line in open(output+"/tmp.tra","r").readlines()[1:]:   # for every transition
        if line.split(" ")[4][:2] == "p1":     # if the line is relevant
            total_actions +=1
            transitions[line.split(" ")[0]] = line.split(" ")[4][3:-1]
    # Transitions = {state, action_string} for every relevant action.
    var_descriptors = ["turn","p1K","p1A","p1W","p1R","p1H","p1_stun","p2K","p2A","p2W","p2R","p2H","p2_stun"]
    for line in open(output+"/tmp.sta","r").readlines()[1:]:   # for every state
        if line.split(":(")[0] in transitions.keys():               # if it's relevant
            single_s = line.split(":(")[0]                          # the state is
            state_desc = line.split(":(")[1][:-2].split(",")
            if choice_available(state_desc):                        # if a choice is needed.
                act = transitions[line.split(":(")[0]]
                guard = guard = "\t[p2_" + act + "] turn = 2 & p1K = "
                guard += state_desc[7] + " & p1A = " + state_desc[8] + " & p1W = " + state_desc[9]
                guard += " & p1R = " + state_desc[10] + " & p1H = " + state_desc[11]
                guard += " & p1_stun = " + state_desc[12] + " &\n\t\t\tp2K = " + state_desc[1]
                guard += " & p2A = " + state_desc[2] + " & p2W = " + state_desc[3] + " & p2R = " + state_desc[4]
                guard += " & p2H = " + state_desc[5] + " & p2_stun = " + state_desc[6] + " ->\n"
                f.write(guard)
                p = 2
                if "skip" in act:
                    result = "(turn' = " + str(3-p) + ") & (p" + str(p) + "_stun' = 0)"
                    action = "\t\t" + result + ";"
                elif act[0] != "A" or len(act) < 4:
                    if "e" in act:
                        damage = "(p" + str(3-p) + act[2] + "' = 0) & "
                    else:
                        damage = "(p" + str(3-p) + act[2] + "' = max(0, p" + str(3-p) + act[2] + " - " + full_name[act[0]] + "_damage)) & "
                    if act[0] == "W":   # add wizard stun to damage
                        damage += "(p" + str(3-p) + "_stun' = " + str(chars.index(act[2])+1) + ") & "
                    if act[0] == "H":   # add healer heal to damage
                        damage += "(p" + str(p) + act[3] + "' = min(" + full_name[act[3]] + "_health, p" + str(p) + act[3] + " + Healer_heal)) & "
                    result = "(turn' = " + str(3-p) + ") & (p" + str(p) + "_stun' = 0)"
                    action = "\t\t(" + full_name[act[0]] + "_accuracy) : " + damage + result + " + "
                    action += "\n\t\t(1 - " + full_name[act[0]] + "_accuracy) : " + result + ";"
                else:
                    result = "(turn' = " + str(3-p) + ") & (p" + str(p) + "_stun' = 0)"
                    targ_1 = "(p" + str(3-p) + act[2] + "' = max(0, p" + str(3-p) + act[2] + " - Archer_damage))"
                    targ_2 = "(p" + str(3-p) + act[3] + "' = max(0, p" + str(3-p) + act[3] + " - Archer_damage))"
                    action = "\t\t(pow(Archer_accuracy,2)) : " + targ_1 + " & " + targ_2 + " & " + result + " + \n"
                    action += "\t\t(Archer_accuracy * (1 - Archer_accuracy)) : " + targ_1 + " & " + result + " + \n"
                    action += "\t\t(Archer_accuracy * (1 - Archer_accuracy)) : " + targ_2 + " & " + result + " + \n"
                    action += "\t\t(pow( (1 - Archer_accuracy),2)) : " + result + ";"
                f.write(action + "\n")

#run("output", "WRH")
