# William Kavanagh, May 2019
# Extended CSG - metagenerator
# Takes a configuration and builds 3 .prism models of MDPs for each material in
# RPGLite against a mixed strategy for a randomly chosen pair.
# Formatting is for a tab length of 2, different tab lengths may be hard to read.
import datetime

def run(file_prefix, configuration):
    # INPUT: configuration to use
    # OUTPUT: 3 files for all material pairs
    for pair in ["KA","KW","AW"]:
        f = open(file_prefix + "/" + pair + "_generator.prism","w")
        f.write("// Author:\tWilliam Kavanagh, University of Glasgow\n")
        f.write("// Created:\t" + str(datetime.datetime.now())[:-7] + "\n")
        f.write("// File:\t\tCSG auto-generated model\n")
        f.write("// Comment:\tThis file is a generator for an initial strategy for " + pair + "\n")
        f.write("\n// Configuration " + configuration.upper() + ":\n")
        f.write(open("configurations/config_" + configuration + ".txt", "r").read())
        f.write("\nmodule game\n\tattack\t: [0..24];\n\tturn\t\t: [0..2];\n")
        for c in ["Knight","Archer","Wizard"]:
            if c[0] in pair:
                f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write(c + "_health;\t// P1 " + c + "\n")
            else:
                f.write("\tp1" + c[0] + "\t\t\t: [0.." + c + "_health]\tinit ")
                f.write("0;\t\t\t\t\t\t\t// P1 " + c + " not used\n")
        f.write(open("generator_stub.txt","r").read())
