# William J Kavanagh, 2/8/19
# Let's give this a bash then.
# Run search for dominance repeatedly using a seed configuration..
# Create a new configuration which nerfs and pairs with an optimal probability of over 0.4

import assess_optimalities

def evaluate_results(res):
    # Takes result dictionary and determines if the configuration is suitable.
    # If not, identifies what pairs need to be changed and in what direction
    # returns 0 if acceptable or dictionary of suggested changes otherwise.
    too_strong = []
    too_weak = []
    for material in res.keys():
        if float(res[material]["res"]) > upper_bound:
            too_strong += [material]
        if float(res[material]["res"]) < lower_bound:
            too_weak += [material]
    if len(too_strong) + len(too_weak) > 0: return(too_strong, too_weak)
    return([0],[0])

def reconfigure(nerfs, buffs, file):
    # takes attributes list [<att0, att1, ..>] to decrease and increase
    # creates new file at file_<++>.txt with required changes
    # returns new file name if successful or 0 if unable to make change (e.g. lowering accuracy at 0.0)
    r_file = open(file,"r").readlines()
    if seed_conf+".txt" in file:        # if first file..
        write_file_addr = file[:-4] + "_1" + ".txt"
    else:
        iteration = file.split("_")[-1].split(".txt")[0]
        write_file_addr = file.split("_")[0] + "_" + str(int(iteration)+1) + ".txt"
    w_file = open(write_file_addr,"w")
    for line in r_file:                                             # for every line in the configuration
        if "_accuracy" in line:                                     # if the line deals with an accuracy value
            char = line.split("_accuracy")[0].split(" ")[-1]
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
    return(write_file_addr)             # return the file name


seed_conf = input("Seed conf: ")
upper_bound = float(input("acceptable upper bound: "))
lower_bound = float(input("acceptable lower bound: "))
delta = float(input("increment delta (0.01 recommended): "))
output = input("output folder: ")
file_string = "configurations/" + seed_conf + ".txt"
full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
nerf, buff = evaluate_results(assess_optimalities.run(seed_conf))
while nerf != [0] or buff != [0]:
    char_to_buff = []
    char_to_nerf = []
    for pair in nerf:
        if full_name[pair[0]] not in char_to_nerf: char_to_nerf += [full_name[pair[0]]]
        if full_name[pair[1]] not in char_to_nerf: char_to_nerf += [full_name[pair[1]]]
    for pair in buff:
        if full_name[pair[0]] not in char_to_nerf: char_to_buff += [full_name[pair[0]]]
        if full_name[pair[1]] not in char_to_nerf: char_to_buff += [full_name[pair[1]]]
    next_attempt = reconfigure(char_to_nerf, char_to_buff, file_string)
    file_string = next_attempt
    if next_attempt == 0:
        print("Unable to change further, exiting.")
        exit()
    print("Reconfiguration complete. Running again.")
    nerf, buff = evaluate_results(assess_optimalities.run(next_attempt[15:-4]))
print("Acceptable configuration identified.")
