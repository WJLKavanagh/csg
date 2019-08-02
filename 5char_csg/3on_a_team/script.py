s = ""
chars = ["K","A","W","R","H"]
for t in range(1,3):
    for c in chars:
        s += "[K"+str(t)+"_"+c+str(3-t)+"], "
s += "\n"
for t in range(1,3):
    for i in range(len(chars)):
        s += "[A"+str(t)+"_"+chars[i]+str(3-t)+"], "
        for j in range(i+1,len(chars)):
            s += "[A"+str(t)+"_"+chars[i]+str(3-t)+chars[j]+str(3-t)+"], "
    s += "\n"
for t in range(1,3):
    for c in chars:
        s += "[W"+str(t)+"_"+c+str(3-t)+"], "
s += "\n"
for t in range(1,3):
    for c in chars:
        s += "[R"+str(t)+"_"+c+str(3-t)+"], "
s += "\n"
for t in range(1,3):
    for i in range(len(chars)):
        for j in range(len(chars)):
            if i==4 and j==4 and t==2: s += "[H"+str(t)+"_"+chars[i]+str(3-t)+chars[j]+str(t)+"]"
            else: s += "[H"+str(t)+"_"+chars[i]+str(3-t)+chars[j]+str(t)+"], "
    s += "\n"
print(s)
