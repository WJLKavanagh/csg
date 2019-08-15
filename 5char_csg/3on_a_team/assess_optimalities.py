import generate_nd_moves, os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

chars = ["K","A","W","R","H"]
trips = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        for k in range(j+1, len(chars)):
            trips += [chars[i]+chars[j]+chars[k]]


def find_result():
    res = open("output/log.txt","r").readlines()
    for line in res:
        if "Result: " in line:
            return(line.split(" ")[1])

def find_opponents():
    f = open("output/tmp.tra","r").readlines()
    for line in f:
        if "choose" in line:
            return(line.split("_")[1][:-1])

def run(conf):
    # Takes a configuration, generates models for all trips and calculates optimal probabilities for them
    # Returns a dictionary of suggested buffs and nerfs.
    results = {}
    for t in trips:
        file_name = "output/" + t + "_opt.prism"
        generate_nd_moves.run(t, conf, file_name)
    print("Files written")
    for t in trips:
        file_name = "output/" + t + "_opt.prism"
        os.system("prism " + file_name + " ../../properties/smg.props \
        -prop 1 -exportadvmdp output/tmp.tra -exportstates output/tmp.sta > output/log.txt")
        pair_res = find_result()
        opp_pair = find_opponents()
        print(t + ": is countered by " + opp_pair + " which prevents it from doing better than " + str(pair_res)[:7])
        results[t] = {"res":pair_res, "opp":opp_pair}

    plt.subplots(figsize=(14,14))

    G = nx.DiGraph()

    evil_nodes = []         # dominant trips
    good_nodes = []         # cycle of effective, non-dominant trips.

    for t in results.keys():
        if float(results[t]["res"]) < 0.499 or p != results[t]["opp"]:
            G.add_edge(results[t]["opp"], p, weight= str(100 - float(results[t]["res"])*100)[:6])
        else:
            evil_nodes += [t]
            G.add_edge(t, t, weight= 0.5)
            print("Adding:",t)
    plt.plot()

    #G
    if len(evil_nodes) == 0:
        try:
            nx.find_cycle(G)
            if len(nx.find_cycle(G)) > 1:
                for e in nx.find_cycle(G):
                    good_nodes += [e[0]]
        except:
            pass


    colour_list = []
    for n in G.nodes():
        if n in good_nodes or n in evil_nodes:
            colour_list += [0]
        else:
            colour_list += [1]

    # create structs for colouring
    carac = pd.DataFrame({'ID':G.nodes(), 'colour_group':colour_list})
    carac= carac.set_index('ID')
    carac=carac.reindex(G.nodes())
    carac['colour_group']=pd.Categorical(carac['colour_group'])
    carac['colour_group'].cat.codes

    # draw labels
    edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
    pos = nx.shell_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=carac['colour_group'].cat.codes, cmap=plt.cm.Set1, draw_network_edge_labels = True, node_size=800)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.title(conf + ": Adversarial probabilities against optimal strategy")
    if len(good_nodes) > 0: plt.annotate("Non-dominant cycle = \n" + str(good_nodes), xy = (1,-1), color="red")
    else: plt.annotate("Dominant strategy = \n" + evil_nodes[0], xy = (1,-1), color="red")
    plt.savefig("results/graphics/" + conf + "_optimality_relationship.png")      # Save graph to file
    plt.show()
    print("~~~~~~~~~~~~~~~~")

    return(results)

run("delta9")
