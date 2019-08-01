# William Kavanagh, May 2019
# Extended CSG - model generator for 5c RPGLite
# Takes a strategy and generates 10 prism models of MDPs for m in M against a defined meta
# Formatting is for a tab length of 2, different tab lengths may be hard to read.
import datetime

def run(file_prefix, configuration, meta_pair, i):
    #INPUT: file destination prefix, configuration to use
    #       opposing pair and iteration number (the meta is pair_strategy_i-1.txt)
    #OUTPUT: writes three models to file.
    chars = ["Knight","Archer","Wizard","Rogue","Healer"]
    trips = []
    for p in range(len(chars)):
        for j in range(i+1,len(chars)):
            for k in range(j+1,len(chars)):
                trips += [chars[p] + chars[j] + chars[k]]
    for trip in trips:
        f = open(file_prefix + "/" + trip + "_vs_" + str(i-1) + ".prism", "w")
        f.write("// Author:\tWilliam Kavanagh, University of Glasgow\n")
        f.write("// Created:\t" + str(datetime.datetime.now()).split(" ")[0] + "\n")
        f.write("// File:\t\tCSG auto-generated model\n")
        f.write("// Comment:\tThis file is a generator for a later strategy for " + trip + "\n")
        f.write("\n// Configuration " + configuration.upper() + ":\n")
        f.write(open("../configurations/" + configuration + ".txt", "r").read())
        f.write("\nmodule game\n\tattack\t: [0..110];\n\tturn\t\t: [0..2];\n")
        for c in chars:
            if c[0] in trip:
                f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write(c + "_health;\t// P1 " + c + "\n")
            else:
                f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write("0;\t\t\t\t\t\t\t// P1 " + c + " not used\n")
        f.write("\tp1_stun\t: [0..5]\t\t\t\t\t\t\tinit 0;\n")
        for c in chars:
            if c[0] in meta_pair:
                f.write("\tp2" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write(c + "_health;\t// P2 " + c + "\n")
            else:
                f.write("\tp2" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write("0;\t\t\t\t\t\t\t// P2 " + c + " not used\n")
        f.write("\tp2_stun\t: [0..5]\t\t\t\t\t\t\tinit 0;\n\n")
        f.write(open("p1_moves.txt","r").read())
        f.write(open(file_prefix + "/" + meta_pair + "_strategy_" + str(i-1) + ".txt", "r").read())
        f.write(open("model_suffix.txt","r").read())

#run("output", "alpha", "RH", 1)
