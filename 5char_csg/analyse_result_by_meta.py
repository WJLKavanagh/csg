import sys, matplotlib.pyplot as plt, numpy as np

# William Kavanagh, 28/6/19
# Examine the output of CSG and suggest redesign based on the form of the metagame.

result = open(sys.argv[1],"r").readlines()  # result as list of lines

metric_dictionary = {}
char_metric_dictionary = {}
chars = ["K","A","W","R","H"]
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i] + chars[j]]

for pair in pairs:          # Calculate mean robustness
    sum = 0
    over_point5 = 0
    win_sum = 0
    count = 0
    for line in result:
        if pair + " can get" in line:
            sum += float(line.split(" ")[-1])
            if float(line.split(" ")[-1]) > 0.5:
                win_sum += float(line.split(" ")[-1])
                over_point5 += 1
            count += 1
    robustness = sum/count
    win_delta = win_sum/over_point5 - 0.5
    loss_delta = 0.5 - (sum-win_sum)/(count-over_point5)
    if win_delta < 0.01: win_delta = 0.0
    if loss_delta < 0.01: loss_delta = 0.0
    metric_dictionary[pair] = {"robustness": robustness, "win_delta": win_delta, "loss_delta": loss_delta}

for char in chars:
    char_metric_dictionary[char] = {"robustness":0,"win_delta":0,"loss_delta":0,"viable":0}
    for pair in pairs:
        if char in pair:
            char_metric_dictionary[char]["robustness"] += metric_dictionary[pair]["robustness"] / 4
            char_metric_dictionary[char]["win_delta"] += metric_dictionary[pair]["win_delta"] / 4
            char_metric_dictionary[char]["loss_delta"] += metric_dictionary[pair]["loss_delta"] / 4

char_meta_count = [0,0,0,0,0]
char_near_meta_count = [0,0,0,0,0]
meta_pairs = []
meta_values = []

for line in result:
    if "can get" in line and float(line.split(" ")[-1]) > 0.5:
        char_metric_dictionary[line[0]]["viable"] += (1/count)/4
        char_metric_dictionary[line[1]]["viable"] += (1/count)/4
    if "is the meta" in line:
        char_meta_count[chars.index(line[0])] += 1
        char_meta_count[chars.index(line[1])] += 1
        meta_pairs += [line[:2]]

meta_index = 0
end_iteration = False
for line in result[34:]:
    if meta_pairs[meta_index] + " can get" in line and end_iteration == False:
        meta_values += [float(line.split(" ")[-1])]
        end_iteration = True
    if "~~~~~~" in line and end_iteration:
        end_iteration = False
        meta_index += 1

meta_index = 0
to_update = [0,0,0,0,0]
for line in result[34:]:
    if "can get" in line and float(line.split(" ")[-1]) > meta_values[meta_index] - 0.03:            # Tunable 'close' indicator
        if line[0] not in meta_pairs[meta_index]: to_update[chars.index(line[0])] = 1
        if line[1] not in meta_pairs[meta_index]: to_update[chars.index(line[1])] = 1
    if "~~~~" in line and meta_index < len(meta_pairs) - 2:
        for i in range(5):
            char_near_meta_count[i] += to_update[i]
        meta_index += 1
        to_update = [0,0,0,0,0]

for i in range(5):
    char_metric_dictionary[chars[i]]["end_result"] = float((result[i-5]).split(" ")[-1])
    char_metric_dictionary[chars[i]]["pick_rate"] = 0.0
    char_metric_dictionary[chars[i]]["change_rate"] = 0.0

for i in range(10):
    metric_dictionary[pairs[i]]["end_result"] = float((result[i-17]).split("\t")[-1])

# for pair in pairs:
#     print(pair, metric_dictionary[pair])
# for char in chars:
#     print(char, char_metric_dictionary[char])


fig, ax = plt.subplots()

