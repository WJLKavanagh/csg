chars = ["K","A","W","R","H"]

"""
c = len(chars)
for i in range(c):
    for j in range(i,c):
        if i == j: continue
        p_string = "\t1/10 : (p2"
        used = [chars[i],chars[j]]
        for c_ in chars:
            if c_ not in used:
                p_string += c_ + "' = 0) & (p2"
        p_string += ") +"
        print(p_string)
"""

attack_num = 1  # first action

for actor in chars:
    for target in chars:
        guard = "attack = 0 & turn = 1 & p1" + actor + " > 0 & p1_stun != "
        guard += str(chars.index(actor) + 1) + " & p2" + target + " > 0"
        command = "(attack' = "
        if actor == "K":
            label = "[p1_K_" + target + "]"
            K_command = command
            K_command += str(attack_num) + ") & (p1_stun' = 0);"
            print(label, guard, "->\n\t", K_command)
            attack_num += 1
        elif actor == "A":
            A_command = command + str(attack_num) + ") & (p1_stun' = 0);"
            label = "[p1_A_" + target + "]"
            print(label, guard, "->\n\t", A_command)
            attack_num += 1
            for st_index in range(chars.index(target)+1, len(chars)):           # second target index
                #attacks[action_string + chars[st_index] + str(2-p)] = attack_num
                label = "[p1_A_" + target + chars[st_index] + "]"
                A_command = command + str(attack_num) + ") & (p1_stun' = 0);"
                A_guard = guard + " & p2" + chars[st_index] + " > 0"
                print(label, A_guard, "->\n\t", A_command)
                attack_num += 1
        elif actor == "W":
            label = "[p2_W_" + target + "]"
            command += str(attack_num) + ") & (p1_stun' = 0);"
            print(label, guard, "->\n\t", command)
            #print(label, attack_num)
            attack_num += 1
        elif actor == "R":
            label = "[p1_R_" + target + "]"
            command += str(attack_num) + ") & (p1_stun' = 0);"
            print(label, guard, "->\n\t", command)
            attack_num += 1
        elif actor == "H":
            for heal_target in chars:
                H_command = command
                label = "[p1_H_" + target + heal_target + "]"
                H_guard = guard + " & p1" + heal_target + " > 0"
                H_command += str(attack_num) + ") & (p1_stun' = 0);"
                print(label, H_guard, "->\n\t", H_command)
                attack_num += 1
