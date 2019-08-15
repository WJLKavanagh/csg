# William J Kavanagh, 2/8/19
# Let's give this a bash then.
# Run search for dominance repeatedly using a seed configuration..
# Create a new configuration which nerfs and pairs with an optimal probability of over 0.4

import assess_optimalities, sys

def evaluate_results(res):
    # Takes result dictionary and determines if the configuration is suitable.
    # If not, identifies what pairs need to be changed and in what direction
    # returns 0 if acceptable or dictionary of suggested changes otherwise.
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
                if float(res[p]['res']) > 0.499:
                    return([p[0],p[1]],[p[0],p[1]])
                if float(res[p]['res']) > best_p:
                    best_p = float(res[p]['res'])
        best_char_vals[char] = best_p
        total_p += best_p
    nerf = []
    buff = []
    avg_p = total_p/5
    for char in chars:
        if best_char_vals[char] - delta > avg_p:
            nerf += [char]
        elif best_char_vals[char] + delta < avg_p:
            buff += [char]
    return(nerf, buff)

def reconfigure(nerfs, buffs, file):
    # takes attributes list [<att0, att1, ..>] to decrease and increase
    # creates new file at file_<++>.txt with required changes
    # returns new file name if successful or 0 if unable to make change (e.g. lowering accuracy at 0.0)
    print("reconfiguring: " + file + " -- nerfs = " + str(nerfs) + " -- buffs = " + str(buffs))
    r_file = open(file,"r").readlines()
    if seed_conf+".txt" in file:        # if first file..
        write_file_addr = file[:-4] + "_1" + ".txt"
    else:
        iteration = file.split("_")[-1].split(".txt")[0]
        write_file_addr = file.split("_")[0] + "_" + str(int(iteration)+1) + ".txt"
    w_file = open(write_file_addr,"w")
    if nerfs != buffs:
        for line in r_file:                                             # for every line in the configuration
            if "_accuracy" in line:                                     # if the line deals with an accuracy value
                char = line.split("_accuracy")[0].split(" ")[-1][0]
                amended_line = line.split("= ")[0]
                if char in nerfs:                             # check if it needs to be nerfed
                    if float(line.split("= ")[1][:-2]) - delta <= 0.0: return(0)
                    amended_line = amended_line + "= " + str(float(line.split("= ")[1][:-2])-delta) + ";\n"
                    w_file.write(amended_line)
                elif char in buffs:
                    if float(line.split("= ")[1][:-2]) + delta >= 1.0: return(0)
                    amended_line = amended_line + "= " + str(float(line.split("= ")[1][:-2])+delta) + ";\n"
                    w_file.write(amended_line)
                else:
                    w_file.write(line)
            else:
                w_file.write(line)
    else:
        for line in r_file:
            if full_name[buffs[0][0]] + "_accuracy" in line or full_name[buffs[0][1]] + "_accuracy" in line:
                char = line.split("_accuracy")[0].split(" ")[-1]
                amended_line = line.split("= ")[0]
                if float(line.split("= ")[1][:-2]) - 0.1 <= 0.0: return(0)
                amended_line = amended_line + "= " + str(float(line.split("= ")[1][:-2])-0.1) + ";\n"
                w_file.write(amended_line)
            else:
                w_file.write(line)
    return(write_file_addr)             # return the file name


seed_conf = sys.argv[1]
delta = float(sys.argv[2])
output = "test_output"
file_string = "configurations/" + seed_conf + ".txt"
full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
nerf, buff = evaluate_results(assess_optimalities.run(seed_conf))
while nerf != [] or buff != []:
    next_attempt = reconfigure(nerf, buff, file_string)
    if next_attempt == 0:
        print("Unable to change further, exiting.")
        exit()
    file_string = next_attempt
    print("Reconfiguration complete. Running again.")
    nerf, buff = evaluate_results(assess_optimalities.run(next_attempt[15:-4]))
print("Acceptable configuration identified.")
