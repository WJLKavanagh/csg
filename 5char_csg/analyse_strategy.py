import sys

def display_action_rundown_from_dictionary(d):
    global act_parse
    # Take a dictionary of actions and the number of times they occur, print the information neatly
    total_actions = 0
    actions_in_order = sorted(d.items(), key=lambda kv: -kv[1])
    for elem in d:
        total_actions += d[elem]
    output_string = ". Of " + str(total_actions) + " actions:\n\t\t\t"
    for action in actions_in_order:
        output_string = output_string + act_parse[action[0][0]] + " attacked " + act_parse[action[0].split("_")[1][0]]
        if len(action[0].split("_")[1]) > 1:
            if action[0][0] == "A": output_string += " and " + act_parse[action[0].split("_")[1][1]]
            else: output_string += " healing " + act_parse[action[0].split("_")[1][1]]
        output_string = output_string +  " " + str(action[1]) + " times,\n\t\t\t"

    return output_string

act_parse = {"K":"Knight", "A":"Archer", "W":"Wizard", "R":"Rogue", "H":"Healer"}
strategy_file = open(sys.argv[1], "r").readlines()      # Read strategy from file as list of lines
for i in range(len(strategy_file)):
    if "// Forced skip" in strategy_file[i]:
        break
strategy_file = strategy_file[i+3:-1]                     # Examine only interesting transitions

chars = ["K","A","W","R","H"]
action_dictionary = {}                                      # Pair every state (list) with action (str)
for i in range(len(strategy_file)):
    if "[p2" in strategy_file[i]:
        action = strategy_file[i][5:].split("]")[0]
        var_suffix = chars + ["_stun"]
        state_list = ""
        for p in range(1,3):
            for suffix in var_suffix:
                state_list += strategy_file[i+p-1].split("p"+str(p) + suffix +" = ")[1].split(" ")[0]+","
        action_dictionary[state_list[:-1]] = action

pairs = []
for j in range(len(chars)):
    for k in range(j+1,len(chars)):
        pairs += [chars[j] + chars[k]]

pair_used = sys.argv[1].split("/")[1][:2]
print("Analysing strategy for a " + pair_used + " pair:\n")

for pair in pairs:
    actions_for_both_alive = {}
    actions_for_first_alive = {}
    actions_for_second_alive = {}
    for s in action_dictionary.keys():
        if int(s.split(",")[chars.index(pair[0])]) > 0 and int(s.split(",")[chars.index(pair[1])]) > 0:
            if int(s.split(",")[6+chars.index(pair_used[0])]) > 0 and int(s.split(",")[6+chars.index(pair_used[1])]) > 0:
                if action_dictionary[s] in actions_for_both_alive:
                    actions_for_both_alive[action_dictionary[s]] += 1
                else:
                    actions_for_both_alive[action_dictionary[s]] = 1
            elif int(s.split(",")[6+chars.index(pair_used[0])]) > 0:
                if action_dictionary[s] in actions_for_first_alive:
                    actions_for_first_alive[action_dictionary[s]] += 1
                else:
                    actions_for_first_alive[action_dictionary[s]] = 1
            elif int(s.split(",")[6+chars.index(pair_used[1])]) > 0:
                if action_dictionary[s] in actions_for_second_alive:
                    actions_for_second_alive[action_dictionary[s]] += 1
                else:
                    actions_for_second_alive[action_dictionary[s]] = 1
    print("Against a " + act_parse[pair[0]] + "-" + act_parse[pair[1]] + " pair:")
    print("\tWith both opponents alive...")
    print("\t\t...and both allied characters alive" + display_action_rundown_from_dictionary(actions_for_both_alive))
    print("\t\t...and only " + pair_used[0] + " alive" + display_action_rundown_from_dictionary(actions_for_first_alive))
    print("\t\t...and only " + pair_used[1] + " alive" + display_action_rundown_from_dictionary(actions_for_second_alive))

    actions_for_both_alive = {}
    for s in action_dictionary.keys():
        if int(s.split(",")[chars.index(pair[0])]) > 3 and int(s.split(",")[chars.index(pair[1])]) > 3:
            if int(s.split(",")[6+chars.index(pair_used[0])]) > 3 and int(s.split(",")[6+chars.index(pair_used[1])]) > 3:
                if action_dictionary[s] in actions_for_both_alive:
                    actions_for_both_alive[action_dictionary[s]] += 1
                else:
                    actions_for_both_alive[action_dictionary[s]] = 1
    print("\twith all characters at high health" + display_action_rundown_from_dictionary(actions_for_both_alive))

    actions_for_both_alive = {}
    for s in action_dictionary.keys():
        if int(s.split(",")[chars.index(pair[0])]) <= 3 and int(s.split(",")[chars.index(pair[1])]) <= 3 and int(s.split(",")[chars.index(pair[0])]) > 0 and int(s.split(",")[chars.index(pair[1])]) > 0:
            if int(s.split(",")[6+chars.index(pair_used[0])]) > 3 and int(s.split(",")[6+chars.index(pair_used[1])]) > 3 and int(s.split(",")[6+chars.index(pair_used[0])]) > 0 and int(s.split(",")[6+chars.index(pair_used[1])]) > 0:
                if action_dictionary[s] in actions_for_both_alive:
                    actions_for_both_alive[action_dictionary[s]] += 1
                else:
                    actions_for_both_alive[action_dictionary[s]] = 1
    print("\twith all characters at low health" + display_action_rundown_from_dictionary(actions_for_both_alive))

    actions_for_both_alive = {}
    for s in action_dictionary.keys():
        if int(s.split(",")[chars.index(pair[0])]) > 0 and s.split(",")[:5].count("0") == 4:
            if int(s.split(",")[6+chars.index(pair_used[0])]) > 0 and int(s.split(",")[6+chars.index(pair_used[1])]) > 0:
                if action_dictionary[s] in actions_for_both_alive:
                    actions_for_both_alive[action_dictionary[s]] += 1
                else:
                    actions_for_both_alive[action_dictionary[s]] = 1

    print("\tWith only opposing " + act_parse[pair[0]] + " alive and both allied characters alive" + display_action_rundown_from_dictionary(actions_for_both_alive))
    actions_for_both_alive = {}
    for s in action_dictionary.keys():
        if int(s.split(",")[chars.index(pair[1])]) > 0 and s.split(",")[:5].count("0") == 4:
            if int(s.split(",")[6+chars.index(pair_used[0])]) > 0 and int(s.split(",")[6+chars.index(pair_used[1])]) > 0:
                if action_dictionary[s] in actions_for_both_alive:
                    actions_for_both_alive[action_dictionary[s]] += 1
                else:
                    actions_for_both_alive[action_dictionary[s]] = 1

    print("\tWith only opposing " + act_parse[pair[1]] + " alive and both allied characters alive" + display_action_rundown_from_dictionary(actions_for_both_alive))
    print()

for s in action_dictionary.keys():
    if action_dictionary[s][0] == "A" and len(action_dictionary[s]) == 3:   # If archer is attacking a single target
        int_list = list(map(int,s.split(",")))
        if sum(int_list[:5]) > max(int_list[:5]):    # if more than one opp is alive
            if sum(int_list[6:]) > max(int_list[6:]):
                print(s, action_dictionary[s])
