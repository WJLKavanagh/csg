import os,sys
chars = ["K","A","W","R","H"]
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i] + chars[j]]
arg = "generator"
#if len(sys.argv) >= 1: arg = "vs_" + sys.argv[1]
for pair in pairs:
    os.system("prism output/test/" + pair + "_" + arg + ".prism ../properties/mdp.props -prop 5")
