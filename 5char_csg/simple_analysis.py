import sys, matplotlib.pyplot as plt, numpy as np

# William Kavanagh, 28/6/19
# Examine the output of CSG and suggest redesign based on the form of the metagame.

result = open(sys.argv[1],"r").readlines()  # result as list of lines
chars = ["K","A","W","R","H"]
char_dict = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
loop_start = 0
total_win_delta = 0.0
pick_rates = {"K":[], "A":[], "W":[], "R":[], "H":[]}
success_dictionary = {"K":0, "A":0, "W":0, "R":0, "H":0}
change_rates = {"K":[], "A":[], "W":[], "R":[], "H":[]}
end_point = 0

for i in range(len(result[2:])):    # Get start of 2nd iteration
    if "~~~" in result[i]:
        break
for i in range(i+1,len(result)):    # Get start of 2nd iteration
    if "~~~" in result[i]:
        break
for i in range(i,len(result)):
    if "can get" in result[i]:
        res = float(result[i].split(" ")[-1])
        char_0 = result[i][0]
        char_1 = result[i][1]
        if res > 0.5:                               # Build win_delta vars
            total_win_delta += res
            success_dictionary[char_0] += res
            success_dictionary[char_1] += res
        prop = 0.0
        if float(result[i+1].split(" ")[-3]) > 0:
            prop = float(result[i+1].split(" ")[-3]) / float(result[i+1].split(" ")[-7])
        change_rates[char_0] += [prop/4]
        change_rates[char_1] += [prop/4]
    if "~~~~" in result[i]:
        if total_win_delta <= 0 and end_point == 0: end_point = len(pick_rates["K"])
        for char in chars:
            if success_dictionary[char] > 0:
                pick_rates[char] += [success_dictionary[char] / total_win_delta]
            else:
                pick_rates[char] += [0]
        total_win_delta = 0
        success_dictionary = {"K":0, "A":0, "W":0, "R":0, "H":0}
    if "Cycle found" in result[i]: end_point = len(pick_rates["K"]) - int(result[i].split(" ")[-1][:-1])

print(end_point)

fairness = []
interest = []
sum = 0
for char in chars:
    sum += np.mean(pick_rates[char][1:end_point])
    fairness += [np.mean(pick_rates[char][1:end_point])]
    interest += [np.mean(change_rates[char])]
print("sum = " + str(sum)[:5] + " \t\t(should be ~2.0),")
print("end point = " + str(end_point) + " \t\t(point at which game is 'solved', confirm with metaplot)")

x_offset = max(fairness)/100
y_offset = max(interest)/30

for i in range(5):
    plt.scatter(fairness[i], interest[i], label=list(char_dict.values())[i], s=100)
    plt.annotate(xy=(fairness[i], interest[i]),
        s=list(char_dict.values())[i],
        horizontalalignment='center',
        verticalalignment='bottom',
        xytext=(fairness[i], interest[i] + y_offset))

plt.annotate(xy=(0.24,0.001), s="too\nweak", horizontalalignment="right", color="orange")
plt.annotate(xy=(0.01,plt.ylim()[1]-0.001), s="too\nweak", horizontalalignment="left", verticalalignment="top", color="orange")
plt.annotate(xy=(0.41,0.001), s="acceptable", horizontalalignment="left", verticalalignment="top", color="blue")
plt.annotate(xy=(0.39,plt.ylim()[1]-0.001), s="acceptable", horizontalalignment="right", color="blue")
plt.annotate(xy=(0.56,plt.ylim()[1]-0.001), s="too\nstrong", horizontalalignment="left", verticalalignment="top", color="red")
plt.annotate(xy=(0.79,0.001), s="too\nstrong", horizontalalignment="right", color="red")


plt.axvline(x=0.4)
plt.axvline(x=0.55, ls="--", c="red")
plt.axvline(x=0.25, ls="--", c="orange")
plt.ylim(bottom=0.0)
plt.xlim(left=0.0, right=0.8)
plt.xlabel("Character fairness")
plt.ylabel("Strategic interest")
plt.tight_layout()
#plt.legend()
plt.show()
