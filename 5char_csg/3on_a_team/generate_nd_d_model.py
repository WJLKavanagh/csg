import datetime, sys, generate_d_p2_moves

chars = ["K","A","W","R","H"]       # characters
full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}

moves = []  # move list -- building..
for c in chars:
    moves += ["K_"+c]
for c1 in range(len(chars)):
    moves += ["A_"+chars[c1]]
    for c2 in range(c1+1,len(chars)):
        moves += ["A_"+chars[c1]+chars[c2]]
for c in chars:
    moves += ["W_"+c]
for c in chars:
    moves += ["R_"+c]
    moves += ["R_"+c+"e"]        # R_xe = target x in execute range.
for c in chars:
    for d in chars:
        moves += ["H_"+c+d]
moves += ["skip"]

def do_choice_and_flip(t):
    f.write("// Choose opposing material" + "\n")
    choices = []
    if len(t) == 2:
        for a in range(len(chars)):
            for b in range(a+1,len(chars)):
                choices += ["choose_"+chars[a]+chars[b]]
    else:
        for a in range(len(chars)):
            for b in range(a+1,len(chars)):
                for c in range(b+1,len(chars)):
                    choices += ["choose_"+chars[a]+chars[b]+chars[c]]
    f.write("\t[choose_opponents] p2K > 0 & p2A > 0 & p2W > 0 & p2R > 0 & p2H > 0 ->" + "\n")
    for c in choices:
        comm = "\t\t1/10 : "
        num_printed = 0
        for ch in chars:
            if ch not in c:
                comm += "(p2" + ch + "' = 0)"
                num_printed += 1
                if num_printed < 5 - len(t):
                    comm += " & "
        if choices.index(c) < len(choices)-1: f.write(comm + " +" + "\n")
        else: f.write(comm + ";" + "\n")
    f.write("\n//who goes first (deterministic)" + "\n")
    f.write("\t[coin_flip] turn = 0 & p2K*p2A*p2W*p2R*p2H = 0 ->\n\t\t0.5 : (turn' = 1) + 0.5 : (turn' = 2);\n" + "\n")

def do_prefix(team, config):
    f.write("// Author:\tWilliam Kavanagh, University of Glasgow\n")
    f.write("// Created:\t" + str(datetime.datetime.now()).split(" ")[0] + "\n")
    f.write("// File:\t\tCSG auto-generated model\n")
    f.write("// Comment:\tThis file is a generator for a later strategy for " + team + "\n")
    f.write("\n// Configuration " + config.upper() + ":\n" + "\n")
    f.write("mdp" + "\n")
    f.write(open("../configurations/" + config + ".txt", "r").read() + "\n")
    f.write("module game" + "\n")
    f.write("\tturn\t: [0..2];" + "\n")
    for char in chars:
        if char in team:
            f.write("\tp1" + char + "\t: [0.." + full_name[char] + "_health]\t\tinit " + full_name[char] + "_health; // P1 " + full_name[char] + "\n")
        else:
            f.write("\tp1" + char + "\t: [0.." + full_name[char] + "_health]\t\tinit 0; // P1 " + full_name[char] + " not used" + "\n")
    f.write("\tp1_stun\t: [0..5];\t\t\t\t//0 - none, 1 - Knight stunned, 2 - Archer stunned, 3 - Wizard stunned .. etc" + "\n")
    for char in chars:
        f.write("\tp2" + char + "\t: [0.." + full_name[char] + "_health]\t\tinit " + full_name[char] + "_health; // P2 " + full_name[char] + "\n")
    f.write("\tp2_stun\t: [0..5];\t\t\t\t//0 - none, 1 - Knight stunned, 2 - Archer stunned, 3 - Wizard stunned .. etc\n" + "\n")
    do_choice_and_flip(team)

def do_guard(p, act):
    if act == "skip":
        f.write("\t[p" + str(p) + "_skip] turn = " + str(p) + " ->" + "\n")
        return()
    # Take a player, p, and an action, act. f.write out the appropriate guard
    guard = "\t[p" + str(p) + "_" + act + "] turn = " + str(p) + " & "          # label and turn information
    guard += "p" + str(p) + act[0] + " > 0 & p" + str(p) + "_stun != " + str(chars.index(act[0])+1) + " &"
    if act[0] != "R":
        guard += " p" + str(3-p) + act[2] + " > 0 "        # target information
    elif "e" not in act:
        guard += " p" + str(3-p) + act[2] + " > Rogue_execute "
    else:
        guard += " p" + str(3-p) + act[2] + " <= Rogue_execute "
    if act[0] == "A" and len(act) > 3:
        guard += "& p" + str(3-p) + act[3] + " > 0 "
    elif act[0] == "H" and act[3] != "H":
        guard += "& p" + str(p) + act[3] + " > 0 "
    f.write(guard + "->" + "\n")

def do_command(p,act):
    # now the actions..
    if act == "skip":
        f.write("\t\t(turn' = " + str(3-p) + ") & (p" + str(p) + "_stun' = 0);" + "\n")
        return()
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
        action = "\t\t" + full_name[act[0]] + "_accuracy : " + damage + result + " + "
        action += "\n\t\t1 - " + full_name[act[0]] + "_accuracy : " + result + ";"
    else:
        result = "(turn' = " + str(3-p) + ") & (p" + str(p) + "_stun' = 0)"
        targ_1 = "(p" + str(3-p) + act[2] + "' = max(0, p" + str(3-p) + act[2] + " - Archer_damage))"
        targ_2 = "(p" + str(3-p) + act[3] + "' = max(0, p" + str(3-p) + act[3] + " - Archer_damage))"
        action = "\t\tpow(Archer_accuracy,2) : " + targ_1 + " & " + targ_2 + " & " + result + " + \n"
        action += "\t\tArcher_accuracy * (1 - Archer_accuracy) : " + targ_1 + " & " + result + " + \n"
        action += "\t\tArcher_accuracy * (1 - Archer_accuracy) : " + targ_2 + " & " + result + " + \n"
        action += "\t\tpow( (1 - Archer_accuracy),2) : " + result + ";"
    f.write(action + "\n")

def run(p1_team, configuration, file_to_write):
    global f
    f = open(file_to_write, "w+")
    do_prefix(p1_team, configuration)
    f.write("// Actions for p1\n")
    for e in moves:
        do_guard(1,e)
        do_command(1,e)
    f.write("\n")
    f.close()
    generate_d_p2_moves.run(file_to_write)
    f = open(file_to_write,"a")
    f.write("endmodule\n" + "\n")
    f.write("formula p1_sum = p1K+p1A+p1W+p1R+p1H;" + "\n")
    f.write("formula p2_sum = p2K+p2A+p2W+p2R+p2H;" + "\n")
    f.write('label "p1_wins" = p1_sum > 0 & p2_sum = 0;' + "\n")
    f.write('label "p2_wins" = p1_sum = 0 & p2_sum > 0;' + "\n")
    f.close()

run("KAW","delta9","mdp_test.prism")
