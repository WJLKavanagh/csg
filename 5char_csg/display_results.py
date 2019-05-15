import matplotlib.pyplot as plt

xseries = []
KA = []
KW = []
KR = []
KH = []
AW = []
AR = []
AH = []
WR = []
WH = []
RH = []
KA_change = [0]
KW_change = [0]
KR_change = [0]
KH_change = [0]
AW_change = [0]
AR_change = [0]
AH_change = [0]
WR_change = [0]
WH_change = [0]
RH_change = [0]
count = 1
f = input("What file are we parsing: ")
lines = open(f, "r").readlines()
for i in range(len(lines)-2):
    if "~~~~" in lines[i]:
        xseries+=[count]
        count+=1
        KA+=[float(lines[i+1].split(" ")[3])]
        KW+=[float(lines[i+4].split(" ")[3])]
        KR+=[float(lines[i+7].split(" ")[3])]
        KH+=[float(lines[i+10].split(" ")[3])]
        AW+=[float(lines[i+13].split(" ")[3])]
        AR+=[float(lines[i+16].split(" ")[3])]
        AH+=[float(lines[i+19].split(" ")[3])]
        WR+=[float(lines[i+22].split(" ")[3])]
        WH+=[float(lines[i+25].split(" ")[3])]
        RH+=[float(lines[i+28].split(" ")[3])]
        if count > 2:
            KA_change += [float(int(lines[i+2].split(" ")[-3]) / int(lines[i+2].split(" ")[3]))]
            KW_change += [float(int(lines[i+5].split(" ")[-3]) / int(lines[i+5].split(" ")[3]))]
            KR_change += [float(int(lines[i+8].split(" ")[-3]) / int(lines[i+8].split(" ")[3]))]
            KH_change += [float(int(lines[i+11].split(" ")[-3]) / int(lines[i+11].split(" ")[3]))]
            AW_change += [float(int(lines[i+14].split(" ")[-3]) / int(lines[i+14].split(" ")[3]))]
            AR_change += [float(int(lines[i+17].split(" ")[-3]) / int(lines[i+17].split(" ")[3]))]
            AH_change += [float(int(lines[i+20].split(" ")[-3]) / int(lines[i+20].split(" ")[3]))]
            WR_change += [float(int(lines[i+23].split(" ")[-3]) / int(lines[i+23].split(" ")[3]))]
            WH_change += [float(int(lines[i+26].split(" ")[-3]) / int(lines[i+26].split(" ")[3]))]
            RH_change += [float(int(lines[i+29].split(" ")[-3]) / int(lines[i+29].split(" ")[3]))]

fig, ax = plt.subplots()
ax.plot(xseries, KA, label="KA")
ax.plot(xseries, KW, label="KW")
ax.plot(xseries, KR, label="KR")
ax.plot(xseries, KH, label="KH")
ax.plot(xseries, AW, label="AW")
ax.plot(xseries, AR, label="AR")
ax.plot(xseries, AH, label="AH")
ax.plot(xseries, WR, label="WR")
ax.plot(xseries, WH, label="WH")
ax.plot(xseries, RH, label="RH")
ax.plot(xseries, [0.5]*len(xseries), "--")
plt.title("max Pwin")
legend = ax.legend(fontsize=14)

fig1, ax2 = plt.subplots()
plt.title('proportion of actions changed')
ax2.plot(xseries, KA_change, label="KA-change")
ax2.plot(xseries, KW_change, label="KW-change")
ax2.plot(xseries, KR_change, label="KR-change")
ax2.plot(xseries, KH_change, label="KH-change")
ax2.plot(xseries, AR_change, label="AW-change")
ax2.plot(xseries, AR_change, label="AR-change")
ax2.plot(xseries, AH_change, label="AH-change")
ax2.plot(xseries, WR_change, label="WR-change")
ax2.plot(xseries, WH_change, label="WH-change")
ax2.plot(xseries, RH_change, label="RH-change")
ax2.plot(xseries, [0]*len(xseries), "--")
legend = ax2.legend(fontsize=14)

plt.tight_layout()
plt.show()
