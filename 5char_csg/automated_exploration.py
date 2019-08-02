# William J Kavanagh, 2/8/19
# Let's give this a bash then.
# Run search for dominance repeatedly using a seed configuration..
# Create a new configuration which nerfs and pairs with an optimal probability of over 0.4

import search_for_dominance

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
    write_file_addr = file[:len("configurations/"+seed_conf)]
    if file[len("configurations/"+seed_conf)] == ".":
        write_file_addr += "_1.txt"
    else:
        write_file_addr = write_file_addr + str(int(file[len("configurations/"+seed_conf)+1:])+1) + ".txt"
    w_file = open(write_file_addr,"w")
    for line in r_file:
        for char in nerfs + buffs:
            if full_name[char.upper()] + "_accuracy" in line:
                amended_line = line.split("= ")[0]
                if char in nerfs:
                    if float(line.split("= ")[1][-1]) - delta <= "0.0": return(0)
                    amended_line = amended_line + "= " + str(float(line.split("= ")[1][-1])-delta) + ";"
                else:
                    if float(line.split("= ")[1][-1]) + delta >= "1.0": return(0)
                    amended_line = amended_line + "= " + str(float(line.split("= ")[1][-1])+delta) + ";"
                w_file.write(amended_line)
            else: w_file.write(line)
    return(write_file_addr[len("configurations/"):].split(".txt")[0])


seed_conf = input("Seed conf: ")
upper_bound = float(input("acceptable upper bound: "))
lower_bound = float(input("acceptable lower bound: "))
delta = float(input("increment delta (0.01 recommended): "))
output = input("output folder: ")
full_name = {"K":"Knight","A":"Archer","W":"Wizard","R":"Rogue","H":"Healer"}
nerf, buff = evaluate_results(search_for_dominance.run(seed_conf,output))
while nerf != [0] or buff != [0]:
    char_to_buff = []
    char_to_nerf = []
    for pair in buff:
        if pair[0] not in char_to_nerf: char_to_nerf += [pair[0]]
        if pair[1] not in char_to_nerf: char_to_nerf += [pair[1]]
    for pair in nerf:
        if pair[0] not in char_to_nerf: char_to_buff += [pair[0]]
        if pair[1] not in char_to_nerf: char_to_buff += [pair[1]]
    file_string = "configurations/" + seed_conf + ".txt"
    next_attempt = reconfigure(char_to_nerf, char_to_buff, file_string)
    seed_conf = next_attempt
    if next_attempt == 0:
        print("Unable to change further, exiting.")
        exit()
    print("Reconfiguration complete. Running again.")
    nerf, buff = evaluate_results(search_for_dominance.run(next_attempt,output))
print("Acceptable configuration identified.")
