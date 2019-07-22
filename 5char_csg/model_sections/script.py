chars = list("KAWRH")
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i] + chars[j]]

for pair in pairs:
    print("[choose_" + pair + "],")
