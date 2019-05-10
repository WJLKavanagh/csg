# William Kavanagh, May 2019
# Extended CSG - Main runnable

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
import metagenerator, strategy_generator, model_generator, strategy_updater

def find_result(file):
    # Take a log file, return the value found by MCing.
    f = open(file, "r").readlines()
    for i in range(len(f)-1,0,-1):
        if "Result:" in f[i]:
            return f[i].split("ult: ")[1].split(" (value")[0]

def loop_check(j):
    # Compare every <pair>_strategy_j.txt to <pair>_strategy_p.txt (p<j) to make sure we aren't in a loop
    global output
    if j < 2: return True
    for p in range(j-1, 0, -1):
        all_clear = False
        for pair in ["KA","KW","AW"]:
            if not filecmp.cmp(output+"/"+pair+"_strategy_"+str(j)+".txt", output+"/"+pair+"_strategy_"+str(p)+".txt", shallow=False):
                all_clear = True
        if not all_clear:
            print("At iteration " + str(j) + " strategies are identical to at iteration " + str(p))
            return False
    return True


# setup
config = input("What configuration are you using (A-E): ").lower()
output = input("What output destination do you want: ")
print("~~~~~~~~~~~~~~~~")
k = 0                                   # iterations
meta_pair = "none"                      # current best strategy is strategy k for pair <meta_pair>
metagenerator.run(output, config)       # Create the 3 generator models
best_probability = 0.0

"""
1.  For m in M:
        calculate strategy(p1/m) giving max( Pwin(p1) (strategy(p1/m),random_strategy(p2/random_m) )
        print the probability of max(Pwin(..))
        translate the strategy from p1 to p2
    denote the strategy with the highest Pwin(..) as 'the meta'
"""
for pair in ["KA","KW","AW"]:
    os.system("prism output/" + pair + "_generator.prism properties/mdp.props \
    -prop 1 -exportadvmdp " + output + "/tmp.tra -exportstates " + output + \
    "/tmp.sta -javamaxmem 5g > " + output + "/log.txt")
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

something_is_new = True
while something_is_new and loop_check(k-1):
    something_is_new = False
    best_probability = 0.0
    best_pair_this_it = "none"
    model_generator.run(output, config, meta_pair, k)       # generate the 3 prism models vs current meta
    for pair in ["KA","KW","AW"]:
        # find the probability of winning
        os.system("prism output/" + pair + "_vs_" + str(k-1) + ".prism properties/mdp.props \
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
        if new > 0:
            something_is_new = True
    meta_pair = best_pair_this_it
    print(meta_pair + " is the meta after " + str(k) + " iterations.\n~~~~~~~~~~~~~~~~")
    k = k + 1
if not something_is_new: print("Dominant strategy found")
