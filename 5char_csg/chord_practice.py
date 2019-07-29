import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

results = {'KA': {'res': '0.217740464642635', 'opp': 'WH'}, 'KW': {'res': '0.36400061678485385', 'opp': 'WH'}, 'KR': {'res': '0.27324713957749186', 'opp': 'WR'}, 'KH': {'res': '0.2895677705543638', 'opp': 'WH'}, 'AW': {'res': '0.2833221421023975', 'opp': 'WH'}, 'AR': {'res': '0.17039787458962413', 'opp': 'WH'}, 'AH': {'res': '0.2586919097453748', 'opp': 'WH'}, 'WR': {'res': '0.38426962625438743', 'opp': 'AW'}, 'WH': {'res': '0.44862622066492686', 'opp': 'WR'}, 'RH': {'res': '0.33647407987116457', 'opp': 'WR'}}

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
plt.title("Adversarial probabilities against optimal strategy")
if len(good_nodes) > 0: plt.annotate("Non-dominant cycle = \n" + str(good_nodes), xy = (1,-1), color="red")
else: plt.annotate("Dominant strategy = \n" + evil_nodes[0], xy = (1,-1), color="red")
#plt.savefig("results/graphics/" + config + "_optimality_relationship.png")
plt.show()
