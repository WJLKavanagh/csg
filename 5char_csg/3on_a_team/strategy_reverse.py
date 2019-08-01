# Author    William Kavanagh, University of Glasgow
# Date      21-5-19
# Change a strategy for RPGLite (.txt) for player 2 to a strategy for player 1

def run(pair, i, file):
    # INPUT: pair used by strategy <str>, iteration played against <int>
    # OUTPUT: file of same name appended with "_flipped"
    file_in = file + "/" + pair + "_strategy_" + str(i)
    file_out = file_in + "_reversed.txt"
    file_in += ".txt"
    strat = open(file_in, "r").readlines()[1:]
    new_s = open(file_out, "w")
    for i in range(len(strat)):
        if "[p2]" in strat[i]:       # if the guard begins on this line
            first_line = strat[i]
            first_line = first_line.replace("p2","p1")
            first_line = first_line.replace("turn = 2", "turn = 1")
            new_s.write(first_line)
            second_line = strat[i+1]
            new_s.write(second_line.replace("p1","p2"))
            third_line = strat[i+2]
            action_int = third_line.split("attack' = ")[1].split(")")[0]
            third_line = third_line.replace(action_int, str(int(action_int)-55))
            new_s.write(third_line.replace("p2","p1"))
        elif "[p2_skip]" in strat[i]:
            new_s.write(strat[i].replace("p2","p1").replace("turn = 2","turn = 1"))
            new_s.write(strat[i+1].replace("p2","p1").replace("= 1", "= 2"))
        elif "[p2" in strat[i]:
            first_line = strat[i]
            first_line = first_line.replace("p2","p1")
            first_line = first_line.replace(" p1"," p2")
            first_line = first_line.replace("turn = 2", "turn = 1")
            new_s.write(first_line)
            second_line = strat[i+1]
            new_s.write(second_line.replace("p2","p1"))
            third_line = strat[i+2]
            action_int = third_line.split("attack' = ")[1].split(")")[0]
            third_line = third_line.replace(action_int, str(int(action_int)-55))
            new_s.write(third_line.replace("p2","p1"))

"""
chars = ["K","A","W","R","H"]
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i] + chars[j]]
for pair in pairs:
    run(pair,7,"output")
"""
