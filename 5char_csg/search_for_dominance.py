# William Kavanagh, May 2019
# Extended CSG - Can we identify dominant strategies without iterating?
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
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

def run_analysis(config, output):
    # setup

    print("~~~~~~~~~~~~~~~~")

    chars = ["K","A","W","R","H"]
    full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
    pairs = []
    for i in range(len(chars)):
        for j in range(i+1,len(chars)):
            pairs += [chars[i] + chars[j]]
    results = {}

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
        found_opp = find_opponents(output+"/tmp.tra")
        minimax = find_result(output+"/log.txt")
        print("\topposing pair selected as: " + found_opp)
        print("\toptimal probability of: " + minimax + "\n")
        results[pair] = {"res":minimax, "opp":found_opp}


    plt.subplots(figsize=(14,14))

    G = nx.DiGraph()

    evil_nodes = []
    good_nodes = []

    for p in results.keys():
        if float(results[p]["res"]) < 0.499 or p != results[p]["opp"]:
            G.add_edge(results[p]["opp"], p, weight= str(100 - float(results[p]["res"])*100)[:6])
        else:
            evil_nodes += [p]
            G.add_edge(p, p, weight= 0.5)
            print("Adding:",p)
    plt.plot()

    #G.set_node_attributes(G, labels, 'colour_group')
    if len(evil_nodes) == 0:
        try:
            nx.find_cycle(G)
            if len(nx.find_cycle(G)) > 1:
                for e in nx.find_cycle(G):
                    good_nodes += [e[0]]
        except:
            pass

    print(good_nodes, evil_nodes)

    colour_list = []
    for n in G.nodes():
        if n in good_nodes or n in evil_nodes:
            colour_list += [0]
        else:
            colour_list += [1]

    print(colour_list)

    carac = pd.DataFrame({'ID':G.nodes(), 'colour_group':colour_list})
    carac= carac.set_index('ID')
    carac=carac.reindex(G.nodes())
    carac['colour_group']=pd.Categorical(carac['colour_group'])
    carac['colour_group'].cat.codes

    edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
    pos = nx.shell_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=carac['colour_group'].cat.codes, cmap=plt.cm.Set1, draw_network_edge_labels = True, node_size=800)

    print("edges", G.edges())
    print("cycle", nx.find_cycle(G))


    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.title(config + ": Adversarial probabilities against optimal strategy")
    if len(good_nodes) > 0: plt.annotate("Non-dominant cycle = \n" + str(good_nodes), xy = (1,-1), color="red")
    else: plt.annotate("Dominant strategy = \n" + evil_nodes[0], xy = (1,-1), color="red")
    plt.savefig("results/graphics/" + config + "_optimality_relationship.png")
#plt.show()

configs = sys.argv[1:]
output = input("What output destination do you want: ")
for c in configs:
    print("Analysing for configuration: " + c)
    run_analysis(c, output)
