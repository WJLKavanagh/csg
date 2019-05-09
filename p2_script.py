for p1K in [1,0]:
    for p1A in [1,0]:
        for p1W in [1,0]:
            for p2K in [1,0]:
                for p2A in [1,0]:
                    for p2W in [1,0]:
                        if p1K+p1A+p1W == 3 or p2K+p2A+p2W == 3 or (p1K+p1A+p1W)*(p2K+p2A+p2W) == 0:
                            continue
                        # Build guard
                        p1sum = p1K+p1A+p1W
                        guard = "  [p2]  attack = 0 & turn = 2 & "
                        if p1K:
                            guard += "p1K > 0 & "
                        else:
                            guard += "p1K = 0 & "
                        if p1A:
                            guard += "p1A > 0 & "
                        else:
                            guard += "p1A = 0 & "
                        if p1W:
                            guard += "p1W > 0 & "
                        else:
                            guard += "p1W = 0 & "
                        if p2K:
                            guard += "p2K > 0 & p2_stun != 1 & \n\t"
                        else:
                            guard += "(p2K = 0 | p2_stun = 1) & \n\t"
                        if p2A:
                            guard += "p2A > 0 & p2_stun != 2 & "
                        else:
                            guard += "(p2A = 0 | p2_stun = 2) & "
                        if p2W:
                            guard += "p2W > 0 & p2_stun != 3 "
                        else:
                            guard += "(p2W = 0 | p2_stun = 3) "
                        # Build command
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

                        print(guard + "->")
                        if len(possible_actions) == 1:
                            print("\t\t(attack' = " + str(possible_actions[0]) + ") & (p2_stun' = 0);")
                        else:
                            for i in range(len(possible_actions)):
                                final_char = " +"
                                if i == len(possible_actions) - 1: final_char = ";"
                                print("\t\t1/"+str(len(possible_actions)) + " : (attack' = " + str(possible_actions[i]) + ") & (p2_stun' = 0)" + final_char)
