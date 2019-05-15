clumps = []
for p1K in [1,0]:
    for p1A in [1,0]:
        for p1W in [1,0]:
            for p1R in [1,0]:
                for p1H in [1,0]:
                    for p2K in [1,0]:
                        for p2A in [1,0]:
                            for p2W in [1,0]:
                                for p2R in [1,0]:
                                    for p2H in [1,0]:
                                        for p2_heal in [4,3,2,1,0]:   # other target that can be healed
                                            p2_sum = p2K+p2A+p2W+p2R+p2H
                                            if p1K+p1A+p1W+p1R+p1H <= 2 and p2_sum <= 2 and p1K+p1A+p1W+p1R+p1H > 0 and p2_sum > 0 :
                                                clumps += [str(p1K)+str(p1A)+str(p1W)+str(p1R)+str(p1H)+str(p2K)+str(p2A)+str(p2W)+str(p2R)+str(p2H)+str(p2_heal)]

for clump in clumps:
    state = {}
    l = ["p1K","p1A","p1W","p1R","p1H","p2K","p2A","p2W","p2R","p2H","p2_heal"]
    for i in range(len(clump)):
        state[l[i]] = int(clump[i])
    p1sum = state["p1K"]+state["p1A"]+state["p1W"]+state["p1R"]+state["p1H"]
    p2sum = state["p2K"]+state["p2A"]+state["p2W"]+state["p2R"]+state["p2H"]
    actors = ["p2K", "p2A", "p2W", "p2R", "p2H"]

    # Build guard
    guard = "\t[p2] attack = 0 & turn = 2 & "

    # Add actor info
    if not state["p2H"] or p1sum != 1:
        for i in range(len(actors)):
            if state[actors[i]]: guard += actors[i] + " > 0 & (p2_stun != " + str(i+1) + ") & "
            else: guard += "(" + actors[i] + " = 0 | p2_stun = " + str(i+1) + ") & "
            if len(guard) > 120 and len(guard) < 150:
                guard += "\n\t"
    else:
        for i in range(len(actors)):
            if state[actors[i]]: guard += actors[i] + " > 0 & (p2_stun != " + str(i+1) + ") & "
            else: guard += "(" + actors[i] + " = 0 | p2_stun = " + str(i+1) + ") & "
            if len(guard) > 120 and len(guard) < 150:
                guard += "\n\t"
        if state["p2_heal"] != 4:  guard += actors[state["p2_heal"]] + " > 0 & "                # if extra heal target is healer..

    # add target info
    dead = []
    for target in ["p1K", "p1A", "p1W", "p1R", "p1H"]:
        if state[target] == 0: dead += [target]
        else: guard += target + " > 0 & "
    guard += "("
    for i in range(len(dead)):
        guard += dead[i]
        if i+1 < len(dead): guard += "+"
    guard += ") = 0"

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

    # Build command

    # find possible actions
    possible_actions = []
    for act in action_d.keys():
        if act[1] == "1": continue
        actor = act[3]
        actor, target = act.split("_")[1], act.split("_")[2]
        if state["p2" + actor]:                     # if the actor is able to act..
            if len(target) == 1:                    # if there is only one target..
                if state["p1" + target]:
                    possible_actions += [action_d[act]]
            elif actor == "A":                      # actor is an archer
                if state["p1" + target[0]] and state["p1" + target[1]]:
                    possible_actions += [action_d[act]]
            else:                                   # actor is a healer
                # if the target is alive then the healer can attack it and heal themself:
                if state["p1" + target[0]] and target[1] == "H":
                    possible_actions += [action_d[act]]
                # if the target is alive and the healer is the only available target then it can check if the heal target is alive to heal them
                elif state["p1" + target[0]] and p2_sum == 1:
                    possible_actions += [action_d[act]]


    #print(guard + " ->")
    if len(possible_actions) == 1:
        print(guard + " ->")
        print("\t\t(attack' = " + str(possible_actions[0]) + ") & (p2_stun' = 0);")
    # else:
    #     for i in range(len(possible_actions)):
    #         final_char = " +"
    #         if i == len(possible_actions) - 1: final_char = ";"
    #         print("\t\t1/"+str(len(possible_actions)) + " : (attack' = " + str(possible_actions[i]) + ") & (p2_stun' = 0)" + final_char)
