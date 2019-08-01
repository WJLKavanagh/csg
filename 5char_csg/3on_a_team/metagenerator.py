# William Kavanagh, May 2019
# Extended CSG - metagenerator for 5c RPGLite
# Takes a configuration and builds 10 .prism models of MDPs for each material in
# RPGLite against a mixed strategy for a randomly chosen pair.
# Formatting is for a tab length of 2, different tab lengths may be hard to read.
import datetime

def run(file_prefix, configuration):
    # INPUT: configuration to use
    # OUTPUT: 3 files for all material pairs
    chars = ["K","A","W","R","H"]
    trips = []
    for i in range(len(chars)):
        for j in range(i+1,len(chars)):
            for k in range(j+1,len(chars)):
                trips += [chars[i] + chars[j] + chars[k]]

    for trip in trips:
        f = open(file_prefix + "/" + trip + "_generator.prism","w")
        f.write("// Author:\tWilliam Kavanagh, University of Glasgow\n")
        f.write("// Created:\t" + str(datetime.datetime.now())[:-7] + "\n")
        f.write("// File:\t\tCSG auto-generated model\n")
        f.write("// Comment:\tThis file is a generator for an initial strategy for " + trip + "\n")
        f.write("\n// Configuration " + configuration.upper() + ":\n")
        f.write(open("../configurations/" + configuration + ".txt", "r").read())
        f.write("\nmodule game\n\tattack\t: [0..110];\n\tturn\t\t: [0..2];\n")
        for c in ["Knight","Archer","Wizard","Rogue","Healer"]:
            if c[0] in trip:
                f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write(c + "_health;\t// P1 " + c + "\n")
            else:
                f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write("0;\t\t\t\t\t\t\t// P1 " + c + " not used\n")
        print = False
        for line in open("generator.prism","r").readlines():
            if print == False:
                if "p1_stun" in line:
                    print = True
                    f.write(line)
            else: f.write(line)
        f.write("rewards\n\tturn = 2 : 1;\nendrewards")

#run("output", "alpha")
