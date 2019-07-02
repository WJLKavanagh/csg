import filecmp

def loop_check(j):
    # Compare every <pair>_strategy_j-1.txt to <pair>_strategy_p.txt (p<j-1) to make sure we aren't in a loop
    global output
    if j < 2: return True
    for p in range(1, j-1):
        print(p)
        all_clear = False
        for pair in pairs:
            if not filecmp.cmp(output+"/"+pair+"_strategy_"+str(j-1)+".txt", output+"/"+pair+"_strategy_"+str(p)+".txt", shallow=False):
                all_clear = True
                break
        if not all_clear:
            print("At iteration " + str(j-1) + " strategies are identical to at iteration " + str(p))
            print("Loop identified, length " + str(j-1-p))
            return False
    return True

output = "output"
chars = ["K","A","W","R","H"]
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i] + chars[j]]
for i in range(1,15):
    print(i)
    print(loop_check(i))
