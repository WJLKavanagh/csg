# William Kavanagh, May 2019
# Extended CSG - Can we identify dominant strategies without iterating?

import sys, os, datetime
import metagenerator, strategy_generator, model_generator, strategy_updater, strategy_reverse, final_material_comp

def find_result(file):
    # Take a log file, return the value found by MCing.
    f = open(file, "r").readlines()
    for i in range(len(f)-1,0,-1):
        if "Result:" in f[i]:
            return f[i].split("ult: ")[1].split(" (value")[0]

def find_opponents(file):
    f = open(file,"r").readlines()
    for line in f:
        if "choose" in line:
            return line.split("_")[1][:-1]

# setup
config = input("What configuration are you using: ").lower()
output = input("What output destination do you want: ")
print("~~~~~~~~~~~~~~~~")

chars = ["K","A","W","R","H"]
full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i] + chars[j]]

for pair in pairs:
    # generate model for pair vs generator

    file_name = pair + "_dominance_check.prism"
    f = open(output + "/" + file_name,"w")
    f.write("// Author:\tWilliam Kavanagh, University of Glasgow\n")
    f.write("// Created:\t" + str(datetime.datetime.now()).split(" ")[0] + "\n")
    f.write("// File:\t\tCSG auto-generated model\n")
    f.write("// Comment:\tThis file is a generator for a later strategy for " + pair + "\n")
    f.write("smg")
    f.write("\n// Configuration " + config.upper() + ":\n")
    f.write(open("configurations/" + config + ".txt", "r").read())
    f.write(open("model_sections/file_prefix.txt").read())
    for char in chars:
        if char in pair:
            f.write("\tp1" + char + "\t: [0.." + full_name[char] + "_health]\t\tinit " + full_name[char] + "_health; // P1 " + full_name[char] + "\n")
        else:
            f.write("\tp1" + char + "\t: [0.." + full_name[char] + "_health]\t\tinit 0; // P1 " + full_name[char] + " not used\n")
    f.write("\tp1_stun\t:\t[0..5];\t\t\t\t//0 - none, 1 - Knight stunned, 2 - Archer stunned, 3 - Wizard stunned .. etc\n")
    for char in chars:
        f.write("\tp2" + char + "\t: [0.." + full_name[char] + "_health]\t\tinit " + full_name[char] + "_health; // P2 " + full_name[char] + "\n")
    f.write("\tp2_stun\t:\t[0..5];\t\t\t\t//0 - none, 1 - Knight stunned, 2 - Archer stunned, 3 - Wizard stunned .. etc\n\n")
    f.write("// Choose opposing material\n")
    f.write(open("model_sections/choose_chars.txt").read())
    f.write("\n\t[coin_flip] turn = 0 & p2K*p2A*p2W = 0 ->\n")
    f.write("\t\t0.5 : (turn' = 1) + 0.5 : (turn' = 2);\n\n")
    f.write(open("model_sections/p1_nd.txt").read())
    f.write(open("model_sections/p2_nd.txt").read())
    f.write(open("model_sections/file_suffix.txt").read())

    os.system("prism " + output + "/" + file_name + " ../properties/smg.props \
    -prop 1 -exportadvmdp " + output + "/tmp.tra -exportstates " + output + \
    "/tmp.sta -javamaxmem 5g -nopre -maxiters 300000 > " + output + "/log.txt")

    print(pair + ":")
    print("\topposing pair selected as: " + find_opponents(output+"/tmp.tra"))
    print("\toptimal probability of: " + find_result(output+"/log.txt") + "\n")

    # p1 can do what they want, as can p2.
    # calculate the optimal strategy for P1, print P and the opposing pair.





#
#     os.system("prism output/" + pair + "_generator.prism ../properties/mdp.props \
#     -prop 1 -exportadvmdp " + output + "/tmp.tra -exportstates " + output + \
#     "/tmp.sta -javamaxmem 5g -nopre -maxiters 300000 > " + output + "/log.txt")
#     probability = float(find_result(output+"/log.txt"))
#     print(pair + " can get " + str(probability))
#     if probability > best_probability:
#         meta_pair = pair
#         best_probability = probability
#     transition_count = strategy_generator.run(output, pair, k)
#     print("Strategy generated, there are: " + str(transition_count) + " transitions.\n")
# print(meta_pair + " is the meta after " + str(k) + " iterations.\n~~~~~~~~~~~~~~~~")
# k += 1
#
# best_probability = 0.0
# while loop_check(k) == 0 or (best_probability > 0.5 and loop_check(k) == 1):
#     best_probability = 0.0
#     best_pair_this_it = "none"
#     model_generator.run(output, config, meta_pair, k)       # generate the 10 prism models vs current meta
#     for pair in pairs:
#         # find the probability of winning
#         os.system("prism output/" + pair + "_vs_" + str(k-1) + ".prism ../properties/mdp.props \
#         -prop 1 -exportadvmdp " + output + "/tmp.tra -exportstates " + output + \
#         "/tmp.sta -javamaxmem 5g > " + output + "/log.txt")
#         probability = float(find_result(output+"/log.txt"))
#         print(pair + " can get " + str(probability))
#         # designate the new meta
#         if probability > best_probability:
#             best_pair_this_it = pair
#             best_probability = probability
#         # generate the new strategies
#         total, seen, new = strategy_updater.run(output, pair, k)
#         # print how many transitions have been updated
#         print("Of " + str(total) + " actions, " + str(seen) + " were seen and " + str(new) +  " have changed.\n")
#     meta_pair = best_pair_this_it
#     print(meta_pair + " is the meta after " + str(k) + " iterations.\n~~~~~~~~~~~~~~~~")
#     k = k + 1
# loop_size = loop_check(k)
# if loop_size != 1: print("Dominant strategy identified")
# else: print("Cycle found of length:", loop_size)
# print("Generation finished, building final table")
# for pair in pairs[1:]:
#     strategy_reverse.run(pair, k-1, output)
# final_material_comp.run(k-1, output, config)
