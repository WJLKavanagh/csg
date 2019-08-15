# Practice

res = {'KA': {'res': '0.4718474362094167', 'opp': 'WH'}, 'KW': {'res': '0.4763729651497536', 'opp': 'KA'}, 'KR': {'res': '0.32790979238460044', 'opp': 'KA'}, 'KH': {'res': '0.4940013190459223', 'opp': 'WR'}, 'AW': {'res': '0.44290514706950945', 'opp': 'AH'}, 'AR': {'res': '0.24857259501125925', 'opp': 'KA'}, 'AH': {'res': '0.3939280565732439', 'opp': 'RH'}, 'WR': {'res': '0.3637935632536699', 'opp': 'AW'}, 'WH': {'res': '0.35958910806825206', 'opp': 'WR'}, 'RH': {'res': '0.37120693354699796', 'opp': 'KW'}}


chars = ["K","A","W","R","H"]
pairs = []
for i in range(len(chars)):
    for j in range(i+1,len(chars)):
        pairs += [chars[i]+chars[j]]
best_char_vals = {}
total_p = 0

for char in chars:
    best_p = 0
    for p in res.keys():
        if char in p:
            if float(res[p]['res']) > best_p:
                best_p = float(res[p]['res'])
    best_char_vals[char] = best_p
    total_p += best_p

nerf = []
buff = []

avg_p = total_p/5
for char in chars:
    if best_char_vals[char] + 0.01 > avg_p:
        nerf += [char]
    elif best_char_vals[char] - 0.01 < avg_p:
        buff += [char]

print("nerf: " + str(nerf))
print("buff: " + str(buff))
