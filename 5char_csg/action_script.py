def full(c):
    f_chars = ["Knight", "Archer", "Wizard", "Rogue", "Healer"]
    for c1 in f_chars:
        if c1[0] == c:
            return c1

# Build attack dictionary
attack_num = 1
attacks = {}
chars = ["K", "A", "W", "R", "H"]
for p in range(2):
    mid = str(p+1) + "_"
    for actor in chars:
        start = actor + mid
        for target in chars:
            action_string = start + target + str(2-p)
            if actor == "K":
                attacks[action_string] = attack_num
                attack_num += 1
            elif actor == "A":
                attacks[action_string] = attack_num
                attack_num += 1
                for st_index in range(chars.index(target)+1, len(chars)):           # second target index
                    attacks[action_string + chars[st_index] + str(2-p)] = attack_num
                    attack_num += 1
            elif actor == "W":
                attacks[action_string] = attack_num
                attack_num += 1
            elif actor == "R":
                attacks[action_string] = attack_num
                attack_num += 1
            else:
                for heal_target in chars:
                    attacks[action_string + heal_target + str(1+p)] = attack_num
                    attack_num += 1

f_chars = ["Knight", "Archer", "Wizard", "Rogue", "Healer"]
print(attacks)
# # parse dict
# guard_attacks = {}
# for a in attacks.keys():
#     new_a = "p" + a[1] + "_"
#     for c in a:
#         if c in ["K","A","W","H","R","_"]:
#             new_a += c
#     guard_attacks[new_a] = attacks[a]
# print(guard_attacks)
"""
# Print G-C
for att in attacks.keys():
    guard = "\t[" + att + "] attack = " + str(attacks[att])
    guard += " & p" + att.split("_")[1][1] + att.split("_")[1][0] + " > 0"
    if len(att) > 5:
        guard += " & p" + att.split("_")[1][3] + att.split("_")[1][2] + " > 0"
    if att[0] == "R":
        guard_2 = guard + " & p" +att.split("_")[1][1] + att.split("_")[1][0] + " <= Rogue_execute"
        guard += " & p" +att.split("_")[1][1] + att.split("_")[1][0] + " > Rogue_execute"
    print(guard + " ->")

    comm_end = " (attack' = 0) & (turn' = " + str(3-int(att[1])) + ")"
    command = "\t\t"
    target = "p" + att[4] + att[3]
    if att[0] == "K":
        hit = "(" + target + "' = max(0, " + target + " - Knight_damage)) &" + comm_end
        command += "Knight_accuracy : " + hit + " + \n\t\t1 - Knight_accuracy :" + comm_end + ";"
    elif att[0] == "A":
        if len(att) > 5:
            # There are two targets
            target_2 = "p" + att[6] + att[5]
            hit_hit = "(" + target + "' = max(0, " + target + " - Archer_damage)) & "
            hit_hit += "(" + target_2 + "' = max(0, " + target_2 + " - Archer_damage)) &" + comm_end
            hit_one = "(" + target + "' = max(0, " + target + " - Archer_damage)) &" + comm_end
            hit_two = "(" + target_2 + "' = max(0, " + target_2 + " - Archer_damage)) &" + comm_end
            command += "pow(Archer_accuracy,2) : " + hit_hit + " +\n\t\t"
            command += "Archer_accuracy * (1 - Archer_accuracy) : " + hit_one + " +\n\t\t"
            command += "Archer_accuracy * (1 - Archer_accuracy) : " + hit_two + " +\n\t\t"
            command += "pow((1 - Archer_accuracy),2) :" + comm_end + ";"
        else:
            # There is one target
            hit = "(" + target + "' = max(0, " + target + " - Archer_damage)) &" + comm_end
            command += "Archer_accuracy : " + hit + " + \n\t\t1 - Archer_accuracy :" + comm_end + ";"
    elif att[0] == "W":
        st_str = "p" + att[4] + "_stun' = " + str(chars.index(att[3]) + 1)                    # stun string
        hit = "(" + target + "' = max(0, " + target + " - Wizard_damage)) & (" + st_str + ") &" + comm_end
        command += "Wizard_accuracy : " + hit + " + \n\t\t1 - Wizard_accuracy :" + comm_end + ";"
    elif att[0] == "R":
        hit = "(" + target + "' = " + target + " - Rogue_damage) &" + comm_end
        command_2 = command + "Rogue_accuracy : " + hit + " + \n\t\t1 - Rogue_accuracy :" + comm_end + ";"
        command += "Rogue_accuracy : " + "(" + target + "' = 0) &" + comm_end + " +"
        command += "\n\t\t1 - Rogue_accuracy :" + comm_end + ";" # can execute, will execute
        print(command_2)
        print(guard_2 + " ->")
    elif att[0] == "H":
        h_target = "p" + att[6] + att[5]
        hit = "(" + target + "' = max(0, " + target + " - Healer_damage)) & ("
        hit += h_target + "' = min(" + full(att[5]) + "_health,(" + h_target + " + Healer_heal))) &" + comm_end
        command += "Healer_accuracy : " + hit + " + \n\t\t1 - Healer_accuracy :" + comm_end + ";"
    print(command)

"""
