# WJL - 31/7
# Generate the PRISM code to describe p2 in 5-char-3-a-side RPGLite playing a naive strategy.
possible_states = []
# s = {p1k, p1a, p1w, p1r, p1h, p2k, p2a, p2w, p2r, p2h}
for p1k_alive in [True, False]:
    for p1a_alive in [True, False]:
        for p1w_alive in [True, False]:
            for p1r_alive in [True,False]:
                for p1h_alive in [True,False]:
                    if p1k_alive + p1a_alive + p1w_alive + p1r_alive + p1h_alive <= 3 and \
                    p1k_alive + p1a_alive + p1w_alive + p1r_alive + p1h_alive > 0:
                        for p2k_alive in [True, False]:
                            for p2a_alive in [True, False]:
                                for p2w_alive in [True, False]:
                                    for p2r_alive in [True,False]:
                                        for p2h_alive in [True,False]:
                                            if p2k_alive + p2a_alive + p2w_alive + p2r_alive + p2h_alive <= 3 \
                                            and p2k_alive + p2a_alive + p2w_alive + p2r_alive + p2h_alive > 0:
                                                for stun in range(6):
                                                    possible_states += [[p1k_alive,
                                                    p1a_alive, p1w_alive, p1r_alive, p1h_alive,
                                                    p2k_alive, p2a_alive, p2w_alive, p2r_alive,
                                                    p2h_alive, stun]]
empty = 0
for s in possible_states:
    possible_actions = []
    guard = "\t[p2]\tattack = 0 & turn = 2 & "
    s_desc = ["p1K","p1A","p1W","p1R","p1H","p2K","p2A","p2W","p2R","p2H","p2_stun"]
    for i in range(11):
        if i < 10:
            guard += s_desc[i] + " "
            if s[i]: guard += "> 0 & "
            else: guard += "= 0 & "
        else:
            guard += "p2_stun = " + str(s[10])
        if i==4:
            guard += "\n\t\t"

    if s[5] and s[10] != 1:     # if K alive and not stunned
        for i in range(5):
            if s[i]:
                possible_actions += [56+i]
    if s[6] and s[10] != 2:     # if A alive and not stunned
        if s[0]: possible_actions += [61]
        if s[0] and s[1]: possible_actions += [62]
        if s[0] and s[2]: possible_actions += [63]
        if s[0] and s[3]: possible_actions += [64]
        if s[0] and s[4]: possible_actions += [65]
        if s[1]: possible_actions += [66]
        if s[1] and s[2]: possible_actions += [67]
        if s[1] and s[3]: possible_actions += [68]
        if s[1] and s[4]: possible_actions += [69]
        if s[2]: possible_actions += [70]
        if s[2] and s[3]: possible_actions += [71]
        if s[2] and s[4]: possible_actions += [72]
        if s[3]: possible_actions += [73]
        if s[3] and s[4]: possible_actions += [74]
        if s[4]: possible_actions += [75]
    if s[7] and s[10] != 3:     # if W alive and not stunned
        for i in range(5):
            if s[i]:
                possible_actions += [76+i]
    if s[8] and s[10] != 4:     # if R alive and not stunned
        for i in range(5):
            if s[i]:
                possible_actions += [81+i]
    if s[9] and s[10] != 5:     # if H alive and not stunned
        for i in range(5):
            if s[i]:
                for j in range(5,10):
                    if s[j]:
                        possible_actions += [81+(5*i)+j]
    command = "\t\t"
    for i in range(len(possible_actions)):
        command += "1/" + str(len(possible_actions)) + " : (attack' = " + str(possible_actions[i]) + ") & (p2_stun' = 0)"
        if i < len(possible_actions)-1: command += " +\n\t\t"
    if len(possible_actions) == 1:
        print(guard + " ->")
        print(command + ";")
    else: empty += 1

# 'p2_K_K': 56, 'p2_K_A': 57, 'p2_K_W': 58, 'p2_K_R': 59, 'p2_K_H': 60,
# 'p2_A_K': 61,  'p2_A_KA': 62, 'p2_A_KW': 63, 'p2_A_KR': 64, 'p2_A_KH': 65, 'p2_A_A': 66, 'p2_A_AW': 67, 'p2_A_AR': 68, 'p2_A_AH': 69, 'p2_A_W': 70,
# 'p2_A_WR': 71, 'p2_A_WH': 72, 'p2_A_R': 73, 'p2_A_RH': 74, 'p2_A_H': 75,
#  'p2_W_K': 76, 'p2_W_A': 77, 'p2_W_W': 78, 'p2_W_R': 79, 'p2_W_H': 80, 'p2_R_K': 81, 'p2_R_A': 82,
# 'p2_R_W': 83, 'p2_R_R': 84, 'p2_R_H': 85, 'p2_H_KK': 86, 'p2_H_KA': 87, 'p2_H_KW': 88, 'p2_H_KR': 89, 'p2_H_KH': 90, 'p2_H_AK': 91, 'p2_H_AA': 92,
# 'p2_H_AW': 93, 'p2_H_AR': 94, 'p2_H_AH': 95, 'p2_H_WK': 96, 'p2_H_WA': 97, 'p2_H_WW': 98, 'p2_H_WR': 99, 'p2_H_WH': 100, 'p2_H_RK': 101, 'p2_H_RA': 102,
# 'p2_H_RW': 103, 'p2_H_RR': 104, 'p2_H_RH': 105, 'p2_H_HK': 106, 'p2_H_HA': 107, 'p2_H_HW': 108, 'p2_H_HR': 109, 'p2_H_HH': 110
