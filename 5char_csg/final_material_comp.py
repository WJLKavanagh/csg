import datetime, os #, strategy_reverse

def find_result(file):
    # Take a log file, return the value found by MCing.
    f = open(file, "r").readlines()
    for i in range(len(f)-1,0,-1):
        if "Result:" in f[i]:
            return f[i].split("ult: ")[1].split(" (value")[0]

def run(iter, file_prefix, configuration):
    chars = ["K","A","W","R","H"]
    pairs = []
    results = {}
    for i in range(len(chars)):
        for j in range(i+1,len(chars)):
            pairs += [chars[i] + chars[j]]
            results[pairs[-1]] = []
    count = 0
    for i in range(len(pairs)):
        for j in range(len(pairs)):
            if count % 5 == 0:
                print(str(count)[:5] + "% complete")
            if j < i:
                results[pairs[i]] += [1 - float(results[pairs[j]][i])]
            elif j == i:
                results[pairs[i]] += [0.500]
            else:
                f = open(file_prefix + "/final_strats.prism","w")
                f.write("// Author:\tWilliam Kavanagh, University of Glasgow\n")
                f.write("// Created:\t" + str(datetime.datetime.now()).split(" ")[0] + "\n")
                f.write("// File:\t\tCSG auto-generated model\n")
                f.write("// Comment:\tThis file is a model of the final strategies for " + pairs[i] + " vs " + pairs[j] + "\n")
                f.write("\n// Configuration " + configuration.upper() + ":\n")
                f.write(open("configurations/" + configuration + ".txt", "r").read())
                f.write("\nmodule game\n\tattack\t: [0..110];\n\tturn\t\t: [0..2];\n")
                for c in ["Knight","Archer","Wizard","Rogue","Healer"]:
                    if c[0] in pairs[j]:
                        f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                        f.write(c + "_health;\t// P1 " + c + "\n")
                    else:
                        f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                        f.write("0;\t\t\t\t\t\t\t// P1 " + c + " not used\n")
                f.write("\tp1_stun\t\t\t: [0..5];\n")
                for c in ["Knight","Archer","Wizard","Rogue","Healer"]:
                    if c[0] in pairs[i]:
                        f.write("\tp2" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                        f.write(c + "_health;\t// P2 " + c + "\n")
                    else:
                        f.write("\tp2" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                        f.write("0;\t\t\t\t\t\t\t// P2 " + c + " not used\n")
                f.write("\tp2_stun\t\t\t: [0..5];\n")
                f.write("[flip_coin]\tturn = 0 & p2K*p2A*p2W = 0 ->\n\t\t0.5 : (turn' = 1) + 0.5 : (turn' = 2);\n")
                f.write(open(file_prefix + "/" + pairs[j]+"_strategy_" + str(iter) + "_reversed.txt","r").read())
                f.write(open(file_prefix + "/" + pairs[i]+"_strategy_" + str(iter) + ".txt","r").read())
                f.write(open("model_suffix.txt","r").read())
                os.system("prism " + file_prefix + "/final_strats.prism ../properties/mdp.props -prop 2 -javamaxmem 4g > " + file_prefix + "/log.txt")
                results[pairs[i]] += [find_result(file_prefix + "/log.txt")]
            count = count + 1
    row = ""

    averages = {}
    # Print pair comparisons
    print("\nRow vs Column, average at end.")
    for header in (pairs):
        row += header + "\t"
        output_line = ""
        total = 0
        for res in results[header]:
            output_line += str(res)[:5] + "\t"
            total += float(res)
            averages[header] = total/len(results[header])
        print(header + "\t" + output_line + ":\t" + str(averages[header])[:6])
    print("\t"+row + "\tAvg\n")

    # Print char comparisons
    for char in chars:
        num_involvement = 0
        total_average = 0.0
        for pair in pairs:
            if char in pair:
                total_average += averages[pair]
                num_involvement += 1
        print(char, "gets an average of: " + str(total_average/num_involvement)[:8])



# chars = ["K","A","W","R","H"]
# pairs = []
# for i in range(len(chars)):
#     for j in range(i+1,len(chars)):
#         pairs += [chars[i] + chars[j]]
# for pair in pairs[1:]:
#     strategy_reverse.run(pair, 78, "output")
#run(78,"output","alpha_updated")
