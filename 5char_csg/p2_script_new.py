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
                                        p2_sum = p2K+p2A+p2W+p2R+p2H
                                        p1_sum = p1K+p1A+p1W+p1R+p1H
                                        if p1_sum <= 2 and p2_sum <= 2 and p1_sum > 0 and p2_sum > 0 :
                                            clumps += [str(p1K)+str(p1A)+str(p1W)+str(p1R)+str(p1H)+str(p2K)+str(p2A)+str(p2W)+str(p2R)+str(p2H)]

for clump in clumps:
    state = {}
    l = ["p1K","p1A","p1W","p1R","p1H","p2K","p2A","p2W","p2R","p2H"]
    for i in range(len(clump)):
        state[l[i]] = int(clump[i])
    p1sum = state["p1K"]+state["p1A"]+state["p1W"]+state["p1R"]+state["p1H"]
    p2sum = state["p2K"]+state["p2A"]+state["p2W"]+state["p2R"]+state["p2H"]
    actors = ["p2K", "p2A", "p2W", "p2R", "p2H"]
    unavailable = []
    for c in actors:
        if not state[c]: unavailable += [c]

    # 4 outcomes:
    #       2 available                 - use guard
    #       1 available, others dead    - use guard_1dead
    #       1 available, other stunned  - use guard_k/a/w/r

    # Build guard
    guard = "\t[p2] attack = 0 & turn = 2 & "

    # Add actor info
    if p2sum == 2:  # if 2 actors are available
        for i in range(len(actors)):
            if state[actors[i]]:
                guard += actors[i] + " > 0 & "
        guard += unavailable[0] + "+" + unavailable[1] + "+" + unavailable[2] + " = 0 & p2_stun = 0 &"
    else:   # only 1 player is available for p2
        for i in range(len(actors)):
            if state[actors[i]]:
                guard += actors[i] + " > 0 & "
                break
        guard_1stuns = [guard, guard, guard, guard, guard]          # Either there's someone else alive but stunned.
        for j in range(len(actors)):
            guard_1stuns[j] += "p2_stun = " + str(j+1) + " & " + actors[j] + " > 0 &"
        guard_1dead = guard + "p2_stun != " + str(i+1) + " & p2_sum = " + actors[i] + " &"  # Or they're the only actor alive


    # add target info
    dead = []
    target_guard = "\n\t\t"
    targets = ["p1K", "p1A", "p1W", "p1R", "p1H"]
    for target in ["p1K", "p1A", "p1W", "p1R", "p1H"]:
        if state[target] == 0: dead += [target]
        else: target_guard += target + " > 0 & "
    for i in range(len(dead)):
        target_guard += dead[i]
        if i+1 < len(dead): target_guard += "+"
    target_guard += " = 0"


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

    # Build command for state with 2 actors
    if p2sum == 2:
        possible_actions = []
        poss_actors = []
        poss_targets = []
        for c in l:
            if state[c] and l.index(c) > 4: poss_actors += [c]
            elif state[c]: poss_targets += [c]
        for ac in poss_actors:
            if ac != "p2H" and ac != "p2A":
                for ta in poss_targets:
                    possible_actions += ["p2_" + ac[2] + "_" + ta[2]]
            elif ac == "p2H":
                for ta in poss_targets:
                    possible_actions += ["p2_" + ac[2] + "_" + ta[2] + poss_actors[0][2]] + ["p2_" + ac[2] + "_" + ta[2] + poss_actors[1][2]]
            else:
                if len(poss_targets) > 1:
                    possible_actions += ["p2_A_" + poss_targets[0][2] + poss_targets[1][2]]
                else:
                    possible_actions += ["p2_A_" + poss_targets[0][2]]
        print(guard+target_guard+" ->")
        if len(possible_actions) == 1:
            print("\t\t\t(attack' = " + str(action_d[possible_actions[0]]) + ") & (p2_stun' = 0);")
        else:
            for i in range(len(possible_actions)):
                final_char = " +"
                if i == len(possible_actions) - 1: final_char = ";"
                print("\t\t\t1/"+str(len(possible_actions)) + " : (attack' = " + str(action_d[possible_actions[i]]) + ") & (p2_stun' = 0)" + final_char)

    else:
        possible_actions = []
        ac = ""
        poss_targets = []
        for c in l:
            if state[c] and l.index(c) > 4: ac = c
            elif state[c]: poss_targets += [c]
        if ac != "p2H" and ac != "p2A":
            for ta in poss_targets:
                possible_actions += ["p2_" + ac[2] + "_" + ta[2]]
        elif ac == "p2H":
            for ta in poss_targets:
                possible_actions += ["p2_" + ac[2] + "_" + ta[2] + "H"]
        else:
            if len(poss_targets) > 1:
                possible_actions += ["p2_A_" + poss_targets[0][2] + poss_targets[1][2]]
            else:
                possible_actions += ["p2_A_" + poss_targets[0][2]]
        print(guard_1dead+target_guard+" ->")
        if len(possible_actions) == 1:
            print("\t\t\t(attack' = " + str(action_d[possible_actions[0]]) + ") & (p2_stun' = 0);")
        else:
            for i in range(len(possible_actions)):
                final_char = " +"
                if i == len(possible_actions) - 1: final_char = ";"
                print("\t\t\t1/"+str(len(possible_actions)) + " : (attack' = " + str(action_d[possible_actions[i]]) + ") & (p2_stun' = 0)" + final_char)
        for stunned_c in range(len(actors)):
            if state[actors[stunned_c]]: continue
            possible_actions_spec = possible_actions
            if ac == "p2H":
                for ta in poss_targets:
                    possible_actions_spec += ["p2_H_" + ta[2] + actors[stunned_c][2]]
            print(guard_1stuns[stunned_c] + target_guard+" ->")
            if len(possible_actions_spec) == 1:
                print("\t\t\t(attack' = " + str(action_d[possible_actions_spec[0]]) + ") & (p2_stun' = 0);")
            else:
                for i in range(len(possible_actions_spec)):
                    final_char = " +"
                    if i == len(possible_actions_spec) - 1: final_char = ";"
                    print("\t\t\t1/"+str(len(possible_actions_spec)) + " : (attack' = " + str(action_d[possible_actions_spec[i]]) + ") & (p2_stun' = 0)" + final_char)
            if ac == "p2H":
                for ta in poss_targets:
                    possible_actions_spec.remove("p2_H_" + ta[2] + actors[stunned_c][2])