for pair in pairs:
    ma = 4
    if pairs.index(pair) % 2 == 0: ma = 5
    ax.scatter(metric_dictionary[pair]["robustness"], metric_dictionary[pair]["end_result"], label=pair, marker=ma, s=75)
lims = [
    np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
    np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
]

# Pick Rate v1.0
total_winning_probability = 0       # total probability at each step
success_dictionary = {"K":0, "A":0, "W":0, "R":0, "H":0}
pick_rates = {"K":[], "A":[], "W":[], "R":[], "H":[]}
for line in result[1:]:
    if "can get" in line and float(line.split(" ")[-1]) > 0.5:
        total_winning_probability += (float(line.split(" ")[-1]) - 0.5)
        success_dictionary[line[0]] += (float(line.split(" ")[-1]) - 0.5)
        success_dictionary[line[1]] += (float(line.split(" ")[-1]) - 0.5)
    if "~~~~~" in line:
        for char in chars:
            if success_dictionary[char] > 0:
                pick_rates[char] += [success_dictionary[char] / total_winning_probability]
            else:
                pick_rates[char] += [0.0]
        total_winning_probability = 0
        success_dictionary = {"K":0, "A":0, "W":0, "R":0, "H":0}

for char in chars:
    # identify loop start
    # cut list at end point of loop start.
    char_metric_dictionary[char]["pick_rate"] = np.mean(pick_rates[char][:33])

change_rates = {"K":[], "A":[], "W":[], "R":[], "H":[]}

for i in range(len(result[1:])):
    if "were seen and" in result[i]:
        c_p = result[i-1][:2]   # pull character pair
        if float(result[i].split(" ")[-3]) > 0.0:
            prop = float(result[i].split(" ")[-3]) / float(result[i].split(" ")[-7])
        else:
            prop = 0.0
        change_rates[c_p[0]] += [prop/4]
        change_rates[c_p[1]] += [prop/4]


for char in chars:
    char_metric_dictionary[char]["change_rate"] = np.mean(change_rates[char])

char_dict = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}

# # now plot both limits against eachother
# ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
# ax.set_aspect('equal')
# ax.set_xlim(lims)
# ax.set_ylim(lims)
# ax.set_title("Pair-wise metagame analysis: " + sys.argv[1].split("/")[1].split(".txt")[0])
# ax.legend()
# plt.xlabel("robustness")
# plt.ylabel("win rate")
# plt.tight_layout()

fig, ax2 = plt.subplots()
for char in chars:
    ax2.scatter(char_metric_dictionary[char]["pick_rate"], char_metric_dictionary[char]["change_rate"], label=char_dict[char], marker = 5, s=75)
ax2.legend()

# Draw f(x) = y
# lims = [
#     np.min([ax2.get_xlim(), ax2.get_ylim()]),  # min of both axes
#     np.max([ax2.get_xlim(), ax2.get_ylim()]),  # max of both axes
# ]
# ax2.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
# ax2.set_aspect('equal')
# ax2.set_xlim(lims)
# ax2.set_ylim(lims)

ax2.set_title("Character-wise metagame analysis: " + sys.argv[1].split("/")[1].split(".txt")[0])

ax2.legend()
plt.xlabel("Fairness - character viability")
plt.ylabel("Interest - strategy variation")
plt.tight_layout()

# ind = np.arange(len(chars))
# fig, ax3 = plt.subplots()
# max_it = plt.plot([0,1,2,3,4], [len(meta_values)]*5, "--")
# base = plt.bar(ind, char_meta_count)
# extra = plt.bar(ind, char_near_meta_count, bottom = char_meta_count)
# plt.legend((base[0],extra[0]),("on meta","near meta (3%)"))
# plt.xticks(ind, chars)
# ax3.annotate(xy=[2, len(meta_values)], s = "iterations = " + str(len(meta_values)))
# ax3.set_title("Character-wise 'on meta'/'near meta' analysis")
plt.show()
