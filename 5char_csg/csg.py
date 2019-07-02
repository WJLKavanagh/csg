# William Kavanagh, May 2019
# Extended CSG - Main runnable for 5c RPGLite

"""
1.  For m in M:
        calculate strategy(p1/m) giving max( Pwin(p1) (strategy(p1/m),random_strategy(p2/random_m) )
        print the probability of max(Pwin(..))
        translate the strategy from p1 to p2
    denote the strategy with the highest Pwin(..) as 'the meta'
2. For m in M:
        calculate stategy'(p1/m) giving max( Pwin(p1) (strategy'(p1/m),'the meta'))
        print the probability of max(Pwin(..))
        update strategy^(k-1)(p2/m) with the reachable transitions from the translation of strategy'(p1/m) -> strategy'(p2/m) to get strategy^k(p2/m)
        print how many actions are different between strategies k(..) and k-1(..)
    update 'the meta' to be the K-strategy with the great Pwin(..)
3.  If any k-strategy is different from k-i strategies (for all i<k) ->
        goto 2.
    elif all k-strategies are identical to all k-j strategies (for some j > 1) ->
        Stop. We have found a cycle of effective strategies to be analysed further
    else ->
        Stop. 'the meta' is a dominant strategy.
"""

import sys, os, filecmp
import metagenerator, strategy_generator, model_generator, strategy_updater, strategy_reverse, final_material_comp

def find_result(file):
    # Take a log file, return the value found by MCing.
    f = open(file, "r").readlines()
    for i in range(len(f)-1,0,-1):
        if "Result:" in f[i]:
            return f[i].split("ult: ")[1].split(" (value")[0]

def loop_check(j):
    # Compare every <pair>_strategy_j-1.txt to <pair>_strategy_p.txt (p<j-1) to make sure we aren't in a loop
    # Return loop length (0 if no loop)
    global output
    if j < 2: return 0
    for p in range(1, j-1):
        all_clear = False
        for pair in pairs:
            if not filecmp.cmp(output+"/"+pair+"_strategy_"+str(j-1)+".txt", output+"/"+pair+"_strategy_"+str(p)+".txt", shallow=False):
                all_clear = True
                break
        if not all_clear:
            #print("At iteration " + str(j-1) + " strategies are identical to at iteration " + str(p))
            return j-1-p
    return 0

# setup
config = input("What configuration are you using: ").lower()
output = input("What output destination do you want: ")
print("~~~~~~~~~~~~~~~~")
k = 0                                   # iterations
meta_pair = "none"                      # current best strategy is strategy k for pair <meta_pair>
metagenerator.run(output, config)       # Create the 10 generator models
best_probability = 0.0
"""
1.  For m in M:
        calculate strategy(p1/m) giving max( Pwin(p1) (strategy(p1/m),random_strategy(p2/random_m) )
        print the probability of max(Pwin(..))
        translate the strategy from p1 to p2
    denote the strategy with the highest Pwin(..) as 'the meta'
"""
chars = ["K","A","W","R","H"]
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i] + chars[j]]
for pair in pairs:
    os.system("prism output/" + pair + "_generator.prism ../properties/mdp.props \
    -prop 1 -exportadvmdp " + output + "/tmp.tra -exportstates " + output + \
    "/tmp.sta -javamaxmem 5g -nopre -maxiters 300000 > " + output + "/log.txt")
    probability = float(find_result(output+"/log.txt"))
    print(pair + " can get " + str(probability))
    if probability > best_probability:
        meta_pair = pair
        best_probability = probability
    transition_count = strategy_generator.run(output, pair, k)
    print("Strategy generated, there are: " + str(transition_count) + " transitions.\n")
print(meta_pair + " is the meta after " + str(k) + " iterations.\n~~~~~~~~~~~~~~~~")
k += 1
"""
2. For m in M:
        calculate stategy'(p1/m) giving max( Pwin(p1) (strategy'(p1/m),'the meta'))
        print the probability of max(Pwin(..))
        update strategy^(k-1)(p2/m) with the reachable transitions from the translation of strategy'(p1/m) -> strategy'(p2/m) to get strategy^k(p2/m)
        print how many actions are different between strategies k(..) and k-1(..)
    update 'the meta' to be the K-strategy with the great Pwin(..)
3.  If any k-strategy is different from k-i strategies (for all i<k) ->
        goto 2.
    elif all k-strategies are identical to all k-j strategies (for some j > 1) ->
        Stop. We have found a cycle of effective strategies to be analysed further
    else ->
        Stop. 'the meta' is a dominant strategy.
"""

best_probability = 0.0
while loop_check(k) == 0 or (best_probability > 0.5 and loop_check(k) == 1):
    best_probability = 0.0
    best_pair_this_it = "none"
    model_generator.run(output, config, meta_pair, k)       # generate the 10 prism models vs current meta
    for pair in pairs:
        # find the probability of winning
        os.system("prism output/" + pair + "_vs_" + str(k-1) + ".prism ../properties/mdp.props \
        -prop 1 -exportadvmdp " + output + "/tmp.tra -exportstates " + output + \
        "/tmp.sta -javamaxmem 5g > " + output + "/log.txt")
        probability = float(find_result(output+"/log.txt"))
        print(pair + " can get " + str(probability))
        # designate the new meta
        if probability > best_probability:
            best_pair_this_it = pair
            best_probability = probability
        # generate the new strategies
        total, seen, new = strategy_updater.run(output, pair, k)
        # print how many transitions have been updated
        print("Of " + str(total) + " actions, " + str(seen) + " were seen and " + str(new) +  " have changed.\n")
    meta_pair = best_pair_this_it
    print(meta_pair + " is the meta after " + str(k) + " iterations.\n~~~~~~~~~~~~~~~~")
    k = k + 1
loop_size = loop_check(k)
if loop_size != 1: print("Dominant strategy identified")
else: print("Cycle found of length:", loop_size)
print("Generation finished, building final table")
for pair in pairs[1:]:
    strategy_reverse.run(pair, k-1, output)
final_material_comp.run(k-1, output, config)
