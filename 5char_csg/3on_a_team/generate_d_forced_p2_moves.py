chars = ["K","A","W","R","H"]
full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
trips = []
for a in range(5):
    for b in range(a+1,5):
        for c in range(b+1,5):
            trips += [chars[a] + chars[b] + chars[c]]

def do_command(guard):
    # takes a guard as list of var declarations, writes the command to file
    available_actions = []
    var_pos = {}        # dictionary of vars and their positions
    for var in guard:
        var_pos[var.split(" ")[0]] = var.split(" ")[1] + " " + var.split(" ")[2]

    # Add Knight
    if var_pos["p2K"] == "> 0" and var_pos["p2_stun"] != "= 1":
        # Knight is a valid actor
        for opp in chars:
            if var_pos["p1" + opp] != "= 0":
                available_actions += ["K_" + opp]
    # Archer
    if var_pos["p2A"] == "> 0" and var_pos["p2_stun"] != "= 2":
        for opp in chars:
            if var_pos["p1" + opp] != "= 0":
                available_actions += ["A_" + opp]
                for opp2 in chars:
                    if chars.index(opp2) > chars.index(opp) and var_pos["p1" + opp2] != "= 0":
                        available_actions += ["A_" + opp + opp2]
    # Wizard
    if var_pos["p2W"] == "> 0" and var_pos["p2_stun"] != "= 3":
        for opp in chars:
            if var_pos["p1" + opp] != "= 0":
                available_actions += ["W_" + opp]
    # Rogue
    if var_pos["p2R"] == "> 0" and var_pos["p2_stun"] != "= 4":
        for opp in chars:
            if var_pos["p1" + opp] != "= 0":
                if var_pos["p1" + opp] == "> Rogue_execute":
                    available_actions += ["R_" + opp]
                else:
                    available_actions += ["R_" + opp + "e"]
    # Healer
    if var_pos["p2H"] == "> 0" and var_pos["p2_stun"] != "= 5":
        for opp in chars:
            if var_pos["p1" + opp] != "= 0":
                for char in chars:
                    if var_pos["p2"+char] != "= 0":
                        available_actions += ["H_" + opp + char]
    # available_actions enumerated
    for act in available_actions:
        p = 2
        if act[0] != "A" or len(act) < 4:
            if "e" in act:
                damage = "(p" + str(3-p) + act[2] + "' = 0) & "
            else:
                damage = "(p" + str(3-p) + act[2] + "' = max(0, p" + str(3-p) + act[2] + " - " + full_name[act[0]] + "_damage)) & "
            if act[0] == "W":   # add wizard stun to damage
                damage += "(p" + str(3-p) + "_stun' = " + str(chars.index(act[2])+1) + ") & "
            if act[0] == "H":   # add healer heal to damage
                damage += "(p" + str(p) + act[3] + "' = min(" + full_name[act[3]] + "_health, p" + str(p) + act[3] + " + Healer_heal)) & "
            result = "(turn' = " + str(3-p) + ") & (p" + str(p) + "_stun' = 0)"
            action = "\t\t(" + full_name[act[0]] + "_accuracy)/" + str(len(available_actions)) + " : " + damage + result + " + "
            action += "\n\t\t(1 - " + full_name[act[0]] + "_accuracy)/" + str(len(available_actions)) + " : " + result
            if available_actions.index(act) == len(available_actions) - 1: action += ";"
            else: action += "+"
        else:
            result = "(turn' = " + str(3-p) + ") & (p" + str(p) + "_stun' = 0)"
            targ_1 = "(p" + str(3-p) + act[2] + "' = max(0, p" + str(3-p) + act[2] + " - Archer_damage))"
            targ_2 = "(p" + str(3-p) + act[3] + "' = max(0, p" + str(3-p) + act[3] + " - Archer_damage))"
            action = "\t\t(pow(Archer_accuracy,2))/" + str(len(available_actions)) + " : " + targ_1 + " & " + targ_2 + " & " + result + " + \n"
            action += "\t\t(Archer_accuracy * (1 - Archer_accuracy))/" + str(len(available_actions)) + " : " + targ_1 + " & " + result + " + \n"
            action += "\t\t(Archer_accuracy * (1 - Archer_accuracy))/" + str(len(available_actions)) + " : " + targ_2 + " & " + result + " + \n"
            action += "\t\t(pow( (1 - Archer_accuracy),2))/" + str(len(available_actions)) + " : " + result
            if available_actions.index(act) == len(available_actions) - 1: action += ";"
            else: action += "+"
    if len(available_actions) == 1: return(action + "\n")
    return("fail")

def run(file):
    # writes full naive, deterministic strategy for p2 to <file>
    global f
    f = open(file,"w")
    f.write("// player 2 - forced moves\n")
    possible_states = {
    "p1K ":["= 0","> 0 & p1K <= Rogue_execute", "> Rogue_execute"],
    "p1A ":["= 0","> 0 & p1A <= Rogue_execute", "> Rogue_execute"],
    "p1W ":["= 0","> 0 & p1W <= Rogue_execute", "> Rogue_execute"],
    "p1R ":["= 0","> 0 & p1R <= Rogue_execute", "> Rogue_execute"],
    "p1H ":["= 0","> 0 & p1H <= Rogue_execute", "> Rogue_execute"]}
    friendly_vars = ["= 0", "> 0"]

    opposition_states = []
    for p1k in possible_states["p1K "]:
        for p1a in possible_states["p1A "]:
            for p1w in possible_states["p1W "]:
                for p1r in possible_states["p1R "]:
                    for p1h in possible_states["p1H "]:
                        if (p1k+p1a+p1w+p1r+p1h).count("= 0") >= 2 and (p1k+p1a+p1w+p1r+p1h).count("= 0") < 5:
                            opposition_guard = "p1K " + p1k + " & p1A " + p1a + " & p1W " + p1w + " & p1R " + p1r + " & p1H " + p1h
                            opposition_states += [opposition_guard]

    friendly_states = []
    for p2k in friendly_vars:
        for p2a in friendly_vars:
            for p2w in friendly_vars:
                for p2r in friendly_vars:
                    for p2h in friendly_vars:
                        for p2_s in range(6):
                            if (p2k+p2a+p2w+p2r+p2h).count("= 0") >= 2 and (p2k+p2a+p2w+p2r+p2h).count("= 0") < 5:
                                friendly_guard = "p2K " + p2k + " & p2A " + p2a + " & p2W " + p2w + " & p2R " + p2r + " & p2H " + p2h
                                friendly_guard += " & p2_stun = " + str(p2_s)
                                friendly_states += [friendly_guard]

    for os in opposition_states:
        for fs in friendly_states:
            comm = do_command((os+" & "+fs).split(" & "))
            if comm != "fail":
                f.write("\t[p2] " + os + " & \n\t  " + fs + " ->\n")    # print guard
                f.write(comm)
    f.close()

run("forced_p2_moves.txt")
