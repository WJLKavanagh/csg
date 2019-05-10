import matplotlib.pyplot as plt

xseries = []
KA = []
KW = []
AW = []
KA_change = [0]
KW_change = [0]
AW_change = [0]
count = 1
f = input("What file are we parsing: ")
lines = open(f, "r").readlines()
for i in range(len(lines)-2):
    if "~~~~" in lines[i]:
        xseries+=[count]
        count+=1
        KA+=[float(lines[i+1].split(" ")[3])]
        KW+=[float(lines[i+4].split(" ")[3])]
        AW+=[float(lines[i+7].split(" ")[3])]
        if count > 2:
            KA_change+=[float(int(lines[i+2].split(" ")[-3]) / int(lines[i+2].split(" ")[3]))]
            KW_change+=[float(int(lines[i+5].split(" ")[-3]) / int(lines[i+5].split(" ")[3]))]
            AW_change+=[float(int(lines[i+8].split(" ")[-3]) / int(lines[i+8].split(" ")[3]))]

y_equals_05 = [0.5]*len(xseries)


fig, ax = plt.subplots()
ax.plot(xseries, KA, label="KA")
ax.plot(xseries, KW, label="KW")
ax.plot(xseries, AW, label="AW")
ax.plot(xseries, y_equals_05, "--")
plt.title("max Pwin")
legend = ax.legend(fontsize=18)

fig1, ax2 = plt.subplots()
plt.title('proportion of actions changed')
ax2.plot(xseries, KA_change, label="KA-change")
ax2.plot(xseries, KW_change, label="KW-change")
ax2.plot(xseries, AW_change, label="AW-change")
legend = ax2.legend(fontsize=18)

plt.tight_layout()
plt.show()
